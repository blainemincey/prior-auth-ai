import { useState } from "react";
import type { SearchResult, PolicyResult, PriorClaimResult } from "../types";

type Filters = SearchResult["query_filters_applied"];

function PipelineViewer({ pipelines }: { pipelines: NonNullable<SearchResult["pipelines"]> }) {
  const [open, setOpen] = useState(false);
  const [tab, setTab] = useState<"policies" | "prior_claims">("policies");

  const formatted = JSON.stringify(pipelines[tab], null, 2);

  return (
    <div style={{
      border: "1px solid var(--border)",
      borderRadius: "var(--radius)",
      background: "var(--surface-sunken)",
      overflow: "hidden",
    }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          width: "100%",
          background: "transparent",
          border: "none",
          padding: "8px 12px",
          display: "flex",
          alignItems: "center",
          gap: 8,
          cursor: "pointer",
          color: "var(--text)",
          fontSize: "var(--fs-sm)",
          fontWeight: "var(--fw-semibold)",
        }}
      >
        <span style={{ fontSize: 10, color: "var(--text-faint)" }}>{open ? "▼" : "▶"}</span>
        <code style={{
          color: "var(--accent-mark)",
          fontFamily: "Source Code Pro, monospace",
          fontSize: "var(--fs-sm)",
        }}>
          $vectorSearch
        </code>
        <span style={{ color: "var(--text-muted)", fontWeight: "var(--fw-regular)" }}>
          — exact aggregation pipeline MongoDB executed
        </span>
      </button>

      {open && (
        <div style={{ borderTop: "1px solid var(--border)" }}>
          <div style={{
            display: "flex",
            gap: 0,
            background: "var(--surface)",
            borderBottom: "1px solid var(--border)",
          }}>
            {(["policies", "prior_claims"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                style={{
                  background: tab === t ? "var(--surface-sunken)" : "transparent",
                  border: "none",
                  borderRight: "1px solid var(--border)",
                  borderBottom: tab === t ? "2px solid var(--accent)" : "2px solid transparent",
                  padding: "6px 14px",
                  color: tab === t ? "var(--text)" : "var(--text-muted)",
                  fontSize: "var(--fs-xs)",
                  fontFamily: "Source Code Pro, monospace",
                  cursor: "pointer",
                  fontWeight: tab === t ? "var(--fw-semibold)" : "var(--fw-regular)",
                }}
              >
                {t === "policies" ? "policies" : "prior_claims"}
              </button>
            ))}
          </div>
          <pre style={{
            margin: 0,
            padding: "var(--space-3) var(--space-4)",
            fontSize: "var(--fs-xs)",
            lineHeight: "var(--lh-base)",
            color: "var(--text-code)",
            fontFamily: "Source Code Pro, monospace",
            maxHeight: 320,
            overflow: "auto",
            whiteSpace: "pre",
          }}>
            {formatted}
          </pre>
        </div>
      )}
    </div>
  );
}

// Rank ramp readable on Slate Blue: Spring → mid → Forest
const RANK_COLORS = ["#00ED64", "#4FB57A", "#00684A"];

