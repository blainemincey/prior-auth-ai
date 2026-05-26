# Demo Runbook — Operator Reference
## MongoDB Atlas Healthcare AI Demo — Live Webcast

This is the step-by-step operator document. Each entry maps a specific action
(command / click) to the script line to say at that moment.

---

## Pre-show checklist (15 minutes before go-live)

- [ ] `.env` is filled in and saved
- [ ] `python scripts/setup.py` has completed successfully (green output, "Setup complete")
- [ ] Smoke-test output shows expected top matches (see Expected Matches section below)
- [ ] `./start.sh --reset` run — backend on :8001, frontend on :5173, claims reset to PENDED (soft: embedding preserved, rationale cleared)
- [ ] To stop after the webcast: `./start.sh --stop`
- [ ] Browser open at **http://localhost:5173** (or LAN IP) — Demo Login screen or scenario cards visible, no errors
- [ ] Click **Sign in as Demo User** if the login gate is showing (cosmetic only; the session is remembered until Sign out)
- [ ] `curl http://localhost:8001/api/health` returns `{"status":"ok"}`
- [ ] Screen sharing is set to browser only (not terminal with credentials)
- [ ] Browser zoom set to ~110% so text is readable on stream
- [ ] If demo fails mid-run: refresh browser — per-scenario progress is preserved in `localStorage`, so you can resume where you left off without re-running prior steps

---

## Fallback plan (if live cluster has issues)

If Atlas is unreachable during the webcast:
- Show the demo script talking points verbally
- Open the README and walk through the architecture diagram
- The engineering story is in the narration, not just the clicks

---

## Expected top-match IDs

These should appear as the first results from Atlas Vector Search after running setup.
Verify before going live by checking the smoke-test output from `setup.py`.

**Scenario A — James Thornton, MRI Lumbar (CLM-2025-0001847)**
*Verified against live Atlas cluster — actual search scores shown*

| Position | Collection | ID | Score | Outcome |
|----------|-----------|-----|-------|---------|
| Policy #1 | policies | `POL-MRI-LUMBAR-2024-03` | 0.847 | Primary medical necessity criteria |
| Policy #2 | policies | `POL-RADICULOPATHY-2024-04` | 0.819 | Lumbar radiculopathy criteria |
| Policy #3 | policies | `POL-IMAGING-CONSERVATIVE-2024-01` | 0.783 | Conservative treatment requirements |
| Prior #1 | prior_claims | `PCL-2024-MRI-1103` | 0.863 | APPROVED — pended-then-approved, same PT doc gap |
| Prior #2 | prior_claims | `PCL-2024-MRI-0892` | 0.841 | APPROVED — L4-L5 radiculopathy, PPO/OH |
| Prior #3 | prior_claims | `PCL-2024-MRI-0671` | 0.823 | DENIED — no conservative therapy (contrast) |

**Scenario B — Eleanor Vasquez, Infliximab (CLM-2025-0003291)**
*Verified against live Atlas cluster — actual search scores shown*

| Position | Collection | ID | Score | Outcome |
|----------|-----------|-----|-------|---------|
| Policy #1 | policies | `POL-INFLIXIMAB-2024-06` | 0.863 | Infliximab coverage + step therapy ref |
| Policy #2 | policies | `POL-BIOLOGIC-RA-2024-07` | 0.811 | Biologic DMARD RA step therapy requirements |
| Policy #3 | policies | `POL-IL6-INHIBITOR-2024-01` | 0.755 | Related biologic criteria |
| Prior #1 | prior_claims | `PCL-2024-BIO-2244` | 0.879 | APPROVED — infliximab continuation, PPO/TX |
| Prior #2 | prior_claims | `PCL-2024-BIO-1891` | 0.870 | APPROVED — identical step therapy pathway |
| Prior #3 | prior_claims | `PCL-2023-BIO-3102` | 0.840 | APPROVED — biologic escalation after adalimumab |

*Hybrid mode (`$rankFusion`) — the prior-claims #3 slot changes:*

| Position | Collection | ID | Ranks | Outcome |
|----------|-----------|-----|-------|---------|
| Prior #3 (hybrid) | prior_claims | `PCL-2024-BIO-3580` | vec #4 / lex #1 | APPROVED — Crohn's, lifted by lexical sub-pipeline; `PCL-2023-BIO-3102` is displaced out of the top 3 |

**Scenario C — Patricia Reeves, Semaglutide/Wegovy (CLM-2025-0007734)**
*Verified against live Atlas cluster — actual search scores shown*

