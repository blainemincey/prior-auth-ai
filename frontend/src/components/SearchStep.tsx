import type { ClaimRecord, SearchMode } from "../types";

export interface SearchFilters {
  planType: string;
  state: string;
  outcome: string;
}

interface Props {
  claim: ClaimRecord;
  filters: SearchFilters;
  onFiltersChange: (f: SearchFilters) => void;
  mode: SearchMode;
  onModeChange: (m: SearchMode) => void;
  loading: boolean;
  onSearch: (filters: Record<string, string | undefined>, mode: SearchMode) => void;
  alreadyDone: boolean;
}

export default function SearchStep({
  filters, onFiltersChange, mode, onModeChange, loading, onSearch, alreadyDone,
}: Props) {
  const { planType, state, outcome } = filters;

  function handleSearch() {
    onSearch(
      {
        plan_type: planType || undefined,
        state: state || undefined,
        adjudication_outcome: outcome || undefined,
      },
      mode,
    );
  }

  const selectStyle: React.CSSProperties = {
    background: "var(--surface-sunken)",
    border: "1px solid var(--border)",
    borderRadius: "var(--radius)",
    padding: "6px 10px",
    color: "var(--text)",
    fontSize: "var(--fs-sm)",
    fontFamily: "inherit",
    outline: "none",
    minWidth: 110,
  };

  return (
    <section className="panel">
      <div className="panel__header">
        <span className={`step-pill ${alreadyDone ? "step-pill--complete" : "step-pill--idle"}`}>
          {alreadyDone ? "✓" : "3"}
        </span>
        <span className="panel__title">Atlas Vector Search</span>
        <span className="panel__subtitle">Semantic similarity + hard metadata filters</span>
      </div>

      <div className="panel__body">
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "var(--space-3)",
          marginBottom: "var(--space-3)",
          flexWrap: "wrap",
        }}>
          <span className="eyebrow" style={{ color: "var(--text-muted)" }}>Retrieval mode</span>
          <div style={{
            display: "inline-flex",
            border: "1px solid var(--border)",
            borderRadius: "var(--radius)",
            overflow: "hidden",
            background: "var(--surface-sunken)",
          }}>
            {(["vector", "hybrid"] as const).map((m) => {
              const active = mode === m;
              return (
                <button
                  key={m}
                  onClick={() => onModeChange(m)}
                  disabled={loading}
                  style={{
                    background: active ? "var(--success-bg)" : "transparent",
                    color: active ? "var(--mist)" : "var(--text-muted)",
                    border: "none",
                    borderRight: m === "vector" ? "1px solid var(--border)" : "none",
                    padding: "5px 14px",
                    fontSize: "var(--fs-xs)",
                    fontFamily: "Source Code Pro, monospace",
                    fontWeight: active ? "var(--fw-semibold)" : "var(--fw-regular)",
                    cursor: loading ? "not-allowed" : "pointer",
                    letterSpacing: "0.02em",
                  }}
                  title={
                    m === "vector"
                      ? "$vectorSearch only — semantic similarity"
                      : "$rankFusion(vector + lexical) — semantic + keyword fused"
                  }
                >
                  {m === "vector" ? "$vectorSearch" : "$rankFusion (hybrid)"}
                </button>
              );
            })}
          </div>
          <span style={{
            fontSize: "var(--fs-xs)",
            color: "var(--text-faint)",
            lineHeight: "var(--lh-base)",
          }}>
            {mode === "vector"
              ? "Semantic similarity only, with hard filters."
              : "Vector + lexical fused via $rankFusion — same filters in both pipelines."}
          </span>
        </div>

        <p style={{
          fontSize: "var(--fs-sm)",
          color: "var(--text-muted)",
          marginBottom: "var(--space-3)",
          lineHeight: "var(--lh-base)",
        }}>
          Atlas Vector Search finds semantically relevant policies and prior cases
          while honoring the filters below as hard constraints — not hints.
        </p>

        <div style={{
          display: "flex", flexWrap: "wrap", gap: "var(--space-4)",
          marginBottom: "var(--space-3)", alignItems: "flex-end",
        }}>
          <div>
            <label className="eyebrow" style={{ display: "block", marginBottom: 4 }}>plan_type</label>
            <select
              value={planType}
              onChange={(e) => onFiltersChange({ ...filters, planType: e.target.value })}
              style={selectStyle}
            >
              <option value="">Any</option>
              <option value="PPO">PPO</option>
              <option value="HMO">HMO</option>
              <option value="Medicare Advantage">Medicare Advantage</option>
            </select>
          </div>
          <div>
            <label className="eyebrow" style={{ display: "block", marginBottom: 4 }}>state</label>
            <select
              value={state}
              onChange={(e) => onFiltersChange({ ...filters, state: e.target.value })}
              style={selectStyle}
            >
              <option value="">Any</option>
              {["OH","TX","FL","IN","KY","TN","GA","NC","MI","WI","MN","IL","PA","NJ","WA","AZ","CO","CA","NY"].map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="eyebrow" style={{ display: "block", marginBottom: 4 }}>adjudication_outcome (prior claims)</label>
            <select
              value={outcome}
              onChange={(e) => onFiltersChange({ ...filters, outcome: e.target.value })}
              style={selectStyle}
            >
              <option value="">Any (approved + denied)</option>
              <option value="APPROVED">APPROVED only</option>
              <option value="DENIED">DENIED only</option>
            </select>
          </div>
          <button
            className="btn-primary"
            onClick={handleSearch}
            disabled={loading}
            style={{ minWidth: 140 }}
          >
            {loading ? (
              <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span className="spinner" style={{ width: 14, height: 14 }} />
                Searching...
              </span>
            ) : alreadyDone ? "Re-run Search" : mode === "hybrid" ? "Run Hybrid Search" : "Run Vector Search"}
          </button>
        </div>

        <div style={{
          background: "var(--surface-sunken)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius)",
          padding: "8px 12px",
          fontSize: "var(--fs-xs)",
          color: "var(--text-muted)",
          fontFamily: "Source Code Pro, monospace",
        }}>
          <span style={{ color: "var(--accent-mark)", fontWeight: 600 }}>
            {mode === "hybrid" ? "$rankFusion(vector + lexical)" : "$vectorSearch"}
          </span>
          {" — numCandidates: 80, limit: 3 (policies), limit: 3 (prior claims), "}
          filter: {"{ plan_type: "}
          <span style={{ color: "var(--text)" }}>"{planType || "any"}"</span>
          {", state: "}
          <span style={{ color: "var(--text)" }}>"{state || "any"}"</span>
          {", adjudication_outcome: "}
          <span style={{ color: "var(--text)" }}>"{outcome || "any"}"</span>
          {" }"}
        </div>
      </div>
    </section>
  );
}
