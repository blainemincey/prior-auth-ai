"""
Coverage policy library — 25 synthetic policies across imaging and biologic clinical areas.

Engineered anchor policies:
  Scenario A: POL-MRI-LUMBAR-2024-03  (primary)
               POL-IMAGING-CONSERVATIVE-2024-01  (secondary)
               POL-RADICULOPATHY-2024-04  (secondary)
  Scenario B: POL-BIOLOGIC-RA-2024-07  (primary)
               POL-INFLIXIMAB-2024-06  (secondary)
               POL-SPECIALTY-DRUG-REVIEW-2024-03  (secondary)
"""

POLICIES = [
    # =====================================================================
    # IMAGING / MRI POLICIES
    # =====================================================================
    {
        "policy_id": "POL-MRI-LUMBAR-2024-03",
        "title": "MRI Lumbar Spine — Medical Necessity Criteria",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "lumbar_spine",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["72148", "72149", "72158"],
        "criteria_text": (
            "MRI of the lumbar spine (CPT 72148, 72149, 72158) is covered as medically "
            "necessary when ALL of the following criteria are satisfied:\n\n"
            "1. CONSERVATIVE TREATMENT REQUIREMENT: Member must have completed a minimum "
            "of six (6) weeks of structured multimodal conservative therapy, which must "
            "include physical therapy (minimum 8 documented sessions with a licensed "
            "physical therapist including an initial evaluation, session notes, and "
            "functional outcome measures) AND at least one of: NSAIDs at therapeutic "
            "dose, muscle relaxants, or chiropractic manipulation.\n\n"
            "2. CLINICAL INDICATION: At least one of the following must be present and "
            "documented by the ordering clinician: (a) lumbar radiculopathy with "
            "dermatomal pain pattern consistent with specific nerve root involvement "
            "(L1–S1), with objective neurological findings on examination; (b) neurogenic "
            "claudication or cauda equina symptoms; (c) progressive neurological deficits "
            "(motor weakness, reflex changes, sensory loss); (d) myelopathy.\n\n"
            "3. PLAIN RADIOGRAPHS: X-ray of the lumbar spine has been obtained within "
            "the preceding 12 months AND is documented as insufficient to guide "
            "definitive clinical management.\n\n"
            "4. PROVIDER DOCUMENTATION: The ordering clinician must explicitly document "
            "inadequate response to conservative therapy and the specific clinical "
            "indication for advanced imaging (e.g., surgical candidacy evaluation, "
            "epidural steroid injection planning, or unresolved diagnostic uncertainty "
            "after conservative management).\n\n"
            "EXCLUSIONS: Acute low back pain under 6 weeks duration without neurological "
            "red flags; routine surveillance without change in clinical status; imaging "
            "ordered solely for chiropractic evaluation.\n\n"
            "REQUIRED DOCUMENTATION: Complete physical therapy records (initial "
            "evaluation, session notes, and discharge/progress summary with functional "
            "outcome measures); radiology reports for any plain films; ordering provider "
            "note documenting conservative therapy failure and specific MRI indication."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-IMAGING-CONSERVATIVE-2024-01",
        "title": "Conservative Treatment Requirements Before Advanced Diagnostic Imaging",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "general",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["72148", "72149", "72158", "72141", "72146", "70553", "70552"],
        "criteria_text": (
            "Advanced diagnostic imaging (MRI, CT) for musculoskeletal conditions "
            "requires documentation of a conservative treatment trial prior to "
            "authorization, except in the presence of defined clinical red flags.\n\n"
            "MINIMUM CONSERVATIVE TREATMENT REQUIREMENTS:\n"
            "For spinal conditions (cervical, thoracic, lumbar): Six (6) weeks of "
            "multimodal conservative therapy including physical therapy (minimum 8 "
            "sessions), analgesic/anti-inflammatory pharmacotherapy, and documentation "
            "of functional limitations. Physical therapy records must include an initial "
            "functional evaluation and outcome measures using a validated instrument "
            "(Oswestry Disability Index, PROMIS-29, or equivalent).\n\n"
            "For extremity joint conditions: Four (4) weeks of structured physical "
            "therapy and pharmacotherapy, with documentation of persistent functional "
            "limitation.\n\n"
            "CLINICAL RED FLAGS BYPASSING CONSERVATIVE REQUIREMENT:\n"
            "Progressive neurological deficit, cauda equina syndrome, suspected "
            "malignancy, spinal infection, pathological fracture, severe trauma.\n\n"
            "DOCUMENTATION STANDARD: All conservative treatment records must be from "
            "the treating provider and must clearly state the treatment modality, "
            "frequency, duration, and clinical response. Provider attestation alone, "
            "without supporting therapy records, does not satisfy this requirement."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-RADICULOPATHY-2024-04",
        "title": "Lumbar Radiculopathy — Clinical Criteria and Imaging Indications",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "radiculopathy",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["72148", "72149", "72158", "64483", "64484"],
        "criteria_text": (
            "Lumbar radiculopathy with documented nerve root compression symptoms "
            "supports medical necessity for lumbar spine MRI when the following clinical "
            "criteria are met:\n\n"
            "CLINICAL CRITERIA FOR LUMBAR RADICULOPATHY:\n"
            "1. Dermatomal pain pattern (radiation below the knee in L4, L5, or S1 "
            "distribution, or above the knee for higher lumbar levels)\n"
            "2. Objective neurological findings: diminished or absent deep tendon "
            "reflexes, dermatomal sensory deficit, or segmental motor weakness\n"
            "3. Positive provocative testing: straight leg raise (SLR) positive at ≤60 "
            "degrees, or positive femoral nerve stretch test\n"
            "4. Duration ≥6 weeks with inadequate response to conservative care "
            "including physical therapy and pharmacotherapy\n\n"
            "IMAGING INDICATION IN RADICULOPATHY:\n"
            "MRI is indicated when: (a) conservative treatment has failed as defined "
            "above; (b) epidural steroid injection or other interventional procedure "
            "is being considered; (c) surgical evaluation is planned; or (d) symptoms "
            "are progressive despite treatment. Plain radiographs must be documented "
            "as insufficient to characterize soft-tissue disc pathology or neural "
            "element involvement.\n\n"
            "L4-L5 DISC HERNIATION: Disc herniation at L4-L5 producing L5 "
            "radiculopathy is among the most common indications for lumbar spine MRI. "
            "Key objective findings include extensor hallucis longus weakness, sensory "
            "deficit on the dorsum of the foot, and diminished tibialis anterior "
            "response. Positive straight leg raise with dermatomal reproduction "
            "provides clinical correlation for suspected L4-L5 pathology."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-MRI-BRAIN-2024-01",
        "title": "MRI Brain — Medical Necessity Criteria",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "brain",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["70551", "70552", "70553"],
        "criteria_text": (
            "MRI of the brain is covered as medically necessary for the evaluation of: "
            "new or progressive neurological symptoms (headache with red flags, focal "
            "deficit, seizure, altered consciousness); suspected intracranial mass or "
            "metastatic disease; stroke or TIA evaluation; demyelinating disease "
            "(multiple sclerosis); cranial nerve dysfunction; and pre-surgical "
            "planning. Conservative treatment requirements do not apply to brain MRI "
            "when neurological indications are present. Contrast enhancement is "
            "indicated for suspected mass lesions, infection, or demyelination."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-MRI-CERVICAL-2024-02",
        "title": "MRI Cervical Spine — Medical Necessity Criteria",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "cervical_spine",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["72141", "72142", "72156"],
        "criteria_text": (
            "MRI of the cervical spine is covered as medically necessary when: (1) "
            "cervical radiculopathy with dermatomal upper-extremity symptoms fails to "
            "respond to 4 weeks of conservative therapy including physical therapy; or "
            "(2) cervical myelopathy signs are present (gait disturbance, upper motor "
            "neuron signs, Lhermitte sign, hand clumsiness); or (3) trauma with "
            "neurological signs. Documentation requirements mirror lumbar spine policy "
            "but with a reduced 4-week conservative treatment threshold given the "
            "potential for cord compromise in cervical disease. Physical therapy records "
            "including outcome measures are required for radiculopathy indications."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-MRI-KNEE-2023-11",
        "title": "MRI Knee — Medical Necessity Criteria",
        "effective_date": "2023-11-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "knee",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "cpt_codes": ["73721", "73723"],
        "criteria_text": (
            "MRI of the knee is covered as medically necessary when: acute internal "
            "derangement is suspected following trauma with persistent symptoms at 4 "
            "weeks; suspected meniscal tear, ligamentous injury, or osteochondral "
            "defect not characterized by clinical examination; pre-surgical planning "
            "for knee arthroplasty or ligament reconstruction; evaluation of "
            "suspected osteonecrosis or occult fracture in patients with persistent "
            "pain and negative plain radiographs. A minimum 4-week course of physical "
            "therapy and NSAID therapy with documented functional limitation is required "
            "for non-traumatic knee pain indications."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-MRI-SHOULDER-2023-08",
        "title": "MRI Shoulder — Medical Necessity Criteria",
        "effective_date": "2023-08-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "shoulder",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "cpt_codes": ["73221", "73222", "73223"],
        "criteria_text": (
            "MRI of the shoulder is medically necessary for evaluation of rotator cuff "
            "pathology with persistent pain and functional limitation after 6 weeks of "
            "conservative treatment (physical therapy, NSAIDs, activity modification); "
            "suspected labral tear or instability in patients with recurrent subluxation "
            "or dislocation; avascular necrosis; or pre-surgical planning for "
            "arthroplasty or reconstruction. Plain shoulder radiographs are required "
            "prior to MRI authorization for non-traumatic indications."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-BACK-PAIN-ACUTE-2023-12",
        "title": "Acute Low Back Pain — Management Guidelines and Imaging Restrictions",
        "effective_date": "2023-12-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "lumbar_spine",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["72100", "72110", "72148", "72149"],
        "criteria_text": (
            "Advanced imaging (MRI) for acute low back pain (duration under 6 weeks) "
            "is not covered absent red-flag symptoms. Red flags justifying early imaging: "
            "significant trauma, suspected malignancy (unexplained weight loss, history "
            "of cancer), fever/infection, progressive neurological deficit, bladder or "
            "bowel dysfunction (cauda equina), age >70 with osteoporosis history. "
            "Routine imaging for acute uncomplicated low back pain does not improve "
            "outcomes and is excluded from coverage. For chronic low back pain (>12 "
            "weeks) or subacute back pain (6–12 weeks) transitioning to radiculopathy, "
            "refer to POL-MRI-LUMBAR-2024-03 and POL-RADICULOPATHY-2024-04."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-PA-IMAGING-2024-02",
        "title": "Prior Authorization Requirements for Advanced Diagnostic Imaging",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "general",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "cpt_codes": ["72148", "72149", "72158", "72141", "70551", "70553", "73221", "73721"],
        "criteria_text": (
            "The following advanced imaging services require prior authorization for "
            "Commercial PPO and HMO members: MRI (brain, spine, extremities), CT "
            "(spine, abdomen/pelvis for non-emergent indications), PET scans. "
            "Authorization requests must be submitted by the ordering provider with "
            "clinical documentation supporting medical necessity. Urgent/emergent "
            "imaging performed in inpatient or emergency settings is exempt from "
            "prospective authorization requirements but remains subject to concurrent "
            "and retrospective review. Point-of-care authorization decisions are "
            "targeted within 72 hours for standard requests and 24 hours for urgent "
            "requests per state regulatory requirements."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-CT-SPINE-2024-05",
        "title": "CT Spine — Medical Necessity Criteria and MRI Relationship",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "spine",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["72128", "72129", "72130", "72131", "72132", "72133"],
        "criteria_text": (
            "CT of the spine is medically necessary for: acute trauma evaluation, "
            "assessment of bony architecture (spondylolisthesis, fracture, pedicle "
            "integrity), surgical planning for instrumentation, or when MRI is "
            "contraindicated (implanted devices, severe claustrophobia). CT is not a "
            "substitute for MRI in soft-tissue disc and neural element evaluation. "
            "When the clinical question involves soft-tissue pathology (disc herniation, "
            "neural foraminal stenosis, cord compression), MRI is the preferred modality "
            "and CT myelography is reserved for MRI-contraindicated patients. "
            "Conservative treatment requirements parallel those in POL-MRI-LUMBAR-2024-03 "
            "for non-traumatic lumbar CT indications."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-SPORTS-IMAGING-2023-09",
        "title": "Sports Medicine Advanced Imaging Criteria",
        "effective_date": "2023-09-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "sports_medicine",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "cpt_codes": ["73221", "73721", "72148", "27447", "29881"],
        "criteria_text": (
            "Advanced imaging for sports-related injuries follows standard clinical "
            "criteria with the following modifications: acute ligamentous injuries "
            "with clinical suspicion of complete tear (grade III) may be authorized "
            "without conservative treatment waiting period when surgical consultation "
            "is planned. MRI for suspected ACL, PCL, or multiligamentous injuries "
            "in athletes may proceed after 2 weeks if conservative treatment has not "
            "resolved instability symptoms and surgical evaluation is documented. "
            "Stress fractures, osteochondral lesions, and labral pathology in "
            "high-demand athletes follow standard criteria. Return-to-sport clearance "
            "imaging requires documentation of prior injury and specific clinical question."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-MYELOPATHY-IMAGING-2024-01",
        "title": "Cervical and Thoracic Myelopathy — Urgent Imaging Protocol",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "imaging",
        "subcategory": "myelopathy",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["72141", "72142", "72146", "72147"],
        "criteria_text": (
            "Cervical or thoracic myelopathy with objective upper motor neuron signs "
            "constitutes a clinical urgency requiring expedited imaging authorization. "
            "Signs include: hyperreflexia, clonus, Babinski response, Hoffman sign, "
            "Lhermitte sign, gait ataxia, or bowel/bladder dysfunction. Conservative "
            "treatment waiting periods are waived for documented myelopathy. MRI of "
            "the affected spinal segment should be completed within 72 hours of "
            "clinical identification. Lumbar stenosis with neurogenic claudication "
            "but without myelopathic signs follows standard criteria under "
            "POL-MRI-LUMBAR-2024-03."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },

    # =====================================================================
    # BIOLOGIC / SPECIALTY DRUG POLICIES
    # =====================================================================
    {
        "policy_id": "POL-BIOLOGIC-RA-2024-07",
        "title": "Biologic DMARD Therapy for Rheumatoid Arthritis — Step Therapy Requirements",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "rheumatoid_arthritis",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": ["J0135", "J1745", "J3380", "J3262", "J0129", "J3357"],
        "criteria_text": (
            "Biologic DMARDs (including TNF inhibitors, IL-6 inhibitors, JAK "
            "inhibitors, and co-stimulation modulators) for rheumatoid arthritis "
            "are covered when ALL of the following criteria are met:\n\n"
            "1. DIAGNOSIS: Confirmed moderate-to-severe rheumatoid arthritis by a "
            "board-certified rheumatologist, with ICD-10 code M05.xx or M06.xx, AND "
            "documented disease activity score DAS28 ≥3.2 or equivalent validated "
            "instrument (CDAI, SDAI, or ACR/EULAR Boolean criteria).\n\n"
            "2. STEP THERAPY — NEW BIOLOGIC INITIATIONS: The member must have "
            "documented adequate trial and failure, intolerance, or contraindication "
            "to BOTH: (a) at least one conventional synthetic DMARD (csDMARD) — "
            "methotrexate at therapeutic dose (≥15 mg/week) for minimum 3 months, "
            "OR documented contraindication or intolerance; AND (b) at least one "
            "additional csDMARD (hydroxychloroquine, leflunomide, or sulfasalazine).\n\n"
            "3. BIOLOGIC CONTINUATION (established patients): Documented clinical "
            "response to the current biologic agent — DAS28 improvement ≥1.2 from "
            "baseline OR current DAS28 <2.6 (clinical remission) — and prescriber "
            "attestation of continued medical necessity. No active serious infection.\n\n"
            "4. SAFETY SCREENING: Negative TB screening (TST or IGRA) within 12 "
            "months of initiation; hepatitis B surface antigen testing prior to "
            "initiation; documented counseling on infection risk.\n\n"
            "5. STEP THERAPY EXCEPTIONS: Step therapy may be bypassed with "
            "documentation of: prior step therapy at another payer within 24 months; "
            "contraindication to all csDMARDs; pregnancy/breastfeeding; or active "
            "TB with appropriate treatment.\n\n"
            "DOCUMENTATION REQUIRED: Rheumatologist specialist note with DAS28 or "
            "equivalent score; complete csDMARD trial history with dates, doses, "
            "and reason for discontinuation; safety screening results; prescriber "
            "attestation for continuation requests."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-INFLIXIMAB-2024-06",
        "title": "Infliximab (Remicade and Biosimilars) — Coverage Criteria",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "tnf_inhibitor",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": ["J1745"],
        "criteria_text": (
            "Infliximab (Remicade; biosimilars Inflectra, Renflexis, Avsola, Ixifi) "
            "is a TNF-alpha inhibitor administered by intravenous infusion. Coverage "
            "is provided for FDA-approved indications including rheumatoid arthritis, "
            "Crohn's disease, ulcerative colitis, ankylosing spondylitis, psoriatic "
            "arthritis, and plaque psoriasis, subject to applicable step therapy "
            "requirements.\n\n"
            "RHEUMATOID ARTHRITIS INDICATIONS: Infliximab for RA requires prior "
            "failure, intolerance, or contraindication to at least one csDMARD per "
            "POL-BIOLOGIC-RA-2024-07. For continuation of established infliximab "
            "therapy, documentation of sustained clinical response and absence of "
            "serious adverse events is required at each renewal.\n\n"
            "DOSING AND SITE OF CARE: Standard RA dosing is 3 mg/kg IV at weeks 0, "
            "2, 6, then every 8 weeks; dose escalation to maximum 10 mg/kg or "
            "reduced interval to every 4 weeks requires documentation of inadequate "
            "response at standard dose. Infusion may be performed in office, "
            "outpatient hospital (POS 22), or authorized infusion center settings "
            "per POL-INFUSION-SITE-2024-02.\n\n"
            "HIGH-COST CLAIM REVIEW: Infliximab claims exceeding $15,000 per event "
            "are subject to concurrent medical necessity review (MN-DRUG-HCB-002) "
            "per POL-SPECIALTY-DRUG-REVIEW-2024-03. Step therapy history must be "
            "verified at each review cycle."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-SPECIALTY-DRUG-REVIEW-2024-03",
        "title": "High-Cost Specialty Drug Medical Necessity Review Criteria",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "specialty_drug",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": [],
        "criteria_text": (
            "Claims for specialty drugs exceeding $15,000 per claim event (including "
            "infusions and self-administered specialty pharmaceuticals) are subject to "
            "concurrent medical necessity review triggered by adjudication code "
            "MN-DRUG-HCB-002. Review criteria for high-cost specialty drugs:\n\n"
            "1. DIAGNOSIS VERIFICATION: ICD-10 diagnosis code must correspond to an "
            "FDA-approved indication for the billed drug. Off-label use requires "
            "clinical evidence review and medical director approval.\n\n"
            "2. STEP THERAPY COMPLIANCE: For drugs subject to step therapy policy, "
            "complete step therapy history must be documented including: all prior "
            "drug trials, dates, doses, duration, and objective reason for "
            "discontinuation or failure.\n\n"
            "3. CLINICAL RESPONSE FOR CONTINUATION: For patients on established "
            "therapy, objective evidence of clinical response must be documented "
            "using validated disease activity measures (DAS28, CDAI, PASI, HBI, "
            "or equivalent). Dose escalation above FDA-approved maximum standard "
            "dose requires additional medical director review.\n\n"
            "4. SAFETY MONITORING: Evidence of required safety monitoring (lab work, "
            "tuberculosis screening, hepatitis screening for immunosuppressants) must "
            "be current per drug-specific monitoring requirements.\n\n"
            "REVIEW TIMELINE: Standard concurrent review is targeted at 3 business "
            "days. Urgent reviews (patient clinically deteriorating) are targeted at "
            "24 hours."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-ADALIMUMAB-2024-05",
        "title": "Adalimumab (Humira and Biosimilars) — Coverage Criteria",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "tnf_inhibitor",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": ["J0135"],
        "criteria_text": (
            "Adalimumab (Humira; biosimilars Hadlima, Hyrimoz, Cyltezo, Yusimry, "
            "Amjevita, Abrilada, and others) is a TNF-alpha inhibitor administered "
            "by subcutaneous injection. Coverage follows applicable step therapy "
            "requirements for each indication. For rheumatoid arthritis, refer to "
            "POL-BIOLOGIC-RA-2024-07. Biosimilar preferencing: this plan requires "
            "an adalimumab biosimilar as the preferred agent when initiating "
            "adalimumab therapy; reference product (Humira) is covered when a "
            "biosimilar has been previously tried and failed, or when a biosimilar "
            "is contraindicated. Failure of one adalimumab product (reference or "
            "biosimilar) satisfies the adalimumab step for purposes of switching "
            "to another biologic class."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-STEP-THERAPY-GENERAL-2024-01",
        "title": "Step Therapy Policy — General Framework",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "step_therapy",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "hcpcs_codes": [],
        "criteria_text": (
            "Step therapy (also called fail-first) requires that members try and fail "
            "one or more preferred, clinically appropriate treatments before coverage "
            "of a higher-cost alternative is authorized. Principles:\n\n"
            "ADEQUATE TRIAL DEFINITION: An adequate trial is defined as the use of "
            "the preferred therapy at a therapeutic dose for the minimum duration "
            "specified in the applicable drug-specific policy, unless earlier "
            "discontinuation is clinically justified (adverse effect, contraindication, "
            "or laboratory abnormality).\n\n"
            "EXCEPTION CRITERIA: Step therapy may be bypassed without a prior trial "
            "when: (1) the member has documented prior failure of the required step at "
            "any plan within the preceding 24 months; (2) the required step is "
            "contraindicated by a comorbid condition or drug interaction; (3) the "
            "required step is clinically inappropriate for the member's specific "
            "presentation; or (4) a state law mandates step therapy exception "
            "procedures (applicable in states with enacted step therapy legislation).\n\n"
            "APPEALS: Step therapy exceptions denied at initial review may be appealed "
            "through standard grievance and appeals procedures. Medical director review "
            "is available upon request."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-BIOLOGIC-PsA-2024-02",
        "title": "Biologic DMARD Therapy for Psoriatic Arthritis",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "psoriatic_arthritis",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": ["J0135", "J1745", "J3380", "J3357"],
        "criteria_text": (
            "Biologic DMARDs for psoriatic arthritis are covered for members with a "
            "rheumatologist-confirmed diagnosis (ICD-10 L40.5x) with moderate-to-"
            "severe disease including active arthritis, dactylitis, enthesitis, or "
            "significant axial disease, following documented failure of at least one "
            "conventional DMARD (methotrexate, leflunomide, or sulfasalazine) for a "
            "minimum of 3 months, unless DMARD use is contraindicated. For biologic "
            "continuation, clinical response per validated instrument (DAS28, DAPSA, "
            "or MDA criteria) must be documented."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-BIOLOGIC-AS-2024-01",
        "title": "Biologic Therapy for Ankylosing Spondylitis",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "ankylosing_spondylitis",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": ["J0135", "J1745", "J3380"],
        "criteria_text": (
            "TNF inhibitor biologics for ankylosing spondylitis (AS; ICD-10 M45.x) "
            "or non-radiographic axial spondyloarthropathy are covered following "
            "confirmed diagnosis by a rheumatologist with documented BASDAI ≥4 or "
            "ASDAS ≥2.1, AND failure of at least 2 NSAIDs at maximum tolerated "
            "doses for a minimum of 4 weeks each (or documented NSAID intolerance "
            "or contraindication). Conventional DMARDs (methotrexate, leflunomide) "
            "are not required as step therapy for axial AS given limited evidence "
            "for efficacy in axial disease. Continuation requires documented BASDAI "
            "improvement ≥2.0 or ASDAS improvement ≥1.1 from baseline."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-BIOLOGIC-CROHN-2023-11",
        "title": "Biologic Therapy for Crohn's Disease and Ulcerative Colitis",
        "effective_date": "2023-11-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "ibd",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": ["J1745", "J0135", "J3380"],
        "criteria_text": (
            "TNF inhibitors and other biologics for inflammatory bowel disease "
            "(Crohn's disease ICD-10 K50.x; ulcerative colitis K51.x) are covered "
            "for moderate-to-severe disease (HBI ≥7 for Crohn's; Mayo score ≥6 for "
            "UC) following documented failure of corticosteroids and at least one "
            "immunomodulator (azathioprine or 6-mercaptopurine for at least 3 months "
            "or methotrexate). Infliximab and adalimumab are preferred agents. "
            "Vedolizumab and ustekinumab require prior biologic failure or documented "
            "contraindication to TNF inhibitors."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-INFUSION-SITE-2024-02",
        "title": "Site of Care for Specialty Infusion Therapy",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "site_of_care",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "hcpcs_codes": ["J1745", "J0135", "J3380", "J3262"],
        "criteria_text": (
            "Specialty infusion services are covered in the following settings in "
            "order of preferred site: (1) home infusion (when clinically appropriate "
            "and member consent obtained); (2) physician office (POS 11) or outpatient "
            "infusion center (POS 22); (3) hospital outpatient department. "
            "For infusions with known anaphylaxis risk (first-dose biologics, certain "
            "chemotherapies), office or facility setting is required for initial "
            "administration with 60-minute post-infusion observation. Infliximab "
            "(J1745) requires first-dose facility or office administration. Site of "
            "care optimization programs are in effect — members may be redirected to "
            "lower-cost alternative sites following utilization review."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-BIOLOGIC-MONITORING-2024-04",
        "title": "Biologic Therapy Laboratory Monitoring Requirements",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "monitoring",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": [],
        "criteria_text": (
            "Members on biologic DMARD therapy are subject to the following monitoring "
            "requirements at each authorization renewal: (1) TB screening (TST or IGRA "
            "QuantiFERON-TB Gold) within 12 months; (2) CBC with differential within "
            "6 months for immunosuppressant-naïve patients or within 12 months for "
            "stable established patients; (3) hepatic function panel within 12 months "
            "for patients on concomitant methotrexate or with known hepatic risk "
            "factors; (4) hepatitis B surface antigen at initiation; (5) documentation "
            "of no active serious infection (including fungal infections, sepsis, "
            "opportunistic infections). Failure to provide current monitoring results "
            "at renewal is grounds for pend of the authorization request pending "
            "documentation completion."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-IL6-INHIBITOR-2024-01",
        "title": "IL-6 Receptor Inhibitor Coverage Criteria (Tocilizumab, Sarilumab)",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "il6_inhibitor",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "hcpcs_codes": ["J3262", "J2800"],
        "criteria_text": (
            "IL-6 receptor inhibitors (tocilizumab [Actemra, J3262]; sarilumab "
            "[Kevzara, J2800]) for rheumatoid arthritis are covered as step therapy "
            "following failure or intolerance of at least one TNF inhibitor AND one "
            "csDMARD, OR when TNF inhibitor use is contraindicated. IL-6 inhibitors "
            "may be used as monotherapy (without concomitant methotrexate) when MTX "
            "is contraindicated or not tolerated — a distinction from TNF inhibitors. "
            "Dose escalation of tocilizumab (above 8 mg/kg IV q4 weeks or 162 mg SC "
            "weekly) requires medical director review with documentation of partial "
            "response at standard dose."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-JAK-INHIBITOR-2024-02",
        "title": "JAK Inhibitor Coverage Criteria (Tofacitinib, Upadacitinib, Baricitinib)",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "jak_inhibitor",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "hcpcs_codes": [],
        "criteria_text": (
            "JAK inhibitors (tofacitinib [Xeljanz], upadacitinib [Rinvoq], "
            "baricitinib [Olumiant]) for rheumatoid arthritis carry an FDA black-box "
            "warning for serious infections, malignancy, and cardiovascular events. "
            "Coverage is provided following failure of at least one TNF inhibitor AND "
            "documented step therapy per POL-BIOLOGIC-RA-2024-07, or when TNF "
            "inhibitors are contraindicated. Additional criteria: member age <65 "
            "without active or prior malignancy (except non-melanoma skin cancer), "
            "no history of major adverse cardiovascular event (MACE), no active "
            "thrombosis. For members ≥65 or with cardiovascular risk factors, "
            "a cardiovascular risk assessment and specialist consultation note are "
            "required prior to authorization."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "policy_id": "POL-DRUG-MN-THRESHOLD-2024-01",
        "title": "Medical Necessity Review Thresholds — Specialty Drug Claims",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "biologic",
        "subcategory": "specialty_drug",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "hcpcs_codes": [],
        "criteria_text": (
            "The following claim thresholds trigger concurrent medical necessity review "
            "for specialty drug claims: (1) single-claim-event cost ≥$15,000 triggers "
            "MN-DRUG-HCB-002 concurrent review; (2) annual specialty drug spend ≥"
            "$100,000 per member triggers pharmacy case management referral; (3) "
            "dose escalation above FDA label maximum requires medical director review. "
            "Triggered reviews are targeted for completion within 3 business days "
            "with a 72-hour urgent track available. Payment is held pending review "
            "outcome. Claims that complete review and are approved are released for "
            "payment at the applicable contracted rate."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },

    # ── Obesity / GLP-1 policies (Scenario C) ────────────────────────────────

    {
        "policy_id": "POL-GLP1-OBESITY-2024-08",
        "title": "GLP-1 Receptor Agonist Coverage for Chronic Weight Management",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "obesity",
        "subcategory": "glp1_pharmacotherapy",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": [],
        "hcpcs_codes": ["S0148", "J3490", "J3590"],
        "criteria_text": (
            "Coverage for glucagon-like peptide-1 (GLP-1) receptor agonists for chronic "
            "weight management — including semaglutide 2.4 mg (Wegovy), liraglutide 3.0 mg "
            "(Saxenda), and tirzepatide (Zepbound) — requires all of the following criteria "
            "to be met prior to authorization.\n\n"
            "ELIGIBILITY CRITERIA:\n"
            "1. Adult member aged 18 or older.\n"
            "2. Body mass index (BMI) at or above 30 kg/m² with at least one qualifying "
            "weight-related comorbidity (type 2 diabetes mellitus, hypertension, "
            "dyslipidemia, obstructive sleep apnea, or established cardiovascular disease), "
            "OR BMI at or above 35 kg/m² regardless of comorbidity status.\n\n"
            "STRUCTURED LIFESTYLE PROGRAM REQUIREMENT:\n"
            "3. Documentation of participation in a structured, medically supervised weight "
            "management program for a minimum of 6 continuous months. Qualifying programs "
            "must include: (a) initial weight assessment and goal-setting by a licensed "
            "healthcare professional; (b) regular follow-up encounters at minimum monthly "
            "intervals with documented weight measurements and dietary counseling; "
            "(c) a structured dietary intervention such as calorie restriction or meal "
            "replacement; (d) physical activity counseling or supervised exercise component; "
            "and (e) a behavioral modification component. Documentation must include program "
            "start and end dates, visit frequency, and a progress or discharge summary.\n"
            "4. Documented evidence that the structured program failed to produce or sustain "
            "clinically meaningful weight loss, defined as 5 percent or more body weight "
            "reduction maintained for at least 3 months.\n\n"
            "PRIOR MEDICATION HISTORY:\n"
            "5. For members with BMI 30.0–34.9 kg/m²: documentation of at least one prior "
            "adequate trial of an FDA-approved non-GLP-1 anti-obesity medication at "
            "therapeutic dose for a minimum of 12 weeks, resulting in inadequate response "
            "or clinically significant adverse effects precluding continuation.\n\n"
            "CONTRAINDICATIONS (coverage excluded if present):\n"
            "- Personal or family history of medullary thyroid carcinoma or Multiple "
            "Endocrine Neoplasia syndrome type 2 (MEN2).\n"
            "- History of acute or chronic pancreatitis.\n"
            "- Pregnancy or active breastfeeding.\n"
            "- Severe renal impairment (eGFR below 15 mL/min/1.73 m²).\n\n"
            "REQUIRED DOCUMENTATION:\n"
            "Qualifying BMI with measurement date; records of 6-month medically supervised "
            "weight management program (program name, visit dates, documented weights, "
            "discharge or progress summary); relevant laboratory results within 90 days; "
            "documentation of prior anti-obesity medication trials for BMI 30–34.9; "
            "prescriber attestation of no contraindications.\n\n"
            "CONTINUATION AUTHORIZATION:\n"
            "Re-authorization at 12 months requires documentation of at least 5 percent "
            "body weight reduction from baseline weight at initiation. If this threshold "
            "is not achieved after 16 weeks at maintenance dose, coverage will not be "
            "continued and clinical review will be required."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },

    {
        "policy_id": "POL-OBESITY-LIFESTYLE-2024-09",
        "title": "Medically Supervised Weight Management Program Requirements for Pharmacotherapy",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "obesity",
        "subcategory": "lifestyle_intervention",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": ["99401", "99402", "99403", "99404"],
        "hcpcs_codes": [],
        "criteria_text": (
            "For coverage of pharmacologic weight management interventions — including GLP-1 "
            "receptor agonists and other FDA-approved anti-obesity medications — the member "
            "must provide documentation of a qualifying structured, medically supervised "
            "weight management program. This policy defines the minimum standards that "
            "constitute a qualifying program.\n\n"
            "QUALIFYING PROGRAM DEFINITION:\n"
            "A qualifying medically supervised weight management program must include all "
            "of the following components:\n"
            "1. Duration: Minimum 6 consecutive months of continuous participation. Gaps "
            "exceeding 30 days reset the program clock unless medically documented and "
            "justified.\n"
            "2. Supervision: Program must be led by or involve supervision from a licensed "
            "medical professional, which includes a physician, nurse practitioner, "
            "physician assistant, or registered dietitian.\n"
            "3. Frequency: Documented in-person or telehealth encounters at minimum monthly "
            "intervals. Intensive behavioral treatment programs with weekly encounters over "
            "12 weeks also satisfy the requirement when followed by monthly maintenance.\n"
            "4. Dietary component: Documented calorie-restricted or structured meal "
            "replacement dietary intervention with individualized targets.\n"
            "5. Physical activity component: Exercise counseling or structured physical "
            "activity program with documented recommendations.\n"
            "6. Behavioral component: Behavioral modification strategies including, but not "
            "limited to, mindful eating techniques, food journaling, and stress management.\n"
            "7. Documentation: Formal program records including start date, all visit dates, "
            "weight measurements at each encounter, and a discharge or progress summary.\n\n"
            "NON-QUALIFYING ACTIVITIES:\n"
            "The following activities do not constitute a qualifying medically supervised "
            "weight management program for purposes of this coverage policy:\n"
            "- Primary care weight counseling provided incidentally at routine health "
            "maintenance visits without a formal program structure.\n"
            "- Self-directed participation in commercial weight loss programs (Weight "
            "Watchers, Noom, Jenny Craig, OPTAVIA) without licensed medical professional "
            "supervision and documented clinical oversight.\n"
            "- Gym membership or personal training alone, without concurrent medical "
            "supervision and documentation.\n"
            "- App-based programs without documented licensed professional involvement "
            "and formal program records.\n\n"
            "DOCUMENTATION SUBMISSION:\n"
            "Acceptable documentation includes: (a) formal letter from program director on "
            "institutional letterhead confirming start date, duration, and completion; "
            "(b) structured progress notes spanning the required 6-month period with dates, "
            "weights, and interventions recorded; or (c) primary care records spanning "
            "6 months with documented monthly weight management encounters meeting the "
            "qualifying program standards above.\n\n"
            "NOTE FOR DUAL-INDICATION REQUESTS:\n"
            "For members where GLP-1 agonist is requested for both weight management and "
            "glycemic management of type 2 diabetes, lifestyle program requirements may be "
            "evaluated concurrently with diabetes management history under the applicable "
            "GLP-1 diabetes coverage policy. In dual-indication cases, documented T2DM "
            "step therapy failure may reduce but does not eliminate the lifestyle "
            "documentation requirement."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },

    {
        "policy_id": "POL-GLP1-T2DM-2024-10",
        "title": "GLP-1 Receptor Agonist Coverage for Type 2 Diabetes Mellitus",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "obesity",
        "subcategory": "diabetes_pharmacotherapy",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": [],
        "hcpcs_codes": ["S0148", "J3490"],
        "criteria_text": (
            "Coverage for GLP-1 receptor agonists — including semaglutide (Ozempic, Wegovy), "
            "dulaglutide (Trulicity), liraglutide (Victoza), exenatide, and tirzepatide "
            "(Mounjaro) — for glycemic management in type 2 diabetes mellitus (T2DM) "
            "requires documentation of the following criteria.\n\n"
            "CLINICAL ELIGIBILITY:\n"
            "1. Confirmed diagnosis of type 2 diabetes mellitus (ICD-10 E11.x).\n"
            "2. HbA1c at or above 7.0 percent documented within 90 days of the authorization "
            "request.\n"
            "3. Member is age 18 or older.\n\n"
            "STEP THERAPY REQUIREMENTS:\n"
            "4. Documentation of an adequate trial of first-line therapy:\n"
            "   a. Metformin at the maximum tolerated dose for a minimum of 90 days, OR\n"
            "   b. Documented metformin contraindication or intolerance, such as eGFR below "
            "30 mL/min/1.73 m², significant GI intolerance, or history of lactic acidosis.\n"
            "5. If metformin was completed or contraindicated, documentation of at least one "
            "additional oral antidiabetic agent trial — SGLT-2 inhibitor, DPP-4 inhibitor, "
            "or sulfonylurea — OR a documented clinical reason for bypassing additional oral "
            "agents, such as established cardiovascular disease requiring a GLP-1 with "
            "proven cardiovascular benefit per ACC/AHA/ADA 2024 guidance.\n\n"
            "CARDIOVASCULAR RISK PATHWAY:\n"
            "Members with established atherosclerotic cardiovascular disease (ASCVD), heart "
            "failure, or chronic kidney disease stage 3 or higher are eligible for GLP-1 "
            "agonist therapy after metformin alone, or as initial therapy if HbA1c is at or "
            "above 7.5 percent, based on cardiovascular outcome trial data from SUSTAIN-6, "
            "LEADER, and REWIND trials.\n\n"
            "DUAL-INDICATION REQUESTS (OBESITY + T2DM):\n"
            "When a GLP-1 agonist is requested for both glycemic management and weight "
            "management — for example, semaglutide 2.4 mg (Wegovy) rather than lower-dose "
            "diabetes formulations — coverage determination will apply the more restrictive "
            "of the applicable policies unless the prescriber documents that the higher-dose "
            "formulation is clinically necessary based on inadequate glycemic response at "
            "lower doses or combined metabolic indication per ADA 2024 Standards of Care.\n\n"
            "REQUIRED DOCUMENTATION:\n"
            "Confirmed T2DM diagnosis with ICD-10 code; HbA1c result within 90 days; "
            "medication history documenting metformin trial and outcome; documentation of "
            "additional oral agent trial or rationale for bypass; laboratory results "
            "confirming no contraindications to GLP-1 therapy.\n\n"
            "CONTINUATION CRITERIA:\n"
            "Re-authorization at 12 months requires HbA1c improvement of at least 0.5 "
            "percent from baseline, or documented achievement of target HbA1c below "
            "7.0 percent, along with confirmation of ongoing medication adherence and "
            "tolerability."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },

    {
        "policy_id": "POL-OBESITY-COMORBIDITY-2024-11",
        "title": "Qualifying Comorbidity Documentation for Anti-Obesity Pharmacotherapy",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "obesity",
        "subcategory": "comorbidity_criteria",
        "plan_applicability": ["Commercial PPO", "Commercial HMO", "Medicare Advantage"],
        "states": "All",
        "cpt_codes": [],
        "hcpcs_codes": [],
        "criteria_text": (
            "For members with BMI 30.0 to 34.9 kg/m² requesting coverage for anti-obesity "
            "pharmacotherapy — including GLP-1 receptor agonists, naltrexone/bupropion, and "
            "phentermine/topiramate — documentation of at least one qualifying weight-related "
            "comorbidity is required. This policy defines qualifying comorbidities and the "
            "required documentation standards.\n\n"
            "QUALIFYING COMORBIDITIES (one or more required for BMI 30.0–34.9):\n\n"
            "1. Type 2 Diabetes Mellitus (ICD-10 E11.x) or Prediabetes (R73.03)\n"
            "   Documented HbA1c at or above 6.5 percent (T2DM) or 5.7 to 6.4 percent "
            "(prediabetes with one additional cardiovascular risk factor), OR fasting glucose "
            "at or above 126 mg/dL (T2DM) or 100 to 125 mg/dL (prediabetes).\n\n"
            "2. Hypertension (ICD-10 I10, I11.x)\n"
            "   Blood pressure at or above 140/90 mmHg documented on two separate readings "
            "at least 4 weeks apart, OR current management with at least one antihypertensive "
            "medication.\n\n"
            "3. Obstructive Sleep Apnea (ICD-10 G47.33)\n"
            "   Diagnosis confirmed by polysomnography or home sleep study with apnea-"
            "hypopnea index (AHI) at or above 5 events per hour, documented by a "
            "pulmonologist or sleep medicine specialist.\n\n"
            "4. Dyslipidemia (ICD-10 E78.x)\n"
            "   LDL-C at or above 160 mg/dL, or triglycerides at or above 200 mg/dL, "
            "or HDL below 40 mg/dL (male) or below 50 mg/dL (female) on two separate "
            "measurements; OR currently managed with lipid-lowering pharmacotherapy.\n\n"
            "5. Established Atherosclerotic Cardiovascular Disease\n"
            "   Prior myocardial infarction, ischemic stroke, peripheral artery disease, "
            "coronary revascularization, or documented atherosclerosis on imaging.\n\n"
            "6. Non-Alcoholic Fatty Liver Disease or NASH (ICD-10 K76.0)\n"
            "   Documented by hepatic imaging (ultrasound, MRI) or biopsy.\n\n"
            "NOTE FOR BMI AT OR ABOVE 35:\n"
            "Members with BMI at or above 35 kg/m² are exempt from the comorbidity "
            "documentation requirement for pharmacotherapy eligibility. Proceed directly "
            "to lifestyle intervention and step therapy documentation requirements per the "
            "applicable coverage policy. Comorbidity documentation remains useful for "
            "supporting the clinical rationale but is not required for coverage approval.\n\n"
            "All comorbidity documentation must be dated within 12 months of the "
            "authorization request and supported by clinical records, including laboratory "
            "values, specialist notes, imaging reports, or pharmacy records of comorbidity "
            "treatment."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },

    {
        "policy_id": "POL-ANTIOBESITY-STEP-2024-12",
        "title": "Anti-Obesity Medication Step Therapy Framework for GLP-1 Prior Authorization",
        "effective_date": "2024-01-01",
        "review_date": "2025-01-01",
        "clinical_area": "obesity",
        "subcategory": "step_therapy",
        "plan_applicability": ["Commercial PPO", "Commercial HMO"],
        "states": "All",
        "cpt_codes": [],
        "hcpcs_codes": ["S0148"],
        "criteria_text": (
            "This policy establishes the step therapy framework for GLP-1 receptor agonists "
            "requested for chronic weight management in members with BMI 30.0 to 34.9 kg/m² "
            "and at least one qualifying comorbidity. Members with BMI at or above 35 kg/m² "
            "are exempt from the prior non-GLP-1 medication requirement.\n\n"
            "STEP THERAPY REQUIREMENT (BMI 30.0–34.9 only):\n"
            "Prior to authorization of a GLP-1 receptor agonist as initial obesity "
            "pharmacotherapy, documentation of at least one adequate trial of an FDA-approved "
            "non-GLP-1 anti-obesity medication is required.\n\n"
            "QUALIFYING PRIOR MEDICATION TRIALS:\n"
            "1. Phentermine/topiramate extended-release (Qsymia): Minimum 12 weeks at "
            "therapeutic dose (phentermine 7.5 mg / topiramate 46 mg or higher). "
            "Documentation of inadequate weight loss response (less than 3 percent body "
            "weight reduction) or discontinuation due to intolerable adverse effects.\n"
            "2. Naltrexone/bupropion extended-release (Contrave): Minimum 16 weeks at "
            "therapeutic dose, with documented inadequate response or adverse events "
            "precluding continuation.\n"
            "3. Orlistat 120 mg three times daily (Xenical): Minimum 12 weeks, with "
            "documented inadequate response or adverse effects.\n\n"
            "STEP THERAPY EXCEPTIONS — GLP-1 COVERED WITHOUT PRIOR STEP:\n"
            "Step therapy may be waived when the prescriber documents that:\n"
            "a. The member has clinical contraindications to all non-GLP-1 anti-obesity "
            "options (for example, uncontrolled hypertension precluding phentermine, "
            "psychiatric contraindication to naltrexone/bupropion, or malabsorptive "
            "condition precluding orlistat); OR\n"
            "b. The member has a concurrent, independently qualifying T2DM indication where "
            "GLP-1 agonist is the next appropriate agent per the diabetes step therapy "
            "policy (POL-GLP1-T2DM-2024-10), AND the prescriber documents clinical rationale "
            "for the weight management dose formulation based on combined metabolic "
            "indication per ADA 2024 Standards of Care.\n\n"
            "DOCUMENTATION FOR PRIOR MEDICATION TRIALS:\n"
            "Submit dispensing records or pharmacy claims confirming prior medication use, "
            "along with prescriber documentation of outcome (inadequate response or adverse "
            "event). Prescriber attestation without dispensing records is not sufficient.\n\n"
            "FORMULARY TIER NOTE:\n"
            "GLP-1 receptor agonists for weight management are placed on the plan's specialty "
            "tier. Even where medical necessity criteria are met, member cost-share applies "
            "per the applicable benefit design. Coverage approval does not reduce specialty "
            "cost-share obligations."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
]
