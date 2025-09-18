# BadmintonSim Examples

This directory contains example projects and usage guides for **BadmintonSim**, a badminton match simulation library.

## Getting Started
1. Clone the repository:
```
git clone https://github.com/yourusername/badmintonSim.git    
```
## How to Run Locally

1. Activate project:
    ```
    python projSetup.py
    ```
2. Run a game using python Shim
    ### Desktop Tkinter App
    ```
    py examples\deskApp.py
    ```
    ### Game1 Application Script
    ```
    py examples\deskApp.py
    ```
## Author
Developed by [Praketa Saxena](https://github.com/kethsaxena)

## Last Edit
_Last updated: 8 Sep 2025_


## 🏸 Badminton Simulation Roadmap & Checklist

This document tracks all phases of the project with detailed subtasks.

### Phase 1: Core Engine
- [x] Implement rally simulation with BWF scoring rules  
- [x] Add Best-of-3 match logic (win by 2, cap at 30)  
- [x] Track set scores (e.g., `21-15 | 18-21 | 21-17`)  
- [x] Add start/end time with frozen duration  
- [x] Implement configurable pacing (`set_match_duration`)  
- [x] Package engine into `simEngine/`  

### Phase 2: Desktop App (Tkinter)
- [x] Create GUI with scoreboard + match log  
- [x] Implement full match simulation (not just rallies/games)  
- [x] Accept pacing input (`60`, `1m`, `1h`)  
- [x] Display final **scoreline** (e.g., `Scoreline: 21-11 | 21-12`)  
- [x] Add reset button to clear screen and start a new match  
- [ ] Add player name input before starting match (optional)  
- [ ] Add export results (CSV/JSON) feature (optional)  

### Phase 3: Backend (FastAPI)
- [x] Create FastAPI app (crud).py.
- [x] Integrate dependency injection (Depends(get_db)).
- [x] Add /matches POST endpoint to create a match.
- [] Add /matches GET endpoint to list all matches with the just matchID column.
- [] Add /matches/{id} GET endpoint to fetch a single match info current state.
- [] Add /matches/{id} PUT endpoint to update a match state.
- [] Add /matches/{id} DELETE endpoint to delete a match.

✅ Deliverable for Phase 3

[] Backend running on old Windows PC
[] Accessible from LAN devices (desktop, monitor, mobile, browser)
[] Optionally exposed to the internet via ngrok or port forwarding

### Step 1: Backend Skeleton 
- [x] Create `backend/` folder  
- [x] Add `main.py` with a minimal FastAPI app  
- [x] Add `requirements.txt`:
    ```
  fastapi
  localBadSim
      ```

    [ ] **Database Setup (SQLite3)**
  - [ ] Use `sqlite3` or `SQLAlchemy` for ORM  
  - [ ] Create `matches.db` file inside `backEnd/`  
  - [ ] Define `Match` model with fields:
    - `id` (primary key, UUID or int)
    - `player_a`, `player_b`
    - `set_scores` (JSON string, e.g. `["21-11", "21-12"]`)
    - `final_winner`
    - `start_time`, `end_time`
    - `duration_seconds`
  - [ ] Initialize DB on app startup if not exists  
### Step 2: Match Management (REST API)
- [] Import BadmintonMatch from simEngine
- [] Implement POST /start_match?player1=X&player2=Y → create new match
- [] Implement GET /summary → return current or final summary

## Step 3: Simulation Endpoint
- [] Implement POST /simulate_match → run full match rally-by-rally
- [] Return final summary after match ends
- [] Print/log updates locally first (before WebSocket)

## Step 5: Live Updates via WebSocket
- [] Add /ws endpoint
- [] On each rally → broadcast JSON update
- [] On match end → broadcast final summary
- [] Test with WebSocket client (Postman, browser, etc.)

## Step 6: Local Deployment on Windows PC
- [] Install Python + pip
- [] Create virtual environment (venv)
- [] Install dependencies:
- [] pip install -r requirements.txt 
- [] Run locally: 

'''
- uvicorn main:app --host 0.0.0.0 --port 8000
- Verify API is available at:
- http://127.0.0.1:8000 (same PC)
- http://<LAN-IP>:8000 (other devices on WiFi)
'''
## Step 7: Make Service Persistent (Optional)
 [] Configure Windows Task Scheduler or NSSM to auto-run uvicorn
 [] Confirm backend stays up after reboot
## Step 8: (Optional) External Access
 [] Install ngrok → expose port 8000 to internet
 [] Or configure router port forwarding → http://<public-ip>:8000


langraph
langraph cloud 
langsmith 
agent
lcel 
