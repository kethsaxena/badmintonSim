import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from dataclasses import dataclass, field
from RESTBackend.crud import init_db, insert_match,get_connection
from enum import Enum
from importlib.metadata import version
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from projEnums import matchType
from simEngine.badmintonDouble import BadmintonMatch
from typing import Dict, Optional, Annotated
import uuid


VERsimengine = version("badsimengine")
@asynccontextmanager
async def lifespanBad(app: FastAPI):
    #Iniitate SQLlite DB
    conn =  get_connection()
    init_db(conn)
    yield
    conn.close()
    
app = FastAPI(title="Badminton Simulation Backend",
               version=f"{VERsimengine}",
               lifespan=lifespanBad)

DB_FILE = Path(__file__).parent / "matches.db"

# MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

#toDo
# IN MEMORY STATE 
@dataclass 
class MatchState:
    match: BadmintonMatch
    lock:asyncio.Lock = field(default_factory=asyncio.Lock)
    per_rally_delay: float = 0.0

#In memory Database
matches: Dict[str, MatchState] = {}

# ROUTES
@app.get("/")
async def root():
    return {"message": "Badminton Simulation App"}


@app.post("/creatematch")
async def create_match(
    # Function Parameters
    gameEvent : Annotated[matchType,Query(description="Badminton game type")]  = matchType.menSingles,
    player1: Annotated[str | None, Query(max_length=50)]  = "Player 1",
    player2: Annotated[str | None, Query(max_length=50)] = "Player 2",
    target_duration: Optional[str] = Query(None, description="e.g. 60, 1m, 1h"),
    estimated_rallies: int = Query(150, ge=1), # Max Number Rallies that can occur should be greater than equal to 1
    player3: Annotated[str | None, Query(max_length=50)] = None,
    player4: Annotated[str | None, Query(max_length=50)] = None
    ##########################################
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

    starttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # insert_match(player_a, player_b, gametype, "pending", starttime)
    return {"match_id": match_id,"event":{gameEvent}, "players": [player1, player2]}


# GET 
@app.get("/matchinfo/{match_id}")
async def read_match(match_id: str):
    """Get current state/summary (CRUD: Read)."""
    st = _get_state(match_id)
    m = st.match
    return {
        "match_id": match_id,
        "event": m.gameType,
        "over": m.match_over(),
        "score": m.scores_display(),
        "games": m.games_display(),
        "scoreline": " | ".join(f"{a}-{b}" for a, b in m.set_scores),
        "summary": m.final_summary(),
    }

# todo 
@app.get("/show_summary/{match_id}")
async def root():
    return {"message": "Hello World"}

#todo 
# PUT 
# @app.put("/simulate_match")
# async def root():
#     match = BadmintonMatch("Player A", "Player B")

#todo 
# @app.put("/modify/{set_duration}")

#todo 
# @app.put("/reset_match")

#todo 
# WEBSOCKETS
# @app.websocket("/ws")
# async def ws(websocket: WebSocket):
#     await websocket.accept()
#     clients.append(websocket)
#     try:
#         await websocket.send_text(json.dumps({"event": "hello", "message": "connected"}))
#         while True: await websocket.receive_text()  # keepalive
#     except WebSocketDisconnect:
#         if websocket in clients: clients.remove(websocket)

# HELPER FUNCTIONS
def _parse_duration_to_seconds(s: Optional[str]) -> int:
    s = (s or "").strip().lower()
    if not s: return 0
    if s.endswith("h"): return int(s[:-1]) * 3600
    if s.endswith("m") and s != "m": return int(s[:-1]) * 60
    return int(s)

def _get_state(match_id: str) -> MatchState:
    st = matches.get(match_id)
    if not st:
        raise HTTPException(status_code=404, detail="match_id not found")
    return st
