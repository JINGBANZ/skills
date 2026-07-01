---
name: us-cancer-screening
description: Use when deciding which cancer screenings to recommend for a person under U.S. guidelines (USPSTF, ACS, and specialty societies) — given their age, sex, smoking, family history, BMI, infections, exposures, and reproductive history. Maps a health profile to risk-stratified screening recommendations, intervals, and which cancers to screen vs. not screen. Built for FixYou's screening advisor but usable by any agent doing U.S.-based screening triage.
---

# U.S. Cancer Screening Guidelines

## Overview

This skill distills current (2025–2026) U.S. cancer screening guidance into rules an LLM can apply to a user profile. It answers: **for this person, which cancers warrant a screening recommendation right now, with what test, how often, and how urgently?**

**Core principle:** U.S. screening is **age + sex + risk-factor gated**. For most cancers there is a population screen with a defined start age and interval; risk factors (family history, genetics, smoking, infections, exposures) *escalate* the recommendation (earlier start, shorter interval, added modality). Several cancers have **no population screen** — recommend screening for those only when a defined high-risk trigger is present, and otherwise route the person to symptom-awareness, not testing.

**Source hierarchy:** USPSTF (graded A/B/C/D/I) is primary for population screening. ACS, and specialty societies (ACG, AASLD, ACR, NCCN, AUA, ACOG) fill gaps and define high-risk surveillance. Where bodies disagree, this skill notes it; default to the more protective evidence-based option and surface the choice.

## How to read the user profile

These rules key on fields a health intake collects. Map whatever profile you're given onto:

| Signal | What to extract |
|---|---|
| `age`, `biological_sex` | gate nearly every recommendation |
| `smoking` | status (never/former/current) **and pack-years**; for former, years since quit |
| `alcohol` | heavy use (≳3 drinks/day or ≳7–14/week) is a risk modifier |
| `BMI` | overweight ≥25, obese ≥30 — modifier for several cancers |
| `family_cancer_history` | per relative: **which cancer, which relative (degree), age at diagnosis**. First-degree = parent/sibling/child |
| `past_medical_history` | IBD, cirrhosis, Barrett's, polyps, pernicious anemia, prior cancer, transplant/immunosuppression, known genetic syndrome |
| `hep_b_c_status` | chronic HBV or HCV → liver surveillance trigger |
| `sun_reaction`, `occupational_exposure` | fair skin/burns easily; carcinogen exposure (asbestos, aromatic amines, radon) |
| `red_flag_symptoms` | **never silently drop** — every reported symptom gets a safety note (see Symptoms) |
| `hpv_vaccinated`, `last_pap_result` | cervical history |
| `hrt`, `parity`, `ever_breastfed`, `menopause_status` | reproductive modifiers (breast/endometrial/ovarian context) |

If a needed field was **declined or unknown**, do not assume a value — make the recommendation on what's known and note it may refine once that fact is available.

## Decision procedure

1. **Filter by age + sex.** Drop cancers whose population window the person hasn't entered (unless a high-risk trigger pulls the start age earlier).
2. **Apply average-risk rule** for each in-window cancer → baseline recommendation.
3. **Scan risk factors** → escalate start age / interval / modality, and raise severity.
4. **Check the "no population screen" list** → recommend only if a high-risk trigger fires; otherwise omit (or, for genetics, suggest genetic counseling).
5. **Handle every red-flag symptom** with an action-leading safety note — this is independent of screening eligibility.
6. **Assign severity** (see Severity) and a **department**.

## Severity mapping

