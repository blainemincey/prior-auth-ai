"""
Synthetic demo claims for the live webcast demonstration.

SCENARIO A — CLM-2025-0001847  (James R. Thornton)
  Lumbar Spine MRI, Prior Auth pended for medical necessity
  Engineered top matches:
    Policy:       POL-MRI-LUMBAR-2024-03
    Prior claims: PCL-2024-MRI-0892, PCL-2024-MRI-1103

SCENARIO B — CLM-2025-0003291  (Eleanor K. Vasquez)
  Infliximab IV infusion, pended for high-cost biologic / step-therapy review
  Engineered top matches:
    Policy:       POL-BIOLOGIC-RA-2024-07
    Prior claims: PCL-2024-BIO-2244, PCL-2024-BIO-1891

SCENARIO C — CLM-2025-0007734  (Patricia A. Reeves)
  Semaglutide (Wegovy) 2.4mg weekly, pended for GLP-1 lifestyle documentation
  Engineered top matches:
    Policy:       POL-GLP1-OBESITY-2024-08
    Prior claims: PCL-2024-GLP1-1456, PCL-2024-GLP1-0923
"""

DEMO_CLAIMS = {
    "A": {
        "claim_id": "CLM-2025-0001847",
        "scenario": "A",
        "demo_claim": True,

        # Member
        "member_id": "HUM-OH-4482019-01",
        "member_name": "James R. Thornton",
        "member_dob": "1967-03-14",
        "member_age": 58,
        "member_gender": "M",

        # Plan
        "plan_type": "PPO",
        "plan_name": "Acme Health Commercial PPO Gold",
        "plan_line_of_business": "Commercial",
        "group_id": "GRP-HUM-4482019",
        "state": "OH",

        # Provider
        "ordering_provider_name": "Dr. Michael Saenz, MD",
        "ordering_provider_npi": "1558473920",
        "ordering_provider_specialty": "Internal Medicine",
        "rendering_facility_name": "Midwest Diagnostic Imaging Center",
        "rendering_facility_npi": "1902837465",
        "rendering_facility_address": {
            "street": "3400 Olentangy River Rd",
            "city": "Columbus",
            "state": "OH",
            "zip": "43202",
        },

        # Service
        "service_date": "2025-05-15",
        "claim_received_date": "2025-05-16",
        "claim_type": "Professional",
        "place_of_service_code": "22",
        "place_of_service_description": "On Campus — Outpatient Hospital",

        # Diagnoses
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "secondary_diagnoses": [
            {"code": "M54.4", "description": "Lumbago with sciatica, unspecified side"},
            {"code": "M47.816", "description": "Spondylosis with radiculopathy, lumbar region"},
        ],

        # Procedures
        "procedure_codes": [
            {
                "code": "72148",
                "type": "CPT",
                "description": "MRI Lumbar Spine without contrast",
                "units": 1,
                "billed_amount": 4250.00,
            }
        ],

        # Financials
        "total_billed_amount": 4250.00,
        "total_allowed_amount": None,
        "total_paid_amount": None,

        # Authorization
        "prior_auth_required": True,
        "prior_auth_number": None,

        # Adjudication
        "adjudication_status": "PENDED",
        "pend_reason_code": "PA-MN-001",
        "pend_reason_description": (
            "Prior Authorization Required — Medical Necessity Not Established. "
            "Physical therapy documentation submitted is incomplete (missing initial "
            "evaluation and functional outcome measures). Additional clinical records "
            "required per plan policy POL-MRI-LUMBAR-2024-03."
        ),
        "assigned_reviewer": "Patricia Chen, RN, CCM",
        "review_due_date": "2025-05-23",

        # Clinical notes (unstructured — embedded by Voyage AI)
        "clinical_notes": (
            "UTILIZATION MANAGEMENT CLINICAL REVIEW NOTE\n"
            "Date: May 16, 2025  |  Reviewer: Patricia Chen, RN, CCM\n"
            "Member: James R. Thornton (HUM-OH-4482019-01)\n"
            "Auth Request: Lumbar Spine MRI without contrast (CPT 72148)\n\n"
            "CLINICAL SUMMARY:\n"
            "Member is a 58-year-old male with a 14-week history of progressive low back "
            "pain with left lower-extremity radiation in an L4-L5 dermatomal distribution, "
            "consistent with lumbar disc herniation causing radiculopathy. Onset followed a "
            "workplace lifting incident in February 2025. Ordering physician Dr. Michael "
            "Saenz (Internal Medicine) documents worsening functional limitation despite a "
            "structured multimodal conservative treatment course.\n\n"
            "CONSERVATIVE TREATMENT HISTORY:\n"
            "- Physical therapy: 12 sessions completed March–April 2025 at St. Luke's "
            "Physical Therapy, Columbus, OH. Discharge summary documents initial NRS pain "
            "score 8/10 improving to 5/10 but with persistent left-sided radiculopathy. "
            "Initial PT evaluation and functional outcome measures were submitted but "
            "discharge functional outcome scores are absent from the documentation packet.\n"
            "- NSAIDs: Naproxen 500 mg BID trialed for 8 weeks; discontinued due to "
            "documented GI intolerance (endoscopy 4/2025 confirming gastritis). Switched "
            "to cyclobenzaprine 5 mg TID PRN with partial response.\n"
            "- Chiropractic manipulation: 6 visits with Dr. A. Patel, DC (March 2025). "
            "Provider attestation dated May 3, 2025 notes no clinically significant "
            "improvement in radicular symptoms.\n\n"
            "CLINICAL EXAMINATION FINDINGS (from Dr. Saenz note, May 14, 2025):\n"
            "- NRS pain score 7/10 at rest, 9/10 with lumbar flexion/extension\n"
            "- Straight leg raise test positive at 45 degrees bilaterally, left > right\n"
            "- Neurological exam: diminished patellar reflex left knee; mild dermatomal "
            "sensory deficit in L4 distribution; no bowel or bladder dysfunction\n"
            "- Plain radiographs (lumbar spine AP/Lateral, April 28, 2025): moderate disc "
            "space narrowing at L4-L5 and L5-S1 with marginal osteophytosis; no acute "
            "fracture or listhesis identified. Radiographs are insufficient to characterize "
            "soft-tissue disc pathology or neural element compromise.\n\n"
            "ORDERING PHYSICIAN RATIONALE:\n"
            "'Patient has completed a structured conservative care program meeting ACR "
            "guidelines. Clinical presentation is consistent with lumbar disc herniation "
            "with L4-L5 radiculopathy. MRI is required to characterize disc morphology, "
            "assess for nerve root compression, and determine candidacy for epidural "
            "steroid injection or surgical consultation. X-ray findings alone are "
            "insufficient to guide interventional management decisions.'\n\n"
            "PEND RATIONALE:\n"
            "Auth request partially meets plan criteria under POL-MRI-LUMBAR-2024-03. "
            "Conservative therapy duration and modality requirements appear met (physical "
            "therapy, NSAID trial, chiropractic). However, physical therapy documentation "
            "is incomplete — discharge functional outcome measures (e.g., Oswestry "
            "Disability Index or equivalent) are absent. Additional documentation "
            "requested. Follow-up due May 23, 2025.\n\n"
            "STATUS: PENDED — Awaiting complete PT documentation."
        ),

        # Embedding fields (populated by setup script)
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,

        # AI output fields (populated by demo loop)
        "ai_rationale": None,
        "ai_determination": None,
        "ai_rationale_generated_at": None,
        "ai_supporting_policies": [],
        "ai_comparable_cases": [],

        # Status tracking
        "created_at": "2025-05-16T09:23:00Z",
        "updated_at": "2025-05-16T10:15:00Z",
        "status_history": [
            {"status": "RECEIVED", "timestamp": "2025-05-16T09:23:00Z", "note": "Claim received via clearinghouse"},
            {"status": "PENDED", "timestamp": "2025-05-16T10:15:00Z", "note": "PA-MN-001: Incomplete PT documentation"},
        ],
    },

    "B": {
        "claim_id": "CLM-2025-0003291",
        "scenario": "B",
        "demo_claim": True,

        # Member
        "member_id": "HUM-TX-2291847-02",
        "member_name": "Eleanor K. Vasquez",
        "member_dob": "1981-07-22",
        "member_age": 44,
        "member_gender": "F",

        # Plan
        "plan_type": "PPO",
        "plan_name": "Acme Health Commercial PPO Platinum",
        "plan_line_of_business": "Commercial",
        "group_id": "GRP-HUM-2291847",
        "state": "TX",

        # Provider
        "ordering_provider_name": "Dr. Priya Nair, MD",
        "ordering_provider_npi": "1679234810",
        "ordering_provider_specialty": "Rheumatology",
        "rendering_facility_name": "Austin Rheumatology Associates",
        "rendering_facility_npi": "1847293011",
        "rendering_facility_address": {
            "street": "12200 Renfert Way, Suite 310",
            "city": "Austin",
            "state": "TX",
            "zip": "78758",
        },

        # Service
        "service_date": "2025-05-19",
        "claim_received_date": "2025-05-20",
        "claim_type": "Professional",
        "place_of_service_code": "11",
        "place_of_service_description": "Office",

        # Diagnoses
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, right shoulder",
        "secondary_diagnoses": [
            {"code": "M05.621", "description": "Rheumatoid arthritis with rheumatoid factor, right elbow"},
            {"code": "Z79.899", "description": "Other long term (current) drug therapy"},
        ],

        # Procedures
        "procedure_codes": [
            {
                "code": "J1745",
                "type": "HCPCS",
                "description": "Infliximab, 10 mg (Remicade)",
                "units": 40,
                "billed_amount": 18420.00,
                "ndc": "57894-030-01",
                "route": "Intravenous infusion",
                "dose": "400 mg (5 mg/kg; member weight 80 kg)",
            }
        ],

        # Financials
        "total_billed_amount": 18420.00,
        "total_allowed_amount": None,
        "total_paid_amount": None,

        # Authorization
        "prior_auth_required": True,
        "prior_auth_number": "PA-2025-BIO-00441",

        # Adjudication
        "adjudication_status": "PENDED",
        "pend_reason_code": "MN-DRUG-HCB-002",
        "pend_reason_description": (
            "Medical Necessity Review Required — High-Cost Biologic claim exceeding "
            "plan threshold ($15,000 per claim event). Step-therapy compliance "
            "verification required per plan policy POL-BIOLOGIC-RA-2024-07. "
            "Automated flag triggered by adjudication engine."
        ),
        "assigned_reviewer": "Sandra Mills, PharmD, RPh",
        "review_due_date": "2025-05-26",

        # Clinical notes (unstructured — embedded by Voyage AI)
        "clinical_notes": (
            "PHARMACY BENEFIT MANAGEMENT — CLINICAL REVIEW NOTE\n"
            "Date: May 20, 2025  |  Reviewer: Sandra Mills, PharmD, RPh\n"
            "Member: Eleanor K. Vasquez (HUM-TX-2291847-02)\n"
            "Claim: Infliximab (Remicade) 400 mg IV infusion — HCPCS J1745 x 40 units\n"
            "NDC: 57894-030-01  |  Billed: $18,420.00\n\n"
            "CLINICAL SUMMARY:\n"
            "Member is a 44-year-old female with an established diagnosis of moderate-to-"
            "severe rheumatoid arthritis (RA) with positive rheumatoid factor (ICD-10 "
            "M05.611, M05.621), first diagnosed in 2019 by Dr. Priya Nair, MD, "
            "Rheumatology, Austin Rheumatology Associates. This claim represents the "
            "fifth infliximab infusion cycle in the current 12-month authorization "
            "period (Auth PA-2025-BIO-00441). Infliximab is dosed at 5 mg/kg IV every "
            "8 weeks; member weight documented at 80 kg.\n\n"
            "STEP THERAPY HISTORY (per rheumatologist chart notes and pharmacy records):\n"
            "1. Methotrexate (MTX) 20 mg weekly PO: initiated January 2020. Trialed for "
            "10 months. Discontinued November 2020 due to hepatotoxicity — ALT 3× ULN "
            "confirmed by lab report dated November 12, 2020 (ALT 112 U/L; ULN 37 U/L). "
            "Documented as intolerance/adverse event, not inadequate response.\n"
            "2. Hydroxychloroquine (Plaquenil) 400 mg daily: initiated December 2020. "
            "Trialed 6 months. Discontinued April 2021 due to inadequate disease response "
            "— DAS28-CRP score 5.4 at 6-month assessment (moderate-to-high disease "
            "activity). Specialist note documents persistent morning stiffness >60 min "
            "and functional limitation.\n"
            "3. Leflunomide (Arava) 20 mg daily: initiated May 2021. Trialed 5 months. "
            "Discontinued September 2021 due to peripheral neuropathy — documented by "
            "neurology consult, Dr. R. Kim, MD, September 8, 2021 (nerve conduction "
            "study confirming sensorimotor polyneuropathy).\n"
            "4. Adalimumab biosimilar (Hadlima, 40 mg SC biweekly): initiated October "
            "2021 following specialist recommendation. Inadequate response at 6 months — "
            "DAS28-CRP 6.1 at April 2022 reassessment. Discontinued June 2022 due to "
            "primary non-response.\n"
            "5. Infliximab (Remicade) 5 mg/kg IV q8 weeks: initiated August 2022 per "
            "Dr. Nair recommendation following adalimumab failure. Current regimen for "
            "approximately 33 months.\n\n"
            "CURRENT CLINICAL STATUS:\n"
            "- DAS28-CRP: 2.8 (low disease activity; target <3.2 per treat-to-target "
            "protocol)\n"
            "- CRP: 0.4 mg/dL (reference <0.8 mg/dL); ESR: 18 mm/hr\n"
            "- RF titer: 1:160; Anti-CCP: 82 U/mL (elevated, confirming seropositive RA)\n"
            "- HAQ-DI (Health Assessment Questionnaire — Disability Index): 0.625 "
            "(mild functional limitation)\n"
            "- Patient reports full ADL independence; able to work full-time\n"
            "- No active or recent infections\n"
            "- TB screening: QuantiFERON-TB Gold negative, March 2025\n"
            "- Hepatitis B surface antigen: negative (baseline, 2022)\n\n"
            "PRESCRIBER ATTESTATION (Dr. Priya Nair, MD — May 18, 2025):\n"
            "'Ms. Vasquez has achieved sustained low disease activity on infliximab after "
            "failing three conventional synthetic DMARDs (methotrexate — hepatotoxicity, "
            "hydroxychloroquine — inadequate response, leflunomide — neuropathy) and one "
            "biologic DMARD (adalimumab biosimilar — primary non-response). Discontinuing "
            "infliximab at this point of disease control would place the patient at "
            "significant risk of disease flare. Continuation of current regimen is "
            "medically necessary to maintain disease remission and prevent joint "
            "destruction.'\n\n"
            "PEND RATIONALE:\n"
            "Claim automatically flagged per plan adjudication protocol — infliximab "
            "claim event exceeds $15,000 threshold triggering medical necessity review "
            "(MN-DRUG-HCB-002). Step therapy history appears robust — three csDMARD "
            "trials documented with objective failure criteria (lab-confirmed "
            "hepatotoxicity, validated disease activity scores, specialist-confirmed "
            "neuropathy) plus one prior biologic failure. Reviewer to verify step therapy "
            "documentation completeness per POL-BIOLOGIC-RA-2024-07 and confirm "
            "continued medical necessity for biologic continuation.\n\n"
            "STATUS: PENDED — Medical necessity and step-therapy compliance verification "
            "in progress."
        ),

        # Embedding fields
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,

        # AI output fields
        "ai_rationale": None,
        "ai_determination": None,
        "ai_rationale_generated_at": None,
        "ai_supporting_policies": [],
        "ai_comparable_cases": [],

        # Status tracking
        "created_at": "2025-05-20T11:47:00Z",
        "updated_at": "2025-05-20T12:30:00Z",
        "status_history": [
            {"status": "RECEIVED", "timestamp": "2025-05-20T11:47:00Z", "note": "Claim received via EDI 837P"},
            {"status": "PENDED", "timestamp": "2025-05-20T12:30:00Z", "note": "MN-DRUG-HCB-002: High-cost biologic threshold exceeded"},
        ],
    },

    "C": {
        "claim_id": "CLM-2025-0007734",
        "scenario": "C",
        "demo_claim": True,

        # Member
        "member_id": "HUM-FL-6619042-03",
        "member_name": "Patricia A. Reeves",
        "member_dob": "1973-03-14",
        "member_age": 52,
        "member_gender": "F",

        # Plan
        "plan_type": "PPO",
        "plan_name": "Acme Health Choice PPO Gold",
        "plan_line_of_business": "Commercial",
        "group_id": "GRP-HUM-6619042",
        "state": "FL",

        # Provider
        "ordering_provider_name": "Dr. Marcus T. Ellis, MD",
        "ordering_provider_npi": "1987654324",
        "ordering_provider_specialty": "Endocrinology",
        "rendering_facility_name": "Tampa Bay Endocrinology & Diabetes Center",
        "rendering_facility_npi": "1834920175",
        "rendering_facility_address": {
            "street": "4502 Fletcher Ave, Suite 210",
            "city": "Tampa",
            "state": "FL",
            "zip": "33613",
        },

        # Service
        "service_date": "2025-03-19",
        "claim_received_date": "2025-03-20",
        "claim_type": "Professional",
        "place_of_service_code": "11",
        "place_of_service_description": "Office",

        # Diagnoses
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "secondary_diagnoses": [
            {"code": "E11.65", "description": "Type 2 diabetes mellitus with hyperglycemia"},
            {"code": "I10",    "description": "Essential (primary) hypertension"},
            {"code": "G47.33", "description": "Obstructive sleep apnea (adult)"},
            {"code": "E78.5",  "description": "Hyperlipidemia, unspecified"},
        ],

        # Procedures
        "procedure_codes": [
            {
                "code": "S0148",
                "type": "HCPCS",
                "description": "Semaglutide injection (Wegovy) 2.4 mg/dose, weekly",
                "units": 4,
                "billed_amount": 1349.02,
                "ndc": "00169-4870-13",
                "route": "Subcutaneous injection",
                "dose": "2.4 mg weekly (maintenance dose)",
            }
        ],

        # Financials
        "total_billed_amount": 1349.02,
        "total_allowed_amount": None,
        "total_paid_amount": None,

        # Authorization
        "prior_auth_required": True,
        "prior_auth_number": None,

        # Adjudication
        "adjudication_status": "PENDED",
        "pend_reason_code": "PA-OBE-GLP1-001",
        "pend_reason_description": (
            "Prior Authorization Required — GLP-1 Agonist for Chronic Weight Management. "
            "Formal documentation of 6-month structured, medically supervised weight "
            "management program not submitted. Plan policy POL-GLP1-OBESITY-2024-08 "
            "requires program records prior to pharmacotherapy authorization."
        ),
        "assigned_reviewer": "Kevin Park, PharmD",
        "review_due_date": "2025-03-27",

        # Clinical notes (unstructured — embedded by Voyage AI)
        "clinical_notes": (
            "PHARMACY & MEDICAL NECESSITY REVIEW — CLINICAL NOTE\n"
            "Date: March 20, 2025  |  Reviewer: Kevin Park, PharmD\n"
            "Member: Patricia A. Reeves (HUM-FL-6619042-03)\n"
            "Claim: Semaglutide 2.4 mg weekly (Wegovy) — HCPCS S0148 x 4 units\n"
            "NDC: 00169-4870-13  |  Billed: $1,349.02\n\n"
            "CLINICAL SUMMARY:\n"
            "Member is a 52-year-old female with a complex metabolic history presenting "
            "for prior authorization of semaglutide 2.4 mg weekly (Wegovy) for chronic "
            "weight management. Requesting provider is Dr. Marcus T. Ellis, MD, Board-"
            "Certified Endocrinology and Metabolism, Tampa Bay Endocrinology & Diabetes "
            "Center. Member was referred by primary care following failure to achieve "
            "sustained weight loss through conventional measures over 24 months and "
            "progressive metabolic deterioration.\n\n"
            "ANTHROPOMETRIC DATA:\n"
            "Height: 5'4\" (162.6 cm)\n"
            "Weight: 222 lbs (100.7 kg) at March 19, 2025 visit\n"
            "BMI: 38.2 kg/m² (Class II Obesity)\n"
            "Waist circumference: 43 inches\n"
            "Blood pressure: 146/91 mmHg (on lisinopril 10 mg daily)\n\n"
            "ACTIVE COMORBIDITIES:\n"
            "1. Morbid obesity (E66.01) — BMI 38.2, present approximately 15 years with "
            "progressive weight gain following menopause onset at age 47. Maximum weight "
            "239 lbs in 2022. Current weight represents a 17 lb reduction from peak, now "
            "plateaued for 8 months despite continued dietary adherence.\n\n"
            "2. Type 2 Diabetes Mellitus with hyperglycemia (E11.65) — Diagnosed 2019. "
            "HbA1c: 7.8% (target <7.0%). Fasting glucose 148 mg/dL at today's visit. "
            "Current regimen: metformin 2000 mg/day (maximum tolerated dose — GI "
            "intolerance limits further escalation). SGLT-2 inhibitor (empagliflozin) "
            "trialed 2023, discontinued after 6 weeks due to recurrent UTIs. Endocrinologist "
            "recommends GLP-1 agonist as next line given dual benefit on glycemic control "
            "and weight reduction per ADA 2024 Standards of Care.\n\n"
            "3. Essential Hypertension (I10) — Managed with lisinopril 10 mg daily. Blood "
            "pressure 146/91 mmHg today, suboptimally controlled. Weight reduction expected "
            "to improve BP trajectory.\n\n"
            "4. Obstructive Sleep Apnea (G47.33) — Diagnosed via polysomnography 2021, AHI "
            "24 events/hour (moderate-severe). CPAP compliant (89% nights > 4 hours per "
            "adherence download). OSA severity expected to improve with weight reduction.\n\n"
            "5. Hyperlipidemia (E78.5) — LDL 134 mg/dL (target <100 mg/dL in T2DM). On "
            "atorvastatin 20 mg, not at goal.\n\n"
            "WEIGHT MANAGEMENT HISTORY:\n"
            "Member reports multiple weight reduction attempts over the prior 5 years:\n"
            "- 2020: Commercial weight loss program (self-directed); 12 lbs lost over 6 "
            "months, regained within 12 months.\n"
            "- 2021: PCP-supervised low-calorie diet; 8 lbs lost over 4 months, plateau.\n"
            "- 2022: Fitness center with personal trainer (3x/week); 14 lbs lost, "
            "discontinued after shoulder injury.\n"
            "- 2024: Mediterranean diet with weekly PCP check-ins; achieved current 17 lb "
            "reduction, plateaued 8 months.\n"
            "NOTE: No formal documentation of a structured 6-month medically supervised "
            "weight management program in submitted records. PCP notes reference weight "
            "counseling at routine visits but do not constitute a structured program per "
            "plan policy criteria (POL-OBESITY-LIFESTYLE-2024-09).\n\n"
            "PRIOR ANTI-OBESITY PHARMACOTHERAPY:\n"
            "- Phentermine/topiramate ER (Qsymia): prescribed 2022, discontinued after 8 "
            "weeks due to cognitive side effects (difficulty concentrating, word-retrieval "
            "deficits) — documented in PCP notes.\n"
            "- Orlistat 120 mg TID: trialed 2021, discontinued within 3 weeks due to "
            "intolerable GI side effects (fecal urgency, steatorrhea).\n"
            "- No prior GLP-1 agonist use.\n\n"
            "CLINICAL RATIONALE FOR SEMAGLUTIDE 2.4 mg (WEGOVY):\n"
            "Dr. Ellis requests initiation of semaglutide 2.4 mg weekly for chronic weight "
            "management based on: (1) BMI 38.2 with four qualifying comorbidities meets "
            "pharmacologic threshold criteria; (2) dual benefit anticipated — weight "
            "reduction expected to improve HbA1c 7.8%, hypertension, and OSA severity; "
            "(3) two prior anti-obesity medications failed due to adverse effects; "
            "(4) metformin maximized, SGLT-2 failed — GLP-1 is next appropriate step per "
            "ADA algorithm (SUSTAIN-6 CV benefit data supports use in T2DM population); "
            "(5) no contraindications: no personal/family history of MEN2 or medullary "
            "thyroid carcinoma, no prior pancreatitis, serum lipase 42 U/L (normal).\n\n"
            "LABORATORY RESULTS (March 19, 2025):\n"
            "HbA1c: 7.8%  |  Fasting glucose: 148 mg/dL\n"
            "LDL: 134 mg/dL  |  HDL: 41 mg/dL  |  TG: 218 mg/dL\n"
            "eGFR: 74 mL/min/1.73m² (mild CKD Stage 2, stable)\n"
            "ALT: 28 U/L  |  AST: 24 U/L  |  Serum lipase: 42 U/L\n"
            "TSH: 1.8 mIU/L (normal)\n\n"
            "PEND RATIONALE:\n"
            "Member's BMI (38.2) and comorbidity burden (T2DM, hypertension, OSA, "
            "hyperlipidemia) meet eligibility thresholds under plan policy "
            "POL-GLP1-OBESITY-2024-08. Two prior anti-obesity medication failures are "
            "documented (phentermine/topiramate — cognitive adverse effects; orlistat — "
            "GI intolerance). T2DM step therapy history is documented (metformin maximized, "
            "SGLT-2 inhibitor failed). However, formal documentation of a 6-month "
            "structured, medically supervised weight management program has not been "
            "submitted. PCP weight counseling notes do not satisfy structured program "
            "requirements per POL-OBESITY-LIFESTYLE-2024-09. Authorization is pended "
            "pending receipt of qualifying program documentation.\n\n"
            "STATUS: PENDED — Awaiting 6-month medically supervised weight management "
            "program documentation."
        ),

        # Embedding fields (populated by setup script)
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,

        # AI output fields (populated by demo loop)
        "ai_rationale": None,
        "ai_determination": None,
        "ai_rationale_generated_at": None,
        "ai_supporting_policies": [],
        "ai_comparable_cases": [],

        # Status tracking
        "created_at": "2025-03-20T14:22:07Z",
        "updated_at": "2025-03-20T15:45:33Z",
        "status_history": [
            {"status": "RECEIVED", "timestamp": "2025-03-20T14:22:07Z", "note": "Prior auth request received from Tampa Bay Endocrinology & Diabetes Center"},
            {"status": "PENDED",   "timestamp": "2025-03-20T15:45:33Z", "note": "PA-OBE-GLP1-001: 6-month supervised weight management program documentation required"},
        ],
    },
}
