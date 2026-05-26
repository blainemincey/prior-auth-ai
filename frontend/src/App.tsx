import { useState, useEffect } from "react";
import type { Scenario, Step, ClaimRecord, EmbeddingResult, SearchResult, RationaleResult, SearchMode } from "./types";
import { api } from "./api";
import Header from "./components/Header";
import ScenarioSelector from "./components/ScenarioSelector";
import StepTabs from "./components/StepIndicator";
import ClaimSummaryBar from "./components/ClaimSummaryBar";
import ClaimRecordPanel from "./components/ClaimRecord";
import EmbeddingStep from "./components/EmbeddingStep";
import SearchStep, { type SearchFilters } from "./components/SearchStep";
import ContextPanel from "./components/ContextPanel";
import RationalePanel from "./components/RationalePanel";
import DemoLogin from "./components/DemoLogin";

const AUTH_KEY = "demo_signed_in";
const STATE_KEY = "demo_state_v1";

type ScenarioSnapshot = {
  step: Step;
  activeTab: Step;
  claim: ClaimRecord | null;
  embedding: EmbeddingResult | null;
  searchFilters: SearchFilters;
  searchMode: SearchMode;
  searchResult: SearchResult | null;
  rationale: RationaleResult | null;
};

type DemoState = ScenarioSnapshot & {
  scenario: Scenario | null;
  snapshots: Partial<Record<Scenario, ScenarioSnapshot>>;
  loading: boolean;
  error: string | null;
};

const initial: DemoState = {
  scenario: null,
  step: 1,
  activeTab: 1,
  claim: null,
  embedding: null,
  searchFilters: { planType: "", state: "", outcome: "" },
  searchMode: "vector",
  searchResult: null,
  rationale: null,
  snapshots: {},
  loading: false,
  error: null,
};

function snapshotFrom(s: DemoState): ScenarioSnapshot {
  return {
    step: s.step,
    activeTab: s.activeTab,
    claim: s.claim,
    embedding: s.embedding,
    searchFilters: s.searchFilters,
    searchMode: s.searchMode,
    searchResult: s.searchResult,
    rationale: s.rationale,
  };
}

function loadPersistedState(): DemoState {
  try {
    const raw = localStorage.getItem(STATE_KEY);
    if (!raw) return initial;
    const saved = JSON.parse(raw) as Partial<DemoState>;
    // Always start fresh for transient fields so a refresh mid-fetch
    // doesn't leave the UI stuck in a loading or error state.
    return { ...initial, ...saved, loading: false, error: null };
  } catch {
    return initial;
  }
}

