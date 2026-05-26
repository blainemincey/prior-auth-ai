import { useState, useEffect, useCallback } from "react";
import { marked } from "marked";
import { api } from "../api";

type DocName = "readme" | "runbook" | "script";

interface Props {
  doc: DocName | null;
  onClose: () => void;
}

export default function DocsModal({ doc, onClose }: Props) {
  const [content, setContent] = useState<string | null>(null);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (name: DocName) => {
    setLoading(true);
    setError(null);
    setContent(null);
    try {
      const res = await api.fetchDoc(name);
      setTitle(res.title);
      setContent(marked.parse(res.content) as string);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (doc) load(doc);
  }, [doc, load]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  if (!doc) return null;

  return (
    <>
      <div
        onClick={onClose}
        style={{
          position: "fixed", inset: 0,
          background: "rgba(0,0,0,0.60)",
          backdropFilter: "blur(2px)",
          zIndex: 200,
        }}
      />

      <div style={{
        position: "fixed", top: 0, right: 0, bottom: 0,
        width: "min(820px, 92vw)",
        background: "var(--surface)",
        borderLeft: "1px solid var(--border)",
        boxShadow: "var(--shadow-md)",
        zIndex: 201,
        display: "flex",
        flexDirection: "column",
      }}>
        <div style={{
          display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "var(--space-4) var(--space-5)",
          borderBottom: "1px solid var(--border)",
          background: "var(--surface-raised)",
          flexShrink: 0,
        }}>
          <span style={{
            fontWeight: "var(--fw-semibold)",
            fontSize: "var(--fs-md)",
            color: "var(--text)",
          }}>
            {title || "Loading…"}
          </span>
          <button
            onClick={onClose}
            style={{
              background: "transparent",
              border: "1px solid var(--border)",
              color: "var(--text-muted)",
              fontSize: 14,
              lineHeight: 1,
              padding: "4px 9px",
              cursor: "pointer",
              borderRadius: "var(--radius)",
              fontWeight: "var(--fw-regular)",
            }}
            title="Close (Esc)"
          >
            ✕
          </button>
        </div>

        <div style={{
          flex: 1,
          overflowY: "auto",
          padding: "var(--space-5) var(--space-6)",
        }}>
          {loading && (
            <div style={{ color: "var(--text-muted)", fontSize: "var(--fs-base)" }}>Loading…</div>
          )}
          {error && (
            <div style={{ color: "var(--error)", fontSize: "var(--fs-base)" }}>{error}</div>
          )}
          {content && (
            <div
              className="docs-content"
              dangerouslySetInnerHTML={{ __html: content }}
            />
          )}
        </div>
      </div>
    </>
  );
}
