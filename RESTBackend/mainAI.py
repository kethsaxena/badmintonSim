# backend/main.py
import asyncio
import uuid
from dataclasses import dataclass
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# If your wheel’s distribution is "badsim" but the package inside is "simengine",
# keep this try/except so both work:
try:
    from simengine import BadmintonMatch
except ImportError:
    from badsim import BadmintonMatch  # only if your package dir is actually 'badsim'

app = FastAPI(title="Badminton CRUD Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# --- In-memory store for multiple matches ---
@dataclass
class MatchState:
    match: BadmintonMatch
    lock: asyncio.Lock
    per_rally_delay: float = 0.0  # pacing managed by backend (seconds)

matches: Dict[str, MatchState] = {}

# ---------- CREATE ----------
@app.post("/matches")
async def create_match(
    player1: str = Query("Player A"),
    player2: str = Query("Player B"),
    target_duration: Optional[str] = Query(None, description="e.g. 60, 1m, 1h"),
    estimated_rallies: int = Query(150, ge=1),
):
    """Create a new match (CRUD: Create) and return match_id."""
    m = BadmintonMatch(player1, player2)
    # Avoid blocking sleeps in engine for web; pace from backend if desired
    try:
        m.set_match_duration(0)
    except Exception:
        pass

    per_rally = _parse_duration_to_seconds(target_duration) / estimated_rallies if target_duration else 0.0
    match_id = uuid.uuid4().hex
    matches[match_id] = MatchState(m, asyncio.Lock(), per_rally_delay=max(per_rally, 0.0))
    return {"match_id": match_id, "players": [player1, player2]}

# ---------- READ ----------
@app.get("/matches/{match_id}")
async def read_match(match_id: str):
    """Get current state/summary (CRUD: Read)."""
    st = _get_state(match_id)
    m = st.match
    return {
        "match_id": match_id,
        "over": m.match_over(),
        "score": m.scores_display(),
        "games": m.games_display(),
        "scoreline": " | ".join(f"{a}-{b}" for a, b in m.set_scores),
        "summary": m.final_summary(),
    }

# ---------- UPDATE (simulate one rally) ----------
@app.post("/matches/{match_id}/rallies")
async def play_rally(match_id: str):
    """Advance by exactly one rally (CRUD: Update)."""
    st = _get_state(match_id)
    async with st.lock:
        if st.match.match_over():
            return {"message": "already_finished", "summary": st.match.final_summary()}
        msg = st.match.rally()
    return {
        "event": "rally",
        "message": msg,
        "score": st.match.scores_display(),
        "games": st.match.games_display(),
    }

# ---------- UPDATE (simulate full match) ----------
@app.post("/matches/{match_id}/simulate-full")
async def simulate_full(match_id: str):
    """Run until the match ends (CRUD: Update)."""
    st = _get_state(match_id)
    async with st.lock:
        while not st.match.match_over():
            st.match.rally()
            if st.per_rally_delay > 0:
                await asyncio.sleep(st.per_rally_delay)
        summary = st.match.final_summary()
    return {"message": "finished", "summary": summary}

# ---------- UPDATE (adjust pacing) ----------
@app.patch("/matches/{match_id}/duration")
async def set_pacing(
    match_id: str,
    target_duration: str = Query(..., description="e.g. 60, 1m, 1h"),
    estimated_rallies: int = Query(150, ge=1),
):
    """Change pacing for this match (optional helper)."""
    st = _get_state(match_id)
    secs = _parse_duration_to_seconds(target_duration)
    st.per_rally_delay = max(secs / float(estimated_rallies), 0.0)
    return {"message": "pacing_updated", "per_rally_delay": st.per_rally_delay}

# ---------- DELETE ----------
@app.delete("/matches/{match_id}")
async def delete_match(match_id: str):
    """Delete a match (CRUD: Delete)."""
    if match_id in matches:
        del matches[match_id]
        return {"message": "deleted", "match_id": match_id}
    raise HTTPException(status_code=404, detail="match_id not found")

# --------- helpers ---------
def _get_state(match_id: str) -> MatchState:
    st = matches.get(match_id)
    if not st:
        raise HTTPException(status_code=404, detail="match_id not found")
    return st

def _parse_duration_to_seconds(s: Optional[str]) -> int:
    s = (s or "").strip().lower()
    if not s: return 0
    if s.endswith("h"): return int(s[:-1]) * 3600
    if s.endswith("m") and s != "m": return int(s[:-1]) * 60
    return int(s)
