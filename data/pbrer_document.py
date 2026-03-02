"""
PBRER Document: Cardiozan (Rivaximab Sodium) 10mg/20mg
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is the SOURCE DOCUMENT that both RAG approaches process.
25 "pages" of a realistic PBRER per ICH E2C(R2).
"""

DOCUMENT_PAGES: dict[int, str] = {
    1: """PERIODIC BENEFIT-RISK EVALUATION REPORT (PBRER)
Drug Name: Cardiozan (Rivaximab Sodium) 10mg / 20mg Tablets
Marketing Authorization Holder: PharmaCorp International Ltd.
International Birth Date: 15-March-2018
Reporting Period: 01-April-2023 to 31-March-2024
Report Version: 6.0
Date of Report: 30-June-2024
Prepared in accordance with ICH E2C(R2) guidelines.""",

    2: """TABLE OF CONTENTS
1. Introduction ................................. Page 3
2. Worldwide Marketing Authorization Status ..... Page 4
3. Actions Taken for Safety Reasons ............. Page 5
4. Changes to Reference Safety Information ...... Page 6
5. Estimated Exposure and Use Patterns .......... Page 7-8
6. Presentation of Data ......................... Page 9
   6.1 Reference Information ................... Page 9
   6.2 Cumulative Summary of SAEs .............. Page 10-11
   6.3 Cumulative Summary from Literature ....... Page 12
7. Signal Evaluation ............................ Page 13-15
   7.1 New Signal: Hepatotoxicity .............. Page 13
   7.2 Ongoing Signal: Thrombocytopenia ........ Page 14
   7.3 Closed Signal: QT Prolongation .......... Page 15
8. Risk Characterization ........................ Page 16-17
   8.1 Identified Risks ........................ Page 16
   8.2 Potential Risks ......................... Page 17
   8.3 Missing Information ..................... Page 17
9. Benefit Evaluation ........................... Page 18-19
10. Benefit-Risk Analysis ....................... Page 20-21
11. Conclusions and Recommendations ............. Page 22
Appendix A: Line Listings of ICSRs ............. Page 23
Appendix B: Cumulative Summary Tabulations ..... Page 24
Appendix C: Literature Search Strategy ......... Page 25""",

    3: """1. INTRODUCTION
Cardiozan (Rivaximab Sodium) is an oral direct Factor Xa inhibitor indicated for:
(a) Prevention of stroke and systemic embolism in adult patients with non-valvular
    atrial fibrillation (NVAF) with one or more risk factors
(b) Treatment of deep vein thrombosis (DVT) and pulmonary embolism (PE)
(c) Prevention of recurrent DVT and PE in adults

This PBRER covers the reporting period from 01-April-2023 to 31-March-2024.
The approved daily dose ranges from 10mg to 20mg depending on indication and
renal function. The drug was first approved on 15-March-2018 in the EU, followed
by US approval on 22-June-2018. This is the 6th PBRER since international birth date.

During this reporting period, no new indications were approved. A pediatric
investigation plan (PIP) for VTE prevention in adolescents aged 12-17 is ongoing
(Study CZ-PED-401). Results are expected Q2-2025.""",

    4: """2. WORLDWIDE MARKETING AUTHORIZATION STATUS
Cardiozan is currently approved in 78 countries across 6 regions:
- EU/EEA: Approved 15-Mar-2018 (all three indications)
- United States: Approved 22-Jun-2018 (NVAF and DVT/PE treatment)
- Japan: Approved 10-Sep-2018 (NVAF only; DVT/PE under review)
- Canada: Approved 05-Dec-2018 (all three indications)
- Australia: Approved 14-Feb-2019 (all three indications)
- China: Approved 20-Aug-2019 (NVAF only)

Pending applications:
- Brazil (ANVISA): Submitted 12-Jan-2024, under review
- South Korea (MFDS): Submitted 08-Nov-2023, Day 120 questions received

During the reporting period, Japan PMDA submitted a query regarding the
DVT/PE indication, requesting additional data from the CZ-DVT-302 study.
Response submitted on 15-Feb-2024. See Section 7 for signal evaluations
that may impact marketing authorization status.""",

    5: """3. ACTIONS TAKEN IN THE REPORTING PERIOD FOR SAFETY REASONS

3.1 Regulatory Actions:
- 15-Jun-2023: EMA PRAC recommended updating SmPC Section 4.4 to include
  warning about hepatotoxicity risk in patients with pre-existing liver disease.
  Implementation completed 01-Sep-2023.
- 22-Aug-2023: US FDA required REMS modification to include hepatic monitoring
  guidance in the Medication Guide.
- 10-Oct-2023: Health Canada issued a Dear Healthcare Professional Communication
  (DHPC) regarding reports of severe thrombocytopenia.

3.2 MAH-Initiated Actions:
- Updated Risk Management Plan (RMP) version 8.0 submitted to EMA on 30-Nov-2023
  to include hepatotoxicity as an identified risk (previously potential risk).
- Initiated post-marketing study CZ-HEP-501 to characterize hepatotoxicity risk
  factors. Study protocol approved by ethics committee 20-Jan-2024.
- Distributed educational materials to 45,000 healthcare professionals across EU
  regarding hepatic monitoring recommendations.

For complete details on signal assessment leading to these actions,
see Section 7.1 (Hepatotoxicity Signal Evaluation).""",

    6: """4. CHANGES TO REFERENCE SAFETY INFORMATION

The Company Core Data Sheet (CCDS) version 12.0 was updated during this
reporting period with the following changes:

4.1 Section 4.3 - Contraindications:
ADDED: "Severe hepatic impairment (Child-Pugh C) associated with coagulopathy
and clinically relevant bleeding risk"

4.2 Section 4.4 - Special Warnings and Precautions:
ADDED: "Hepatotoxicity: Cases of drug-induced liver injury (DILI), including
cases requiring hospitalization, have been reported. Liver function tests should
be performed prior to initiation and periodically during treatment. Cardiozan
should be discontinued if ALT > 5x ULN or ALT > 3x ULN with symptoms."

4.3 Section 4.8 - Undesirable Effects:
ADDED: "Hepatocellular injury" under 'Uncommon' (>=1/1,000 to <1/100)
UPDATED: "Thrombocytopenia" moved from 'Rare' to 'Uncommon'

4.4 Section 4.5 - Drug Interactions:
ADDED: "Concomitant use with strong CYP3A4 and P-gp inhibitors (e.g.,
ketoconazole, ritonavir) increases Cardiozan exposure by approximately 160%.
Dose adjustment recommended. See Appendix B, Table B-3 for PK data."

Full CCDS comparison (tracked changes) available in the reference information
section (Section 6.1).""",

    7: """5. ESTIMATED EXPOSURE AND USE PATTERNS (Part 1)

5.1 Cumulative Patient Exposure (since IBD):
- Total cumulative patient exposure: approximately 2.4 million patient-years
- Exposure during current reporting period: approximately 520,000 patient-years

5.2 Exposure by Indication (current reporting period):
| Indication                        | Patient-Years | % of Total |
|-----------------------------------|--------------|------------|
| NVAF - Stroke Prevention           | 312,000      | 60.0%      |
| DVT Treatment                      | 93,600       | 18.0%      |
| PE Treatment                       | 62,400       | 12.0%      |
| DVT/PE Recurrence Prevention       | 52,000       | 10.0%      |
| TOTAL                              | 520,000      | 100.0%     |

5.3 Exposure by Region (current reporting period):
| Region          | Patient-Years | % of Total |
|-----------------|--------------|------------|
| Europe (EU/EEA) | 218,400      | 42.0%      |
| North America   | 156,000      | 30.0%      |
| Asia-Pacific    | 104,000      | 20.0%      |
| Rest of World   | 41,600       | 8.0%       |
| TOTAL           | 520,000      | 100.0%     |""",

    8: """5. ESTIMATED EXPOSURE AND USE PATTERNS (Part 2)

5.4 Exposure by Age Group:
| Age Group    | Patient-Years | % of Total | Notes                          |
|-------------|--------------|------------|--------------------------------|
| 18-44 years | 26,000       | 5.0%       | Mainly DVT/PE treatment        |
| 45-64 years | 156,000      | 30.0%      | Mixed indications              |
| 65-74 years | 213,200      | 41.0%      | Predominantly NVAF             |
| >=75 years  | 124,800      | 24.0%      | NVAF; higher bleeding risk     |

5.5 Exposure by Dose:
- 20mg once daily: 364,000 patient-years (70%) — standard NVAF dose
- 10mg once daily: 156,000 patient-years (30%) — renal impairment / DVT prevention

5.6 Special Populations:
- Renal impairment (CrCl 15-50 mL/min): ~62,400 patient-years (12%)
- Hepatic impairment (Child-Pugh A/B): ~15,600 patient-years (3%)
- Elderly >=80 years: ~52,000 patient-years (10%)
- Concomitant antiplatelet therapy: ~78,000 patient-years (15%)

5.7 Data Sources:
Exposure estimates derived from IMS Health prescription data, company sales data,
and patient registries (CARDIO-REAL registry, n=28,450 patients enrolled).
Post-marketing study CZ-HEP-501 enrollment: 1,200 of planned 5,000 patients
as of data cutoff. For hepatotoxicity-specific exposure data, see Section 7.1.""",

    9: """6. PRESENTATION OF DATA

6.1 Reference Information:
The Reference Safety Information for this PBRER is the Company Core Data Sheet
(CCDS) version 12.0, dated 01-Sep-2023. Changes during the reporting period
are detailed in Section 4 of this report. The CCDS serves as the reference
document for determining expected vs. unexpected adverse reactions.

During this reporting period, the MAH received a total of 14,820 Individual
Case Safety Reports (ICSRs) from all sources:
- Spontaneous reports: 8,892 (60%)
- Clinical study reports: 2,964 (20%)
- Literature reports: 1,482 (10%)
- Other sources (registries, PSPs): 1,482 (10%)

Of these, 3,705 (25%) were classified as serious. The reporting rate for
serious cases was 7.1 per 1,000 patient-years, consistent with previous
reporting periods (range: 6.5-7.8 per 1,000 patient-years).

For a complete tabulation of all ICSRs by System Organ Class, refer to
Appendix B, Table B-1.""",

    10: """6.2 CUMULATIVE SUMMARY OF SERIOUS ADVERSE EVENTS (Part 1)

Cumulative SAEs by System Organ Class (SOC) — Top 10 SOCs:

| SOC                                    | Cumulative | This Period | Rate*  |
|----------------------------------------|-----------|-------------|--------|
| Blood and lymphatic system disorders    | 1,842     | 412         | 0.79   |
|   - Thrombocytopenia                   | 623       | 187         | 0.36   |
|   - Anaemia                            | 489       | 95          | 0.18   |
|   - Pancytopenia                       | 82        | 28          | 0.05   |
| Hepatobiliary disorders                 | 1,245     | 523         | 1.01   |
|   - Drug-induced liver injury          | 387       | 198         | 0.38   |
|   - Hepatocellular injury              | 312       | 156         | 0.30   |
|   - Cholestatic hepatitis              | 189       | 78          | 0.15   |
|   - Hepatic failure                    | 45        | 18          | 0.03   |
| Gastrointestinal disorders              | 1,156     | 267         | 0.51   |
|   - GI hemorrhage                      | 678       | 145         | 0.28   |
|   - Upper GI bleeding                  | 389       | 98          | 0.19   |
| Vascular disorders                      | 987       | 198         | 0.38   |
|   - Hemorrhage NOS                     | 567       | 112         | 0.22   |
| Nervous system disorders                | 876       | 178         | 0.34   |
|   - Intracranial hemorrhage            | 234       | 45          | 0.09   |

*Rate per 1,000 patient-years in current reporting period

NOTE: Hepatobiliary disorders showed the highest increase (+38%) compared to
the previous reporting period. See Section 7.1 for detailed signal evaluation.""",

    11: """6.2 CUMULATIVE SUMMARY OF SERIOUS ADVERSE EVENTS (Part 2)

Continued — SOCs ranked 6-10:

| SOC                                    | Cumulative | This Period | Rate*  |
|----------------------------------------|-----------|-------------|--------|
| Cardiac disorders                       | 756       | 156         | 0.30   |
|   - Myocardial infarction              | 234       | 48          | 0.09   |
|   - Cardiac failure                    | 178       | 34          | 0.07   |
| Renal and urinary disorders             | 645       | 134         | 0.26   |
|   - Acute kidney injury                | 312       | 67          | 0.13   |
| Respiratory disorders                   | 534       | 112         | 0.22   |
|   - Pulmonary hemorrhage               | 267       | 56          | 0.11   |
| Skin and subcutaneous disorders         | 423       | 89          | 0.17   |
| Infections and infestations             | 389       | 78          | 0.15   |

Fatal Cases Summary (Current Period):
- Total fatal cases: 67 (reporting rate: 0.13 per 1,000 patient-years)
- Intracranial hemorrhage: 23 (34.3% of fatal cases)
- Hepatic failure: 12 (17.9% of fatal cases)  <- NEW: See Section 7.1
- GI hemorrhage: 11 (16.4% of fatal cases)
- Pulmonary hemorrhage: 8 (11.9% of fatal cases)
- Cardiac causes: 7 (10.4% of fatal cases)
- Other: 6 (9.0% of fatal cases)

The increase in hepatic failure fatalities (from 4 in previous period to 12 in
current period) is being evaluated. See Section 7.1 for complete analysis.
For individual case narratives, refer to Appendix A.""",

    12: """6.3 CUMULATIVE SUMMARY FROM LITERATURE

During the reporting period, 342 publications relevant to Cardiozan safety
were identified through systematic literature review (see Appendix C for
search strategy). Key publications:

12.1 Hepatotoxicity:
- Chen et al. (2023), J Hepatology: Case series of 15 DILI cases with
  Cardiozan. Median time to onset: 45 days (range 14-180). 3 cases required
  transplant. Pattern: predominantly hepatocellular (73%), mixed (20%),
  cholestatic (7%). Risk factors identified: age >65, concomitant statin use,
  pre-existing NAFLD. [Assessed in Signal Evaluation, Section 7.1]

- Yamamoto et al. (2024), Drug Safety: Population-based cohort study (n=45,000)
  reporting hepatotoxicity incidence of 0.42% (95% CI: 0.35-0.49%) with
  Cardiozan vs. 0.18% with warfarin. Adjusted OR: 2.3 (95% CI: 1.8-2.9).

12.2 Thrombocytopenia:
- Rodriguez et al. (2023), Blood: Immune-mediated thrombocytopenia mechanism
  proposed. Anti-PF4 antibodies detected in 8/12 tested patients.

12.3 Beneficial Effects:
- CARDIO-STROKE trial (Martinez et al., NEJM 2024): Confirmed 62% relative
  risk reduction in stroke/systemic embolism vs placebo in NVAF patients
  (HR 0.38, 95% CI: 0.30-0.48). NNT = 24 over 2 years.

- CARDIO-VTE trial (Wilson et al., Lancet 2023): VTE recurrence rate 2.1%
  vs 8.7% with placebo at 12 months (HR 0.24, 95% CI: 0.18-0.32).""",

    13: """7. SIGNAL EVALUATION

7.1 NEW SIGNAL: HEPATOTOXICITY (Drug-Induced Liver Injury)

Signal Source: Spontaneous reports, clinical study data, literature
Signal Detection Date: 15-May-2023
Signal Status: CONFIRMED — Moved from potential to identified risk

7.1.1 Background:
Hepatotoxicity was listed as a potential risk in the RMP since version 3.0
(2020). During Q1-2023, disproportionality analysis detected a strengthening
signal: PRR = 2.8 (95% CI: 2.4-3.3) for hepatocellular injury with Cardiozan
vs. other DOACs in the EudraVigilance database.

7.1.2 Case Series Analysis:
During this reporting period, 198 new DILI cases were reported (cumulative: 387).

Demographics of DILI cases (current period, n=198):
- Mean age: 68.4 years (SD: 12.1)
- Female: 58% | Male: 42%
- Median time to onset: 42 days (IQR: 21-90 days)
- Median dose: 20mg (78% on 20mg dose)

Outcomes (current period):
- Recovered/resolved: 134 (67.7%)
- Recovering: 28 (14.1%)
- Not resolved: 18 (9.1%)
- Fatal: 12 (6.1%)     <- See also Section 6.2, fatal cases
- Unknown: 6 (3.0%)

Causality Assessment (WHO-UMC): Certain: 12, Probable: 89, Possible: 78,
Unlikely: 15, Unassessable: 4.

Dechallenge positive in 112/134 recovered cases (83.6%).
Rechallenge positive in 8/11 rechallenged cases (72.7%).

CONTINUED ON NEXT PAGE — Risk factors and mechanism analysis""",

    14: """7.2 ONGOING SIGNAL: THROMBOCYTOPENIA

Signal Source: Spontaneous reports, literature (Rodriguez et al., 2023)
Signal Detection Date: 10-Jan-2022
Signal Status: ONGOING EVALUATION

7.2.1 Current Assessment:
During this period, 187 new thrombocytopenia cases were reported (cumulative: 623).
Reporting rate increased from 0.28 to 0.36 per 1,000 patient-years.

Severity Distribution:
- Grade 1 (75,000-150,000/uL): 45%
- Grade 2 (50,000-75,000/uL): 28%
- Grade 3 (25,000-50,000/uL): 18%
- Grade 4 (<25,000/uL): 9% — includes 3 fatal hemorrhages secondary to
  severe thrombocytopenia

7.2.2 Mechanism Investigation:
Based on Rodriguez et al. (2023), an immune-mediated mechanism is suspected.
Anti-PF4 antibodies were detected in 8/12 tested patients, suggesting a
heparin-induced thrombocytopenia (HIT)-like mechanism.

The MAH has initiated laboratory investigation Study CZ-PLT-001 to further
characterize this mechanism. Interim results expected Q3-2024.

7.2.3 Risk Factors Identified:
- Concomitant heparin use (within 30 days): OR 3.2 (95% CI: 2.1-4.8)
- Prior HIT history: OR 5.7 (95% CI: 2.8-11.6)
- Autoimmune conditions: OR 2.1 (95% CI: 1.4-3.2)

Recommendation: Continue monitoring. Consider CCDS update to include
platelet monitoring recommendation for high-risk patients.
See also: Section 8.2 (Potential Risks) and Appendix B, Table B-4.""",

    15: """7.3 CLOSED SIGNAL: QT PROLONGATION

Signal Source: Spontaneous reports
Signal Detection Date: 05-Mar-2022
Signal Closure Date: 20-Dec-2023
Signal Status: CLOSED — Refuted

7.3.1 Summary:
A signal of QT prolongation was detected in March 2022 based on 23 spontaneous
reports of QT prolongation or Torsade de Pointes. Initial PRR was 1.8 (95% CI:
1.1-2.9) in the WHO VigiBase database.

7.3.2 Evaluation Performed:
- Thorough QT (TQT) study CZ-QT-201 completed (n=240 healthy volunteers):
  Mean ddQTcF at supratherapeutic dose (60mg): +3.2ms (90% CI: 1.8-4.6ms)
  This is below the 10ms threshold of regulatory concern.

- Retrospective ECG analysis from Phase 3 studies (n=8,450):
  No signal detected. Mean QTcF change from baseline: -0.8ms (95% CI: -1.4 to -0.2)

- Confounding analysis of 23 reported cases:
  * 18/23 patients had concomitant QT-prolonging drugs (amiodarone, sotalol)
  * 4/23 had pre-existing long QT syndrome
  * 1/23 had electrolyte imbalance (hypokalemia)

7.3.3 Conclusion:
The TQT study demonstrated no clinically relevant QT effect. The spontaneous
reports were confounded by concomitant medications and pre-existing conditions.
Signal closed as refuted. No CCDS changes required.""",

    16: """8. RISK CHARACTERIZATION

8.1 IDENTIFIED RISKS

| Risk                          | Source of Evidence          | Status Change |
|-------------------------------|----------------------------|---------------|
| Major bleeding                | Clinical trials, post-mkt  | Unchanged     |
| Intracranial hemorrhage       | Clinical trials, post-mkt  | Unchanged     |
| GI hemorrhage                 | Clinical trials, post-mkt  | Unchanged     |
| Hepatotoxicity/DILI           | Post-mkt, literature       | NEW (was potential)|
| Anemia                        | Clinical trials, post-mkt  | Unchanged     |
| Hypersensitivity reactions    | Post-marketing             | Unchanged     |

8.1.1 Hepatotoxicity — Detailed Risk Characterization:
Based on the signal evaluation in Section 7.1, hepatotoxicity has been
reclassified from potential risk to identified risk. Key risk metrics:
- Incidence rate: 0.38 per 1,000 patient-years (spontaneous reporting)
- Estimated true incidence (Yamamoto et al.): 0.42% (4.2 per 1,000)
- Case fatality rate: 6.1% among reported DILI cases
- Risk ratio vs. warfarin: 2.3 (95% CI: 1.8-2.9)

Risk factors (see Section 7.1 for full analysis):
- Age >65 years
- Pre-existing liver disease (NAFLD, hepatitis)
- Concomitant statin use
- CYP3A4 inhibitor co-administration

Risk minimization measures implemented:
- CCDS updated (Section 4)
- DHPC distributed (Section 3)
- Post-marketing study initiated (CZ-HEP-501)
- Educational materials distributed""",

    17: """8.2 POTENTIAL RISKS

| Risk                          | Source of Evidence          | Next Steps        |
|-------------------------------|----------------------------|--------------------|
| Thrombocytopenia (immune)     | Post-mkt, literature       | Study CZ-PLT-001  |
| Interstitial lung disease     | Post-marketing (12 cases)  | Monitoring         |
| Stevens-Johnson syndrome      | Post-marketing (4 cases)   | Monitoring         |
| Embryo-fetal toxicity         | Animal studies              | Contraindicated    |

8.2.1 Thrombocytopenia:
Remains as potential risk pending results of CZ-PLT-001 mechanism study.
If immune-mediated mechanism is confirmed, will be reclassified as identified
risk with appropriate CCDS updates. See Section 7.2 for full assessment.

8.3 MISSING INFORMATION

| Area                              | Action Planned                         |
|-----------------------------------|----------------------------------------|
| Pediatric use (<18 years)          | PIP Study CZ-PED-401 ongoing          |
| Pregnancy/lactation exposure       | Pregnancy registry CARDIO-PREG active |
| Severe renal impairment (CrCl<15)  | Contraindicated; PK study planned     |
| Long-term use (>5 years)           | CARDIO-REAL registry follow-up        |
| Extremes of body weight            | PK sub-study CZ-BW-201 planned        |

For comprehensive tabulations of all identified risks, potential risks, and
missing information with detailed risk minimization measures, refer to
Appendix B, Tables B-5 through B-8.""",

    18: """9. BENEFIT EVALUATION (Part 1)

9.1 Approved Indications and Clinical Evidence:

9.1.1 NVAF — Stroke Prevention:
Pivotal trial CARDIO-AF (n=14,264): Cardiozan 20mg vs. warfarin
- Primary endpoint (stroke/SE): HR 0.79 (95% CI: 0.66-0.96), p=0.02
- Major bleeding: HR 1.04 (95% CI: 0.90-1.20), NS
- ICH: HR 0.67 (95% CI: 0.47-0.93), p=0.02 — significant reduction
- All-cause mortality: HR 0.85 (95% CI: 0.70-1.02), NS trend

Post-marketing confirmation (CARDIO-STROKE, Martinez et al., NEJM 2024):
- Stroke/SE: HR 0.38 (95% CI: 0.30-0.48) vs. placebo — see Section 6.3
- NNT = 24 over 2 years

9.1.2 DVT/PE Treatment:
Pivotal trial CARDIO-VTE (n=8,282): Cardiozan vs. enoxaparin/warfarin
- Primary endpoint (recurrent VTE): HR 0.89 (95% CI: 0.73-1.09), non-inferior
- Major bleeding: HR 0.54 (95% CI: 0.37-0.79), p=0.001 — significant reduction
- Net clinical benefit: HR 0.79 (95% CI: 0.68-0.93), p=0.003

Post-marketing confirmation (CARDIO-VTE extension, Wilson et al., Lancet 2023):
- VTE recurrence: 2.1% vs 8.7% at 12 months, HR 0.24 (95% CI: 0.18-0.32)""",

    19: """9. BENEFIT EVALUATION (Part 2)

9.2 Real-World Evidence:

CARDIO-REAL Registry (n=28,450 enrolled as of data cutoff):
- Stroke/SE rate in NVAF patients: 1.2 per 100 patient-years
  (comparable to clinical trial rate of 1.3 per 100 patient-years)
- Major bleeding rate: 3.1 per 100 patient-years
  (slightly higher than trial rate of 2.8 — expected in real-world setting)
- Treatment persistence at 12 months: 82.3%
- Patient satisfaction score: 7.8/10 (vs. 6.2/10 for warfarin historical data)

9.3 Comparative Effectiveness:
Meta-analysis by Thompson et al. (2024), comparing all DOACs in NVAF:
- Stroke prevention: Cardiozan ranked 2nd (after apixaban)
- Major bleeding: Cardiozan ranked 3rd
- GI bleeding: Cardiozan ranked 4th (higher GI bleeding vs. apixaban/edoxaban)
- ICH prevention: Cardiozan ranked 1st (lowest ICH rate among DOACs)

9.4 Convenience and Compliance Benefits:
- Once-daily dosing (vs. twice-daily for some competitors)
- No routine coagulation monitoring (vs. warfarin INR monitoring)
- Fewer food interactions than warfarin
- Predictable pharmacokinetics

Overall, the clinical benefits of Cardiozan remain substantial and well-
established across all approved indications.""",

    20: """10. BENEFIT-RISK ANALYSIS (Part 1)

10.1 Framework:
This benefit-risk analysis follows the ICH E2C(R2) structured approach,
incorporating the PrOACT-URL framework.

10.2 Benefit-Risk Balance by Indication:

10.2.1 NVAF — Stroke Prevention:
BENEFITS:
- 21% relative risk reduction in stroke/SE vs. warfarin (pivotal trial)
- 62% RRR vs. placebo (post-marketing, CARDIO-STROKE)
- 33% reduction in ICH vs. warfarin
- Once-daily dosing, no INR monitoring

RISKS:
- Major bleeding rate comparable to warfarin
- NEW: Hepatotoxicity risk (0.42% incidence, case fatality 6.1%)
- GI bleeding higher than some competitor DOACs
- Thrombocytopenia (potential immune-mediated mechanism under investigation)

ASSESSMENT: Benefits clearly outweigh risks for NVAF indication. The newly
identified hepatotoxicity risk, while clinically important, is manageable with
appropriate monitoring (LFTs before and during treatment). The stroke prevention
benefit is life-saving and well-demonstrated.

Impact of hepatotoxicity on benefit-risk: The estimated excess hepatic fatality
risk is approximately 0.023 per 1,000 patient-years, while the stroke prevention
benefit prevents approximately 8.3 strokes per 1,000 patient-years. The benefit-
risk ratio remains strongly favorable.""",

    21: """10. BENEFIT-RISK ANALYSIS (Part 2)

10.2.2 DVT/PE Treatment and Secondary Prevention:
BENEFITS:
- Non-inferior efficacy to standard of care (enoxaparin/warfarin)
- 46% reduction in major bleeding vs. standard of care
- Superior net clinical benefit
- Simplified single-drug approach (no initial parenteral therapy needed)

RISKS:
- Same hepatotoxicity risk applies
- Shorter treatment duration may reduce cumulative hepatic risk

ASSESSMENT: Benefits outweigh risks. Bleeding reduction is particularly
important in the acute VTE setting.

10.3 Special Populations Considerations:
- Elderly (>=75 years): Higher bleeding risk but also higher stroke risk.
  Net benefit maintained. Hepatic monitoring especially important.
- Renal impairment: 10mg dose provides adequate efficacy with acceptable safety.
  No dose adjustment needed for CrCl >50 mL/min.
- Hepatic impairment: Contraindicated in Child-Pugh C. Use with caution in
  Child-Pugh A/B with enhanced monitoring. See updated CCDS Section 4.3.

10.4 Overall Benefit-Risk Conclusion:
The overall benefit-risk balance of Cardiozan remains FAVORABLE across all
approved indications, with the requirement for hepatic monitoring as an
additional risk minimization measure. The benefit-risk should be reassessed
upon completion of studies CZ-HEP-501 and CZ-PLT-001.""",

    22: """11. CONCLUSIONS AND RECOMMENDATIONS

11.1 Key Conclusions:

1. The overall benefit-risk balance of Cardiozan remains FAVORABLE for all
   approved indications.

2. Hepatotoxicity has been reclassified from potential to IDENTIFIED RISK
   based on cumulative evidence (387 DILI cases, PRR 2.8, literature support).
   Appropriate risk minimization measures have been implemented.

3. The thrombocytopenia signal remains under evaluation, with a possible
   immune-mediated mechanism (anti-PF4 antibodies). The CZ-PLT-001 study
   is ongoing to characterize the mechanism.

4. The QT prolongation signal has been CLOSED as refuted, based on a
   thorough QT study and confounding analysis.

5. No new safety signals were detected during this reporting period.

11.2 Recommendations:

1. Continue routine pharmacovigilance with enhanced monitoring for
   hepatotoxicity and thrombocytopenia.
2. Submit RMP version 8.0 update to all relevant regulatory authorities.
3. Complete CZ-HEP-501 enrollment by Q4-2024 (target: 5,000 patients).
4. Await CZ-PLT-001 interim results (Q3-2024) before next CCDS update.
5. Next PBRER due: 30-June-2025 (covering 01-Apr-2024 to 31-Mar-2025).
6. Recommend no changes to approved indications, doses, or target populations.

For complete references, data tabulations, and supplementary materials,
see Appendices A through C.""",

    23: """APPENDIX A: LINE LISTINGS OF INDIVIDUAL CASE SAFETY REPORTS (ICSRs)

[Appendix A is referenced throughout the report for individual case narratives]

A.1 Fatal Cases — Hepatic Failure (n=12):
Case CZ-2023-00891: 72F, NVAF, 20mg, concomitant atorvastatin 40mg + amlodipine.
Onset Day 38. ALT 1,245 U/L, AST 987 U/L, bilirubin 8.9 mg/dL. Hy's Law case.
Transplant waitlisted but died Day 52 from multi-organ failure.
Causality: Certain (WHO-UMC). RUCAM score: 9 (highly probable).

Case CZ-2023-01204: 81M, DVT treatment, 20mg, pre-existing NAFLD, concomitant
ritonavir (HIV). Onset Day 21. Rapid progression to fulminant hepatic failure.
Died Day 28. Notable: CYP3A4 inhibitor interaction likely contributed.
Causality: Probable. RUCAM score: 7.

Case CZ-2023-01567: 67F, NVAF, 20mg, no significant comorbidities. Onset Day 90.
Gradual onset. ALT peaked at 678 U/L. Initially improving but developed
hepatorenal syndrome. Died Day 112.
Causality: Probable. RUCAM score: 6.

[... 9 additional fatal hepatic cases listed in full appendix ...]

A.2 Fatal Cases — Intracranial Hemorrhage (n=23):
[... detailed case narratives available in full appendix ...]

A.3 Fatal Cases — GI Hemorrhage (n=11):
[... detailed case narratives available in full appendix ...]""",

    24: """APPENDIX B: CUMULATIVE SUMMARY TABULATIONS

Table B-1: All ICSRs by System Organ Class and Seriousness
[Referenced from Section 6.1 — Full tabulation of 14,820 ICSRs]
Total Serious: 3,705 | Total Non-Serious: 11,115

Table B-2: ICSRs by Reporter Type and Region
Healthcare Professionals: 9,876 (66.6%) | Consumers: 4,944 (33.4%)

Table B-3: Pharmacokinetic Drug Interaction Data
[Referenced from Section 4.4 — CCDS changes]
| Interacting Drug        | Effect on Cardiozan AUC | Recommendation         |
|------------------------|------------------------|------------------------|
| Ketoconazole 400mg     | +160%                  | Dose reduce to 10mg    |
| Ritonavir 600mg        | +153%                  | Dose reduce to 10mg    |
| Erythromycin 500mg     | +34%                   | No adjustment needed   |
| Fluconazole 200mg      | +42%                   | Caution; consider 10mg |
| Rifampicin 600mg       | -50%                   | Avoid concomitant use  |
| Carbamazepine          | -35%                   | Avoid concomitant use  |

Table B-4: Thrombocytopenia Cases by Severity and Risk Factor
[Referenced from Section 7.2]

Table B-5 through B-8: Risk Minimization Measures
[Referenced from Section 8.3]
B-5: Identified Risks - Detailed Measures
B-6: Potential Risks - Detailed Measures
B-7: Missing Information - Study Status
B-8: Effectiveness of Risk Minimization (metrics)""",

    25: """APPENDIX C: LITERATURE SEARCH STRATEGY

[Referenced from Section 6.3]

C.1 Search Databases:
- PubMed/MEDLINE
- Embase
- Cochrane Library
- WHO Pharmaceutical Newsletter
- Reactions Weekly

C.2 Search Terms:
Primary: "Cardiozan" OR "Rivaximab" OR "rivaximab sodium"
Combined with: "adverse" OR "safety" OR "toxicity" OR "side effect" OR
"pharmacovigilance" OR "post-marketing"

C.3 Search Period: 01-April-2023 to 31-March-2024

C.4 Results:
- Total hits: 1,247
- After duplicate removal: 892
- After title/abstract screening: 342 relevant publications
- Full-text review: 342 (all relevant publications reviewed)
- Publications with new safety information: 28
- Publications requiring ICSR submission: 15

C.5 Key Publications (with new safety information):
1. Chen et al. (2023) J Hepatology — DILI case series [Section 6.3, 7.1]
2. Yamamoto et al. (2024) Drug Safety — Hepatotoxicity cohort [Section 6.3, 7.1]
3. Rodriguez et al. (2023) Blood — Thrombocytopenia mechanism [Section 6.3, 7.2]
4. Martinez et al. (2024) NEJM — CARDIO-STROKE efficacy [Section 6.3, 9.1]
5. Wilson et al. (2023) Lancet — CARDIO-VTE extension [Section 6.3, 9.1]
6. Thompson et al. (2024) — DOAC meta-analysis [Section 9.3]

END OF PBRER REPORT""",
}


def get_full_text() -> str:
    return "\n\n".join(f"[PAGE {p}]\n{c}" for p, c in sorted(DOCUMENT_PAGES.items()))


def get_page(page_num: int) -> str:
    return DOCUMENT_PAGES.get(page_num, "")


def get_pages(start: int, end: int) -> str:
    return "\n\n".join(
        f"[PAGE {p}]\n{DOCUMENT_PAGES[p]}"
        for p in range(start, end + 1)
        if p in DOCUMENT_PAGES
    )
