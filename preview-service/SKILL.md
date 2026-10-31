---
name: preview-service
description: Publish static HTML mockups, designs, and reports through this machine's private Tailscale Preview service. Use when producing an HTML preview for the user or revising a previously published preview. Does not deploy applications or change server configuration.
---

# Preview service

Read `~/.config/vps-setup/preview-service.json`. Setup records `preview_root`,
`base_url`, and `publisher` there. If missing, report that Preview service must
be selected in JINGBANZ/vps-setup; do not start an ad hoc server or publish publicly.

Create a self-contained UTF-8 HTML file with embedded styles, scripts, and images
as needed. Use example data, never real credentials. Check the rendered design
when a browser or renderer is available; publishing verifies delivery, not appearance.

Choose a descriptive lowercase task name such as `jarvis-connections`. Create
one directory per task, then reuse that name throughout revisions of the task.
Do not reuse another task's directory. A name collision requires a more specific
readable name, not a random suffix.

Run the configured publisher with Python 3 (quote all paths):

```bash
python3 /path/from/config/publish.py --new --task jarvis-connections /path/to/preview.html
```

For revisions, omit `--new` and keep the same task name. The publisher preserves
`v1.html`, `v2.html`, etc. inside the task directory and updates `index.html`.
Use the script rather than writing into the served folder directly.

On success, return the JSON result's `url` (latest) and, when useful,
`revision_url` (fixed revision). These are ordinary browser links for devices
allowed by the owner's Tailscale policy. On failure, report the error; never
claim an unverified URL works. Files may have been saved before verification
failed, so inspect the error before retrying. Do not delete prior previews,
weaken access controls, enable Funnel, or change Tailscale configuration.