function RankScore({ rank, score, vectorRank, lexicalRank }: {
  rank: number;
  score?: number;
  vectorRank?: number | null;
  lexicalRank?: number | null;
}) {
  const color = RANK_COLORS[rank - 1] ?? "var(--text-faint)";
  const isHybrid = vectorRank !== undefined || lexicalRank !== undefined;
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minWidth: 64,
      gap: 4,
      flexShrink: 0,
    }}>
      <span style={{
        fontSize: 18,
        fontWeight: "var(--fw-bold)",
        color,
        lineHeight: 1,
      }}>
        #{rank}
      </span>
      {!isHybrid && score !== undefined && (
        <>
          <code style={{ fontSize: "var(--fs-base)", fontWeight: "var(--fw-bold)", color }}>
            {score.toFixed(3)}
          </code>
          <div style={{
            width: 36, height: 3,
            background: "var(--border)",
            borderRadius: 2,
            overflow: "hidden",
          }}>
            <div style={{
              width: `${Math.round(score * 100)}%`,
              height: "100%",
              background: color,
              borderRadius: 2,
            }} />
          </div>
          <span style={{
            fontSize: 9,
            color: "var(--text-faint)",
            letterSpacing: "0.04em",
            textTransform: "uppercase",
          }}>
            similarity
          </span>
        </>
      )}
      {isHybrid && (
        <div style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch",
          gap: 2,
          fontFamily: "Source Code Pro, monospace",
          fontSize: 10,
          lineHeight: 1.2,
        }}>
          <span style={{
            color: vectorRank != null ? "var(--mist)" : "var(--text-faint)",
            background: vectorRank != null ? "rgba(0,104,74,0.18)" : "transparent",
            border: "1px solid var(--border)",
            borderRadius: 3,
            padding: "1px 5px",
            whiteSpace: "nowrap",
            textAlign: "center",
          }}>
            vec {vectorRank != null ? `#${vectorRank}` : "—"}
          </span>
          <span style={{
            color: lexicalRank != null ? "var(--info)" : "var(--text-faint)",
            background: lexicalRank != null ? "var(--info-bg)" : "transparent",
            border: "1px solid var(--border)",
            borderRadius: 3,
            padding: "1px 5px",
            whiteSpace: "nowrap",
            textAlign: "center",
          }}>
            lex {lexicalRank != null ? `#${lexicalRank}` : "—"}
          </span>
        </div>
      )}
    </div>
  );
}

function FilterPill({ label, value, active }: { label: string; value: string; active: boolean }) {
  return (
    <span style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 4,
      padding: "2px 8px",
      borderRadius: "var(--radius-pill)",
      fontSize: 10,
      fontWeight: "var(--fw-semibold)",
      fontFamily: "Source Code Pro, monospace",
      background: active ? "rgba(0,104,74,0.22)" : "rgba(255,255,255,0.04)",
      border: `1px solid ${active ? "var(--accent)" : "var(--border)"}`,
      color: active ? "var(--mist)" : "var(--text-faint)",
    }}>
      {active && <span style={{ fontSize: 9 }}>✓</span>}
      {label}: {value}
    </span>
  );
}

function AutoScopePill({ value }: { value: string }) {
  return (
    <span style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 4,
      padding: "2px 8px",
      borderRadius: "var(--radius-pill)",
      fontSize: 10,
      fontWeight: "var(--fw-semibold)",
      fontFamily: "Source Code Pro, monospace",
      background: "var(--info-bg)",
      border: "1px solid rgba(94,146,255,0.35)",
      color: "var(--info)",
    }}>
      auto · clinical_area: {value}
    </span>
  );
}

function ResultCard({ rank, children }: { rank: number; children: React.ReactNode }) {
  const borderColor = RANK_COLORS[rank - 1] ?? "var(--border)";
  return (
    <div style={{
      background: "var(--surface-sunken)",
      border: "1px solid var(--border)",
      borderLeft: `3px solid ${borderColor}`,
      borderRadius: "var(--radius)",
      padding: "var(--space-3) var(--space-4)",
      display: "flex",
      gap: "var(--space-4)",
    }}>
      {children}
    </div>
  );
}

function PolicyCard({ policy, rank, hybrid }: { policy: PolicyResult; rank: number; hybrid: boolean }) {
  return (
    <ResultCard rank={rank}>
      <RankScore
        rank={rank}
        score={policy.vector_score}
        vectorRank={hybrid ? policy.vector_rank : undefined}
        lexicalRank={hybrid ? policy.lexical_rank : undefined}
      />
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
        <code style={{
          fontSize: "var(--fs-sm)",
          color: "var(--accent-mark)",
          fontWeight: "var(--fw-semibold)",
        }}>
          {policy.policy_id}
        </code>
        <div style={{
          fontSize: "var(--fs-base)",
          fontWeight: "var(--fw-semibold)",
          color: "var(--text)",
          lineHeight: "var(--lh-tight)",
        }}>
          {policy.title}
        </div>
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
          <AutoScopePill value={policy.clinical_area} />
          <FilterPill label="subcategory" value={policy.subcategory} active={false} />
        </div>
        <div style={{
          fontSize: "var(--fs-xs)",
          color: "var(--text-code)",
          lineHeight: "var(--lh-base)",
          maxHeight: 90,
          overflowY: "auto",
          background: "rgba(0,0,0,0.25)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius)",
          padding: "6px 10px",
        }}>
          {policy.criteria_text?.slice(0, 400)}
          {(policy.criteria_text?.length || 0) > 400 ? "..." : ""}
        </div>
      </div>
    </ResultCard>
  );
}