| Position | Collection | ID | Score | Outcome |
|----------|-----------|-----|-------|---------|
| Policy #1 | policies | `POL-GLP1-OBESITY-2024-08` | 0.876 | Primary GLP-1 obesity PA criteria (BMI thresholds, step therapy, 6-month program) |
| Policy #2 | policies | `POL-GLP1-T2DM-2024-10` | 0.834 | GLP-1 for T2DM — dual-indication step therapy |
| Policy #3 | policies | `POL-ANTIOBESITY-STEP-2024-12` | 0.832 | Anti-obesity step therapy framework |
| Prior #1 | prior_claims | `PCL-2024-GLP1-1456` | 0.850 | APPROVED — BMI 38.1, T2DM+HTN+OSA, PPO/FL, 6-month Tampa General program |
| Prior #2 | prior_claims | `PCL-2024-GLP1-0312` | 0.846 | DENIED — BMI 28.9 below threshold, no qualifying program (contrast) |
| Prior #3 | prior_claims | `PCL-2024-GLP1-0644` | 0.792 | DENIED — BMI 31.2, T2DM, missing 6-month program doc |

---

## Step-by-step run sequence

### Opening (before clicking anything)

**Action:** If the **Demo Login** screen is showing, click **Sign in as Demo User** (the gate is cosmetic — no real authentication). The "Demo User" indicator and Sign-out button then appear in the header. Screen shows the scenario selector with three cards — no scenario selected yet.

**Say:**
> "Major healthcare payers already rely on MongoDB for mission-critical systems. The next question is whether AI at a payer of that scale will require another data layer, or whether the same platform can serve as both the operational system and the retrieval foundation for AI workloads. Today we are going to walk one synthetic pended claim through that architecture end to end using Voyage embeddings and Atlas Vector Search inside the same platform."

Brief architecture frame (30 sec, per script). Then select the scenario.

---

### STEP 1 — Operational Record

**Action:** Click **Scenario A** (or B / C for subsequent runs).

**What happens:** The claim record loads below the scenario cards. The step indicator shows Step 1 active. Scroll slowly so the audience sees the full document structure.

**Say (pointing at the document):**
> "This is the pended claim as it actually lives in MongoDB. Notice what's here: a realistic member ID, an NPI, ICD-10 and CPT codes you'd see in a real adjudication system, place-of-service codes, pend reason codes — and right alongside all of that structured data, unstructured clinical notes."

**Key fields to call out:**
- `adjudication_status: PENDED` (yellow badge)
- `pend_reason_code: PA-MN-001` (Scenario A), `MN-DRUG-HCB-002` (Scenario B), or `PA-OBE-GLP1-001` (Scenario C)
- `clinical_notes` — scroll to show it's substantive clinical text
- `clinical_embedding: null` — "Not embedded yet. That's about to change."
- `ai_rationale: null` — "No AI output yet. This is where we'll write the recommendation."

**Pause point:** Give the audience a moment to read the claim structure before moving on.

---

### STEP 2 — Voyage Embedding

**Action:** Click **Generate Embedding**.

**What happens:** Button shows spinner ("Embedding..."), backend calls Voyage AI voyage-3, stores vector in MongoDB, returns stats. UI shows: model name, 1,024 dimensions, timestamp, first 8 vector values. The claim record updates — `clinical_embedding` changes from `null` to `<vector: 1024 dims>`.

**Say (while spinner is active):**
> "Atlas is now generating a Voyage AI embedding for these clinical notes..."

**Say (when result appears):**
> "That vector was written directly into the same MongoDB document. The embedding now lives in the same record as the member ID, the diagnosis codes, and the clinical notes."

**Key callouts:**
- Point to "Dimensions: 1,024" — "voyage-3, general-purpose, 1,024-dimensional"
- Point to "Storage: MongoDB document" — "not a separate system"
- Point to the vector preview — "The semantic fingerprint of the clinical notes"

**Say the synchronization tax line:**
> "In a typical AI pipeline, you have your operational database here, a text extraction step here, an embedding model call here, a vector store here, and then retrieval that has to be reconciled back to the operational record. That's the synchronization tax — glue code, drift risk, a whole category of operational complexity that exists solely to move data between systems. The Atlas architecture I'm showing you today eliminates that category."

---

### STEP 3 — Atlas Vector Search

**Action:** Review filters (leave plan_type and state pre-set from the claim), then click **Run Vector Search**.

**Before clicking — say:**
> "Look at these filter controls. We have hard filters for plan type, state, and optionally adjudication outcome. These aren't hints to the semantic model. These are enforced constraints. Atlas Vector Search finds the most semantically relevant documents first, then applies the filter."

