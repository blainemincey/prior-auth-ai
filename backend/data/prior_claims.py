"""
Prior adjudicated claims corpus — 60 synthetic records across imaging and biologic areas.

ENGINEERED ANCHOR RECORDS (intended top matches for demo claims):

  Scenario A — James Thornton MRI:
    PCL-2024-MRI-0892  APPROVED  (primary match — nearly identical presentation)
    PCL-2024-MRI-1103  APPROVED  (secondary — pended-then-approved with same doc issue)
    PCL-2024-MRI-0671  DENIED    (contrast — denied for missing conservative therapy)

  Scenario B — Eleanor Vasquez infliximab:
    PCL-2024-BIO-2244  APPROVED  (primary match — infliximab continuation, RA, PPO/TX)
    PCL-2024-BIO-1891  APPROVED  (secondary — step therapy identical pathway)
    PCL-2023-BIO-3102  APPROVED  (tertiary — biologic escalation after adalimumab failure)
    PCL-2024-BIO-3580  APPROVED  (hybrid demo — Crohn's, semantically distant from
                                  Scenario B's RA notes but lexically close via shared
                                  Remicade / biosimilar exclusion / POL-INFLIXIMAB
                                  references; designed so $rankFusion(vector + lexical)
                                  lifts it into top 3 while pure $vectorSearch does not)
"""

