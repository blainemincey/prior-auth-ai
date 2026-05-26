# MongoDB Atlas — Healthcare AI Demo

**Architectural thesis:** MongoDB Atlas serves as both the operational system of record and
the retrieval foundation for AI workloads. Operational data, Voyage AI embeddings, Atlas
Vector Search retrieval, and generated AI output all anchored in one platform — fewer
moving parts, no separate vector store to keep in sync.

---

## What this demo shows

A single synthetic pended healthcare claim walks through a five-step AI-enrichment loop,
entirely inside MongoDB Atlas:

| Step | What happens | MongoDB role |
|------|-------------|-------------|
| 1 | Display the operational claim record | Operational database |
| 2 | Generate a Voyage AI embedding from clinical notes | Stores vector in same document |
| 3 | Run Atlas Vector Search with metadata filters | Vector + filter index |
| 4 | Display retrieved policies and prior analogs | Context from the same cluster |
| 5 | Generate template-driven rationale; write back to claim | AI output written to same record |

Three engineered demo scenarios:
- **Scenario A** — Lumbar Spine MRI prior authorization (CPT 72148), pended for medical necessity
- **Scenario B** — Infliximab infusion (HCPCS J1745), pended for high-cost biologic / step-therapy review
- **Scenario C** — Semaglutide (Wegovy) 2.4 mg/wk (HCPCS S0148), pended for lifestyle program documentation

### Vector Search filter behavior

Step 3 supports three user-set hard filters (enforced constraints, not hints):

| Filter | Source | Effect |
|--------|--------|--------|
| `plan_type` | Pre-seeded from claim; editable | Restricts prior claims and (indirectly) policy applicability |
| `state` | Pre-seeded from claim; editable | Restricts prior claims by member state |
| `adjudication_outcome` | Empty by default; user-selectable | Restrict prior claims to APPROVED or DENIED only |

One additional filter is **auto-inferred** from the claim's procedure codes and applied
silently in the background:

| Filter | How it's set | Why |
|--------|-------------|-----|
| `clinical_area` | CPT codes → `imaging`; HCPCS J codes → `biologic`; HCPCS S codes → `obesity` | Prevents cross-domain results (e.g. biologic policies surfacing for an imaging claim) |

The Retrieved Context panel distinguishes these clearly: user hard filters appear as green ✓
pills on each result card; the auto-inferred scope appears as a separate blue "auto" badge.
The active filter count in the header reflects only user-set filters.

### Inspect the actual `$vectorSearch` pipeline

The Retrieved Context panel includes an expandable **`$vectorSearch`** toggle that shows
the exact aggregation pipeline MongoDB executed for both the `policies` and `prior_claims`
collections. Useful for engineering-leaning audiences who want to see the query shape
beyond the rendered results.

The 1024-dimension query vector is rendered as a placeholder
(`<1024-dim embedding from step 2>`) so the JSON stays readable; everything else — index
name, `numCandidates`, `limit`, the `filter` object, and the `$project` stage — is shown
verbatim as MongoDB received it.

### Hybrid retrieval via `$rankFusion`

Step 3 includes a **retrieval mode** toggle: `$vectorSearch` (semantic only, the default)
or `$rankFusion (hybrid)` — Atlas's native hybrid-search stage that fuses a `$vectorSearch`
sub-pipeline with a `$search` (lexical / text) sub-pipeline using reciprocal rank fusion.
Same data, same platform, no separate search engine.

When hybrid mode is active, each result card shows the rank it received from each input
pipeline as a small `vec #N` / `lex #M` chip pair — a missing rank shows as `—`, meaning
that pipeline didn't surface the document at all. The pipeline viewer above the cards
expands to show the full `$rankFusion` JSON.

Requirements:
- MongoDB 8.1+ on the Atlas cluster (the `$rankFusion` stage was added in 8.1)
- Atlas Search indexes alongside the Vector Search indexes —
  `policy_search_index` and `prior_claims_search_index`, both created automatically
  by `scripts/setup.py`

Lexical sub-pipeline field mappings:

