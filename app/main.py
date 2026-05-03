from fastapi import FastAPI
from app.workers.agent_worker import process_alert

app = FastAPI()

@app.post("/alert")
async def handle_alert(payload: dict):
    result = process_alert(payload)
    return {"status": "processed", "result": result}