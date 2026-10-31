#!/usr/bin/env python3
"""Publish one self-contained HTML revision to the configured Preview service."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Preview verification redirected; check the service configuration")


def regular_bytes(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as source:
        if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
            raise ValueError("Source must be a regular HTML file")
        content = source.read()
    content.decode("utf-8")
    return content


def verify(url, expected):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(url, timeout=10) as response:
        if response.status != 200 or response.read(len(expected) + 1) != expected:
            raise ValueError("Preview content verification failed: " + url)


def write_temp(directory, content):
    fd, name = tempfile.mkstemp(prefix=".publish-", dir=directory)
    try:
        with os.fdopen(fd, "wb") as output:
            os.fchmod(output.fileno(), 0o640)
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        return Path(name)
    except BaseException:
        Path(name).unlink(missing_ok=True)
        raise


def publish(config, source, task, new=False):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", task) or len(task) > 100:
        raise ValueError("Use a readable lowercase task name with hyphens (maximum 100 characters)")
    root = Path(config["preview_root"])
    if not root.is_absolute() or root.is_symlink() or not root.is_dir():
        raise ValueError("Configured preview directory is unavailable or is a symlink")
    if not isinstance(config.get("base_url"), str):
        raise ValueError("Preview service configuration has no valid base_url; rerun setup")
    base = config["base_url"].rstrip("/")
    url = urllib.parse.urlsplit(base)
    if (url.scheme != "https" or not url.hostname or not url.hostname.endswith(".ts.net")
            or url.username or url.password or url.path or url.query or url.fragment):
        raise ValueError("Expected a private Tailscale HTTPS base URL")
    source = Path(source)
    if source.suffix.lower() not in (".html", ".htm"):
        raise ValueError("Publish a self-contained .html or .htm file")
    content = regular_bytes(source)
    directory = root / task
    if new:
        # Inherit the service group and setgid from the root without chmod,
        # which can clear setgid when this session is not a group member.
        previous_umask = os.umask(0o027)
        try:
            directory.mkdir(mode=0o2750)
        finally:
            os.umask(previous_umask)
    elif directory.is_symlink() or not directory.is_dir():
        raise ValueError("Task does not exist; use --new for a new task")
    lock_fd = os.open(directory / ".publish.lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(lock_fd, "r+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        revisions = [int(m.group(1)) for p in directory.iterdir()
                     if (m := re.fullmatch(r"v([1-9][0-9]*)\.html", p.name))]
        revision = max(revisions, default=0) + 1
        filename = "v%d.html" % revision
        temporary = write_temp(directory, content)
        try:
            # Linking installs the complete revision without replacing an existing name.
            os.link(temporary, directory / filename)
        finally:
            temporary.unlink(missing_ok=True)
        revision_url = base + "/" + task + "/" + filename
        try:
            verify(revision_url, content)
        except Exception as error:
            raise ValueError("Saved %s, but verification failed; latest was not updated: %s" %
                             (directory / filename, error)) from error
        try:
            temporary = write_temp(directory, content)
            try:
                os.replace(temporary, directory / "index.html")
            finally:
                temporary.unlink(missing_ok=True)
        except OSError as error:
            raise ValueError("Saved %s, but latest page update failed: %s" %
                             (directory / filename, error)) from error
        latest_url = base + "/" + task + "/"
        try:
            verify(latest_url, content)
        except Exception as error:
            raise ValueError("Published %s, but latest URL verification failed: %s" %
                             (directory, error)) from error
        return {"task": task, "revision": revision, "url": latest_url, "revision_url": revision_url}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--task", required=True)
    parser.add_argument("--new", action="store_true", help="Create a new task; fail if the name exists")
    args = parser.parse_args()
    config_path = Path.home() / ".config/vps-setup/preview-service.json"
    try:
        config = json.loads(regular_bytes(config_path))
        if config.get("version") != 1:
            raise ValueError("Unsupported Preview service configuration; rerun setup")
        result = publish(config, args.source, args.task, args.new)
        print(json.dumps(result))
    except (OSError, ValueError, KeyError) as error:
        print("Preview service: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