Severity is a *per-person urgency* the advisor assigns (it feeds FixYou's shield score) — **not** a guideline grade. Assign:

- **high** — a strong population screen (USPSTF A/B) that applies now AND the person carries elevated personal risk (smoking meeting lung criteria, first-degree family history pulling the start age in, a known precursor lesion or genetic syndrome); OR **active high-risk surveillance** triggered by cirrhosis / chronic HBV/HCV, a precursor lesion (GIM, Barrett's), or a genetic syndrome — this is disease monitoring, so the I/D-grade caveat doesn't apply.
- **medium** — a standard population screen that applies now at average risk (e.g., a 46-year-old at average CRC risk). Absent any screening-history dates, in-window average-risk screens default here.
- **low** — shared-decision / borderline (prostate PSA 55–69; person approaching but not yet at start age; optional add-on).

The profile carries no last-screening date except `last_pap_result`, so do **not** infer "overdue" for other cancers; only cervical can be flagged overdue (a `last_pap_result` older than the interval). Never assign high on a guideline I-statement (insufficient evidence) alone.

## Writing the output fields

- **`screening_name`** — the single first-line/preferred test for this person's risk tier, formatted *modality (interval)* — e.g. "Colonoscopy (every 10 years)", "Low-dose CT (annual)". When tests are co-equal, use the `(preferred)`-marked one and mention alternatives in `summary`.
- **`summary`** — plain language for a layperson, 1–2 sentences: the profile fact that triggered the recommendation + what the test is. Do **not** include guideline grades, risk-score numbers, or citations/DOIs.

---

## Population screening (average-risk)

### Colorectal
- **Who:** all adults, **start 45**, continue to **75**. Ages 76–85 individualize (life expectancy >10y); do not screen 86+.
- **Tests / interval:** colonoscopy **q10y** (preferred) · FIT **annually** · multi-target stool DNA (Cologuard) **q1–3y** · CT colonography **q5y** · flex sig **q5y**. Any positive non-colonoscopy test → colonoscopy.
- **High-risk escalation (ACG/NCCN):**
  - 1 first-degree relative (FDR) with CRC/advanced polyp **<60**, OR ≥2 FDRs any age → **start 40, or 10y before youngest case** (whichever earlier); **colonoscopy q5y**.
  - 1 FDR diagnosed **≥60** → start 40 (or 10y before youngest), then **resume average-risk screening** (≈q10y) — not a fixed q5y.
  - **Lynch syndrome** → colonoscopy **q1–2y from age 20–25** (MLH1 / MSH2 / EPCAM); **MSH6 / PMS2** start later, **30–35, q1–3y**. **FAP** → **from age 10–15, annually**.
  - **IBD (UC/Crohn colitis)** → colonoscopy **8y after onset**, then q1–3y (with PSC: annually from diagnosis).
- **Source:** USPSTF 2021 (A 50–75, B 45–49). ACS start 45 — 2018 guideline, reaffirmed in the **2026 update**. High-risk: ACG 2021 / NCCN v1.2024 / ACG IBD 2019.
- **Department:** Gastroenterology.

### Breast
- **Who:** women, biennial mammography **40–74** (USPSTF 2024, Grade B). ACS: optional annual 40–44, annual 45–54, then q1–2y, no hard stop while healthy.
- **Tests / interval:** mammography (digital/tomosynthesis) **q1–2y**.
- **High-risk escalation (ACS/ACR/NCCN):** add **annual breast MRI + annual mammography** when lifetime risk ≥20% — i.e. **BRCA1/2** carrier (or untested FDR of a carrier), **chest radiation age 10–30**, Li-Fraumeni/Cowden. BRCA: annual MRI from 25, add mammography at 30. Pull discussion earlier with strong family history.
- **Note:** USPSTF gives I-statement for supplemental imaging in dense breasts and for screening 75+. Interval disagreement: USPSTF biennial vs ACR annual.
- **Department:** Breast imaging / Breast surgery.

### Lung
- **Who:** adults **50–80** who are **current smokers or quit ≤15y** with **≥20 pack-years**.
- **Test / interval:** **low-dose CT (LDCT) annually**. (No chest X-ray.)
- **Stop:** USPSTF — once quit 15y, or life expectancy/surgical-candidacy limited. **ACS 2023 dropped the 15-year-quit limit** → former smokers with ≥20 pack-years stay eligible regardless of quit time. When a former smoker quit >15y ago, surface LDCT as an ACS-supported option even though USPSTF would stop it.
- **Pack-years = packs/day × years.** Use the smoking summary to compute; if it gives "a pack a day for 25 years" → 25 pack-years (eligible).
- **Source:** USPSTF 2021 Grade B.
- **Department:** Pulmonology.

### Cervical
- **Who:** women with a cervix. **Start 21** (USPSTF) / **25** (ACS); **stop 65** if adequate prior negative screening. Not after hysterectomy with cervix removed and no high-grade history.
- **Tests / interval:** USPSTF 2018 — 21–29 → cytology **q3y**; 30–65 → cytology q3y · **hrHPV q5y** · co-test q5y (no modality ranked "preferred"). ACS prefers **HPV primary testing q5y** across 25–65.
- **Self-collection:** vaginal self-collected HPV is FDA-cleared (2024) and an accepted option in the **ACS 2025 update**; it is **not** part of the USPSTF 2018 final (a USPSTF update is in draft).
- **High-risk:** HIV/immunocompromised, in-utero DES, prior CIN2+ → screen more often, continue past 65. **HPV-vaccination status does NOT change the schedule.**
- **Source:** USPSTF 2018 (Grade A; Grade D for <21, >65 with adequate prior screening, and post-hysterectomy); ACS 2020 (updated 2025).
- **Department:** Gynecology.

### Prostate
- **Who:** men **55–69**, **shared decision-making** (USPSTF Grade C) — PSA only after discussing trade-offs. **Against routine PSA ≥70** (Grade D).
- **High-risk earlier start (ACS):** **Black men** and FDR diagnosed <65 → discuss at **45**; >1 early FDR or BRCA → **40**.
- **Test / interval:** PSA ± DRE; individualized interval (commonly q1–2y; q2y if PSA <2.5).
- **Severity:** keep **low/medium** unless high-risk — this is preference-sensitive, not a push.
- **Department:** Urology.

---

## No average-risk population screen (high-risk surveillance, or awareness-only for some)

Recommend these **only** when the trigger fires. Otherwise omit the cancer (or suggest genetic counseling where a syndrome is implied). A few (bladder, testicular) have **no surveillance test even at high risk** — route to symptom-awareness/workup instead.

### Liver (HCC)
- **Trigger:** **cirrhosis of any cause** (Child-Pugh A–B, or C only if a transplant candidate), OR **chronic HBV** in a higher-risk subset (man from an endemic country >40, woman from an endemic country >50, person of African ancestry at an earlier age — third decade, family history of HCC, or PAGE-B ≥10), OR chronic HCV with advanced fibrosis.
- **Surveillance:** **ultrasound + AFP every 6 months** (AASLD 2023 — both, in combination). AFP ≥20 or any lesion → multiphasic CT/MRI.
- **Profile hook:** `hep_b_c_status` = chronic HBV/HCV, or cirrhosis in `past_medical_history`.
- **Department:** Hepatology. **Severity:** high (active surveillance program).

### Gastric
- **Trigger (AGA 2025):** first-generation immigrant from high-incidence region (East Asia, Russia/former USSR, Andean South America), FDR with gastric cancer, or precursor (atrophic gastritis, **gastric intestinal metaplasia**, pernicious anemia), or **CDH1**/Lynch/FAP.
- **Surveillance:** upper endoscopy; GIM surveillance ~**q3y**. Test and eradicate **H. pylori**.
- **Department:** Gastroenterology.

### Esophageal (adenocarcinoma / Barrett's)
- **Trigger (ACG 2022):** **chronic GERD + ≥3 of**: male, age >50, White, smoking, obesity, FDR with Barrett's/esophageal adenocarcinoma → one screening **EGD**.
- **Surveillance by dysplasia:** none → q3–5y; low-grade → eradication therapy or q6–12mo; high-grade → endoscopic eradication.
- **Note:** squamous-cell esophageal cancer (tobacco + heavy alcohol) has no formal U.S. screen — manage via symptom evaluation.
- **Department:** Gastroenterology.

### Pancreatic
- **Average risk: USPSTF Grade D — do NOT screen.**
- **Trigger (CAPS/NCCN high-risk surveillance, MRI/MRCP ± EUS annually):** familial pancreatic cancer (≥2 FDRs); **BRCA1/2, PALB2, ATM** with family history (start ~50); Lynch (~50); **Peutz-Jeghers** (~35–40); hereditary pancreatitis PRSS1 (~40); CDKN2A/FAMMM (~40).
- **Department:** Gastroenterology / high-risk pancreatic clinic.

### Ovarian
- **Average risk: USPSTF Grade D — do NOT screen** (CA-125/TVUS cause net harm).
- **Trigger:** **BRCA1/2** or **Lynch** → refer for risk-reducing salpingo-oophorectomy counseling (BRCA1 ~35–40, BRCA2 ~40–45); interim TVUS+CA-125 is optional, not proven.
- **Department:** Gynecologic oncology / genetics.

### Endometrial
- **No routine screen.** Counsel all (esp. postmenopausal, on `hrt`/tamoxifen, obese) to **report any postmenopausal bleeding immediately** — that's the detection pathway.
- **Trigger:** **Lynch** → risk-reducing hysterectomy after childbearing; surveillance endometrial biopsy ± TVUS may be offered (~30–35).
- **Department:** Gynecology.

### Bladder
- **No screening, even high-risk (USPSTF I).** Smokers and aromatic-amine occupational exposure raise risk but there's no test to recommend.
- **Action:** any **hematuria** (`blood_in_urine`) → urology evaluation, not screening.
- **Department:** Urology.

### Kidney
- **No population screen.** Surveillance only for hereditary syndromes (VHL, Birt-Hogg-Dubé, HLRCC, hereditary papillary RCC) → abdominal MRI per syndrome. Most RCC is incidental.
- **Department:** Urology / genetics.

### Testicular
- **USPSTF Grade D — do NOT screen.** Awareness only. Cryptorchidism history raises risk → report any scrotal mass.
- **Department:** Urology.

### Skin
- **USPSTF I-statement — no routine whole-body screening for average-risk asymptomatic adults.**
- **High-risk surveillance reasonable (ACS/AAD, not USPSTF-graded):** fair skin / burns easily (`sun_reaction`), many/atypical nevi, **personal or family history of melanoma**, immunosuppression (transplant), heavy UV/tanning, outdoor occupational exposure → periodic dermatologic exam + self-exam.
- **Severity:** low/medium; never high on the I-statement alone.
- **Department:** Dermatology.

### Oral
- **USPSTF I-statement — no recommended routine screening.**
- **High-risk context:** tobacco (incl. smokeless), heavy alcohol, combined use, HPV-16, betel quid → opportunistic oral exam at dental visits (ADA), not a graded screen.
- **Department:** Dentistry / ENT.

---

## Red-flag symptoms (independent of screening)

Every reported symptom gets an **action-leading** safety note — lead with what to do and when, not the cancer name. Never drop one.

| Symptom | Primary concern | Action lead |
|---|---|---|
| `blood_in_stool` | colorectal | GI evaluation / colonoscopy within 1–2 weeks; urgent care if heavy bleeding or faintness |
| `blood_in_urine` | bladder | urology + cystoscopy referral; any visible blood warrants prompt workup |
| `persistent_cough` | lung | imaging + primary care soon; urgent if hemoptysis |
| `unexplained_weight_loss` | varies (GI/lung/pancreatic) | primary care workup within weeks |
| `new_lump` | breast/lymphoma/testicular by site | clinical exam + imaging promptly |
| `changing_skin_lesion` | melanoma | dermatology evaluation soon |
| `persistent_abdominal_pain` | GI/pancreatic/ovarian | primary care/GI evaluation |
| `dysphagia_hoarseness` | esophageal / head-neck | ENT or GI evaluation; persistent >2–3 weeks warrants scope |
| `postmenopausal_bleeding` | endometrial | gynecology + endometrial evaluation promptly — high-yield red flag |

A symptom alert is **not** a cancer diagnosis — it's a route-to-care signal. Pair it with relevant screening if the person is also eligible.

## Guardrails

- Stay within guideline scope: recommend screenings appropriate to the person's **age, sex, and risk**. Do not invent family history, symptoms, or exposures not in the profile.
- Honor **USPSTF D (against)** — do not recommend ovarian/pancreatic/testicular screening at average risk, even gently.
- Honor **I-statements** — present skin/oral as optional/high-risk, never as a strong push.
- When a high-risk trigger implies a genetic syndrome (BRCA, Lynch, FAP, CDH1, Li-Fraumeni), recommend **genetic counseling** alongside any surveillance.
- Distinguish **screening** (asymptomatic) from **diagnostic workup** (symptomatic). A person with a red-flag symptom needs evaluation regardless of screening age.

## Quick reference

- **Population screens:** colorectal (45–75), breast (40–74), lung (50–80 if ≥20 pack-yr & current/quit ≤15y), cervical (21/25–65), prostate (55–69 shared decision).
- **High-risk-only:** liver (HBV/HCV/cirrhosis), gastric (precursor/immigrant/FDR), esophageal (GERD+risk), ovarian (BRCA/Lynch), endometrial (Lynch), pancreatic (familial / BRCA2·PALB2·ATM · Lynch · Peutz-Jeghers), skin·oral (risk-factor surveillance).
- **Do not screen at average risk:** ovarian, pancreatic, testicular (Grade D); bladder, kidney (no test); skin, oral (I-statement).
- **Pack-years** drive lung eligibility — always compute from the smoking summary.
- **Every red-flag symptom → one action-leading note.** Never drop one.