export default function App() {
  const [state, setState] = useState<DemoState>(() => loadPersistedState());
  const [signedIn, setSignedIn] = useState<boolean>(
    () => localStorage.getItem(AUTH_KEY) === "true"
  );

  useEffect(() => {
    try {
      localStorage.setItem(
        STATE_KEY,
        JSON.stringify({ ...state, loading: false, error: null })
      );
    } catch {
      // ignore quota / serialization errors — demo persistence is best-effort
    }
  }, [state]);

  function signIn() {
    localStorage.setItem(AUTH_KEY, "true");
    setSignedIn(true);
  }

  function signOut() {
    localStorage.removeItem(AUTH_KEY);
    localStorage.removeItem(STATE_KEY);
    setSignedIn(false);
    setState(initial);
  }

  if (!signedIn) {
    return <DemoLogin onSignIn={signIn} />;
  }

  function set(patch: Partial<DemoState>) {
    setState((s) => ({ ...s, ...patch }));
  }

  async function selectScenario(scenario: Scenario) {
    if (state.scenario === scenario) return;

    // Snapshot the outgoing scenario's progress so switching back restores it.
    const snapshots = state.scenario
      ? { ...state.snapshots, [state.scenario]: snapshotFrom(state) }
      : state.snapshots;

    // If we've worked on this scenario before, restore it instead of refetching.
    const restored = snapshots[scenario];
    if (restored) {
      set({ ...restored, scenario, snapshots, loading: false, error: null });
      return;
    }

    // Fresh load.
    set({ ...initial, snapshots, scenario, loading: true, error: null });
    try {
      const claim = await api.getClaim(scenario);
      // Seed filter defaults from the claim so the first search is pre-configured
      const searchFilters: SearchFilters = {
        planType: claim.plan_type || "",
        state: claim.state || "",
        outcome: "",
      };
      set({ claim, searchFilters, step: 1, activeTab: 1, loading: false });
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  async function runEmbed() {
    if (!state.scenario) return;
    set({ loading: true, error: null });
    try {
      const embedding = await api.generateEmbedding(state.scenario);
      const claim = await api.getClaim(state.scenario);
      // Advance to the Vector Search tab so the next action is immediately visible
      set({ embedding, claim, step: 2, activeTab: 3, loading: false });
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  async function runSearch(filters: Record<string, string | undefined>, mode: SearchMode) {
    if (!state.scenario) return;
    set({ loading: true, error: null, searchMode: mode });
    try {
      const searchResult = await api.runSearch(state.scenario, filters, mode);
      // Advance to Retrieved Context to show results immediately
      set({ searchResult, step: 3, activeTab: 4, loading: false });
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  async function runSoftReset() {
    set({ loading: true, error: null });
    try {
      await api.softResetAll();
      // Return to blank slate — user re-selects scenario to reload
      setState(initial);
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  async function runRationale() {
    if (!state.scenario || !state.searchResult) return;
    set({ loading: true, error: null });
    try {
      const rationale = await api.generateRationale(
        state.scenario,
        state.searchResult.policies,
        state.searchResult.prior_claims
      );
      set({ rationale, step: 5, activeTab: 5, loading: false });
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  const { scenario, step, activeTab, claim, embedding, searchFilters, searchMode, searchResult, rationale, loading, error } = state;

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Header
        onReset={runSoftReset}
        resetEnabled={!!claim}
        resetting={loading}
        onSignOut={signOut}
      />

      <main style={{ flex: 1, maxWidth: 1200, margin: "0 auto", padding: "0 24px 48px", width: "100%" }}>
        <ScenarioSelector active={scenario} onSelect={selectScenario} disabled={loading} />

        {error && (
          <div style={{
            margin: "12px 0",
            padding: "10px 16px",
            background: "rgba(255,105,96,0.12)",
            border: "1px solid rgba(255,105,96,0.3)",
            borderRadius: "var(--radius)",
            color: "var(--mdb-error)",
            fontSize: 13,
          }}>
            {error}
          </div>
        )}

        {claim && (
          <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 16 }}>
            {/* Claim summary — always visible, updates in place when rationale writes back */}
            <ClaimSummaryBar claim={claim} rationale={rationale} />

            {/* Tab nav */}
            <StepTabs
              step={step}
              activeTab={activeTab}
              onTabClick={(tab) => set({ activeTab: tab })}
            />

            {/* Active tab panel */}
            <div className="fade-in" key={activeTab} style={{ marginTop: 4 }}>
              {activeTab === 1 && (
                <ClaimRecordPanel
                  claim={rationale ? rationale.updated_claim : claim}
                  updated={!!rationale}
                />
              )}

              {activeTab === 2 && (
                <EmbeddingStep
                  embedding={embedding}
                  loading={loading}
                  onEmbed={runEmbed}
                  alreadyDone={step >= 2}
                />
              )}

              {activeTab === 3 && (
                <SearchStep
                  claim={claim}
                  filters={searchFilters}
                  onFiltersChange={(f) => set({ searchFilters: f })}
                  mode={searchMode}
                  onModeChange={(m) => set({ searchMode: m })}
                  loading={loading}
                  onSearch={runSearch}
                  alreadyDone={step >= 3}
                />
              )}

              {activeTab === 4 && searchResult && (
                <ContextPanel result={searchResult} />
              )}

              {activeTab === 4 && !searchResult && (
                <div style={{ padding: "40px 0", textAlign: "center", color: "var(--mdb-text-dim)", fontSize: 13 }}>
                  Run Vector Search (tab 3) to retrieve policies and prior cases.
                </div>
              )}

              {activeTab === 5 && (
                <RationalePanel
                  result={rationale}
                  loading={loading}
                  onGenerate={runRationale}
                />
              )}
            </div>
          </div>
        )}

        {!claim && !loading && !error && (
          <div style={{ textAlign: "center", marginTop: 80, color: "var(--mdb-text-dim)" }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>⬆</div>
            <p style={{ fontSize: 16, marginBottom: 8 }}>Select a demo scenario above to begin.</p>
            <p style={{ fontSize: 13 }}>
              Scenario A — MRI Prior Auth &nbsp;·&nbsp; Scenario B — Infliximab Infusion &nbsp;·&nbsp; Scenario C — GLP-1 / Semaglutide
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