| Collection | `string` (free-text) | `token` (exact-match filter parity) |
|------------|----------------------|-------------------------------------|
| `policies` | `title`, `criteria_text`, `subcategory` | `clinical_area` |
| `prior_claims` | `clinical_note`, `outcome_rationale`, `primary_diagnosis_description`, `procedure_codes.description` | `plan_type`, `state`, `clinical_area`, `adjudication_outcome`, `procedure_codes.code` |

Both sub-pipelines apply the same hard filters so the comparison stays apples-to-apples —
constraints are not relaxed when crossing retrieval styles.

To verify cluster support after a cluster move or version change:

```bash
python scripts/check_rankfusion_support.py    # prints server version, runs a tiny $rankFusion
python scripts/test_hybrid_search.py          # full hybrid smoke test
```

### Rationale generation

Step 5 uses a **template-driven approach** — no external LLM API call is made. The rationale
is assembled from the retrieved policy criteria text and prior case outcome rationales, then
structured into a reviewer-voice recommendation. This keeps the demo self-contained and
eliminates latency and API key requirements beyond Voyage AI and MongoDB Atlas.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.9+ | Backend runtime |
| Node.js 18+ | Frontend build |
| MongoDB Atlas cluster (M10 or higher) | Free tier does NOT support Atlas Vector Search |
| Voyage AI API key | https://dash.voyageai.com/api-keys |

---

## Setup (from a bare cluster)

### 1. Clone and configure

```bash
git clone <repo-url>
cd healthcaredemo

cp .env.example .env
# Edit .env — fill in MONGODB_URI and VOYAGE_API_KEY
```

Your `.env` should look like:
```
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
VOYAGE_API_KEY=pa-xxxxx
```

### 2. Install Python dependencies

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Run setup (creates all Atlas infrastructure + seeds data)

```bash
cd backend && source .venv/bin/activate && cd ..
python scripts/setup.py
```

This script (idempotent — safe to re-run):
- Creates the `healthcare_demo` database and three collections
- Creates Atlas Vector Search indexes via the MongoDB driver
- Seeds 30 coverage policies with Voyage AI embeddings
- Seeds 71 prior adjudicated claims with Voyage AI embeddings
- Inserts the three demo claims with embeddings
- Waits for indexes to reach READY state
- Runs a smoke-test vector search and prints the top matches

**Expected runtime:** 3–6 minutes (most time is waiting for indexes to initialize).

---

## ⚠ Atlas UI Steps Required

**Atlas Vector Search index creation is submitted programmatically**, but Atlas takes
1–5 minutes to build and bring indexes to READY state. The setup script waits for this
automatically. No UI clicks are required for index creation.

**If the setup script times out** waiting for indexes (rare on first cluster creation):
1. Go to Atlas UI → your cluster → **Search** tab
2. Confirm the three indexes (`policy_vector_index`, `prior_claims_vector_index`,
   `claims_vector_index`) show status **Active**
3. Re-run `python scripts/setup.py` — it will skip existing indexes and data

---

## Launch the demo

```bash
./start.sh
```

Open **http://localhost:5173** in a browser. If running on a remote host, use its LAN IP
instead (e.g. `http://<your-host-ip>:5173`) — Vite binds to all interfaces by default.

On first load you'll see a **Demo Login** gate — click **Sign in as Demo User** to enter.
This is cosmetic (no real authentication); the session is remembered in `localStorage`
until you click **Sign out** in the header.

Per-scenario progress (claim, embedding, search results, rationale, active tab) is also
persisted in `localStorage`, so a browser refresh or switching between scenarios will
not lose your work. **Reset Demo** in the header clears the persisted progress and
restores all claims to `PENDED` in MongoDB; **Sign out** clears everything client-side.

The two-command sequence from a clean clone:
```bash
python scripts/setup.py   # ~4 min first time
./start.sh                # starts both services
```

### start.sh command reference