**Note on clinical_area filter:** A `clinical_area` filter is also applied automatically — inferred from the claim's procedure codes (CPT codes → `imaging`; HCPCS J codes → `biologic`; HCPCS S codes → `obesity`). This prevents cross-domain results. It is not shown in the user filter controls because the audience didn't set it; the UI displays it separately as an "auto-scoped" badge in the Retrieved Context panel.

**Action:** Click **Run Vector Search**.

**What happens:** Backend runs `$vectorSearch` aggregation with filters, returns top 3 policies and top 3 prior claims. Loading spinner shows during search. The `$vectorSearch` query preview at the bottom of the panel shows all three user-set filter values updating live as you change the dropdowns.

**Say (while loading):**
> "Atlas Vector Search is finding documents by semantic similarity — not keyword match, not ICD-10 code lookup — by the meaning of the clinical situation."

**Optional bonus — Hybrid retrieval via `$rankFusion` (Scenario B only):**

> ⚠ **Run this beat on Scenario B only.** The Crohn's contrast prior (`PCL-2024-BIO-3580`) that lights up the `vec #4 / lex #1` chip pair is only wired into Scenario B (Eleanor Vasquez / infliximab). On Scenarios A and C the hybrid toggle works, but there is no rank disagreement to point at. Skip this optional beat for A and C.

After the vector search completes, switch the **Retrieval mode** segmented control above the filters from `$vectorSearch` to `$rankFusion (hybrid)` and click **Run Hybrid Search**. The backend now runs a `$rankFusion` aggregation combining a vector sub-pipeline and a `$search` (lexical) sub-pipeline with the same hard filters applied to both. Point at the `vec #N` / `lex #M` chips on each result card — they reveal each result's rank inside each pipeline (or `—` if that pipeline didn't surface the document). Cluster requirement: MongoDB 8.1+.

