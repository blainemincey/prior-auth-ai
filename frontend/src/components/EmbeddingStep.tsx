import type { EmbeddingResult } from "../types";

interface Props {
  embedding: EmbeddingResult | null;
  loading: boolean;
  onEmbed: () => void;
  alreadyDone: boolean;
}

export default function EmbeddingStep({ embedding, loading, onEmbed, alreadyDone }: Props) {
  return (
    <section className="panel">
      <div className="panel__header">
        <span className={`step-pill ${embedding ? "step-pill--complete" : "step-pill--idle"}`}>
          {embedding ? "✓" : "2"}
        </span>
        <span className="panel__title">Voyage AI Embedding</span>
        <span className="panel__subtitle">voyage-3 · 1024 dims · stored in MongoDB</span>
        <div className="panel__spacer" />
        <button
          className={embedding ? "btn-secondary" : "btn-primary"}
          onClick={onEmbed}
          disabled={loading || (alreadyDone && !!embedding)}
          style={{ minWidth: 150 }}
        >
          {loading && !embedding ? (
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span className="spinner" style={{ width: 14, height: 14 }} />
              Embedding...
            </span>
          ) : embedding ? "Re-embed" : "Generate Embedding"}
        </button>
      </div>

      <div className="panel__body">
        {!embedding && !loading && (
          <p style={{ color: "var(--text-muted)", fontSize: "var(--fs-base)" }}>
            Click <strong style={{ color: "var(--text)" }}>Generate Embedding</strong> to have Voyage AI embed the clinical notes
            and write the vector directly into this MongoDB document — no separate vector store.
          </p>
        )}

        {loading && !embedding && (
          <p style={{
            color: "var(--text-muted)",
            fontSize: "var(--fs-base)",
            display: "flex", alignItems: "center", gap: 8,
          }}>
            <span className="spinner" />
            Calling Voyage AI voyage-3 · writing vector to MongoDB document...
          </p>
        )}

        {embedding && (
          <div className="fade-in" style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
            <div style={{ display: "flex", gap: "var(--space-4)", flexWrap: "wrap" }}>
              {[
                { label: "Embedding Model", value: embedding.embedding_model, accent: true },
                { label: "Dimensions",      value: embedding.embedding_dimensions.toLocaleString(), accent: true },
                { label: "Storage",         value: "MongoDB document", accent: false },
                { label: "Generated",       value: (embedding.generated_at?.slice(0, 19).replace("T", " ") + " UTC"), accent: false },
              ].map((item) => (
                <div
                  key={item.label}
                  className={`kv-tile ${item.accent ? "kv-tile--accent" : ""}`}
                  style={{ flex: 1, minWidth: 150 }}
                >
                  <span className="kv-tile__label">{item.label}</span>
                  <span className="kv-tile__value">{item.value}</span>
                </div>
              ))}
            </div>

            <div>
              <p className="eyebrow" style={{ marginBottom: 6 }}>
                Vector preview · first 8 of 1,024 dimensions
              </p>
              <code
                className="code-block"
                style={{ color: "var(--accent-mark)", letterSpacing: "0.03em" }}
              >
                [{embedding.embedding_preview.map((v) => v.toFixed(6)).join(", ")}, ...]
              </code>
            </div>

            <p style={{
              fontSize: "var(--fs-sm)",
              color: "var(--text-muted)",
              borderLeft: "2px solid var(--accent)",
              paddingLeft: 10,
              lineHeight: "var(--lh-base)",
            }}>
              {embedding.message}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
