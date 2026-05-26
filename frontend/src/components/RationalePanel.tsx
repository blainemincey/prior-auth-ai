import { useMemo } from "react";
import { marked } from "marked";
import type { RationaleResult } from "../types";

interface Props {
  result: RationaleResult | null;
  loading: boolean;
  onGenerate: () => void;
}

function determinationColor(det: string) {
  if (det.includes("APPROVE")) return "var(--brand)";
  if (det.includes("DENY"))    return "var(--error)";
  return "var(--warn)";
}

export default function RationalePanel({ result, loading, onGenerate }: Props) {
  const renderedRationale = useMemo(
    () => (result ? marked.parse(result.rationale) as string : ""),
    [result]
  );

  return (
    <section className="panel panel--generated">
      <div className="panel__header">
        <span className={`step-pill ${result ? "step-pill--complete" : "step-pill--idle"}`}>
          {result ? "✓" : "5"}
        </span>
        <span className="panel__title">AI Rationale + Write-back</span>
        <span className="panel__subtitle">
          Template generates · MongoDB stores · claim updates in place
        </span>
        <div className="panel__spacer" />
        <button
          className={result ? "btn-secondary" : "btn-primary"}
          onClick={onGenerate}
          disabled={loading}
          style={{ minWidth: 160 }}
        >
          {loading ? (
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span className="spinner" style={{ width: 14, height: 14 }} />
              Generating...
            </span>
          ) : result ? "Regenerate" : "Generate Rationale"}
        </button>
      </div>

      <div className="panel__body">
        {!result && !loading && (
          <p style={{
            color: "var(--text-muted)",
            fontSize: "var(--fs-base)",
            lineHeight: "var(--lh-base)",
          }}>
            Click <strong style={{ color: "var(--text)" }}>Generate Rationale</strong> to assemble a structured
            reviewer-voice recommendation grounded in the retrieved policy criteria and prior case analogues,
            then write it back into the same claim record.
            Watch the claim document above update in place — adjudication status, rationale, and timestamp
            all written to the same MongoDB document that held the operational data.
          </p>
        )}

        {loading && (
          <p style={{
            color: "var(--text-muted)",
            fontSize: "var(--fs-base)",
            display: "flex", alignItems: "center", gap: 8,
          }}>
            <span className="spinner" />
            Assembling grounded rationale from retrieved context · writing back to MongoDB...
          </p>
        )}

        {result && (
          <div className="fade-in" style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
            <div style={{
              display: "flex",
              alignItems: "center",
              gap: "var(--space-3)",
              padding: "var(--space-3) var(--space-4)",
              background: "var(--surface-sunken)",
              border: "1px solid var(--border)",
              borderLeft: "3px solid var(--accent)",
              borderRadius: "var(--radius)",
              flexWrap: "wrap",
            }}>
              <span className="eyebrow eyebrow--accent">AI Generated</span>
              <span style={{ color: "var(--border-strong)" }}>·</span>
              <span style={{ fontSize: "var(--fs-xs)", color: "var(--text-faint)" }}>Recommendation</span>
              <span style={{
                fontSize: "var(--fs-md)",
                fontWeight: "var(--fw-bold)",
                color: determinationColor(result.determination),
                letterSpacing: "0.02em",
              }}>
                {result.determination}
              </span>
              <span style={{ marginLeft: "auto", fontSize: "var(--fs-xs)", color: "var(--text-faint)" }}>
                Draft · Human reviewer attestation required
              </span>
            </div>

            <div style={{ display: "flex", gap: "var(--space-3)", flexWrap: "wrap" }}>
              <div className="kv-tile kv-tile--accent" style={{ flex: 1, minWidth: 220 }}>
                <span className="kv-tile__label">Supporting Policies · written to record</span>
                <span className="kv-tile__value" style={{ display: "flex", flexDirection: "column", gap: 2 }}>
                  {result.supporting_policy_ids.map((id) => (
                    <span key={id}>{id}</span>
                  ))}
                </span>
              </div>
              <div className="kv-tile kv-tile--accent" style={{ flex: 1, minWidth: 220 }}>
                <span className="kv-tile__label">Comparable Cases · written to record</span>
                <span className="kv-tile__value" style={{ display: "flex", flexDirection: "column", gap: 2 }}>
                  {result.comparable_case_ids.map((id) => (
                    <span key={id}>{id}</span>
                  ))}
                </span>
              </div>
            </div>

            <div>
              <p className="eyebrow" style={{ marginBottom: 6 }}>
                Full rationale · written to <code className="code-inline" style={{ marginLeft: 4 }}>claims.ai_rationale</code>
              </p>
              <div
                className="docs-content output-body"
                style={{
                  background: "var(--surface-sunken)",
                  border: "1px solid var(--border)",
                  borderRadius: "var(--radius)",
                  padding: "var(--space-4)",
                  maxHeight: 480,
                  overflowY: "auto",
                }}
                dangerouslySetInnerHTML={{ __html: renderedRationale }}
              />
            </div>

            <div style={{
              padding: "var(--space-2) var(--space-3)",
              background: "var(--success-bg)",
              border: "1px solid var(--success-border)",
              borderRadius: "var(--radius)",
              fontSize: "var(--fs-sm)",
              color: "var(--text-muted)",
              lineHeight: "var(--lh-base)",
            }}>
              <strong style={{ color: "var(--mist)" }}>Write-back complete.</strong>{" "}
              The claim record above now reflects: <code className="code-inline">adjudication_status: READY_FOR_REVIEW</code>,
              the full rationale text, supporting policy IDs, comparable case IDs, and an updated status history entry —
              all written back to the same MongoDB document that holds the operational data.
              Operational data, embeddings, retrieval, and AI output: one platform.
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
