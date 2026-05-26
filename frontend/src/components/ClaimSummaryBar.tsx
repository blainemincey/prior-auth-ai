import type { ClaimRecord, RationaleResult } from "../types";

function StatusBadge({ status }: { status: string }) {
  const cls =
    status === "PENDED" ? "badge-pended" :
    status === "READY_FOR_REVIEW" ? "badge-ready" :
    status === "APPROVED" ? "badge-approved" : "badge-info";
  return <span className={`badge ${cls}`}>{status.replace(/_/g, " ")}</span>;
}

interface Props {
  claim: ClaimRecord;
  rationale: RationaleResult | null;
}

export default function ClaimSummaryBar({ claim, rationale }: Props) {
  const current = rationale ? rationale.updated_claim : claim;
  const updated = !!rationale;

  return (
    <div
      className={updated ? "highlight-update" : ""}
      style={{
        background: "var(--surface)",
        border: `1px solid ${updated ? "var(--success-border)" : "var(--border)"}`,
        borderRadius: "var(--radius-lg)",
        padding: "var(--space-3) var(--space-4)",
        display: "flex",
        alignItems: "center",
        flexWrap: "wrap",
        gap: "var(--space-3)",
        boxShadow: "var(--shadow-sm)",
        transition: "border-color 0.4s",
      }}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: 1, marginRight: 4 }}>
        <span style={{ fontSize: "var(--fs-xs)", color: "var(--text-faint)" }}>
          {current.claim_id}
        </span>
        <span style={{
          fontSize: "var(--fs-base)",
          fontWeight: "var(--fw-semibold)",
          color: "var(--text)",
          whiteSpace: "nowrap",
        }}>
          {current.member_name}
        </span>
        <span style={{ fontSize: "var(--fs-xs)", color: "var(--text-faint)" }}>
          {current.plan_type} · {current.state}
        </span>
      </div>

      <div style={{ width: 1, height: 44, background: "var(--border)", flexShrink: 0 }} />

      <div style={{ display: "flex", gap: "var(--space-2)", flexWrap: "wrap", flex: 1 }}>
        <div className="kv-tile">
          <span className="kv-tile__label">pend_reason</span>
          <span className="kv-tile__value">{current.pend_reason_code}</span>
        </div>
        <div className={`kv-tile ${current.clinical_embedding ? "kv-tile--accent" : ""}`}>
          <span className="kv-tile__label">clinical_embedding</span>
          <span className="kv-tile__value">
            {current.clinical_embedding ? "stored · 1024 dims" : "null"}
          </span>
        </div>
        {current.ai_determination && (
          <div className="kv-tile kv-tile--accent">
            <span className="kv-tile__label">ai_determination</span>
            <span className="kv-tile__value">{current.ai_determination}</span>
          </div>
        )}
      </div>

      <div style={{
        marginLeft: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-end",
        gap: 3,
      }}>
        <span className="eyebrow">adjudication_status</span>
        <StatusBadge status={current.adjudication_status} />
      </div>
    </div>
  );
}