**The Scenario B prior-claims demo moment:** the third row in hybrid mode is `PCL-2024-BIO-3580` (Crohn's disease, not RA). In pure `$vectorSearch` mode this case falls to rank #4 because the Crohn's narrative is semantically distant from Eleanor Vasquez's RA notes. In hybrid mode the `vec #4 / lex #1` chip pair makes the disagreement visible — the lexical sub-pipeline found this case via shared operational tokens (`Remicade`, `biosimilar exclusion clause`, `5 mg/kg every 8 weeks`, `MN-DRUG-HCB-002`, `POL-INFLIXIMAB-2024-06`) and `$rankFusion` lifted it into the top 3. Point at that row when you say "this is the case lexical surfaced that vector smoothed over."

---

### STEP 4 — Retrieved Context

**Action:** The browser switches to the Retrieved Context tab automatically after the search completes.

**What to point at:**
- **Rank badge and similarity score** on the left of each card (e.g. `#1 / 0.863`) — "Higher score means more semantically similar to this claim's clinical notes"
- **Green ✓ filter pills** on each card — these light up when the card's field value matched a hard filter you set. For example, if you filtered on `plan_type: PPO`, any result with `plan_type: PPO` shows a green ✓ pill.
- **Blue "auto-scoped" badge** in the section header — `clinical_area: imaging` (A), `clinical_area: biologic` (B), or `clinical_area: obesity` (C). Applied automatically from the claim's procedure codes, not by the user.
- Policy #1: `POL-MRI-LUMBAR-2024-03` (A) / `POL-INFLIXIMAB-2024-06` (B) / `POL-GLP1-OBESITY-2024-08` (C)
- Prior #1: `PCL-2024-MRI-1103` (A) / `PCL-2024-BIO-2244` (B) / `PCL-2024-GLP1-1456` (C)
- Prior #3 (Scenario A): `PCL-2024-MRI-0671` — DENIED — "This is a contrast case showing what a denial looks like for the same procedure code with different clinical circumstances"
- Prior #2 (Scenario C): `PCL-2024-GLP1-0312` — DENIED — BMI 28.9, below threshold — "Same drug, same diagnosis code, but different outcome because the eligibility criteria weren't met"

**Say:**
> "Look at what came back. The top policy match is the specific lumbar spine MRI medical necessity criteria. The second is the conservative treatment requirements. And the prior claim results include an almost identical approved case — same diagnosis, same plan type, same state — plus a case that was initially pended for incomplete PT documentation and then approved. Sound familiar?"

**Point at the filter pills:**
> "The green checkmarks on each card tell you exactly which fields matched the filters you set. You can see at a glance that these results are from the same plan type and state — that's not coincidence, that's Atlas Vector Search enforcing your constraints before returning results."

**Point at the blue auto-scope badge:**
> "The blue badge shows a filter the system set automatically — it inferred from the procedure code that this is an imaging claim and scoped the search accordingly. That's why you're seeing MRI policies and not biologic or obesity policies." (Adjust per scenario: biologic for Scenario B, obesity for Scenario C.)

**Optional — for engineering-leaning audiences:** Expand the **`$vectorSearch`** toggle above the result cards. It reveals the exact aggregation pipeline MongoDB executed (one tab for `policies`, one for `prior_claims`), including the index name, `numCandidates`, `limit`, the `filter` object, and the `$project` stage. The 1024-dim query vector is shown as a placeholder so the JSON is readable. Useful when an engineer in the audience asks "what query is actually running?"

**Key point:**
> "The value here is not that AI generated words. The value is that Atlas Vector Search found the right context. The rationale we're about to generate is only as good as what it gets to work with."

---

### STEP 5 — Rationale + Write-back

**Action:** Click **Generate Rationale**.

**What happens:** The backend assembles a structured, reviewer-voice recommendation directly from the retrieved policy criteria text and prior case outcome rationales — no external LLM API call is made. The result is written back to MongoDB (updates `ai_rationale`, `ai_determination`, `ai_supporting_policies`, `ai_comparable_cases`, `adjudication_status`, `status_history`). UI shows: determination badge, supporting IDs, full rationale text. The claim summary bar at the top updates immediately.

**Say (while loading ~1-2 seconds):**
> "The backend is assembling a reviewer-voice recommendation grounded in what Atlas Vector Search just retrieved — the actual policy criteria text and the outcome rationales from those prior cases. No additional API call. The retrieved context is the input."

**Say (when determination appears):**
> "Read the determination. It references specific clinical findings from this chart. It names the policy and the specific criterion. It cites prior claim IDs as analogs."

**Point at the claim record updating:**
> "Watch the claim record at the top of the page. The `adjudication_status` just changed from PENDED to READY_FOR_REVIEW. The `ai_rationale` field is populated. The supporting policy IDs and comparable case IDs are written. This is the same MongoDB document we started with, updated in place."

**Architecture interlude (natural, not a pause):**
> "A question from an engineering audience: does running vector search on the same cluster impact transactional performance? The honest answer is it can if you don't isolate the workloads. Atlas addresses this with Search Nodes — dedicated infrastructure for vector search that scales independently from the core database nodes."

---

### CLOSING

**Action:** Scroll to show the full claim record — the updated fields highlighted in green.

**Say (recommended close, close to verbatim):**
> "If this pattern holds, the takeaway is simple: MongoDB is not just where a payer stores operational data. It is a practical way to keep operational data, embeddings, retrieval, and AI output close together in one architecture that engineering teams can reason about, scale, and standardize."

> "We started with a pended claim. The clinical notes became a Voyage embedding, stored in the same document. Atlas Vector Search retrieved the right policies and prior analogs using semantic similarity with hard metadata filters. The backend assembled a grounded, reviewer-voice recommendation directly from that retrieved context. And that recommendation was written back into the original record — status updated, rationale stored, audit trail intact — without the data ever leaving the platform."

> "That's the architecture. One platform. Fewer moving parts."

---

## Resetting between runs

There are two reset modes. Choose based on whether you want Step 2 to make a live
Voyage AI call or return instantly from the cached embedding.

### Soft reset (recommended for most repeat runs)

Clears the AI rationale and adjudication status. **Preserves the Voyage AI embedding**
stored in MongoDB. When the audience clicks Step 2, the backend detects the existing
embedding and returns it immediately — no Voyage API call, no rate-limit risk.
The UI looks identical to a fresh run.

```bash
./start.sh --reset          # stop services, reset, restart
```

Or without restarting the services:

```bash
cd backend && source .venv/bin/activate && cd ..
python scripts/reset_demo.py
```

### Hard reset (when you need a live Voyage API call in Step 2)

Clears everything including the embedding. Step 2 will make a real Voyage AI call.
Use this for the very first run with a new audience, or when you explicitly want to
demonstrate the live embedding call. Be mindful of free-tier rate limits if running
this more than a few times in quick succession.

```bash
./start.sh --reset-hard          # stop services, full reset, restart
```

Or without restarting:

```bash
python scripts/reset_demo.py --hard
```

After either reset, refresh the browser — all three claims will show `PENDED` with
`ai_rationale: null`. With a soft reset, `clinical_embedding` shows `<vector:1024 dims>`;
with a hard reset it shows `null`.

---

## Running Scenario B after Scenario A

1. Click **Scenario B** in the scenario selector at the top of the page
2. The infliximab claim loads. Scenario A's progress (claim, embedding, search results, rationale) is preserved in the background — clicking back to Scenario A will restore it on whatever tab you left, without re-running any steps.
3. Run through Steps 1–5 for Scenario B — the architecture is identical, the clinical situation is different
4. Key differences to call out in Scenario B:
   - `total_billed_amount: $18,420` — much higher-cost claim
   - `pend_reason_code: MN-DRUG-HCB-002` — high-cost biologic threshold
   - Procedure is HCPCS J1745 (not CPT) — pharmacy benefit management, not imaging
   - Step therapy history in the clinical notes is extensive (5 drug trials)
   - Top policy match will be `POL-INFLIXIMAB-2024-06` — infliximab coverage + step therapy ref
   - Prior claims will show Texas PPO biologic approvals with similar step therapy history
   - Determination will be **APPROVE** (step therapy thoroughly documented)
5. **Optional hybrid-mode beat (Scenario B is the best scenario for this):** after running pure vector search, toggle Retrieval mode to **`$rankFusion (hybrid)`** and re-run. Prior #3 becomes `PCL-2024-BIO-3580` (Crohn's, not RA) with `vec #4 / lex #1` chips — the engineered "lexical surfaced what vector smoothed over" moment. See Step 3 of the run sequence above for the exact talking point.

---

## Running Scenario C after Scenario B

1. Click **Scenario C** in the scenario selector at the top of the page
2. The GLP-1 semaglutide claim loads. Earlier scenarios remain preserved — switch back at any time to re-show prior results.
3. Run through Steps 1–5 for Scenario C

**Key differences to call out in Scenario C:**
- Member: Patricia A. Reeves, 52F, PPO/FL
- `pend_reason_code: PA-OBE-GLP1-001` — GLP-1 lifestyle documentation gap
- Procedure is HCPCS S0148 — semaglutide (Wegovy) 2.4 mg/wk, $1,349/month
- Auto-inferred `clinical_area: obesity` (S-code inference) — blue badge in Step 4
- Clinical notes document BMI 38.2, T2DM (HbA1c 7.8%), hypertension, sleep apnea, and prior anti-obesity medication failures (phentermine/topiramate, orlistat), but **no formal 6-month supervised weight management program**
- Top policy match: `POL-GLP1-OBESITY-2024-08` (0.876) — the PA criteria policy; policy #2 is the T2DM GLP-1 policy (dual-indication), policy #3 is the step therapy framework
- Prior #1: `PCL-2024-GLP1-1456` (0.850) — APPROVED, nearly identical presentation (BMI 38.1, same comorbidities, PPO/FL) but with a complete 6-month Tampa General program on file
- Prior #2: `PCL-2024-GLP1-0312` (0.846) — DENIED, BMI 28.9, below threshold — useful contrast to show the eligibility floor enforced
- Prior #3: `PCL-2024-GLP1-0644` (0.792) — DENIED, BMI 31.2 with T2DM, same missing program gap as the pending case
- Determination will be **ADDITIONAL INFORMATION REQUIRED** — member qualifies clinically but the lifestyle program documentation is missing
- Step 5 rationale will cite both the obesity policy (BMI threshold met, step therapy documented) and the outstanding documentation gap (6-month supervised program)

**Talking points for Scenario C:**
> "This is the fastest-growing category of prior auth volume right now — GLP-1 weight management drugs. The member clearly qualifies clinically: BMI 38, three comorbidities, two prior medication failures. But there's a specific documentation gap: the plan requires a formal six-month medically supervised program, and the notes don't show one. Atlas Vector Search found the analogous approved case, which had that documentation. That's the context the reviewer needs to issue the right determination."

---

## Emergency recovery steps

**Scenario won't load:**
- Refresh the browser
- If still empty: `curl http://localhost:8001/api/claims/A/record` — should return JSON
- If 404: backend is not reaching Atlas — check `.env` connection string

**Embedding fails:**
- Check Voyage AI key in `.env`: `VOYAGE_API_KEY` must be set
- Error appears in the UI as a red error bar

**Search returns no results:**
- The vector search index may not be READY yet
- Wait 2 minutes and retry
- If still empty, the index may have been dropped — re-run `python scripts/setup.py`

**Rationale generation fails:**
- Rationale is template-based (no external API) — failures are backend errors, not key issues
- Check backend logs for the Python traceback
- Retry — if the search results are already shown, describe the rationale verbally from the script

**Wrong top matches surface:**
- This can happen if filters are too restrictive (try removing the state filter)
- Or if another claim in the corpus accidentally outranks the engineered anchor
- The engineered anchors are designed to win, but verify before the webcast with the smoke test