| Command | Effect |
|---------|--------|
| `./start.sh` | Start backend + frontend |
| `./start.sh --reset` | Soft reset (keep embedding, clear rationale), then start |
| `./start.sh --reset-hard` | Full reset (clear everything), then start |
| `./start.sh --stop` | Stop running services |

Running `./start.sh` when the services are already up stops the previous instance
automatically before starting fresh — it can be used as a restart.

### Resetting between runs

After stepping through the demo, claim records are fully enriched (embedding stored,
rationale written, status changed to `READY_FOR_REVIEW`). Pass a reset flag to `start.sh`
to clean up before the next run.

**Soft reset (default, recommended)** — clears only the AI output and status fields.
The Voyage AI embedding is preserved in MongoDB, so clicking Step 2 returns the stored
result without making another API call. Eliminates rate-limit risk on repeat runs.

```bash
./start.sh --reset
```

**Hard reset** — clears everything including the embedding. Use this when you want a true
first-run experience where Step 2 makes a live Voyage AI call.

```bash
./start.sh --reset-hard
```

If the services are already running and you only want to reset without restarting:

```bash
cd backend && source .venv/bin/activate && cd ..
python scripts/reset_demo.py           # soft
python scripts/reset_demo.py --hard    # hard
```

Then refresh the browser — no service restart needed.

---

## Data architecture

```
healthcare_demo (database)
├── claims          — operational claim records + embeddings + written-back rationale
├── policies        — 30 coverage policies with Voyage embeddings
└── prior_claims    — 71 prior adjudicated claims with Voyage embeddings

Atlas Vector Search indexes
├── policy_vector_index      → policies.clinical_embedding (1024 dims)
├── prior_claims_vector_index → prior_claims.clinical_embedding (1024 dims)
└── claims_vector_index      → claims.clinical_embedding (1024 dims)
```

All three indexes live on the same Atlas cluster as the operational data.

---

## Engineered demo top-match IDs

These are the intended #1 results from Atlas Vector Search for each scenario.
Verify them from the setup script smoke-test output.

**Scenario A (MRI lumbar — James Thornton):** *Verified live*

| Rank | Type | ID | Score | Outcome |
|------|------|----|-------|---------|
| 1 | Policy | `POL-MRI-LUMBAR-2024-03` | 0.847 | Primary medical necessity criteria |
| 2 | Policy | `POL-RADICULOPATHY-2024-04` | 0.819 | Lumbar radiculopathy criteria |
| 3 | Policy | `POL-IMAGING-CONSERVATIVE-2024-01` | 0.783 | Conservative treatment requirements |
| 1 | Prior claim | `PCL-2024-MRI-1103` | 0.863 | APPROVED — pended-then-approved, same PT doc gap |
| 2 | Prior claim | `PCL-2024-MRI-0892` | 0.841 | APPROVED — nearly identical presentation |
| 3 | Prior claim | `PCL-2024-MRI-0671` | 0.823 | DENIED — contrast case, no conservative therapy |

**Scenario B (Infliximab — Eleanor Vasquez):** *Verified live*

| Rank | Type | ID | Score | Outcome |
|------|------|----|-------|---------|
| 1 | Policy | `POL-INFLIXIMAB-2024-06` | 0.863 | Infliximab coverage + step therapy ref |
| 2 | Policy | `POL-BIOLOGIC-RA-2024-07` | 0.811 | Biologic DMARD RA step therapy requirements |
| 3 | Policy | `POL-IL6-INHIBITOR-2024-01` | 0.755 | Related biologic criteria |
| 1 | Prior claim | `PCL-2024-BIO-2244` | 0.879 | APPROVED — infliximab continuation, PPO/TX |
| 2 | Prior claim | `PCL-2024-BIO-1891` | 0.870 | APPROVED — identical step therapy pathway |
| 3 | Prior claim | `PCL-2023-BIO-3102` | 0.840 | APPROVED — biologic escalation after adalimumab |

