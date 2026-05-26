export type Scenario = "A" | "B" | "C";

export type Step = 1 | 2 | 3 | 4 | 5;

export interface ClaimRecord {
  _id?: string;
  claim_id: string;
  scenario: Scenario;
  member_id: string;
  member_name: string;
  plan_type: string;
  plan_name: string;
  state: string;
  service_date: string;
  primary_diagnosis_code: string;
  primary_diagnosis_description: string;
  procedure_codes: Array<{ code: string; type: string; description: string; billed_amount?: number }>;
  total_billed_amount: number;
  adjudication_status: string;
  pend_reason_code: string;
  pend_reason_description: string;
  clinical_notes: string;
  clinical_embedding: string | null;
  embedding_model?: string;
  embedding_generated_at?: string | null;
  ai_rationale?: string | null;
  ai_determination?: string | null;
  ai_rationale_generated_at?: string | null;
  ai_supporting_policies?: string[];
  ai_comparable_cases?: string[];
  status_history?: Array<{ status: string; timestamp: string; note: string }>;
  [key: string]: unknown;
}

export interface EmbeddingResult {
  status: string;
  claim_id: string;
  embedding_model: string;
  embedding_dimensions: number;
  embedding_preview: number[];
  generated_at: string;
  message: string;
}

export type SearchMode = "vector" | "hybrid";

export interface PolicyResult {
  policy_id: string;
  title: string;
  clinical_area: string;
  subcategory: string;
  criteria_text: string;
  vector_score?: number;
  // Hybrid mode only — rank in each sub-pipeline (null if absent from one).
  vector_rank?: number | null;
  lexical_rank?: number | null;
}

export interface PriorClaimResult {
  claim_id: string;
  plan_type: string;
  state: string;
  service_date: string;
  primary_diagnosis_description: string;
  adjudication_outcome: string;
  outcome_rationale: string;
  clinical_note: string;
  vector_score?: number;
  vector_rank?: number | null;
  lexical_rank?: number | null;
}

export interface SearchResult {
  mode?: SearchMode;
  query_filters_applied: {
    plan_type?: string;
    state?: string;
    clinical_area?: string;
    adjudication_outcome?: string;
  };
  policies: PolicyResult[];
  prior_claims: PriorClaimResult[];
  pipelines?: {
    policies: unknown[];
    prior_claims: unknown[];
  };
  meta: {
    policy_count: number;
    prior_claim_count: number;
    embedding_model: string;
  };
}

export interface RationaleResult {
  rationale: string;
  determination: string;
  supporting_policy_ids: string[];
  comparable_case_ids: string[];
  updated_claim: ClaimRecord;
}
