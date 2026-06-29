---
name: china-cancer-screening
description: Use when deciding which cancer screenings to recommend for a person under Chinese guidelines (国家癌症中心/NCC, 中国抗癌协会/CACA, 国家卫健委 NHC 方案) — given their age, sex, smoking, family history, BMI, HBV/HCV status, region, and exposures. Maps a health profile to China's risk-stratified (高危人群) screening recommendations, intervals, and modalities. Built for FixYou's screening advisor but usable by any agent doing China-based screening triage.
---

# China Cancer Screening Guidelines

> A full **Chinese-language version** of this skill is in [`SKILL.zh.md`](./SKILL.zh.md) — identical content, structure, and numbers, in native clinical Chinese.

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
| **region / origin** (if known) | residence in a **high-incidence area** is a formal trigger for esophageal/gastric/nasopharyngeal — infer from `occupational_exposure`/free-text if present; otherwise treat as unknown |

If a field is declined/unknown, don't assume — recommend on what's known and note the gap. **HBV/HCV status, H. pylori, and family history are the highest-yield fields** in the Chinese framework; flag them when missing.

## Decision procedure

1. **Check infection + family-history triggers first** (HBV/HCV → liver; H. pylori/precursors/FDR → gastric; FDR → colorectal/esophageal). These drive Chinese screening more than age.
2. **Apply the 高危人群 definition** for each cancer; if met, recommend the targeted screen.
3. **Apply numeric risk scores** where they exist (gastric score, colorectal questionnaire, liver aMAP tier) to set interval.
4. **Apply the women's program** (cervical + breast) by age.
5. **Handle every red-flag symptom** with an action-leading note.
6. **Assign severity** and a **department** (科室).

## Severity mapping

FixYou maps severity to points (high=30, medium=20, low=10):
- **high** — person clearly meets a 高危人群 definition with an active program (HBV carrier → liver; H. pylori + atrophic gastritis → gastric; high gastric score; FDR with GI cancer pulling start age in) AND screening is due.
- **medium** — standard program screening that applies by age (e.g., woman 45–70 for breast; adult in colorectal high-risk questionnaire range).
- **low** — borderline / shared-decision (prostate PSA; approaching but below high-risk threshold; thyroid where China stays neutral).

---

## High-incidence cancers (China screens actively)

