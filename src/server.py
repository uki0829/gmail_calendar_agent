import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.agent import Agent
import uvicorn
import threading

app = FastAPI()

# Allow CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to the extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Agent Instance
# Poll every 60 seconds by default
agent = Agent(poll_interval=60)

@app.get("/status")
def get_status():
    return {"status": agent.status, "running": agent.running}

@app.post("/start")
def start_agent(background_tasks: BackgroundTasks):
    if not agent.running:
        # The agent.start() method already spawns a thread, so we can call it directly.
        # However, to be safe and non-blocking for the API, we can use BackgroundTasks 
        # or just rely on the agent's internal threading.
        # Agent.start() is non-blocking (spawns thread), so this is fine.
        agent.start()
        return {"message": "Agent started"}
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.agent import Agent
import uvicorn
import threading

app = FastAPI()

# Allow CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to the extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Agent Instance
# Poll every 60 seconds by default
agent = Agent(poll_interval=60)

@app.post("/start")
def start_agent(background_tasks: BackgroundTasks):
    if not agent.running:
        # The agent.start() method already spawns a thread, so we can call it directly.
        # However, to be safe and non-blocking for the API, we can use BackgroundTasks 
        # or just rely on the agent's internal threading.
        # Agent.start() is non-blocking (spawns thread), so this is fine.
        agent.start()
        return {"message": "Agent started"}
    return {"message": "Agent already running"}

@app.post("/stop")
def stop_agent():
    if agent.running:
        agent.stop()
        return {"message": "Agent stopped"}
    return {"message": "Agent is not running"}

@app.get("/status")
async def status():
    return {
        "status": agent.status,
        "running": agent.running,
        "stats": agent.stats
    }

@app.get("/recent_emails")
async def recent_emails():
    return {"emails": agent.recent_emails}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
