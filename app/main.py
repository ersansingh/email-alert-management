from fastapi import FastAPI
from app.agents.classifier_agent import classifier_agent
from app.agents.decision_agent import decision_agent
from app.agents.executor_agent import executor_agent
from app.agents.state import AlertState
from prometheus_client import make_asgi_app, Counter, Histogram
import time

# Metrics
ALERT_COUNT = Counter("processed_alerts_total", "Total count of processed alerts", ["status"])
PROCESSING_TIME = Histogram("alert_processing_duration_seconds", "Time spent processing an alert")

app = FastAPI()

# Add prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.post("/agents/classifier")
async def run_classifier(state: AlertState):
    start_time = time.time()
    try:
        result = classifier_agent(state.dict())
        ALERT_COUNT.labels(status="classifier_success").inc()
        return result
    finally:
        PROCESSING_TIME.observe(time.time() - start_time)

@app.post("/agents/decision")
async def run_decision(state: AlertState):
    return decision_agent(state.dict())

@app.post("/agents/executor")
async def run_executor(state: AlertState):
    return executor_agent(state.dict())