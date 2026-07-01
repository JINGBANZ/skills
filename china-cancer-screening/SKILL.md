---
name: china-cancer-screening
description: Use when deciding which cancer screenings to recommend for a person under Chinese guidelines (国家癌症中心/NCC, 中国抗癌协会/CACA, 国家卫健委 NHC 方案) — given their age, sex, smoking, family history, BMI, HBV/HCV status, region, and exposures. Maps a health profile to China's risk-stratified (高危人群) screening recommendations, intervals, and modalities. Built for FixYou's screening advisor but usable by any agent doing China-based screening triage.
---

# China Cancer Screening Guidelines

## Overview

This skill distills current (2025–2026) Chinese cancer screening guidance into rules an LLM can apply to a user profile. It answers: **for this person, which cancers warrant a screening recommendation right now, with what test, how often, and how urgently — under China's guidelines?**

**Core principle:** Chinese screening is **risk-stratified, not age-blanket**. The central concept is **高危人群 (high-risk population)** — for most cancers, guidelines define explicit high-risk criteria (infection status, geographic high-incidence region, family history, exposures, numeric risk scores), and screening is recommended primarily for people who meet them. This reflects China's epidemiology (high HBV, H. pylori, regional esophageal/gastric belts) and finite endoscopy capacity. So the question is usually **"does this person meet the 高危人群 definition?"** rather than "have they hit the start age?"

**Where China differs from the U.S. (apply these instincts):**
- **Upper-GI cancers (gastric, esophageal, liver) are screened actively** from ~age 40–45 — they are high-incidence in China and have organized programs.
- **Liver screening centers on HBV** (the dominant cause) and screens non-cirrhotic HBV carriers from age 40.
- **Breast screening leans on ultrasound** (Chinese women have denser breasts), often co-primary with mammography.
- **Prostate screening starts later** (~60 average) — lower incidence.
- **Screening eligibility often uses numeric risk scores** (gastric score, colorectal questionnaire, aMAP for liver).

**Source hierarchy:** National Cancer Center (NCC) guidelines (《中国…筛查与早诊早治指南》), 国家卫健委 (NHC) 方案 (2024 versions for lung/colorectal/gastric/esophageal), and CACA (中国抗癌协会) integrated guidelines. Delivered via national programs: **城市癌症早诊早治项目** (urban: lung, colorectal, upper-GI, breast, liver), rural high-incidence programs (esophageal/gastric/liver), and the **两癌筛查** women's program (cervical + breast, ages 35–64).

## How to read the user profile

| Signal | What to extract |
|---|---|
| `age`, `biological_sex` | gate, but secondary to high-risk status |
| `smoking` | status + **pack-years**; passive-smoke exposure also counts in China's lung criteria |
| `alcohol` | heavy use — esophageal/liver modifier (esp. with hot foods, smoking) |
| BMI | overweight/obese — colorectal & gastric score input |
| `family_cancer_history` | per relative: cancer + degree + age at dx. **First-degree family history is a high-risk trigger for nearly every GI cancer in China** |
| `past_medical_history` | **chronic atrophic gastritis, gastric intestinal metaplasia, gastric ulcer/polyps, pernicious anemia, cirrhosis, MAFLD/fatty liver, IBD, prior cancer, Lynch/FAP** |
| `hep_b_c_status` | **chronic HBV or HCV → the central liver-screening trigger in China** |
| `occupational_exposure` | radon/asbestos/arsenic/chromium (lung), aromatic amines (bladder) |
| `sun_reaction` | minor — skin cancer is low-incidence in Chinese populations |
| `red_flag_symptoms` | never drop — every one gets a safety note |
| `hpv_vaccinated`, `last_pap_result` | cervical history |
| `hrt`, `parity`, `ever_breastfed`, `menopause_status` | breast/endometrial reproductive context |
| **region / origin** (if known) | residence in a **high-incidence area** is a formal trigger for esophageal/gastric/nasopharyngeal — read it **only** from an explicit residence/free-text statement; do NOT infer it from unrelated fields. If unstated, treat as unknown and note esophageal/gastric/nasopharyngeal can't be fully assessed |

If a field is declined/unknown, don't assume — recommend on what's known and note the gap. **HBV/HCV status, H. pylori, and family history are the highest-yield fields** in the Chinese framework; flag them when missing.

## Decision procedure