In hybrid mode (`$rankFusion`), prior #3 changes — `PCL-2024-BIO-3580` (Crohn's,
APPROVED) is lifted into the top 3 by the lexical sub-pipeline (vec #4 / lex #1)
on the strength of shared operational tokens (`Remicade`, `biosimilar exclusion
clause`, `5 mg/kg every 8 weeks`, `MN-DRUG-HCB-002`, `POL-INFLIXIMAB-2024-06`).
`PCL-2023-BIO-3102` drops out of the top 3. This is the engineered "lexical
surfaced what vector smoothed over" moment for the hybrid-mode demonstration.

**Scenario C (Semaglutide — Patricia Reeves):** *Verified live*

| Rank | Type | ID | Score | Outcome |
|------|------|----|-------|---------|
| 1 | Policy | `POL-GLP1-OBESITY-2024-08` | 0.876 | Primary GLP-1/obesity PA criteria |
| 2 | Policy | `POL-GLP1-T2DM-2024-10` | 0.834 | GLP-1 for T2DM — dual-indication step therapy |
| 3 | Policy | `POL-ANTIOBESITY-STEP-2024-12` | 0.832 | Anti-obesity step therapy framework |
| 1 | Prior claim | `PCL-2024-GLP1-1456` | 0.850 | APPROVED — BMI 38.1, T2DM+HTN+OSA, PPO/FL, 6-month Tampa General program |
| 2 | Prior claim | `PCL-2024-GLP1-0312` | 0.846 | DENIED — BMI 28.9 below threshold, no qualifying program (contrast) |
| 3 | Prior claim | `PCL-2024-GLP1-0644` | 0.792 | DENIED — BMI 31.2, T2DM, missing 6-month program doc |

---

## FAQ

**Is this production-ready or a demo?**
The architecture pattern is production-grade — Atlas Vector Search, hybrid `$rankFusion`,
and Search Nodes are all generally available Atlas features. The demo runs on a real
Atlas cluster with real Voyage AI embeddings. The data is synthetic; the plumbing is
what you'd actually build.

**How does this scale?**
The operational cluster and vector search workloads scale independently on Atlas via
Search Nodes — dedicated infrastructure for vector workloads provisioned alongside the
OLTP cluster. You're not trading off operational performance for search performance.

**What about HIPAA and PHI?**
MongoDB Atlas offers HIPAA-eligible configurations. In this architecture, embeddings,
retrieval, and AI output all stay inside the Atlas cluster — no PHI leaves the
environment. The one boundary to design around is the embedding API call; that can be
a private endpoint or an on-premise model depending on your compliance posture.

**Can a different embedding model be substituted for Voyage?**
Yes. Embedding dimension and model are configuration. Voyage-3 is a strong general-purpose
model for clinical text; the architecture itself is model-agnostic. Swap the model,
rebuild the embeddings, and the Vector Search index adapts.

**Why no LLM for the rationale?**
Deliberate choice. The rationale is assembled from retrieved policy text and prior-case
outcomes via deterministic templates — no model call, no hallucination surface, every
citation traceable to a real document. The retrieval layer (Voyage embeddings + Atlas
Vector Search + `$rankFusion`) is where the AI value sits; adding a generative model
on top would obscure the architectural point rather than reinforce it.

---

## Troubleshooting

**`setup.py` fails with auth error:**
- Check `MONGODB_URI` in `.env` — ensure username/password are correct
- Ensure your Atlas IP access list includes your current IP (Atlas UI → Network Access)

**"collection not found" or search returns no results:**
- The vector search index may still be building — wait 2–3 more minutes and retry
- Run `python scripts/setup.py` again — it's idempotent

**Frontend can't reach backend:**
- Confirm backend is running on port 8001: `curl http://localhost:8001/api/health`
- Check `CORS_ORIGIN` in `.env` matches your frontend URL

**Voyage AI rate limits:**
- `setup.py` embeds ~104 documents in batches of 64 with a 1-second pause between
  batches — this is already handled and should not 429 on free-tier keys.
- During the demo, Step 2 calls Voyage AI only on the first run per claim. Subsequent
  runs (after `--reset`) return the stored embedding with no API call.
- If you do hit a 429 during setup, re-run `python scripts/setup.py` — it skips
  documents that are already embedded.
