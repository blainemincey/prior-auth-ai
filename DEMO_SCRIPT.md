# Demo Script — MongoDB Atlas Healthcare AI Demo
## Spoken Narration for Live Webcast

---

### RECOMMENDED OPENING (use close to verbatim)

> "Major healthcare payers already rely on MongoDB for mission-critical systems. The next question is whether AI at a payer of that scale will require another data layer — or whether the same platform can serve as both the operational system and the retrieval foundation for AI workloads. Today we are going to walk one synthetic pended healthcare claim through that architecture end to end, using Voyage embeddings and Atlas Vector Search inside the same platform."

---

### [BEFORE CLICKING ANYTHING] — Architecture framing (30 sec)

> "What you're looking at is a live connection to a MongoDB Atlas cluster. This is the same kind of cluster an engineering team at a major healthcare payer would run for operational systems — claims adjudication, member records, authorization workflows. The question we're answering today is: does AI enrichment force that data to leave this platform, or can the platform do both jobs?"

> "We have three demo scenarios loaded. Scenario A is a prior authorization request for an MRI — a lumbar spine study that's been pended for medical-necessity review. Scenario B is a high-cost biologic infusion claim — infliximab for rheumatoid arthritis — pended because it triggered the plan's high-cost drug threshold. Scenario C is a GLP-1 weight management drug — semaglutide — pended for a lifestyle program documentation gap. Same architecture, three very different clinical situations."

---

### STEP 1 — Operational Record

**[Click Scenario A or B]**

> "This is the pended claim as it actually lives in MongoDB. Notice what's here: a realistic member ID, an NPI, ICD-10 and CPT codes you'd see in a real adjudication system, place-of-service codes, pend reason codes — and right alongside all of that structured data, unstructured clinical notes. The utilization management nurse's review, the treatment history, the clinical findings."

> "This is the kind of document the engineering teams actually own. Structured and unstructured data already live together in one place. The question is whether AI enrichment forces this record to leave the platform."

> "Notice the `clinical_embedding` field is null. The `ai_rationale` field is null. That's the state of this claim right now: pended, waiting for a reviewer. We're going to walk it through the whole loop."

---

### STEP 2 — Voyage Embeddings

**[Click "Generate Embedding"]**

> "Atlas is now generating a Voyage AI embedding for these clinical notes. The model is voyage-3 — Voyage AI's general-purpose embedding model, 1,024 dimensions. What I want you to notice is what just happened: that vector was written directly into the same MongoDB document. The embedding now lives in the same record as the member ID, the diagnosis codes, and the clinical notes."

> "There's no separate vector store. No pipeline that extracts text, ships it to a different system, and tries to keep things in sync. If a reviewer edits the clinical notes tomorrow and the embedding needs to be regenerated — that's one write to one document, in one platform."

> "Let me put a name on what that alternative looks like. In a typical AI pipeline, you have your operational database here, a text extraction step here, an embedding model call here, a vector store here, and then retrieval that has to be reconciled back to the operational record. That's what I'd call the synchronization tax — glue code, drift risk, a whole category of operational complexity that exists solely to move data between systems. The Atlas architecture I'm showing you today eliminates that category."

> "You can see the vector preview — the first 8 of 1,024 floating-point values. This is the semantic fingerprint of the clinical notes, living in the same place as the note itself."

---

### STEP 3 — Atlas Vector Search

**[Review filters and click "Run Vector Search"]**

> "Now this is where it gets interesting. We're about to query by meaning — not by keyword, not by an exact code match — by the semantic content of this clinical situation. But look at these filter controls."

> "We have hard filters for plan type and state. These aren't hints to the semantic model. These are enforced constraints. Atlas Vector Search finds the most semantically relevant documents first, then applies the filter — so we get PPO-Ohio policies, not all policies globally."

> "That's the difference between useful search and dangerous search in a healthcare context. Unguarded semantic search in UM would be a compliance problem. Healthcare teams need semantic relevance plus hard operational guardrails — that's exactly what Atlas Vector Search delivers. One engine, both capabilities."

