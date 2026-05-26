#!/usr/bin/env bash
# =============================================================================
# Healthcare Demo — Start/Stop Script
#
# Usage:
#   ./start.sh               — start backend + frontend
#   ./start.sh --reset       — soft reset (keep embedding), then start
#   ./start.sh --reset-hard  — full reset (clear embedding too), then start
#   ./start.sh --stop        — stop running services
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/.demo.pids"

# ── Parse flags ──────────────────────────────────────────────────
RESET=0
RESET_HARD=0
STOP=0
for arg in "$@"; do
  case "$arg" in
    --reset|-r)      RESET=1 ;;
    --reset-hard)    RESET=1; RESET_HARD=1 ;;
    --stop|-s)       STOP=1 ;;
    *) echo "Usage: $0 [--reset | --reset-hard | --stop]"; exit 1 ;;
  esac
done

# ── Stop ─────────────────────────────────────────────────────────
stop_services() {
  if [ -f "$PID_FILE" ]; then
    # shellcheck disable=SC1090
    source "$PID_FILE"
    echo "  Stopping backend  (pid $BACKEND_PID)..."
    # Kill the process group so npm-spawned children (e.g. the Vite grandchild) also die
    kill -- "-$(ps -o pgid= -p "$BACKEND_PID"  2>/dev/null | tr -d ' ')" 2>/dev/null || kill "$BACKEND_PID"  2>/dev/null || true
    echo "  Stopping frontend (pid $FRONTEND_PID)..."
    kill -- "-$(ps -o pgid= -p "$FRONTEND_PID" 2>/dev/null | tr -d ' ')" 2>/dev/null || kill "$FRONTEND_PID" 2>/dev/null || true
    sleep 1
    rm -f "$PID_FILE"
  else
    # No PID file — fall back to port-based kill
    echo "  No PID file found — stopping by port..."
    fuser -k 8001/tcp 2>/dev/null || true
    fuser -k 5173/tcp 2>/dev/null || true
    sleep 1
  fi
  echo "  Done."
}

if [ "$STOP" -eq 1 ]; then
  echo ""
  echo "============================================================"
  echo "  Healthcare Demo — Stopping"
  echo "============================================================"
  echo ""
  stop_services
  echo ""
  exit 0
fi

# ── Ensure backend venv exists & is activated ───────────────────
# voyageai 0.3.7 requires Python >=3.9,<3.14 — pick a compatible interpreter.
ensure_backend_venv() {
  if [ ! -f "$SCRIPT_DIR/backend/.venv/bin/activate" ]; then
    local py=""
    for candidate in python3.13 python3.12 python3.11 python3.10 python3.9 python3; do
      if command -v "$candidate" >/dev/null 2>&1; then
        # Verify version is < 3.14
        if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info < (3,14) else 1)' 2>/dev/null; then
          py="$candidate"
          break
        fi
      fi
    done
    if [ -z "$py" ]; then
      echo "ERROR: no Python 3.9–3.13 found on PATH (required by voyageai)."
      echo "  Install one, e.g.: brew install python@3.12"
      exit 1
    fi
    echo "  Creating backend Python venv using $py ($("$py" --version 2>&1))..."
    "$py" -m venv "$SCRIPT_DIR/backend/.venv"
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/backend/.venv/bin/activate"
    echo "  Installing backend dependencies (this may take a minute)..."
    pip install --quiet --upgrade pip
    pip install --quiet -r "$SCRIPT_DIR/backend/requirements.txt"
  else
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/backend/.venv/bin/activate"
  fi
}

# ── Ensure .env exists ───────────────────────────────────────────
if [ ! -f .env ]; then
  echo "ERROR: .env not found."
  echo "  cp .env.example .env  and fill in your credentials."
  exit 1
fi

# ── Stop any already-running instance ────────────────────────────
if [ -f "$PID_FILE" ]; then
  echo "  Stopping previous instance..."
  stop_services
  sleep 1
fi

echo ""
echo "============================================================"
echo "  Healthcare Demo — Starting"
echo "============================================================"
echo ""

# ── Optional reset ───────────────────────────────────────────────
if [ "$RESET" -eq 1 ]; then
  ensure_backend_venv
  cd backend
  if [ "$RESET_HARD" -eq 1 ]; then
    echo "  Resetting demo claims (hard — embedding + rationale cleared)..."
    python ../scripts/reset_demo.py --hard
  else
    echo "  Resetting demo claims (soft — rationale cleared, embedding preserved)..."
    python ../scripts/reset_demo.py
  fi
  cd "$SCRIPT_DIR"
  echo ""
fi

# ── Backend ──────────────────────────────────────────────────────
echo "  [1/2] Starting FastAPI backend on http://localhost:8001 ..."
ensure_backend_venv
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 --reload \
  >> "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

sleep 2  # give backend a moment to bind

# ── Frontend ─────────────────────────────────────────────────────
echo "  [2/2] Starting Vite frontend on http://localhost:5173 ..."
cd frontend
npm run dev -- --host \
  >> "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

# Save PIDs so --stop can find them later
echo "BACKEND_PID=$BACKEND_PID" > "$PID_FILE"
echo "FRONTEND_PID=$FRONTEND_PID" >> "$PID_FILE"

echo ""
echo "============================================================"
echo "  Demo running:"
echo "    Frontend: http://localhost:5173"
echo "    Backend:  http://localhost:8001"
echo "    API docs: http://localhost:8001/docs"
echo ""
echo "  Logs:     tail -f backend.log  |  tail -f frontend.log"
echo "  To stop:  ./start.sh --stop"
echo "  Press Ctrl+C to stop both services."
echo "============================================================"
echo ""

# ── Cleanup on exit ──────────────────────────────────────────────
cleanup() {
  echo ""
  echo "  Stopping demo..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  rm -f "$PID_FILE"
  echo "  Done."
}
trap cleanup INT TERM

wait "$BACKEND_PID" "$FRONTEND_PID"