function PriorClaimCard({ claim, rank, filters, hybrid }: { claim: PriorClaimResult; rank: number; filters: Filters; hybrid: boolean }) {
  const outcomeClass =
    claim.adjudication_outcome === "APPROVED" ? "badge-approved" :
    claim.adjudication_outcome === "DENIED"   ? "badge-denied"   : "badge-info";

  return (
    <ResultCard rank={rank}>
      <RankScore
        rank={rank}
        score={claim.vector_score}
        vectorRank={hybrid ? claim.vector_rank : undefined}
        lexicalRank={hybrid ? claim.lexical_rank : undefined}
      />
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <code style={{
            fontSize: "var(--fs-sm)",
            color: "var(--text)",
            fontWeight: "var(--fw-semibold)",
          }}>
            {claim.claim_id}
          </code>
          <span className={`badge ${outcomeClass}`}>{claim.adjudication_outcome}</span>
        </div>
        <div style={{
          fontSize: "var(--fs-sm)",
          color: "var(--text)",
          lineHeight: "var(--lh-tight)",
        }}>
          {claim.primary_diagnosis_description}
        </div>
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
          <FilterPill
            label="plan_type"
            value={claim.plan_type}
            active={!!filters.plan_type && filters.plan_type === claim.plan_type}
          />
          <FilterPill
            label="state"
            value={claim.state}
            active={!!filters.state && filters.state === claim.state}
          />
          {claim.service_date && (
            <FilterPill label="service_date" value={claim.service_date} active={false} />
          )}
          <FilterPill
            label="outcome"
            value={claim.adjudication_outcome}
            active={!!filters.adjudication_outcome && filters.adjudication_outcome === claim.adjudication_outcome}
          />
        </div>
        <div style={{
          fontSize: "var(--fs-xs)",
          color: "var(--text-code)",
          lineHeight: "var(--lh-base)",
          maxHeight: 72,
          overflowY: "auto",
          background: "rgba(0,0,0,0.25)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius)",
          padding: "6px 10px",
        }}>
          {claim.clinical_note?.slice(0, 280)}
          {(claim.clinical_note?.length || 0) > 280 ? "..." : ""}
        </div>
      </div>
    </ResultCard>
  );
}

function SectionHeader({ title, collection }: { title: string; collection: string }) {
  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      gap: "var(--space-2)",
      marginBottom: "var(--space-3)",
      paddingLeft: "var(--space-3)",
      borderLeft: "2px solid var(--accent)",
    }}>
      <span style={{
        fontSize: "var(--fs-sm)",
        fontWeight: "var(--fw-semibold)",
        color: "var(--text)",
      }}>
        {title}
      </span>
      <code className="code-inline" style={{ fontSize: 10 }}>{collection}</code>
    </div>
  );
}