**[Optional — toggle the retrieval mode to `$rankFusion (hybrid)` and re-run the search]**

> **⚠️ PRESENTER NOTE — RUN THIS BEAT ON SCENARIO B ONLY.** The Crohn's contrast prior (`PCL-2024-BIO-3580`) that lights up the `vec #4 / lex #1` chip pair is only wired into Scenario B (Eleanor Vasquez / infliximab). On Scenarios A and C the hybrid toggle works, but there is no rank disagreement to point at — the talking points below will not match what's on screen. If you are running A or C, skip this optional beat.

> "Pure vector search is excellent when meaning matters more than exact words. But sometimes the exact word matters — a specific drug name, a procedure code, a regulatory phrase. With `$rankFusion`, Atlas runs a vector pipeline and a lexical text pipeline in parallel, fuses the rankings, and returns one merged result list. No second search engine, no app-side rerank, no extra data layer to keep in sync. The same hard filters apply identically to both pipelines."

> "Watch the cards after we re-run — each result now shows the rank it received from each input pipeline. Where vector and lexical disagree, you can see exactly which pipeline contributed the lift."

**[Point at the third prior-claim card — `PCL-2024-BIO-3580`, with `vec #4 / lex #1` chips]**

> "Look at this third result. The chips tell the story — vector pipeline ranked it fourth, lexical pipeline ranked it first. This is a Crohn's disease infliximab claim, not RA. Semantically the embedding sees it as further away from our pended RA case, so pure vector pushes it out of the top three. But lexically it shares the operationally important tokens — Remicade, biosimilar exclusion, five milligrams per kilogram, the same policy reference, the same high-cost biologic pend code. The lexical pipeline found a case the embedding smoothed over, and `$rankFusion` brought it into the top three where a human reviewer can see it. That is the practical win of hybrid retrieval — same platform, same data, two retrieval styles, no separate index to maintain."

---

### STEP 4 — Retrieved Context

**[Pause on results]**

> "Look at what came back. The top policy match is the specific medical necessity criteria for this procedure — those are not random. Atlas Vector Search found them because the clinical language in this claim semantically aligns with the language in those policies."

> "And the prior claims include an almost identical approved case — same diagnosis, same plan type, same state — plus contrast cases that show what a denial looks like under different clinical circumstances."

**[Point at green ✓ filter pills on each card]**

> "The green checkmarks on each card tell you exactly which fields matched the filters you set. You can see at a glance that these results are from the same plan type and state — that's not coincidence, that's Atlas Vector Search enforcing your constraints before returning results."

**[Point at the blue auto-scoped badge in the section header]**

> "The blue badge shows a filter the system set automatically. It inferred from the procedure code that this is an [imaging / biologic / obesity] claim and scoped the search to that clinical domain. That's why you're seeing the right policies and not results from a completely different part of the formulary."

**[Optional — if engineers are in the room, click the `$vectorSearch` toggle above the results]**

> "For the engineers — that's the exact aggregation pipeline MongoDB ran. Same `$vectorSearch` stage you'd write in any application, with the operational filters applied as a `filter` clause inside the search itself, then a normal `$project` to shape the response. The 1024-dim query vector is rendered as a placeholder so the JSON stays readable, but the rest is verbatim. No translation layer, no separate search service."

> "The value here is not that AI generated words. The value is that Atlas Vector Search found the right context. The rationale we're about to generate is only as good as what it gets to work with. The retrieval architecture is the foundation. If that's wrong, the output is wrong, and no amount of prompt engineering fixes a bad retrieval layer."

---

### STEP 5 — Rationale + Write-back

**[Click "Generate Rationale"]**

> "The backend is now assembling a reviewer-voice recommendation grounded in what Atlas Vector Search just retrieved — the actual policy criteria text and the outcome rationales from those prior cases. No additional API call. The retrieved context is the input."

**[As rationale appears]**

> "Read the determination section. It references the specific clinical findings from this chart. It names the policy ID and the specific criterion. It references the prior claim IDs as analogs."

