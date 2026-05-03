from pydantic import BaseModel
from typing import List, Dict, Optional

class AlertState(BaseModel):
    message: str
    severity: Optional[str] = None
    alert_type: Optional[str] = None
    service: Optional[str] = None
    root_cause: Optional[str] = None
    recommendation: Optional[str] = None
    similar_incidents: List[Dict] = []
    decision: Optional[str] = None
    remediation_plan: List[Dict] = []
    execution_status: Optional[str] = None
    validation_status: Optional[str] = None