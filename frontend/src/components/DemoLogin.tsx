interface Props {
  onSignIn: () => void;
}

export default function DemoLogin({ onSignIn }: Props) {
  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "var(--space-5)",
      background: "var(--bg)",
    }}>
      <div style={{
        width: "min(440px, 100%)",
        background: "var(--surface)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-lg)",
        boxShadow: "var(--shadow-md)",
        padding: "var(--space-6) var(--space-6) var(--space-5)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "var(--space-4)",
      }}>
        <img
          src="/mongodb-leaf.svg"
          alt="MongoDB"
          width={140}
          height={36}
          style={{ display: "block" }}
        />

        <div style={{ textAlign: "center" }}>
          <span className="eyebrow eyebrow--accent">Demo Login</span>
          <h1 style={{
            margin: "6px 0 4px",
            fontSize: "var(--fs-lg)",
            fontWeight: "var(--fw-semibold)",
            color: "var(--text)",
            letterSpacing: "-0.01em",
          }}>
            Healthcare AI Demo
          </h1>
          <p style={{
            margin: 0,
            fontSize: "var(--fs-sm)",
            color: "var(--text-muted)",
          }}>
            Atlas · Voyage AI · Vector Search
          </p>
        </div>

        <button
          onClick={onSignIn}
          style={{
            width: "100%",
            background: "var(--brand)",
            color: "#fff",
            border: "1px solid var(--brand)",
            borderRadius: "var(--radius)",
            padding: "10px 16px",
            fontSize: "var(--fs-base)",
            fontWeight: "var(--fw-semibold)",
            cursor: "pointer",
            transition: "filter 0.15s",
          }}
          onMouseEnter={e => (e.currentTarget.style.filter = "brightness(1.08)")}
          onMouseLeave={e => (e.currentTarget.style.filter = "none")}
        >
          Sign in as Demo User
        </button>

        <p style={{
          margin: 0,
          fontSize: "var(--fs-xs)",
          color: "var(--text-faint)",
          textAlign: "center",
          lineHeight: "var(--lh-base)",
        }}>
          Cosmetic gate for presentation purposes only.
          No authentication is performed.
        </p>
      </div>
    </div>
  );
}
