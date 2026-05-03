from fastapi import FastAPI
from app.workers.agent_worker import process_alert
from prometheus_client import make_asgi_app, Counter, Histogram
import time

# Metrics
ALERT_COUNT = Counter("processed_alerts_total", "Total count of processed alerts", ["status"])
PROCESSING_TIME = Histogram("alert_processing_duration_seconds", "Time spent processing an alert")

app = FastAPI()

# Add prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.post("/alert")
async def handle_alert(payload: dict):
    start_time = time.time()
    try:
        result = process_alert(payload)
        ALERT_COUNT.labels(status="success").inc()
        return {"status": "processed", "result": result}
    except Exception as e:
        ALERT_COUNT.labels(status="error").inc()
        raise e
    finally:
        PROCESSING_TIME.observe(time.time() - start_time)