> "That's what grounded means. This output can't cite a policy that doesn't exist, because the policies we retrieved are right there as the source. The citations are real."

**[As claim record updates]**

> "And now watch the claim record at the top of the page. The `adjudication_status` just changed from `PENDED` to `READY_FOR_REVIEW`. The `ai_rationale` field is populated. The `ai_supporting_policies` and `ai_comparable_cases` arrays are written. The `status_history` has a new entry. This is not a separate result panel. This is the same MongoDB document we started with, updated in place."

> "MongoDB is not just storing the source data here. It is anchoring the embeddings, the retrieval results, and the generated AI output in the same operational context. One document, one platform, one place for engineering to reason about what happened."

---

### [ARCHITECTURE INTERLUDE — natural, woven into the flow]

*After the write-back lands, address the architectural question before moving on:*

> "A question I'd expect from an engineering audience: does running vector search on the same cluster impact transactional performance? The honest answer is it can if you don't isolate the workloads."

> "Atlas addresses this with Search Nodes — dedicated infrastructure for vector search workloads that scale independently from the core database nodes. Your OLTP cluster keeps handling operational writes without competing for resources with embedding queries. You get workload isolation without breaking the architectural simplicity — without adding another system. That's the pattern: one cluster, separated workloads, no new operational surface area."

---

### RECOMMENDED CLOSE (use close to verbatim)

**[Show the updated claim document, both field sections visible]**

> "If this pattern holds, the takeaway is simple: MongoDB is not just where a payer stores operational data. It is a practical way to keep operational data, embeddings, retrieval, and AI output close together in one architecture that engineering teams can reason about, scale, and standardize."

> "We started with a pended claim. The clinical notes became a Voyage embedding, stored in the same document. Atlas Vector Search retrieved the right policies and prior analogs using semantic similarity with hard metadata filters. The backend assembled a grounded, reviewer-voice recommendation directly from that retrieved context. And that recommendation was written back into the original record — status updated, rationale stored, audit trail intact — without the data ever leaving the platform."

> "That's the architecture. One platform. Fewer moving parts."

---

---

### Scenario C key talking points (GLP-1 / semaglutide)

**[Select Scenario C and run through Steps 1–5]**

> "This is the fastest-growing category of prior auth volume right now — GLP-1 weight management drugs. The member clearly qualifies clinically: BMI 38, three comorbidities, two prior medication failures. But there's a specific documentation gap: the plan requires a formal six-month medically supervised program, and the notes don't show one."

**[Step 4 — point at Prior #1 `PCL-2024-GLP1-1456`]**

> "The top prior claim is an approved case with nearly identical clinical facts — same BMI range, same comorbidities, same state and plan type — but with a complete six-month Tampa General program on file. That's the context the reviewer needs to understand exactly what documentation would move this case to approval."

**[Step 4 — point at Prior #2 `PCL-2024-GLP1-0312`]**

> "And here's a denial case with the same drug and same diagnosis code, but BMI 28.9 — below the coverage threshold. Same procedure, different outcome, different clinical facts. The vector search surfaced both because both are semantically relevant to this claim."

---

### Talking points if audience asks follow-up questions

**"Is this production-ready or a demo?"**
> "The architecture pattern is production-grade. What you're seeing is a working demo on a real Atlas cluster with real Voyage embeddings and real Vector Search. The demo data is synthetic, but the plumbing is what you'd actually build."

**"How does this scale?"**
> "The operational cluster and the vector search nodes scale independently on Atlas. You're not choosing between operational performance and search performance — you provision both to match your load."

**"What about data governance and HIPAA?"**
> "MongoDB Atlas has HIPAA-eligible configurations. Everything in this demo stays in your Atlas cluster — no PHI leaves the environment. The AI call is the one boundary to design around, and that can be a private endpoint or an on-prem model depending on your compliance posture."

**"Could we use a different embedding model?"**
> "Yes. The embedding dimension and model are configuration. Voyage-3 is a strong general-purpose model for clinical text. If you have domain-specific requirements, the architecture is the same — swap the model, rebuild the embeddings, the Vector Search index adapts."