PRIOR_CLAIMS = [
    # ==============================================================
    # ENGINEERED ANCHORS — SCENARIO A (MRI Lumbar)
    # ==============================================================
    {
        "claim_id": "PCL-2024-MRI-0892",
        "member_id": "HUM-OH-5517203-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2024-09-12",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3950.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Medical necessity established. Member completed 10 sessions of physical therapy with documented initial evaluation and Oswestry Disability Index scores. L4-L5 radiculopathy with positive SLR and dermatomal deficit confirmed on examination. Conservative therapy including NSAIDs and PT failed to resolve radicular symptoms. Plain radiographs obtained and documented as insufficient for soft-tissue evaluation. Authorization approved per POL-MRI-LUMBAR-2024-03.",
        "clinical_note": (
            "56-year-old male, Commercial PPO, Ohio. Lumbar spine MRI requested for "
            "progressive L4-L5 disc degeneration with left-sided radiculopathy in L4 "
            "dermatomal distribution. Member completed 10 physical therapy sessions "
            "with documented initial evaluation and Oswestry Disability Index scores "
            "improving from 52% to 38% disability but with persistent radiculopathy. "
            "NSAID trial (ibuprofen 800 mg TID x 6 weeks) completed; discontinued due "
            "to renal function concerns. SLR positive at 40 degrees left side. "
            "Neurological exam: diminished left patellar reflex, L4 sensory deficit. "
            "Plain lumbar radiographs (June 2024) showed L4-L5 disc space narrowing "
            "insufficient to characterize disc-neural interface. Authorization approved."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-1103",
        "member_id": "HUM-OH-6634811-02",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2024-11-04",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.4",
        "primary_diagnosis_description": "Lumbago with sciatica",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4100.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Initially pended for incomplete PT documentation (missing functional outcome measures). Supplemental physical therapy discharge summary with ODI scores submitted within the 5-day documentation window. Upon receipt of complete records confirming 12 PT sessions and failure of conservative therapy, authorization approved. Member has L5-S1 radiculopathy with positive SLR and S1 dermatomal deficit consistent with disc herniation. MRI indicated for surgical evaluation planning.",
        "clinical_note": (
            "61-year-old female, PPO, Ohio. Lumbar MRI request for lumbar disc "
            "herniation with L5-S1 radiculopathy and sciatica for 16 weeks. "
            "Initially pended — PT documentation incomplete (12 sessions completed "
            "but discharge summary with functional outcome measures absent). "
            "Supplemental ODI score (48% disability) and PT discharge note provided "
            "within documentation window. Step therapy history: physical therapy 12 "
            "sessions, naproxen 500 mg BID x 8 weeks (tolerated, partial response), "
            "cyclobenzaprine PRN. SLR positive bilaterally at 50 degrees. S1 dermatomal "
            "sensory loss right foot. Plain radiographs showed L5-S1 disc space "
            "narrowing. Authorization approved after complete documentation received."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0671",
        "member_id": "HUM-OH-3391047-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2024-07-22",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.5",
        "primary_diagnosis_description": "Low back pain",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3800.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied — conservative treatment requirement not met. Symptom onset 3 weeks prior to imaging request. No physical therapy initiated. Provider requested MRI for acute low back pain without radiculopathy signs or neurological deficit. No red flag symptoms documented. Denial per POL-BACK-PAIN-ACUTE-2023-12 and POL-MRI-LUMBAR-2024-03: acute onset without conservative care completion or neurological findings does not meet medical necessity criteria. Member directed to initiate physical therapy and NSAIDs.",
        "clinical_note": (
            "44-year-old male, PPO, Ohio. Lumbar spine MRI requested for acute low "
            "back pain with onset 3 weeks prior following lifting injury. No radiculopathy, "
            "no neurological deficit documented on examination. SLR negative bilaterally. "
            "No physical therapy initiated. Ibuprofen 600 mg TID prescribed at PCP visit "
            "but reported as only 1 week of use. No plain radiographs obtained. "
            "Ordering physician attestation: 'Patient in significant pain, MRI needed.' "
            "No specific clinical indication beyond acute pain. Denied per plan policy — "
            "conservative treatment not completed, acute onset without neurological findings."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },

    # ==============================================================
    # ENGINEERED ANCHORS — SCENARIO B (Infliximab / RA)
    # ==============================================================
    {
        "claim_id": "PCL-2024-BIO-2244",
        "member_id": "HUM-TX-3381920-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-10-08",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, right shoulder",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg (Remicade)"}],
        "billed_amount": 17840.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Medical necessity confirmed for infliximab continuation. Seropositive rheumatoid arthritis with moderate-to-severe disease activity at initiation (DAS28-CRP 5.1). Step therapy completed: methotrexate failed due to GI intolerance (6 months), leflunomide discontinued at 4 months due to elevated LFTs, adalimumab biosimilar primary non-response at 6 months (DAS28 5.8). Current DAS28-CRP 2.6 on infliximab 5 mg/kg q8 weeks — sustained low disease activity. TB screening negative, no active infections. Approved per POL-BIOLOGIC-RA-2024-07, POL-INFLIXIMAB-2024-06.",
        "clinical_note": (
            "48-year-old female, Commercial PPO, Texas. Infliximab (Remicade) 400 mg "
            "IV continuation claim for seropositive rheumatoid arthritis (ICD-10 "
            "M05.611). DAS28-CRP at initiation: 5.1. Step therapy: methotrexate "
            "failed GI intolerance at 6 months; leflunomide elevated LFTs discontinued "
            "at 4 months; adalimumab biosimilar (Hadlima) primary non-response at 6 "
            "months DAS28-CRP 5.8. Infliximab initiated August 2022 by rheumatologist. "
            "Current DAS28-CRP 2.6 (low disease activity). CRP normal, ESR 21. TB "
            "QuantiFERON negative March 2024. No active infections. Functional status "
            "improved — HAQ-DI 0.75. Step therapy fully documented. Authorization "
            "approved for 12-month continuation per plan biologic RA policy."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1891",
        "member_id": "HUM-TX-7742031-02",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-08-14",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.621",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, right elbow",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg (Remicade)"}],
        "billed_amount": 16950.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "High-cost biologic review completed — step therapy and medical necessity confirmed. Seropositive RA, DAS28 6.2 at initiation. Documented step therapy: MTX 20mg weekly x 10 months discontinued due to hepatotoxicity (ALT 4x ULN); hydroxychloroquine inadequate response at 6 months (DAS28 5.6); leflunomide intolerance (peripheral neuropathy). Infliximab 5 mg/kg q8w initiated 18 months ago. Current DAS28-CRP 2.9 — therapeutic response confirmed. Safety monitoring current. Approved per POL-BIOLOGIC-RA-2024-07.",
        "clinical_note": (
            "41-year-old female, PPO, Texas. Infliximab infusion for moderate-to-severe "
            "seropositive rheumatoid arthritis (M05.621). Diagnosis confirmed by "
            "rheumatologist, DAS28-CRP at start 6.2 (high disease activity). Step "
            "therapy completed: methotrexate 20 mg weekly x 10 months — hepatotoxicity "
            "(ALT 4× ULN lab-confirmed); hydroxychloroquine 400 mg daily x 6 months — "
            "inadequate response DAS28 5.6; leflunomide — peripheral neuropathy "
            "documented by neurology. Adalimumab biosimilar tried, inadequate response "
            "at 6 months. Infliximab 5 mg/kg q8 weeks ongoing 18 months. DAS28-CRP "
            "now 2.9. QuantiFERON-TB negative. No active infection. Medical necessity "
            "confirmed, high-cost concurrent review complete. Authorization approved."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2023-BIO-3102",
        "member_id": "HUM-TX-2201884-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2023-11-20",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.69",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg (Remicade)"}],
        "billed_amount": 15200.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Biologic escalation to infliximab approved after documented adalimumab biosimilar primary non-response (DAS28-CRP remained 6.0 at 6-month reassessment). Prior csDMARD step therapy: methotrexate intolerance, leflunomide inadequate response. Two csDMARDs and one biologic failed per plan criteria. Rheumatologist attestation supports infliximab initiation as next-line IV biologic. Step therapy pathway complete. Approved per POL-BIOLOGIC-RA-2024-07 step therapy exception for prior biologic failure.",
        "clinical_note": (
            "39-year-old female, PPO, Texas. Infliximab (Remicade) initiation for "
            "seropositive RA following adalimumab biosimilar (Hadlima) primary "
            "non-response. Rheumatoid arthritis diagnosis 2019. csDMARD step therapy: "
            "methotrexate — intolerance (nausea, hair loss at 3 months); leflunomide "
            "— inadequate response DAS28 5.2 at 6 months. Adalimumab biosimilar "
            "initiated 2022, DAS28-CRP 6.0 at 6-month assessment — primary non-"
            "response. Rheumatologist Dr. P. Nair recommends escalation to IV TNF "
            "inhibitor (infliximab). Biologic switch documented with objective failure "
            "criteria. TB negative, hep B negative. Step therapy pathway complete. "
            "Infliximab 3 mg/kg initiation authorized."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },
    # ── Hybrid-mode demonstration case ──────────────────────────────
    # Different disease (Crohn's, not RA) — semantically distant from Scenario B's
    # clinical narrative, so pure $vectorSearch ranks this case outside top 3.
    # Shares specific operational tokens with Scenario B (Remicade, biosimilar
    # exclusion clause, 5 mg/kg q8w, MN-DRUG-HCB-002, POL-INFLIXIMAB-2024-06),
    # so $search lifts it on lexical match and $rankFusion brings it into the
    # top 3. The vec #N / lex #M chips will visibly disagree on this row.
    {
        "claim_id": "PCL-2024-BIO-3580",
        "member_id": "HUM-TX-4458172-03",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-12-03",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "K50.10",
        "primary_diagnosis_description": "Crohn's disease of large intestine without complications",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg (Remicade)"}],
        "billed_amount": 17120.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": (
            "Infliximab (Remicade) continuation approved for moderate-severe Crohn's "
            "disease (K50.10) per POL-INFLIXIMAB-2024-06. Member had primary failure "
            "of an infliximab biosimilar (Inflectra) at 12 weeks confirmed by "
            "follow-up endoscopy (CDEIS 14, persistent terminal ileal ulceration). "
            "Originator product Remicade approved under the plan's biosimilar "
            "exclusion clause for documented biosimilar non-response. Step therapy "
            "documented: budesonide induction failure, azathioprine discontinued for "
            "hepatotoxicity (ALT 3.5x ULN), 6-MP discontinued after acute pancreatitis. "
            "Current regimen 5 mg/kg IV every 8 weeks. High-cost biologic review per "
            "MN-DRUG-HCB-002 completed; CDAI 88 confirming clinical remission. TB "
            "QuantiFERON-TB Gold negative March 2024. No active infection."
        ),
        "clinical_note": (
            "37-year-old male, Commercial PPO, Texas. Infliximab (Remicade) 400 mg IV "
            "infusion continuation claim for moderate-severe Crohn's disease (ICD-10 "
            "K50.10) involving the terminal ileum and ascending colon. Diagnosis "
            "established September 2021 by colonoscopy with biopsy at Houston Methodist "
            "Gastroenterology. Member previously trialed an infliximab biosimilar "
            "(Inflectra, infliximab-dyyb) starting October 2023 — primary non-response "
            "confirmed at the week-12 reassessment endoscopy (CDEIS score 14, terminal "
            "ileal stricture with active ulceration and aphthous lesions). Per plan "
            "policy POL-INFLIXIMAB-2024-06 biosimilar exclusion clause for documented "
            "biosimilar non-response, member was switched to originator infliximab "
            "(Remicade brand) in January 2024. Current regimen Remicade 5 mg/kg IV "
            "every 8 weeks; member weight 76 kg. Conventional step therapy fully "
            "documented prior to biologic initiation: budesonide 9 mg PO daily x 8 "
            "weeks — induction failure (CDAI remained 287); azathioprine 2 mg/kg "
            "discontinued at 4 months due to hepatotoxicity (ALT 3.5x ULN, lab-"
            "confirmed); 6-mercaptopurine attempted as alternative thiopurine — "
            "discontinued after acute pancreatitis event documented November 2022. "
            "CDAI score at originator infliximab initiation: 312 (moderate-severe). "
            "Current CDAI: 88 (clinical remission). Fecal calprotectin 47 mg/kg "
            "(normal range). CRP 0.3 mg/dL. QuantiFERON-TB Gold negative March 2024. "
            "Hepatitis B serology negative. No active infection, no recent "
            "hospitalization. Pend reason code MN-DRUG-HCB-002 (high-cost biologic "
            "threshold) triggered; concurrent review confirms ongoing medical "
            "necessity and biosimilar exclusion criteria met."
        ),
        "clinical_embedding": None,
        "embedding_model": "voyage-3",
        "embedding_generated_at": None,
    },

    # ==============================================================
    # GENERAL CORPUS — IMAGING / MRI (29 additional records)
    # ==============================================================
    {
        "claim_id": "PCL-2024-MRI-0211",
        "member_id": "HUM-IN-4401923-01",
        "plan_type": "HMO",
        "state": "IN",
        "service_date": "2024-03-18",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3600.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. 8 PT sessions documented with complete records, NSAID trial, SLR positive, L5 radiculopathy. Meets all criteria POL-MRI-LUMBAR-2024-03.",
        "clinical_note": "52-year-old male, HMO, Indiana. Lumbar MRI for L5 radiculopathy after 8 weeks conservative care (8 PT sessions, naproxen trial). SLR positive right side at 55 degrees. Plain X-ray disc space narrowing L5-S1. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0334",
        "member_id": "HUM-KY-5503812-01",
        "plan_type": "PPO",
        "state": "KY",
        "service_date": "2024-04-09",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.4",
        "primary_diagnosis_description": "Lumbago with sciatica",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4050.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Member completed 6 weeks PT with complete documentation including ODI. Sciatic nerve tension sign positive. Planning epidural steroid injection; MRI indicated for procedural guidance.",
        "clinical_note": "63-year-old female, PPO, Kentucky. Lumbar MRI for lumbago with sciatica. 6 weeks PT completed (ODI documented 54% disability). Considering ESI, MRI required for needle placement. SLR positive 45 degrees. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0489",
        "member_id": "HUM-TN-6612034-02",
        "plan_type": "HMO",
        "state": "TN",
        "service_date": "2024-05-21",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M47.816",
        "primary_diagnosis_description": "Spondylosis with radiculopathy, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3750.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. Physical therapy records submitted are from chiropractic care only — does not satisfy the licensed physical therapist requirement under POL-MRI-LUMBAR-2024-03. Member not eligible for authorization until PT with licensed therapist is completed and documented.",
        "clinical_note": "58-year-old male, HMO, Tennessee. Lumbar MRI for spondylosis with lumbar radiculopathy. Provider submitted 8 chiropractic visits as conservative therapy. Plan requires licensed PT (not chiropractic) for PT documentation requirement. Denied — incorrect therapy type submitted.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2023-MRI-1847",
        "member_id": "HUM-OH-2290173-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2023-10-15",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3900.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. 12 PT sessions, complete documentation, NSAID and muscle relaxant trials, failed conservative management documented. L4-L5 disc degeneration with L5 radiculopathy. Plain films obtained. All criteria POL-MRI-LUMBAR-2024-03 satisfied.",
        "clinical_note": "55-year-old male, PPO, Ohio. Lumbar disc degeneration L4-L5. 12 PT sessions completed with full documentation. NSAIDs and cyclobenzaprine trialed. L5 radiculopathy with positive SLR. Surgical evaluation being considered. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0601",
        "member_id": "HUM-FL-8841920-01",
        "plan_type": "PPO",
        "state": "FL",
        "service_date": "2024-06-14",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.5",
        "primary_diagnosis_description": "Low back pain",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4200.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. Acute low back pain at 2 weeks — no conservative therapy initiated, no neurological signs, no red flags. Denied per POL-BACK-PAIN-ACUTE-2023-12.",
        "clinical_note": "47-year-old male, PPO, Florida. Acute LBP 2 weeks post-injury. No PT, no neuro signs. Denied — acute onset without conservative treatment or red flags.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0722",
        "member_id": "HUM-GA-9902011-01",
        "plan_type": "PPO",
        "state": "GA",
        "service_date": "2024-07-03",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M47.812",
        "primary_diagnosis_description": "Spondylosis with radiculopathy, cervical region",
        "procedure_codes": [{"code": "72141", "type": "CPT", "description": "MRI Cervical Spine without contrast"}],
        "billed_amount": 3850.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Cervical radiculopathy with objective neurological findings, 4 weeks PT completed with documentation. C5-C6 radiculopathy suspected. Meets POL-MRI-CERVICAL-2024-02.",
        "clinical_note": "51-year-old female, PPO, Georgia. Cervical radiculopathy right upper extremity C5-C6 distribution. 4 weeks PT, triceps reflex diminished right. Approved per cervical MRI criteria.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0843",
        "member_id": "HUM-NC-1102933-01",
        "plan_type": "HMO",
        "state": "NC",
        "service_date": "2024-08-19",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.2",
        "primary_diagnosis_description": "Cervicalgia",
        "procedure_codes": [{"code": "72141", "type": "CPT", "description": "MRI Cervical Spine without contrast"}],
        "billed_amount": 3700.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. Cervicalgia without radiculopathy or myelopathy. Conservative treatment only 2 weeks. No neurological findings. Denied.",
        "clinical_note": "45-year-old female, HMO, North Carolina. Cervicalgia 2 weeks. No radiculopathy, no neuro deficit. Conservative care just initiated. Denied.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0956",
        "member_id": "HUM-OH-7743122-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2024-09-05",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.36",
        "primary_diagnosis_description": "Other intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72149", "type": "CPT", "description": "MRI Lumbar Spine with contrast"}],
        "billed_amount": 4600.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Post-surgical lumbar MRI with contrast for evaluation of recurrent disc herniation. Prior L4-L5 discectomy 2022. New onset left-sided radiculopathy with objective neurological deficit. PT and conservative care not required for post-surgical recurrence evaluation. Approved.",
        "clinical_note": "60-year-old male, PPO, Ohio. Post-surgical evaluation for recurrent L4-L5 disc herniation after 2022 discectomy. New left radiculopathy. Conservative care waiver applied for post-surgical setting. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-1034",
        "member_id": "HUM-MI-3312099-01",
        "plan_type": "PPO",
        "state": "MI",
        "service_date": "2024-10-22",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.4",
        "primary_diagnosis_description": "Lumbago with sciatica",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3950.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Sciatica with positive SLR, 10 PT sessions with complete documentation. Considering epidural steroid injection. All criteria met.",
        "clinical_note": "57-year-old female, PPO, Michigan. Sciatica right lower extremity. 10 PT sessions completed with ODI documentation. SLR positive right 50 degrees. ESI planning. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-1212",
        "member_id": "HUM-WI-4421088-01",
        "plan_type": "HMO",
        "state": "WI",
        "service_date": "2024-11-08",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M47.816",
        "primary_diagnosis_description": "Spondylosis with radiculopathy, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3800.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Lumbar spondylosis with radiculopathy. 8 PT sessions, NSAID trial, complete documentation with functional outcome measures. Meets all criteria.",
        "clinical_note": "54-year-old male, HMO, Wisconsin. Lumbar spondylosis with L4 radiculopathy. 8 PT sessions, ibuprofen 800mg TID x 6 weeks. ODI documented. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-MRI-0112",
        "member_id": "HUM-OH-8814037-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2025-01-14",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.5",
        "primary_diagnosis_description": "Low back pain",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4250.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. Physical therapy documentation submitted but only 5 sessions — plan minimum is 8 sessions for lumbar spine MRI criteria. No neurological deficit documented. Denial with appeal rights. Additional PT sessions should be completed.",
        "clinical_note": "62-year-old female, PPO, Ohio. Chronic LBP. Only 5 PT sessions documented — below 8-session minimum. No objective neuro findings. Denied pending completion of adequate PT course.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-MRI-0288",
        "member_id": "HUM-IN-9923041-01",
        "plan_type": "PPO",
        "state": "IN",
        "service_date": "2025-02-03",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4100.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Lumbar disc degeneration with L4-L5 radiculopathy, 10 PT sessions documented with complete records, SLR positive, planning surgical evaluation. Criteria met.",
        "clinical_note": "53-year-old male, PPO, Indiana. L4-L5 disc degeneration with radiculopathy. 10 PT sessions, complete documentation, SLR positive. Surgical evaluation. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-1391",
        "member_id": "HUM-KY-7712834-01",
        "plan_type": "PPO",
        "state": "KY",
        "service_date": "2024-12-09",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M47.812",
        "primary_diagnosis_description": "Spondylosis with radiculopathy, cervical region",
        "procedure_codes": [{"code": "72141", "type": "CPT", "description": "MRI Cervical Spine without contrast"}],
        "billed_amount": 3900.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Cervical spondylosis with radiculopathy, 4 weeks PT, objective neurological findings. Meets POL-MRI-CERVICAL-2024-02.",
        "clinical_note": "49-year-old female, PPO, Kentucky. Cervical spondylosis C6-C7 radiculopathy. 4 weeks PT completed. Diminished triceps reflex. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-1488",
        "member_id": "HUM-MN-5531094-01",
        "plan_type": "PPO",
        "state": "MN",
        "service_date": "2024-12-20",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.16",
        "primary_diagnosis_description": "Radiculopathy, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3800.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Lumbar radiculopathy with positive SLR, 8 PT sessions, NSAID trial. Complete documentation. Approved.",
        "clinical_note": "59-year-old male, PPO, Minnesota. Lumbar radiculopathy right L4. 8 PT sessions completed. NSAID trial 6 weeks. SLR positive. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0183",
        "member_id": "HUM-AZ-2233091-01",
        "plan_type": "HMO",
        "state": "AZ",
        "service_date": "2024-02-28",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M75.1",
        "primary_diagnosis_description": "Rotator cuff syndrome",
        "procedure_codes": [{"code": "73221", "type": "CPT", "description": "MRI Shoulder without contrast"}],
        "billed_amount": 3200.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Shoulder MRI for suspected rotator cuff tear after 6 weeks PT and NSAID trial. Persistent functional limitation. Meets POL-MRI-SHOULDER-2023-08.",
        "clinical_note": "50-year-old male, HMO, Arizona. Rotator cuff syndrome right shoulder. 6 weeks PT, NSAID trial, persistent pain and functional limitation. Approved per shoulder MRI criteria.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0291",
        "member_id": "HUM-CO-3344192-01",
        "plan_type": "PPO",
        "state": "CO",
        "service_date": "2024-04-01",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M23.200",
        "primary_diagnosis_description": "Derangement of meniscus, unspecified, right knee",
        "procedure_codes": [{"code": "73721", "type": "CPT", "description": "MRI Knee without contrast"}],
        "billed_amount": 3100.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Suspected medial meniscus tear after sports injury. 4 weeks conservative care, persistent locking and joint line tenderness. Surgical evaluation planned. Meets POL-MRI-KNEE-2023-11.",
        "clinical_note": "38-year-old female, PPO, Colorado. Suspected medial meniscus tear right knee after sports injury. 4 weeks conservative care. Locking symptoms, joint line tenderness. Surgical evaluation. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2023-MRI-2019",
        "member_id": "HUM-TX-4451290-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2023-11-02",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.4",
        "primary_diagnosis_description": "Lumbago with sciatica",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3950.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Lumbago with sciatica, SLR positive, 12 PT sessions, conservative management failed. Criteria met.",
        "clinical_note": "67-year-old male, PPO, Texas. Lumbago with sciatica. 12 PT sessions. SLR positive. Conservative care failed. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0509",
        "member_id": "HUM-IL-8823041-01",
        "plan_type": "PPO",
        "state": "IL",
        "service_date": "2024-05-30",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M47.816",
        "primary_diagnosis_description": "Spondylosis with radiculopathy, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4000.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Lumbar spondylosis with radiculopathy. Conservative care completed, functional outcome measures documented. L4-L5 involvement. Approved.",
        "clinical_note": "64-year-old female, PPO, Illinois. Lumbar spondylosis with radiculopathy L4-L5. 9 PT sessions, functional outcomes documented. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0748",
        "member_id": "HUM-PA-3302198-01",
        "plan_type": "HMO",
        "state": "PA",
        "service_date": "2024-07-25",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.5",
        "primary_diagnosis_description": "Low back pain",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3650.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. Non-specific low back pain without radiculopathy. PT records submitted show only 4 sessions — below 8-session minimum. No neurological examination findings. Denied.",
        "clinical_note": "48-year-old male, HMO, Pennsylvania. Non-specific LBP without radiculopathy. Only 4 PT sessions. Below minimum. No neuro findings. Denied.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-MRI-0141",
        "member_id": "HUM-OH-1123041-02",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2025-01-28",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4300.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. PPO Ohio, lumbar disc degeneration, complete conservative treatment course, L4-L5 radiculopathy with neurological findings. Surgical evaluation. Approved.",
        "clinical_note": "71-year-old male, PPO, Ohio. Lumbar disc degeneration L4-L5. 11 PT sessions with complete documentation. SLR positive. Diminished reflexes. Surgical evaluation. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0384",
        "member_id": "HUM-WA-6612044-01",
        "plan_type": "PPO",
        "state": "WA",
        "service_date": "2024-04-18",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "G54.3",
        "primary_diagnosis_description": "Thoracic root disorders",
        "procedure_codes": [{"code": "72146", "type": "CPT", "description": "MRI Thoracic Spine without contrast"}],
        "billed_amount": 3850.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Thoracic root disorder with chest wall radiculopathy, rule out disc herniation vs. intrinsic spinal pathology. Myelopathy screening indicated. Approved with expedited track.",
        "clinical_note": "55-year-old female, PPO, Washington. Thoracic radiculopathy, chest wall dermatomal pain, concern for myelopathy. Expedited imaging approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-1091",
        "member_id": "HUM-OH-9934712-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2024-10-30",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.4",
        "primary_diagnosis_description": "Lumbago with sciatica",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3950.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Ohio PPO, sciatica with SLR positive, 10 PT sessions documented, functional outcomes included. NSAIDs trialed. Criteria met.",
        "clinical_note": "59-year-old male, PPO, Ohio. Sciatica left leg, 10 PT sessions, SLR positive 45 degrees, NSAIDs trialed. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-1147",
        "member_id": "HUM-TX-1101923-02",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-11-15",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4100.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Lumbar disc degeneration with radiculopathy, 12 PT sessions, conservative management failed, SLR positive, neurological deficit. Criteria met.",
        "clinical_note": "61-year-old male, PPO, Texas. L4-L5 disc degeneration, radiculopathy, 12 PT sessions. SLR positive. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0821",
        "member_id": "HUM-FL-2212034-01",
        "plan_type": "PPO",
        "state": "FL",
        "service_date": "2024-08-07",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.16",
        "primary_diagnosis_description": "Radiculopathy, lumbar region",
        "procedure_codes": [{"code": "72158", "type": "CPT", "description": "MRI Lumbar Spine with and without contrast"}],
        "billed_amount": 4700.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Post-lumbar fusion MRI with and without contrast for evaluation of adjacent segment disease. Radiculopathy new onset at L3-L4. Criteria met for post-surgical evaluation.",
        "clinical_note": "65-year-old female, PPO, Florida. Post-L4-L5 fusion evaluation. New radiculopathy L3-L4 adjacent segment. MRI with/without contrast approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-MRI-0389",
        "member_id": "HUM-OH-4412091-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2025-03-19",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4050.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. PPO Ohio, lumbar disc degeneration with L4-L5 radiculopathy. Complete PT documentation, NSAIDs failed, SLR positive. Criteria satisfied.",
        "clinical_note": "56-year-old female, PPO, Ohio. Lumbar disc degeneration L4-L5 with radiculopathy. Complete 10-session PT documented. NSAIDs GI intolerance. SLR positive. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-0617",
        "member_id": "HUM-NJ-5521038-01",
        "plan_type": "HMO",
        "state": "NJ",
        "service_date": "2024-06-25",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.4",
        "primary_diagnosis_description": "Lumbago with sciatica",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3700.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Sciatica with conservative care completed, neurological findings present. Criteria met.",
        "clinical_note": "53-year-old male, HMO, New Jersey. Sciatica with 8 PT sessions completed, neurological deficit left foot. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2023-MRI-2211",
        "member_id": "HUM-OH-3393041-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2023-12-11",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M47.816",
        "primary_diagnosis_description": "Spondylosis with radiculopathy, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 3900.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Ohio PPO, lumbar spondylosis with radiculopathy. 9 PT sessions, conservative care failed, neurological deficit. Criteria met.",
        "clinical_note": "57-year-old male, PPO, Ohio. Lumbar spondylosis L4-L5 with radiculopathy. 9 PT sessions, NSAID trial, SLR positive. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-MRI-1309",
        "member_id": "HUM-WI-6623041-01",
        "plan_type": "PPO",
        "state": "WI",
        "service_date": "2024-12-02",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M54.4",
        "primary_diagnosis_description": "Lumbago with sciatica",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4050.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. Provider submitted 8 PT sessions but no functional outcome measures documented. Physical therapy records consist of billing records only. Denied pending resubmission with complete PT documentation including outcome measures.",
        "clinical_note": "62-year-old male, PPO, Wisconsin. Sciatica. 8 PT sessions billed but no functional outcome measures documented. Denied — incomplete PT records.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-MRI-0499",
        "member_id": "HUM-OH-5514023-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2025-04-07",
        "clinical_area": "imaging",
        "primary_diagnosis_code": "M51.16",
        "primary_diagnosis_description": "Intervertebral disc degeneration, lumbar region",
        "procedure_codes": [{"code": "72148", "type": "CPT", "description": "MRI Lumbar Spine without contrast"}],
        "billed_amount": 4200.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Ohio PPO lumbar disc degeneration. 10 PT sessions including ODI scores. SLR positive. Failed NSAIDs and cyclobenzaprine. Surgical candidacy evaluation planned. All criteria POL-MRI-LUMBAR-2024-03 satisfied.",
        "clinical_note": "60-year-old male, PPO, Ohio. L4-L5 disc degeneration with L4 radiculopathy. 10 PT sessions, ODI 44%. NSAIDs and muscle relaxants trialed. SLR positive. Surgical evaluation. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    # ==============================================================
    # GENERAL CORPUS — BIOLOGIC / SPECIALTY DRUG (25 additional records)
    # ==============================================================
    {
        "claim_id": "PCL-2024-BIO-0441",
        "member_id": "HUM-TX-8812039-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-04-02",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.79",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 16200.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab continuation for RA. Step therapy complete — MTX intolerance, hydroxychloroquine inadequate response. DAS28 2.4 on current therapy. Safety monitoring current. Approved.",
        "clinical_note": "52-year-old female, PPO, Texas. Infliximab for RA. MTX intolerance, HCQ inadequate response. DAS28-CRP 2.4. TB negative. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-0712",
        "member_id": "HUM-FL-3341092-01",
        "plan_type": "PPO",
        "state": "FL",
        "service_date": "2024-06-18",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, right shoulder",
        "procedure_codes": [{"code": "J0135", "type": "HCPCS", "description": "Adalimumab 20mg"}],
        "billed_amount": 6800.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Adalimumab biosimilar for RA. Step therapy: MTX 6 months inadequate response, leflunomide 4 months — elevated LFTs. DAS28 3.0 at 6-month check. Approved.",
        "clinical_note": "46-year-old female, PPO, Florida. Adalimumab biosimilar for seropositive RA. MTX inadequate response 6 months, leflunomide elevated LFTs. DAS28 3.0. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-0893",
        "member_id": "HUM-GA-4452019-01",
        "plan_type": "HMO",
        "state": "GA",
        "service_date": "2024-08-05",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor",
        "procedure_codes": [{"code": "J0135", "type": "HCPCS", "description": "Adalimumab 20mg"}],
        "billed_amount": 5400.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. Step therapy not met — only methotrexate tried for 2 months (below 3-month minimum). No second csDMARD tried. Biologic not yet authorized without step therapy completion. Member to continue MTX at minimum 3 months and add a second csDMARD or document intolerance.",
        "clinical_note": "42-year-old male, HMO, Georgia. Adalimumab for RA. MTX only 2 months — below 3-month minimum. No second csDMARD. Step therapy incomplete. Denied.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2023-BIO-2891",
        "member_id": "HUM-TX-9923041-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2023-09-12",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.69",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 14800.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab initiation for RA following complete step therapy — MTX hepatotoxicity, leflunomide neuropathy, adalimumab primary non-response. Criteria fully met.",
        "clinical_note": "43-year-old female, PPO, Texas. Infliximab initiation for RA. MTX hepatotoxicity, leflunomide neuropathy, adalimumab biosimilar primary non-response. Step therapy complete. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1041",
        "member_id": "HUM-TX-1121034-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-09-23",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 17100.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab renewal. Seropositive RA, sustained low disease activity DAS28-CRP 2.7. Step therapy historically complete. TB negative, no active infection. Approved.",
        "clinical_note": "50-year-old female, PPO, Texas. Infliximab renewal RA. DAS28-CRP 2.7, TB negative, step therapy complete. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1209",
        "member_id": "HUM-CA-6641092-01",
        "plan_type": "PPO",
        "state": "CA",
        "service_date": "2024-10-14",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "L40.50",
        "primary_diagnosis_description": "Arthropathic psoriasis, unspecified",
        "procedure_codes": [{"code": "J0135", "type": "HCPCS", "description": "Adalimumab 20mg"}],
        "billed_amount": 6200.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Adalimumab for psoriatic arthritis. MTX and leflunomide tried. DAPSA score 18 (moderate activity). Step therapy complete per POL-BIOLOGIC-PsA-2024-02.",
        "clinical_note": "38-year-old male, PPO, California. Adalimumab for psoriatic arthritis. MTX and leflunomide failed. DAPSA 18. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1348",
        "member_id": "HUM-NY-7752011-01",
        "plan_type": "HMO",
        "state": "NY",
        "service_date": "2024-11-07",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M45.9",
        "primary_diagnosis_description": "Ankylosing spondylitis, unspecified",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 15800.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab for ankylosing spondylitis. BASDAI 5.2, failed 2 NSAIDs. No csDMARD requirement for axial AS. TB negative. Approved per POL-BIOLOGIC-AS-2024-01.",
        "clinical_note": "35-year-old male, HMO, New York. Infliximab for ankylosing spondylitis. BASDAI 5.2. 2 NSAID failures. Axial disease — no csDMARD step required. TB negative. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1502",
        "member_id": "HUM-OH-8813044-01",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2024-12-01",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.79",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J3262", "type": "HCPCS", "description": "Tocilizumab (Actemra)"}],
        "billed_amount": 12400.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Tocilizumab for RA after TNF inhibitor failure. Step therapy complete: MTX, leflunomide, adalimumab (primary non-response). IL-6 inhibitor step after biologic failure. DAS28 4.1. Approved.",
        "clinical_note": "55-year-old female, PPO, Ohio. Tocilizumab for RA after adalimumab failure. csDMARDs and biologic step therapy complete. DAS28 4.1. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1674",
        "member_id": "HUM-TX-2231091-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-12-19",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 18100.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab continuation, seropositive RA, DAS28 2.5, step therapy documented, safety monitoring current. High-cost review completed. Approved.",
        "clinical_note": "47-year-old female, PPO, Texas. Infliximab renewal seropositive RA. DAS28-CRP 2.5. TB negative, no infection. High-cost review complete. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-BIO-0188",
        "member_id": "HUM-TX-3341029-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2025-01-20",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.69",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 17600.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab renewal RA. Step therapy: MTX hepatotoxicity, hydroxychloroquine inadequate response, leflunomide neuropathy, adalimumab primary non-response. DAS28 2.6 on infliximab. Approved.",
        "clinical_note": "44-year-old female, PPO, Texas. Infliximab renewal RA. MTX hepatotoxicity, HCQ inadequate response, leflunomide neuropathy, adalimumab non-response. DAS28 2.6. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-0381",
        "member_id": "HUM-IL-9923041-01",
        "plan_type": "PPO",
        "state": "IL",
        "service_date": "2024-03-27",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "K50.10",
        "primary_diagnosis_description": "Crohn's disease of large intestine without complications",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 16800.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab for Crohn's disease. HBI 8 (moderate-severe). Azathioprine failed 4 months (inadequate response), mesalamine not applicable. Approved per POL-BIOLOGIC-CROHN-2023-11.",
        "clinical_note": "33-year-old male, PPO, Illinois. Infliximab for Crohn's disease, HBI 8. Azathioprine inadequate response. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2023-BIO-4012",
        "member_id": "HUM-TX-4441092-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2023-08-14",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 15600.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab for RA following documented step therapy failure of two csDMARDs and adalimumab. DAS28-CRP 3.0 at initiation. Medical necessity confirmed.",
        "clinical_note": "39-year-old female, PPO, Texas. Infliximab for RA. Two csDMARD failures and adalimumab non-response. DAS28 3.0. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-0588",
        "member_id": "HUM-AZ-6612041-01",
        "plan_type": "HMO",
        "state": "AZ",
        "service_date": "2024-05-12",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.69",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J0135", "type": "HCPCS", "description": "Adalimumab 20mg"}],
        "billed_amount": 5800.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. Biologic requested for RA without specialist (rheumatologist) documentation. PCP ordered biologic without rheumatology confirmation of diagnosis or DAS28 score. Medical director review: biologic not authorized without specialist confirmation of moderate-severe disease.",
        "clinical_note": "61-year-old male, HMO, Arizona. Adalimumab for RA ordered by PCP without rheumatologist confirmation. DAS28 not documented. Denied — specialist documentation required.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1781",
        "member_id": "HUM-WA-7723041-01",
        "plan_type": "PPO",
        "state": "WA",
        "service_date": "2024-12-30",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.79",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 17400.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab continuation RA. DAS28 2.8. Long-standing therapy with documented clinical response. Step therapy historically complete. Safety monitoring current. Approved.",
        "clinical_note": "53-year-old male, PPO, Washington. Infliximab renewal RA. DAS28 2.8. Long-term therapy, step therapy complete. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-BIO-0334",
        "member_id": "HUM-TX-5512034-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2025-02-11",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 16700.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab continuation seropositive RA. DAS28-CRP 2.9. Step therapy documented including MTX intolerance and adalimumab non-response. Medical necessity confirmed. Approved.",
        "clinical_note": "45-year-old female, PPO, Texas. Infliximab continuation for seropositive RA. Step therapy complete. DAS28-CRP 2.9. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-0978",
        "member_id": "HUM-NC-8831041-01",
        "plan_type": "PPO",
        "state": "NC",
        "service_date": "2024-09-03",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.69",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J0135", "type": "HCPCS", "description": "Adalimumab 20mg"}],
        "billed_amount": 6100.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Adalimumab biosimilar for RA. Step therapy: MTX 4 months then stopped (patient preference without intolerance), leflunomide 6 months inadequate response. DAS28 4.2. Biologic approved, MTX preference-stop noted in chart but documented.",
        "clinical_note": "56-year-old female, PPO, North Carolina. Adalimumab biosimilar for RA. MTX stopped patient preference, leflunomide inadequate response. DAS28 4.2. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1124",
        "member_id": "HUM-TX-6601034-01",
        "plan_type": "HMO",
        "state": "TX",
        "service_date": "2024-10-28",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 17900.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. High-cost concurrent review complete. Infliximab for seropositive RA. Step therapy: MTX hepatotoxicity, leflunomide GI intolerance, adalimumab biosimilar primary non-response. DAS28 2.7. Medical necessity confirmed.",
        "clinical_note": "49-year-old female, HMO, Texas. Infliximab for RA. MTX hepatotoxicity, leflunomide GI intolerance, adalimumab biosimilar non-response. DAS28 2.7. High-cost review complete. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-BIO-0481",
        "member_id": "HUM-TX-4413021-02",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2025-03-03",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.621",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, right elbow",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 18200.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab continuation seropositive RA. DAS28-CRP 3.0. Complete step therapy history on file — three csDMARD failures and one biologic failure. Medical necessity confirmed at concurrent review.",
        "clinical_note": "43-year-old female, PPO, Texas. Infliximab for RA (M05.621). Three csDMARD failures and prior biologic failure. DAS28-CRP 3.0. High-cost concurrent review. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-1851",
        "member_id": "HUM-CO-9912034-01",
        "plan_type": "PPO",
        "state": "CO",
        "service_date": "2024-12-15",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.69",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor, multiple sites",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 16500.00,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. TB screening expired — QuantiFERON-TB result on file is 18 months old (beyond 12-month renewal requirement per POL-BIOLOGIC-MONITORING-2024-04). Authorization held pending current TB screening. Restart infusion authorization after current test submitted.",
        "clinical_note": "58-year-old male, PPO, Colorado. Infliximab renewal for RA. TB screening expired (18 months old). Denied pending current QuantiFERON-TB result.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2024-BIO-0234",
        "member_id": "HUM-TX-1112034-01",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-02-08",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M05.611",
        "primary_diagnosis_description": "Rheumatoid arthritis with rheumatoid factor",
        "procedure_codes": [{"code": "J1745", "type": "HCPCS", "description": "Infliximab 10mg"}],
        "billed_amount": 17200.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Infliximab for RA. Step therapy: MTX intolerance (GI), hydroxychloroquine and leflunomide tried — inadequate response documented. Adalimumab biosimilar non-response. DAS28-CRP 2.8. Full step therapy compliance confirmed.",
        "clinical_note": "40-year-old female, PPO, Texas. Infliximab for seropositive RA. Full step therapy compliance. DAS28-CRP 2.8. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
    {
        "claim_id": "PCL-2025-BIO-0622",
        "member_id": "HUM-GA-3341019-01",
        "plan_type": "PPO",
        "state": "GA",
        "service_date": "2025-04-14",
        "clinical_area": "biologic",
        "primary_diagnosis_code": "M06.00",
        "primary_diagnosis_description": "Rheumatoid arthritis without rheumatoid factor, unspecified",
        "procedure_codes": [{"code": "J0135", "type": "HCPCS", "description": "Adalimumab 20mg"}],
        "billed_amount": 6600.00,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. Seronegative RA. MTX 6 months inadequate response, leflunomide 4 months discontinued (elevated LFTs). DAS28 4.8. Adalimumab biosimilar approved as first biologic.",
        "clinical_note": "37-year-old female, PPO, Georgia. Adalimumab biosimilar for seronegative RA. MTX inadequate, leflunomide elevated LFTs. DAS28 4.8. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    # ── GLP-1 / Obesity prior claims (Scenario C engineered anchors) ──────────

    {
        "claim_id": "PCL-2024-GLP1-1456",
        "member_id": "HUM-FL-7723041-03",
        "plan_type": "PPO",
        "state": "FL",
        "service_date": "2024-09-11",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection (Wegovy) 2.4 mg/dose weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": (
            "Approved. 54-year-old female, BMI 38.1, PPO/FL. Qualifying comorbidities: "
            "T2DM (HbA1c 8.1%), hypertension (on lisinopril), obstructive sleep apnea "
            "(AHI 19). T2DM step therapy documented: metformin maximized (GI intolerance "
            "at higher dose), SGLT-2 inhibitor (canagliflozin) failed after 8 weeks due "
            "to recurrent genitourinary infections. 6-month medically supervised weight "
            "management program submitted — Tampa General Hospital Metabolic Weight "
            "Management program, February–August 2024, monthly endocrinology visits, "
            "documented 4.2% body weight loss insufficient for sustained glycemic control. "
            "Two prior anti-obesity medication failures: orlistat (GI intolerance, "
            "discontinued 3 weeks) and phentermine/topiramate (hypertension precaution, "
            "discontinued 6 weeks). No contraindications to semaglutide. Dual-indication "
            "approval: weight management and T2DM glycemic control per ADA 2024 guidelines."
        ),
        "clinical_note": (
            "54-year-old female, PPO/FL. BMI 38.1, morbid obesity with T2DM (HbA1c 8.1%), "
            "hypertension, and obstructive sleep apnea (AHI 19, CPAP compliant). Metformin "
            "at maximum tolerated dose; SGLT-2 inhibitor failed due to recurrent genitourinary "
            "infections. Prior anti-obesity medications failed: orlistat (severe GI effects), "
            "phentermine/topiramate (hypertension concern). Completed 6-month medically "
            "supervised weight management program at Tampa General Hospital — endocrinologist-"
            "led, monthly visits, documented 4.2% weight loss, plateau. Requesting semaglutide "
            "2.4 mg weekly for combined weight management and glycemic control. HbA1c target "
            "not achieved on oral agents alone. No MEN2 history, no pancreatitis history, "
            "lipase normal. Approved for dual-indication: weight management plus T2DM."
        ),
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-0923",
        "member_id": "HUM-GA-5541820-02",
        "plan_type": "PPO",
        "state": "GA",
        "service_date": "2024-07-08",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection (Wegovy) 2.4 mg/dose weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": (
            "Approved. 49-year-old female, BMI 36.4, PPO/GA. Qualifying comorbidities: "
            "obstructive sleep apnea (AHI 28, CPAP compliant), hypertension (amlodipine "
            "5 mg, BP 142/88 mmHg suboptimally controlled), hyperlipidemia (LDL 148 mg/dL "
            "on atorvastatin). Six-month medically supervised weight management program "
            "documented: Emory Bariatric and Weight Management Center, January–June 2024, "
            "biweekly dietitian visits, documented caloric restriction and behavioral "
            "therapy, 3.8% weight loss at 6 months. Prior anti-obesity medication trial: "
            "naltrexone/bupropion ER (Contrave) for 16 weeks — inadequate response (less "
            "than 2% body weight reduction), discontinued per clinical protocol. BMI 35+ "
            "threshold met; comorbidity documentation supports but is not required at this "
            "BMI tier. Approved."
        ),
        "clinical_note": (
            "49-year-old female, PPO/GA. BMI 36.4 with obstructive sleep apnea (AHI 28, "
            "CPAP adherent), hypertension on amlodipine (BP 142/88), and hyperlipidemia on "
            "atorvastatin (LDL 148). No diabetes. Completed 6-month Emory Bariatric and "
            "Weight Management program: biweekly dietitian-supervised visits, behavioral "
            "therapy, structured meal plan. 3.8% body weight reduction at 6 months — "
            "insufficient, continued plateau. Prior naltrexone/bupropion ER trial 16 weeks: "
            "less than 2% weight response, discontinued. Requesting Wegovy 2.4 mg weekly "
            "for chronic weight management. Endocrinologist referral. No contraindications. "
            "Approved under BMI ≥ 35 pathway with supporting lifestyle documentation."
        ),
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-0312",
        "member_id": "HUM-FL-3318804-01",
        "plan_type": "PPO",
        "state": "FL",
        "service_date": "2024-04-22",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.09",
        "primary_diagnosis_description": "Other obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection (Wegovy) 2.4 mg/dose weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": (
            "Denied. 41-year-old female, BMI 28.9, PPO/FL. BMI below 30 kg/m² threshold "
            "for anti-obesity pharmacotherapy coverage. Member does not meet BMI eligibility "
            "criterion under plan policy POL-GLP1-OBESITY-2024-08 (requires BMI ≥ 30 with "
            "comorbidity, or BMI ≥ 35). No qualifying comorbidities documented (normotensive, "
            "normoglycemic, no OSA diagnosis). Additionally, no documentation of a 6-month "
            "medically supervised weight management program — submitted records reflect only "
            "three primary care office notes over 4 months with brief weight counseling, "
            "which does not constitute a qualifying structured program per plan policy. "
            "Denial upheld. Appeal rights communicated to member and prescriber."
        ),
        "clinical_note": (
            "41-year-old female, PPO/FL. BMI 28.9. Requesting Wegovy 2.4 mg for weight "
            "management. No qualifying comorbidities: blood pressure 118/74, fasting glucose "
            "88 mg/dL, no sleep apnea diagnosis, LDL 102 mg/dL. No formal structured weight "
            "management program documentation — submitted PCP notes show 3 office visits over "
            "4 months with weight counseling but no structured program. BMI below coverage "
            "threshold and no qualifying comorbidity to meet 30.0–34.9 tier. Denied. "
            "Member and prescriber notified of appeal process."
        ),
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    # ── GLP-1 / Obesity corpus records ────────────────────────────────────────

    {
        "claim_id": "PCL-2024-GLP1-0571",
        "member_id": "HUM-TX-4412783-02",
        "plan_type": "PPO",
        "state": "TX",
        "service_date": "2024-06-14",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 39.2, T2DM HbA1c 8.4%, hypertension. 6-month program completed. Metformin and sitagliptin failed. No contraindications.",
        "clinical_note": "58-year-old male, PPO/TX. BMI 39.2, T2DM (HbA1c 8.4%), hypertension. 6-month UT Southwestern weight program. Metformin and sitagliptin failed. Semaglutide approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-0788",
        "member_id": "HUM-NC-6628011-03",
        "plan_type": "HMO",
        "state": "NC",
        "service_date": "2024-08-19",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 37.8, OSA (AHI 31), hypertension. 6-month UNC Weight Management program. Orlistat failed (GI intolerance). Lifestyle documentation complete.",
        "clinical_note": "51-year-old female, HMO/NC. BMI 37.8, OSA (AHI 31, CPAP compliant), hypertension on metoprolol. UNC Weight Management 6-month program completed. Orlistat GI intolerance. Semaglutide approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-1102",
        "member_id": "HUM-OH-8834521-02",
        "plan_type": "PPO",
        "state": "OH",
        "service_date": "2024-10-03",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 41.0, T2DM HbA1c 9.1%, hyperlipidemia, HTN. OSU Weight Management program 6 months. Metformin at max dose, SGLT-2 contraindicated (CKD Stage 3). Dual indication approved.",
        "clinical_note": "62-year-old male, PPO/OH. BMI 41.0, T2DM (HbA1c 9.1%), CKD Stage 3, HTN, hyperlipidemia. OSU 6-month weight program. SGLT-2 contraindicated (eGFR 38). Metformin max dose. Approved dual indication.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-0644",
        "member_id": "HUM-FL-2219873-01",
        "plan_type": "PPO",
        "state": "FL",
        "service_date": "2024-05-28",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. BMI 31.2 with T2DM but no 6-month supervised program documentation. PCP notes submitted cover only 3 visits over 5 months. Program requirement not met. Pending appeal.",
        "clinical_note": "45-year-old female, PPO/FL. BMI 31.2, T2DM HbA1c 7.4%. Requesting Wegovy. Only 3 PCP visits submitted as lifestyle documentation — does not meet 6-month structured program requirement. Denied.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-0855",
        "member_id": "HUM-AZ-5521049-02",
        "plan_type": "PPO",
        "state": "AZ",
        "service_date": "2024-07-31",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 36.9, T2DM, HTN, OSA. Banner Health 6-month weight program documented. Phentermine/topiramate cognitive side effects at 10 weeks. Metformin max dose, DPP-4 inhibitor inadequate HbA1c response. Approved.",
        "clinical_note": "55-year-old female, PPO/AZ. BMI 36.9, T2DM (HbA1c 7.9%), HTN, OSA. Banner Health 6-month program. Phentermine/topiramate cognitive SE. Metformin + sitagliptin: HbA1c still 7.9%. Semaglutide approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-1244",
        "member_id": "HUM-CA-7731882-03",
        "plan_type": "HMO",
        "state": "CA",
        "service_date": "2024-11-12",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 35.1, HTN, hyperlipidemia. UCSF 6-month program. Naltrexone/bupropion 16 weeks inadequate (<3% weight loss). No diabetes but meets BMI ≥ 35 threshold. Approved.",
        "clinical_note": "47-year-old male, HMO/CA. BMI 35.1, HTN, hyperlipidemia. UCSF 6-month weight program. Naltrexone/bupropion 16 weeks, <3% weight loss. No T2DM. BMI ≥ 35 pathway. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2023-GLP1-2891",
        "member_id": "HUM-FL-1102945-01",
        "plan_type": "PPO",
        "state": "FL",
        "service_date": "2023-11-07",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 40.5, T2DM HbA1c 8.8%, OSA, HTN, hyperlipidemia. AdventHealth Orlando 6-month program. Metformin + empagliflozin; SGLT-2 discontinued for recurrent UTIs. Phentermine/topiramate elevated BP. Full documentation. Approved.",
        "clinical_note": "60-year-old female, PPO/FL. BMI 40.5, T2DM, OSA, HTN, hyperlipidemia. AdventHealth 6-month program complete. SGLT-2 UTI history. Phentermine/topiramate elevated BP. Full step therapy. Approved dual indication.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-0197",
        "member_id": "HUM-TN-4429017-02",
        "plan_type": "PPO",
        "state": "TN",
        "service_date": "2024-03-15",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. BMI 32.4, T2DM HbA1c 6.8% (at goal). Lifestyle program documentation submitted covers only 4 months. Program duration requirement (6 months) not met. No prior anti-obesity medication trial documented. Denied pending resubmission.",
        "clinical_note": "48-year-old female, PPO/TN. BMI 32.4, T2DM HbA1c 6.8% (controlled). Requesting Wegovy. 4-month PCP program only. No prior anti-obesity meds. Lifestyle requirement not met. Denied.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-1388",
        "member_id": "HUM-GA-3318824-02",
        "plan_type": "PPO",
        "state": "GA",
        "service_date": "2024-10-22",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 37.2, T2DM, hypertension, OSA. Piedmont Weight Management 6-month program. Metformin GI intolerance; orlistat GI side effects. Approved dual indication per ADA 2024 guidelines.",
        "clinical_note": "53-year-old female, PPO/GA. BMI 37.2, T2DM, HTN, OSA. Piedmont 6-month weight program. Metformin GI intolerance; orlistat GI adverse effects. Semaglutide approved dual indication.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-0482",
        "member_id": "HUM-CO-9910472-01",
        "plan_type": "PPO",
        "state": "CO",
        "service_date": "2024-05-09",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 38.7, OSA (AHI 22), hyperlipidemia. UCHealth 6-month program. Orlistat failed 3 weeks GI intolerance. No T2DM but BMI ≥ 35 pathway. Approved.",
        "clinical_note": "44-year-old male, PPO/CO. BMI 38.7, OSA AHI 22, hyperlipidemia. UCHealth 6-month weight program. Orlistat intolerable GI effects. No diabetes, BMI ≥ 35 pathway. Approved.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-1511",
        "member_id": "HUM-FL-5523901-02",
        "plan_type": "HMO",
        "state": "FL",
        "service_date": "2024-12-04",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "DENIED",
        "outcome_rationale": "Denied. BMI 33.1, HTN only. Lifestyle documentation covers 6 months but submitted program is Noom app-based without documented licensed professional supervision — does not qualify as medically supervised program. Denied. Appeal rights communicated.",
        "clinical_note": "39-year-old female, HMO/FL. BMI 33.1, HTN. 6-month Noom app program submitted — app-based without medical supervision. Does not meet structured program criteria. Denied.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },

    {
        "claim_id": "PCL-2024-GLP1-0739",
        "member_id": "HUM-SC-6612038-02",
        "plan_type": "PPO",
        "state": "SC",
        "service_date": "2024-06-27",
        "clinical_area": "obesity",
        "primary_diagnosis_code": "E66.01",
        "primary_diagnosis_description": "Morbid (severe) obesity due to excess calories",
        "procedure_codes": [{"code": "S0148", "type": "HCPCS", "description": "Semaglutide injection 2.4 mg weekly"}],
        "billed_amount": 1349.02,
        "adjudication_outcome": "APPROVED",
        "outcome_rationale": "Approved. BMI 35.8, T2DM HbA1c 7.6%, HTN. MUSC Weight Management 6-month program. Metformin max dose, glipizide inadequate HbA1c response. No prior anti-obesity meds — BMI ≥ 35 step therapy exemption. Approved.",
        "clinical_note": "56-year-old male, PPO/SC. BMI 35.8, T2DM HbA1c 7.6%, HTN. MUSC 6-month weight program. Metformin + glipizide: HbA1c 7.6% not at goal. BMI ≥ 35 exempts from anti-obesity med step. Approved dual indication.",
        "clinical_embedding": None, "embedding_model": "voyage-3", "embedding_generated_at": None,
    },
]