### 肝癌 / Liver (HCC)
- **高危人群:** chronic liver disease or hereditary risk, **especially males 40–75**, with any of: **HBV and/or HCV infection**, cirrhosis (any cause), heavy alcohol, **MAFLD/fatty liver**, aflatoxin exposure, or family history of liver cancer. **Non-cirrhotic chronic HBV carriers are screened** — this is the defining China difference.
- **Test / interval:** **腹部超声 (ultrasound) + 血清 AFP every 6 months** minimum. Higher tiers add **AFP-L3 + 异常凝血酶原 (DCP/PIVKA-II)** ("肝癌三联检") and enhanced MRI.
- **Risk score (aMAP) tiers:** low → annual; medium → q6mo; high → q3–6mo + MRI; extremely high → US+AFP **q3mo** + MRI q6mo.
- **Profile hook:** `hep_b_c_status` = chronic HBV/HCV is an immediate **high-severity** trigger.
- **Source:** 《原发性肝癌诊疗指南（2024版）》NHC; CACA. **科室: 肝病科 / 感染科.**

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
- **高危人群:** **age 50–80** with **≥1** of: **smoking ≥20 pack-years** (former smokers eligible if quit **≤5 years** — note China's cutoff is tighter than the U.S. 15y); **passive smoke ≥20 years**; **occupational carcinogen exposure ≥5 years** (radon, arsenic, beryllium, chromium, asbestos, chloromethyl ether, silica, coke-oven/soot — ≥1y if high-intensity); **family history of lung cancer in a 1st/2nd-degree relative PLUS ≥15 pack-years or ≥15y passive smoke**.
- **Test / interval:** **低剂量螺旋CT (LDCT) annually**; two consecutive negatives → may extend to q2y.
- **Key China difference:** non-smoking pathways matter (passive smoke, occupational exposure, family history) — China has high never-smoker lung cancer burden, so don't gate solely on personal pack-years.
- **Source:** 《中国肺癌筛查与低剂量螺旋CT指南（2025）》NCC; NHC 2024 方案. **科室: 呼吸科 / 胸外科.**

### 结直肠癌 / Colorectal
- **高危人群 (two pathways):**
  - **Sporadic:** risk questionnaire scoring age, sex, **FDR with CRC**, smoking, BMI → **≥4 points = high-risk** (a single FDR <60 or ≥2 FDRs scores 4 outright). Screening window **age 40–74** for high-risk individuals.
  - **Hereditary:** **Lynch syndrome (林奇综合征)** / **FAP (家族性腺瘤性息肉病)** → separate intensive surveillance.
- **Test / interval:** **结肠镜 (colonoscopy)** first-line, **q5–10y** (normal → up to 10y); **annual 便潜血 (FIT)**. Alternatives if colonoscopy declined: sigmoidoscopy, CT colonography (结肠CT成像), **multi-target stool DNA (多靶点粪便DNA)**.
- **Key China difference:** starts at **40** but **only screens questionnaire-identified high-risk people** (risk-gated, not blanket) — reflecting endoscopy capacity.
- **Source:** 《中国结直肠癌筛查与早诊早治指南（2020）》NCC; NHC 2024 方案. **科室: 消化内科 / 肛肠科.**

---

## Women's-program cancers

### 乳腺癌 / Breast
- **一般风险:** women, **start 45, stop 70**; **乳腺X线/钼靶 (mammography) q2y**; **add 超声 (ultrasound)** for dense breasts (common in Chinese women — ultrasound is a co-primary modality, not just adjunct).
- **高危人群:** FDR with breast/ovarian cancer; ≥2 second-degree relatives with breast/ovarian cancer before 50; **BRCA1/2** carrier; chest radiotherapy before 30; elevated model risk → **start before 40**, **annual mammography + ultrasound q6–12mo**, add **MRI** when indicated.
- **National 两癌 program:** clinical exam + ultrasound + mammography for women **35–64**.
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
- **高危人群:** FDR with prostate cancer → start PSA at **45**; **BRCA2** carrier → start ~**40**.
- **Note:** starts later than the U.S. (lower incidence). **科室: 泌尿外科.** Severity low/medium.

### 鼻咽癌 / Nasopharyngeal (regionally important — no U.S. analog)
- **高危人群:** residents of **endemic southern China** (广东/广西/福建/湖南/海南), age ~30–69, esp. with family history or EBV high-risk markers.
- **Test:** **EBV serology (VCA-IgA / EBNA1-IgA) and/or plasma EBV-DNA**; positive → 鼻咽镜 (nasopharyngoscopy) + head/neck MRI. Typically annual in high-risk cohorts.
- **Source:** NCC / 中山大学肿瘤防治中心 regional programs. **科室: 耳鼻喉科 / 头颈外科.** Only recommend with a regional/family trigger.

### 甲状腺癌 / Thyroid
- **无人群筛查推荐 / No population screening** — China stays neutral due to **overdiagnosis (过度诊断)** concerns (rising incidence, flat mortality). Aligns with U.S. (against screening asymptomatic adults).
- **High-risk only:** childhood/neck radiation, family history / hereditary syndrome (MEN2, RET, FAP), or a known nodule → neck ultrasound + **TI-RADS**; suspicious → FNAB. **科室: 甲状腺外科 / 内分泌科.**

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
- Don't push screening China doesn't recommend at population level (thyroid, ovarian, pancreatic, skin, oral, bladder, kidney, testicular, endometrial) — require a high-risk trigger.
- Don't invent region, infection, or family history not in the profile. When region is unknown, note that high-incidence-area cancers (esophageal/gastric/nasopharyngeal) may need refinement.
- Distinguish **screening** (asymptomatic) from **diagnostic workup** (symptomatic).

## Quick reference

- **Actively screened from ~40–45:** liver (HBV/HCV/cirrhosis, US+AFP q6mo), gastric (≥45 + H. pylori/precursor/FDR, gastroscopy by score), esophageal (≥45 + region/FDR/lifestyle, iodine endoscopy), colorectal (≥40, questionnaire ≥4 → colonoscopy/FIT), lung (50–80, ≥20 pack-yr or passive/occupational/family).
- **Women's program (35–64):** cervical (HPV q5y / TCT q3y, 25–65) + breast (mammography + **ultrasound**, 45–70).
- **Later / opportunistic:** prostate (~60, PSA q2y), nasopharyngeal (endemic-region EBV only).
- **No population screen (high-risk only):** thyroid, skin, oral, ovarian, pancreatic, bladder, kidney, endometrial, testicular.
- **Signature China triggers:** chronic **HBV/HCV** → liver · **H. pylori** + atrophic gastritis → gastric · **high-incidence region** + FDR → esophageal/gastric/nasopharyngeal.
- **Every red-flag symptom → one action-leading note.** Never drop one.

## Sources

Every rule above is traceable to a named Chinese guideline or national program. Chinese guidelines are published as National Cancer Center (NCC) / CACA documents (in 中华肿瘤杂志 / 中国肿瘤) and as 国家卫健委 (NHC) 方案 — the document name + issuing body + year is the stable citation; public landing pages are linked where they resolve.

**National Cancer Center (NCC) — 国家癌症中心筛查与早诊早治指南:**
- 《中国肺癌筛查与低剂量螺旋CT指南（2025）》
- 《中国胃癌筛查与早诊早治指南（2022，北京）》— 中国肿瘤 2022;31(7)
- 《中国食管癌筛查与早诊早治指南（2022，北京）》— 中华肿瘤杂志 2022;44(6)
- 《中国结直肠癌筛查与早诊早治指南（2020）》
- 《中国女性乳腺癌筛查与早诊早治指南（2021，北京）》
- 《中国前列腺癌筛查与早诊早治指南（2022，北京）》— https://www.caivd-org.cn/m/article.asp?id=12617

**国家卫健委 (NHC) 方案 (2024 版):** 肺癌 / 结直肠癌 / 胃癌 / 食管癌筛查与早诊早治方案（2024年版）; 《原发性肝癌诊疗指南（2024版）》.

**CACA / 中华预防医学会 / 协会共识:**
- CACA 整合诊治指南 (乳腺癌、肝癌、甲状腺癌等) — 甲状腺癌: 《中国抗癌协会甲状腺癌整合诊治指南（2022）》
- 《中国女性乳腺癌筛查标准 T/CPMA 014-2020》— 中华预防医学会
- 《中国子宫颈癌筛查指南（2023）》; 加速消除宫颈癌行动

**National programs:**
- 城市癌症早诊早治项目 (Cancer Screening Program in Urban China) — https://www.cicams.ac.cn/dzb/news/dong/detail/2256.html
- 农村高发区早诊早治项目 (esophageal/gastric/liver); 两癌筛查 (cervical + breast, women 35–64)
- 鼻咽癌 EBV 区域筛查 — 中山大学肿瘤防治中心: http://www.sysucc.org.cn/node/2802

Guideline bodies update periodically (note several have 2024/2025 revisions); re-verify against the named document before relying on a specific age/interval/score cutoff. This skill is decision support, not a substitute for the source guideline or a clinician.