1. **Check infection + family-history triggers first** (HBV/HCV → liver; H. pylori/precursors/FDR → gastric; FDR → colorectal/esophageal). These drive Chinese screening more than age.
2. **Apply the 高危人群 definition** for each cancer; if met, recommend the targeted screen.
3. **Apply numeric risk scores where the inputs exist.** The gastric score (needs pepsinogen / gastrin-17 / H. pylori serology) and liver aMAP (needs albumin / bilirubin / platelets) rely on **labs the profile does not collect** — do not compute or fabricate them; absent the labs, drive the recommendation from the qualitative 高危人群 definition and flag the missing labs as high-yield. The colorectal questionnaire uses only profile fields (age, sex, FDR, smoking, BMI) and **is** computable.
4. **Apply the women's-program cancers** (cervical, breast) by their 一般风险 / 高危人群 age gates.
5. **Handle every red-flag symptom** with an action-leading note.
6. **Assign severity** and a **department** (科室).

## Severity mapping

Severity is a *per-person urgency* the advisor assigns (it feeds FixYou's shield score) — **not** a guideline grade. Assign:
- **high** — person clearly meets a 高危人群 definition with an active program (HBV carrier → liver; H. pylori + atrophic gastritis → gastric; high gastric score; **FDR with a GI cancer** — a standalone 高危人群 qualifier, though screening still starts at each cancer's own age gate, e.g. ≥45 for gastric/esophageal) AND screening is due.
- **medium** — standard program screening that applies by age at average risk (e.g., woman 45–70 for breast).
- **low** — borderline / shared-decision (prostate PSA; person approaching but below a high-risk threshold).

Colorectal in China is recommended **only** for questionnaire-identified 高危人群 (score ≥4), so a colorectal recommendation is always **high** — there is no average-risk colorectal tier for "medium" to apply to.

## Writing the output fields

- **`screening_name`** — the single first-line/preferred test for this person's tier, formatted *modality (interval)* in the user's locale — e.g. "结肠镜（每5–10年）", "低剂量螺旋CT（每年）". When tests are co-equal, use the first-line one and mention alternatives in `summary`.
- **`summary`** — plain language for a layperson, 1–2 sentences: the profile fact that triggered the recommendation + what the test is. Do **not** include guideline names, risk-score numbers, or citations.

---

## High-incidence cancers (China screens actively)

### 肝癌 / Liver (HCC)
- **高危人群:** chronic liver disease or hereditary risk, **especially males >40** (the 2021 早筛 consensus frames the target as males 40–75), with any of: **HBV and/or HCV infection**, cirrhosis (any cause), heavy alcohol, **MAFLD/fatty liver**, aflatoxin B1 exposure, or family history of liver cancer. **Non-cirrhotic chronic HBV carriers are screened** — this is the defining China difference.
- **Test / interval:** **腹部超声 (ultrasound) + 血清 AFP, at least every 6 months** (诊疗指南 2024). **AFP-L3** and **异常凝血酶原 (DCP/PIVKA-II)** are listed as additional early-detection markers (combined in the GALAD model); enhanced MRI for higher-risk tiers.
- **Risk stratification:** the **aMAP score is 3-tier** — low (0–50), medium (50–60), high (60–100) (defined in the 诊疗指南). Surveillance **intervals** come from the **2021 中国肝癌早筛策略专家共识 / 二级预防指南**, not aMAP itself: low → annual US+AFP; medium → q6mo; high → q3–6mo (+ MRI q6mo); a separate **极高危 (extremely-high)** category → US+AFP **q3mo** + MRI q6mo.
- **Profile hook:** `hep_b_c_status` = chronic HBV/HCV is an immediate **high-severity** trigger.
- **Source:** 《原发性肝癌诊疗指南（2024版）》国家卫健委; 《中国肝癌早筛策略专家共识（2021）》(aMAP tiers + intervals). **科室: 肝病科 / 感染科.**

### 胃癌 / Gastric
- **高危人群:** **age ≥45** plus any of: residence in a **gastric-cancer high-incidence region**; **H. pylori infection**; precancerous condition (**chronic atrophic gastritis, gastric intestinal metaplasia, gastric ulcer/polyps, operated stomach, pernicious anemia**); **first-degree relative with gastric cancer**; high-salt/pickled diet, smoking, heavy alcohol.
- **Test:** **胃镜 (gastroscopy)** is the gold standard; H. pylori by urea breath test.
- **Risk score (新型胃癌筛查评分系统, 0–23):** inputs = age, sex, **H. pylori antibody, PGI/PGII ratio (pepsinogen), gastrin-17**. High (17–23) → gastroscopy **yearly**; medium (12–16) → **q2y**; low (0–11) → **q3y**. (Serum pepsinogen alone is not a standalone screen.)
- **Profile hook:** atrophic gastritis / intestinal metaplasia / pernicious anemia in `past_medical_history`, or FDR gastric cancer → high severity.
- **Source:** 《中国胃癌筛查与早诊早治指南（2022）》NCC; NHC 2024 方案. **科室: 消化内科.**

### 食管癌 / Esophageal (squamous)
- **高危人群:** **age ≥45** plus any of: residence in an **esophageal-cancer high-incidence region** (age-standardized incidence >15/100,000 — rural belts in 河南/河北/山西 etc.); **first-degree family history**; esophageal precancerous lesion; lifestyle risks (**smoking, alcohol, very hot food/drink, pickled foods, poor oral hygiene**, prior head-neck/upper-GI squamous cancer).
- **Test / interval:** **内镜 (endoscopy)** with **Lugol's iodine chromoendoscopy (碘染色)** or **NBI** — the preferred modality. **Start 45, stop ~75.** High-risk → **q5y**; low-grade dysplasia → q1–3y.
- **Note:** China targets **squamous-cell** carcinoma (very different from the U.S. Barrett's/adenocarcinoma model). Geography + family history are the dominant triggers.
- **Source:** 《中国食管癌筛查与早诊早治指南（2022）》NCC; NHC 2024 方案. **科室: 消化内科.**

### 肺癌 / Lung
- **高危人群（依据 NHC 2024 方案）:** **age 50–74**, with **≥1** of: **smoking ≥20 pack-years** (including former smokers who **quit <15 years ago**); **passive smoke ≥20 years** (living with a smoker or sharing a workspace); **COPD (慢性阻塞性肺疾病)**; **occupational carcinogen exposure ≥1 year** (asbestos, radon, beryllium, chromium, cadmium, nickel, silica, soot/coal-smoke); **first-degree relative diagnosed with lung cancer** (standalone criterion).
- **Test / interval:** **低剂量螺旋CT (LDCT) annually** (原则上每年一次). Positive/indeterminate nodules shorten the interval (e.g. ≥6 mm → 3-month recheck).
- **Key China difference:** non-smoking pathways matter (passive smoke, COPD, occupational exposure, family history) — China has a high never-smoker lung-cancer burden, so don't gate solely on personal pack-years. (The ≥20 pack-year + quit-<15-year threshold itself matches USPSTF.)
- **Source:** 《肺癌筛查与早诊早治方案（2024年版）》国家卫健委（现行权威方案）. **科室: 呼吸科 / 胸外科.**

### 结直肠癌 / Colorectal
- **高危人群 (two pathways):**
  - **Sporadic (per NHC 2024 方案):** risk questionnaire scoring age (≤49=0, 50–59=1, ≥60=2), sex (male=1), **FDR with CRC** (=1, but a single FDR <60 OR ≥2 FDRs = 4 outright), smoking (=1), BMI ≥23 (=1) → **cumulative ≥4 points = high-risk**. Screening window **age 40–74**.
  - **Hereditary:** **Lynch syndrome (林奇综合征)** (MLH1/MSH2 → colonoscopy from 20–25, MSH6/PMS2 → from 30–35) / **FAP (家族性腺瘤性息肉病)** (annual colonoscopy from age 10) → separate intensive surveillance.
- **Test / interval:** **结肠镜 (colonoscopy)** first-line, **q5–10y** (normal → up to 10y); **annual 便潜血 (FIT)**. Alternatives if colonoscopy declined: sigmoidoscopy, CT colonography (结肠CT成像), **multi-target stool DNA (多靶点粪便DNA)**.
- **Key China difference:** starts at **40** but **only screens questionnaire-identified high-risk people** (risk-gated, not blanket) — reflecting endoscopy capacity.
- **Source:** 《结直肠癌筛查与早诊早治方案（2024年版）》国家卫健委 (≥4-point questionnaire, 40–74); 《中国结直肠癌筛查与早诊早治指南（2020）》NCC (tests, hereditary). **科室: 消化内科 / 肛肠科.**

---

## Women's-program cancers

### 乳腺癌 / Breast
- **一般风险:** women, **45–70**, screen **every 1–2 years** (每1～2年). The T/CPMA 014-2020 standard makes **乳腺超声 (ultrasound) the primary modality** (use 乳腺X线/钼靶 mammography only where ultrasound is unavailable); the NCC 2021 guideline recommends **mammography + ultrasound together for dense breasts** (common in Chinese women).
- **高危人群:** FDR with breast/ovarian cancer; ≥2 second-degree relatives with breast/ovarian cancer before 50; **BRCA1/2** carrier; chest radiotherapy before 30; elevated model risk → **start at 40**, **annual** screening (ultrasound + mammography), add **MRI** when indicated.
- **National 两癌 program:** clinical exam + ultrasound + mammography for women **35–64**.
- **Recommendation gate:** default start is 一般风险 **45–70** (or 高危人群 → **40**); treat the 35–64 两癌 program as an earlier-access option to *mention*, not the default start.
- **Source:** 《中国女性乳腺癌筛查与早诊早治指南（2021）》NCC; CACA. **科室: 乳腺外科 / 乳腺科.**

### 宫颈癌 / Cervical
- **一般风险:** women, **start 25, stop 65** (if adequate prior negatives). **HR-HPV q5y** (preferred) · co-test q5y · **TCT/cytology q3y**. Abnormal → 阴道镜 (colposcopy).
- **高危人群:** HIV+/immunocompromised, prior CIN2+, DES exposure → start earlier, screen more often, continue past 65. **HPV-vaccination status does not change the schedule.** Women <25 generally not screened.
- **National 两癌 program:** gyn exam + cytology + colposcopy for women **35–64**, 3-year cycle, prioritizing rural/unemployed women. HPV vaccination subsidized for adolescent girls in many provinces.
- **Source:** 《中国子宫颈癌筛查指南（2023）》; aligned with 加速消除宫颈癌行动. **科室: 妇科.**

---

## Lower-priority / no population screen

### 前列腺癌 / Prostate
- **一般风险:** men, **start ~60**, baseline **PSA then q2y** if life expectancy >10y (opportunistic/shared-decision, not a universal program).
- **高危人群:** age ≥45 with **family history of prostate cancer** (前列腺癌家族史) → start PSA at **45**; **BRCA2** carrier age ≥40 → start ~**40**.
- **Note:** starts later than the U.S. (lower incidence). **科室: 泌尿外科.** Severity low/medium.

### 鼻咽癌 / Nasopharyngeal (regionally important — no U.S. analog)
- **高危人群:** residents of **endemic southern China** (广东/广西/福建/湖南/海南), age ~30–69, esp. with family history or EBV high-risk markers.
- **Test:** **EBV serology (VCA-IgA / EBNA1-IgA) and/or plasma EBV-DNA**; positive → 鼻咽镜 (nasopharyngoscopy) + head/neck MRI. Typically annual in high-risk cohorts.
- **No canonical `cancer_type` id** — never emit nasopharyngeal as a recommendation's `cancer_type`. When its regional/family trigger fires, surface it via a `symptom_alert` or in another recommendation's `summary` (recommend EBV serology, route to 耳鼻喉科).
- **Source:** NCC / 中山大学肿瘤防治中心 regional programs. **科室: 耳鼻喉科 / 头颈外科.** Only recommend with a regional/family trigger.

### 甲状腺癌 / Thyroid
- **无人群筛查推荐 / No population screening** — China stays neutral due to **overdiagnosis (过度诊断)** concerns (rising incidence, flat mortality). Aligns with U.S. (against screening asymptomatic adults).
- **High-risk only:** childhood/neck radiation, family history / hereditary syndrome (MEN2, RET, FAP), or a known nodule → neck ultrasound + **TI-RADS**; suspicious → FNAB. **科室: 甲状腺外科 / 内分泌科.**
- **No canonical `cancer_type` id** and no population screening — effectively never emitted as a recommendation; mention in prose only if a high-risk trigger fires.

### Cancers with no China population screening (高危/surveillance only)
For all of these: **无人群筛查推荐** — recommend only on a clear high-risk trigger; otherwise route to symptom awareness.
- **皮肤癌 / Skin:** low incidence in Chinese populations; surveillance only for albinism, xeroderma pigmentosum, chronic ulcers/scars. **科室: 皮肤科.**
- **口腔癌 / Oral:** opportunistic exam for **betel-nut (槟榔) chewers** (notable in 湖南/海南), heavy smokers/drinkers, oral leukoplakia. **科室: 口腔科.**
- **卵巢癌 / Ovarian:** no screen (CA-125+TVUS no mortality benefit). High-risk = BRCA1/2, Lynch → surveillance + risk-reducing surgery counseling. **科室: 妇科 / 遗传咨询.**
- **胰腺癌 / Pancreatic:** no screen. High-risk = familial / BRCA2/PALB2/CDKN2A/Lynch/Peutz-Jeghers → MRI/MRCP ± EUS at specialized centers. **科室: 消化内科.**
- **膀胱癌 / Bladder:** no screen. Occupational aromatic-amine exposure + heavy smoking → urine cytology ± cystoscopy in occupational-health settings only. Hematuria → workup. **科室: 泌尿外科.**
- **肾癌 / Kidney:** no screen; mostly incidental. Hereditary (VHL, BHD) → periodic imaging. **科室: 泌尿外科.**
- **子宫内膜癌 / Endometrial:** no screen. Lynch/obesity/PCOS/unopposed estrogen → sampling ± TVUS. **Postmenopausal bleeding → immediate evaluation. 科室: 妇科.**
- **睾丸癌 / Testicular:** no screen (rare). Cryptorchidism history → awareness/exam. **科室: 泌尿外科.**

---

## Red-flag symptoms (independent of screening)

Every reported symptom gets an **action-leading** safety note; never drop one.

| Symptom | Primary concern | Action lead |
|---|---|---|
| `blood_in_stool` | colorectal | 消化内科 / colonoscopy within 1–2 weeks; urgent care if heavy bleeding |
| `blood_in_urine` | bladder | 泌尿外科 + cystoscopy; any visible blood warrants prompt workup |
| `persistent_cough` | lung | imaging + 呼吸科 soon; urgent if hemoptysis |
| `unexplained_weight_loss` | GI/lung/pancreatic | workup within weeks |
| `new_lump` | breast/testicular/lymph by site | exam + imaging promptly |
| `changing_skin_lesion` | melanoma | 皮肤科 evaluation |
| `persistent_abdominal_pain` | GI/pancreatic/ovarian | 消化内科 evaluation |
| `dysphagia_hoarseness` | **esophageal** (high China incidence) | 消化内科 endoscopy if persistent >2–3 weeks |
| `postmenopausal_bleeding` | endometrial | 妇科 + endometrial evaluation promptly |

A symptom alert routes to care; it is not a diagnosis. Note for China: dysphagia and upper-GI symptoms carry higher prior probability given esophageal/gastric incidence — treat them as high-yield.

## Guardrails

- Lead with **高危人群 status**: in China, "do they meet the high-risk definition?" drives the recommendation more than age. Flag missing high-yield fields (**HBV/HCV, H. pylori, family history, region**).
- **Screen HBV/HCV carriers for liver and H. pylori/precursor carriers for gastric** — these are the signature Chinese screens; don't omit them by applying U.S. instincts.
- Prefer **ultrasound** as a real screening modality (liver, breast-dense, thyroid-nodule) — it's central to Chinese practice, not just adjunct.
- Don't push screening China doesn't recommend at population level — require a high-risk trigger (see Quick reference for the list).
- **Only emit a `cancer_type` from the 16 canonical ids.** Nasopharyngeal and thyroid are **not** in that set — never emit them as `cancer_type`; surface nasopharyngeal via a `symptom_alert`/prose when its trigger fires.
- Don't invent region, infection, or family history not in the profile. When region is unknown, note that high-incidence-area cancers (esophageal/gastric/nasopharyngeal) may need refinement.
- Distinguish **screening** (asymptomatic) from **diagnostic workup** (symptomatic).

## Quick reference

- **Actively screened from ~40–45:** liver (HBV/HCV/cirrhosis, US+AFP q6mo), gastric (≥45 + H. pylori/precursor/FDR, gastroscopy by score), esophageal (≥45 + region/FDR/lifestyle, iodine endoscopy), colorectal (≥40, questionnaire ≥4 → colonoscopy/FIT), lung (50–74, ≥20 pack-yr/quit<15y, or passive/COPD/occupational/family).
- **Women's program (35–64):** cervical (HPV q5y / TCT q3y, 25–65) + breast (**ultrasound** ± mammography, 45–70, q1–2y).
- **Later / opportunistic:** prostate (~60, PSA q2y), nasopharyngeal (endemic-region EBV only).
- **No population screen (high-risk only):** thyroid, skin, oral, ovarian, pancreatic, bladder, kidney, endometrial, testicular.
- **Signature China triggers:** chronic **HBV/HCV** → liver · **H. pylori** + atrophic gastritis → gastric · **high-incidence region** + FDR → esophageal/gastric/nasopharyngeal.
- **Every red-flag symptom → one action-leading note.** Never drop one.
