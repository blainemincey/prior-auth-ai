import type { Step } from "../types";

const STEPS: { n: Step; label: string }[] = [
  { n: 1, label: "Operational Record" },
  { n: 2, label: "Voyage Embedding" },
  { n: 3, label: "Vector Search" },
  { n: 4, label: "Retrieved Context" },
  { n: 5, label: "Rationale + Write-back" },
];

// Tab n is enabled when step progress has reached the unlock threshold.
// Steps 4 and 5 unlock together once search is complete (step >= 3).
function isEnabled(n: Step, step: Step): boolean {
  if (n <= 2) return step >= 1;
  if (n === 3) return step >= 2;
  return step >= 3; // tabs 4 and 5
}

function isComplete(n: Step, step: Step): boolean {
  if (n === 1) return false; // record tab is live, never "done"
  if (n === 4) return step >= 3;
  return step >= n;
}

interface Props {
  step: Step;
  activeTab: Step;
  onTabClick: (tab: Step) => void;
}

export default function StepTabs({ step, activeTab, onTabClick }: Props) {
  return (
    <div style={{
      display: "flex",
      borderBottom: "1px solid var(--border)",
      overflowX: "auto",
      gap: 2,
    }}>
      {STEPS.map((s) => {
        const enabled = isEnabled(s.n, step);
        const complete = isComplete(s.n, step);
        const active = activeTab === s.n;

        const pillClass =
          active    ? "step-pill step-pill--active" :
          complete  ? "step-pill step-pill--complete" :
                      "step-pill step-pill--idle";

        return (
          <button
            key={s.n}
            onClick={() => enabled && onTabClick(s.n)}
            disabled={!enabled}
            style={{
              background: active ? "var(--surface-raised)" : "transparent",
              border: "none",
              borderBottom: active
                ? "3px solid var(--brand)"
                : "3px solid transparent",
              borderRadius: "var(--radius) var(--radius) 0 0",
              padding: "10px 16px",
              marginBottom: -1,
              display: "flex",
              alignItems: "center",
              gap: 8,
              cursor: enabled ? "pointer" : "not-allowed",
              opacity: enabled ? 1 : 0.4,
              whiteSpace: "nowrap",
              transition: "background 0.15s, border-color 0.15s, opacity 0.15s",
              flexShrink: 0,
            }}
          >
            <span className={pillClass} style={{ width: 20, height: 20, fontSize: 10 }}>
              {complete ? "✓" : s.n}
            </span>
            <span style={{
              fontSize: "var(--fs-sm)",
              fontWeight: active ? "var(--fw-semibold)" : "var(--fw-regular)",
              color: active ? "var(--text)" : "var(--text-muted)",
            }}>
              {s.label}
            </span>
          </button>
        );
      })}
    </div>
  );
}
