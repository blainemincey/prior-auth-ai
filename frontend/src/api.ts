import type { ClaimRecord, EmbeddingResult, SearchResult, RationaleResult, PolicyResult, PriorClaimResult } from "./types";

const BASE = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

export const api = {
  getClaim: (scenario: string) =>
    request<ClaimRecord>(`/claims/${scenario}/record`),

  generateEmbedding: (scenario: string) =>
    request<EmbeddingResult>(`/claims/${scenario}/embed`, { method: "POST" }),

  runSearch: (
    scenario: string,
    filters: Record<string, string | undefined>,
    mode: "vector" | "hybrid" = "vector",
  ) =>
    request<SearchResult>(`/search/${scenario}`, {
      method: "POST",
      body: JSON.stringify({ filters, mode }),
    }),

  softResetAll: () =>
    request<{ status: string; claims_reset: { claim_id: string; scenario: string; embedding_preserved: boolean }[]; message: string }>(
      `/claims/reset-all`,
      { method: "POST" }
    ),

  generateRationale: (
    scenario: string,
    policies: PolicyResult[],
    prior_claims: PriorClaimResult[]
  ) =>
    request<RationaleResult>(`/claims/${scenario}/rationale`, {
      method: "POST",
      body: JSON.stringify({ policies, prior_claims }),
    }),

  fetchDoc: (name: "readme" | "runbook" | "script") =>
    request<{ name: string; title: string; content: string }>(`/docs/${name}`),
};
