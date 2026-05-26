import type { Scenario } from "../types";

const SCENARIOS = [
  {
    key: "A" as Scenario,
    label: "Scenario A",
    title: "MRI Prior Authorization",
    subtitle: "Lumbar Spine · CPT 72148",
    detail: "58-year-old male, PPO/OH. Pended for medical-necessity review. 14-week lumbar radiculopathy with conservative treatment history.",
    pend: "PA-MN-001",
  },
  {
    key: "B" as Scenario,
    label: "Scenario B",
    title: "Specialty Drug Infusion",
    subtitle: "Infliximab (Remicade) · HCPCS J1745",
    detail: "44-year-old female, PPO/TX. High-cost biologic ($18,420). Step-therapy compliance review triggered by adjudication engine.",
    pend: "MN-DRUG-HCB-002",
  },
  {
    key: "C" as Scenario,
    label: "Scenario C",
    title: "GLP-1 Prior Authorization",
    subtitle: "Semaglutide (Wegovy) 2.4mg · HCPCS S0148",
    detail: "52-year-old female, PPO/FL. Morbid obesity (BMI 38.2) with T2DM, hypertension, and sleep apnea. Pended for lifestyle program documentation.",
    pend: "PA-OBE-GLP1-001",
  },
];

interface Props {
  active: Scenario | null;
  onSelect: (s: Scenario) => void;
  disabled: boolean;
}

export default function ScenarioSelector({ active, onSelect, disabled }: Props) {
  return (
    <div style={{ marginTop: "var(--space-5)", marginBottom: "var(--space-2)" }}>
      <p className="eyebrow" style={{ marginBottom: "var(--space-3)" }}>
        Select Demo Scenario
      </p>
      <div style={{ display: "flex", gap: "var(--space-4)", flexWrap: "wrap" }}>
        {SCENARIOS.map((s) => {
          const isActive = active === s.key;
          return (
            <button
              key={s.key}
              onClick={() => onSelect(s.key)}
              disabled={disabled}
              style={{
                flex: 1,
                minWidth: 280,
                maxWidth: 480,
                textAlign: "left",
                background: isActive ? "var(--success-bg)" : "var(--surface)",
                border: `1px solid ${isActive ? "var(--brand)" : "var(--border)"}`,
                borderRadius: "var(--radius-lg)",
                padding: "var(--space-4) var(--space-5)",
                color: "var(--text)",
                cursor: disabled ? "not-allowed" : "pointer",
                opacity: disabled ? 0.7 : 1,
                boxShadow: isActive ? "var(--shadow-sm)" : "none",
                transition: "border-color 0.2s, background 0.2s, box-shadow 0.2s",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", marginBottom: 6, flexWrap: "wrap" }}>
                <span className="eyebrow eyebrow--accent">{s.label}</span>
                <span style={{ color: "var(--border-strong)" }}>·</span>
                <span style={{
                  fontSize: "var(--fs-xs)",
                  color: "var(--text-faint)",
                  fontFamily: "Source Code Pro, monospace",
                }}>
                  pend: {s.pend}
                </span>
              </div>
              <div style={{
                fontSize: "var(--fs-md)",
                fontWeight: isActive ? "var(--fw-bold)" : "var(--fw-semibold)",
                color: "var(--text)",
                marginBottom: 2,
              }}>
                {s.title}
              </div>
              <div style={{
                fontSize: "var(--fs-sm)",
                color: "var(--accent-mark)",
                fontFamily: "Source Code Pro, monospace",
                marginBottom: 6,
              }}>
                {s.subtitle}
              </div>
              <div style={{
                fontSize: "var(--fs-sm)",
                color: "var(--text-muted)",
                lineHeight: "var(--lh-base)",
              }}>
                {s.detail}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