export default function ContextPanel({ result }: { result: SearchResult }) {
  const { policies, prior_claims, query_filters_applied, meta, pipelines, mode } = result;
  const hybrid = mode === "hybrid";

  // clinical_area is auto-inferred from the claim's procedure codes, not a user-set constraint
  const userFilters = { ...query_filters_applied, clinical_area: undefined };
  const activeFilterCount = Object.values(userFilters).filter(Boolean).length;

  return (
    <section className="panel panel--retrieved fade-in">
      <div className="panel__header">
        <span className="step-pill step-pill--complete">✓</span>
        <span className="panel__title">Retrieved Context</span>
        <span className="panel__subtitle">
          {meta.policy_count} policies · {meta.prior_claim_count} prior claims · {meta.embedding_model}
          {hybrid && " · $rankFusion(vector + lexical)"}
        </span>
        <div className="panel__spacer" />
        {query_filters_applied.clinical_area && (
          <span style={{
            fontSize: "var(--fs-xs)",
            color: "var(--info)",
            background: "var(--info-bg)",
            border: "1px solid rgba(94,146,255,0.35)",
            borderRadius: "var(--radius-pill)",
            padding: "2px 10px",
            fontWeight: "var(--fw-semibold)",
          }}>
            auto-scoped: {query_filters_applied.clinical_area}
          </span>
        )}
        {activeFilterCount > 0 && (
          <span style={{
            fontSize: "var(--fs-xs)",
            color: "var(--mist)",
            background: "rgba(0,104,74,0.22)",
            border: "1px solid var(--accent)",
            borderRadius: "var(--radius-pill)",
            padding: "2px 10px",
            fontWeight: "var(--fw-semibold)",
          }}>
            {activeFilterCount} hard filter{activeFilterCount > 1 ? "s" : ""} applied
          </span>
        )}
      </div>

      <div className="panel__body" style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "var(--space-4)",
          fontSize: "var(--fs-xs)",
          color: "var(--text-faint)",
          flexWrap: "wrap",
        }}>
          <span>
            <span style={{
              display: "inline-block", width: 10, height: 10,
              borderRadius: 2, background: RANK_COLORS[0],
              marginRight: 5, verticalAlign: "middle",
            }} />
            {hybrid ? "Fused rank ($rankFusion)" : "Rank by semantic similarity"}
          </span>
          {hybrid && (
            <>
              <span style={{
                display: "inline-flex", alignItems: "center", gap: 4,
                padding: "1px 6px", borderRadius: 3,
                fontSize: 10, fontFamily: "Source Code Pro, monospace",
                background: "rgba(0,104,74,0.18)", border: "1px solid var(--border)",
                color: "var(--mist)",
              }}>vec #N</span>
              <span style={{
                display: "inline-flex", alignItems: "center", gap: 4,
                padding: "1px 6px", borderRadius: 3,
                fontSize: 10, fontFamily: "Source Code Pro, monospace",
                background: "var(--info-bg)", border: "1px solid var(--border)",
                color: "var(--info)",
              }}>lex #M</span>
              <span>= rank inside each input pipeline (— = absent)</span>
            </>
          )}
          <span style={{
            display: "inline-flex", alignItems: "center", gap: 4,
            padding: "1px 8px", borderRadius: "var(--radius-pill)",
            fontSize: 10, fontWeight: "var(--fw-semibold)",
            background: "rgba(0,104,74,0.22)", border: "1px solid var(--accent)",
            color: "var(--mist)",
          }}>
            ✓ field: value
          </span>
          <span>= user hard filter</span>
          <span style={{
            display: "inline-flex", alignItems: "center", gap: 4,
            padding: "1px 8px", borderRadius: "var(--radius-pill)",
            fontSize: 10, fontWeight: "var(--fw-semibold)",
            background: "var(--info-bg)", border: "1px solid rgba(94,146,255,0.35)",
            color: "var(--info)",
          }}>
            auto · clinical_area: imaging
          </span>
          <span>= inferred from claim procedure codes</span>
        </div>

        {pipelines && <PipelineViewer pipelines={pipelines} />}

        <div>
          <SectionHeader title="Coverage Policies" collection="healthcare_demo.policies" />
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
            {policies.map((p, i) => (
              <PolicyCard key={p.policy_id} policy={p} rank={i + 1} hybrid={hybrid} />
            ))}
          </div>
        </div>

        <div>
          <SectionHeader title="Comparable Prior Cases" collection="healthcare_demo.prior_claims" />
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
            {prior_claims.map((c, i) => (
              <PriorClaimCard key={c.claim_id} claim={c} rank={i + 1} filters={query_filters_applied} hybrid={hybrid} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
