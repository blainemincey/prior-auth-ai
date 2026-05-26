import type { ClaimRecord as ClaimType } from "../types";

function Field({ label, value, mono = false, highlight = false }: {
  label: string; value: React.ReactNode; mono?: boolean; highlight?: boolean;
}) {
  const valueClass = `field-row__value${mono ? " field-row__value--mono" : ""}`;
  return (
    <div className={`field-row${highlight ? " field-row--highlight" : ""}`}>
      <span className="field-row__label">{label}</span>
      <span className={valueClass}>{value}</span>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const cls =
    status === "PENDED" ? "badge-pended" :
    status === "READY_FOR_REVIEW" ? "badge-ready" :
    status === "APPROVED" ? "badge-approved" : "badge-info";
  return <span className={`badge ${cls}`}>{status}</span>;
}

interface Props {
  claim: ClaimType;
  updated: boolean;
}

export default function ClaimRecord({ claim, updated }: Props) {
  const procedures = claim.procedure_codes || [];

  return (
    <section className={`panel ${updated ? "highlight-update" : ""}`}>
      <div className="panel__header">
        <span style={{
          width: 8, height: 8, borderRadius: "50%",
          background: "var(--brand)",
          display: "inline-block",
        }} />
        <span className="panel__title">Claim Record</span>
        <code className="code-inline">healthcare_demo.claims</code>
        <div className="panel__spacer" />
        <StatusBadge status={claim.adjudication_status} />
        <span className="panel__subtitle" style={{ fontFamily: "Source Code Pro, monospace" }}>
          {claim.claim_id}
        </span>
      </div>

      <div className="panel__body" style={{ display: "flex", flexDirection: "column", gap: 0 }}>
        <p className="eyebrow" style={{ marginBottom: "var(--space-2)" }}>Member &amp; Plan</p>
        <Field label="member_name" value={claim.member_name} />
        <Field label="member_id" value={claim.member_id} mono />
        <Field label="plan_name" value={claim.plan_name} />
        <Field label="plan_type / state" value={`${claim.plan_type} · ${claim.state}`} />

        <p className="eyebrow" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
          Diagnosis
        </p>
        <Field label="primary_diagnosis_code" value={claim.primary_diagnosis_code} mono />
        <Field label="primary_diagnosis_description" value={claim.primary_diagnosis_description} />

        <p className="eyebrow" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
          Procedure Codes
        </p>
        {procedures.map((p) => (
          <Field
            key={p.code}
            label={`${p.type} ${p.code}`}
            value={`${p.description}${p.billed_amount ? ` · $${p.billed_amount.toLocaleString()}` : ""}`}
          />
        ))}
        <Field
          label="total_billed_amount"
          value={`$${(claim.total_billed_amount || 0).toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
        />

        <p className="eyebrow" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
          Adjudication
        </p>
        <Field label="adjudication_status" value={<StatusBadge status={claim.adjudication_status} />} />
        <Field label="pend_reason_code" value={claim.pend_reason_code} mono />
        <Field label="pend_reason_description" value={claim.pend_reason_description} />

        <p className="eyebrow" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
          Voyage AI Embedding <code className="code-inline" style={{ marginLeft: 6 }}>stored in this document</code>
        </p>
        <Field
          label="clinical_embedding"
          value={
            claim.clinical_embedding
              ? <span style={{ color: "var(--mist)" }}>
                  {claim.clinical_embedding} · model: {claim.embedding_model}
                </span>
              : <span style={{ color: "var(--text-faint)" }}>null — not yet generated</span>
          }
        />
        <Field
          label="embedding_generated_at"
          value={claim.embedding_generated_at || "null"}
          mono
        />

        <p className="eyebrow" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
          Clinical Notes <span className="muted" style={{ textTransform: "none", letterSpacing: 0, fontWeight: 400 }}>— unstructured, embedded by Voyage AI</span>
        </p>
        <div style={{
          background: "var(--surface-sunken)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius)",
          padding: "var(--space-3) var(--space-3)",
          maxHeight: 200,
          overflowY: "auto",
          fontSize: "var(--fs-xs)",
          lineHeight: "var(--lh-loose)",
          color: "var(--text-code)",
          fontFamily: "Source Code Pro, monospace",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}>
          {claim.clinical_notes}
        </div>

        {claim.ai_rationale && (
          <>
            <p className="eyebrow eyebrow--accent" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
              AI-Generated Rationale — written back to this record
            </p>
            <Field label="ai_determination" value={claim.ai_determination || ""} highlight />
            <Field label="ai_rationale_generated_at" value={claim.ai_rationale_generated_at || ""} mono />
            <Field label="ai_supporting_policies" value={(claim.ai_supporting_policies || []).join(", ")} mono highlight />
            <Field label="ai_comparable_cases" value={(claim.ai_comparable_cases || []).join(", ")} mono highlight />
          </>
        )}

        {claim.status_history && claim.status_history.length > 0 && (
          <>
            <p className="eyebrow" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
              Status History
            </p>
            {claim.status_history.map((h, i) => (
              <Field
                key={i}
                label={h.timestamp?.slice(0, 19) || ""}
                value={`${h.status} — ${h.note}`}
                highlight={i === claim.status_history!.length - 1 && !!claim.ai_rationale}
              />
            ))}
          </>
        )}
      </div>
    </section>
  );
}
