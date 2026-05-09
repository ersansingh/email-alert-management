# Low-Level Design (LLD) - Email Alert Management System

## 1. Data Models

### 1.1. AlertState (Pydantic)
The `AlertState` is the central object passed between agents.
- `message`: `str` (The raw alert message)
- `severity`: `Optional[str]` (e.g., Critical, Warning, Info)
- `alert_type`: `Optional[str]` (e.g., DiskUsage, CPUBurst, Connectivity)
- `service`: `Optional[str]` (The affected service name)
- `root_cause`: `Optional[str]` (Identified cause)
- `recommendation`: `Optional[str]` (Initial recommendation)
- `similar_incidents`: `List[Dict]` (Retrieved historical data)
- `decision`: `Optional[str]` (auto_remediate or escalate)
- `remediation_plan`: `List[Dict]` (Steps to fix the issue)
- `execution_status`: `Optional[str]` (Success/Failure of executor)
- `validation_status`: `Optional[str]` (Outcome of verification)

## 2. Agent Details

### 2.1. Classifier Agent
- **Input:** `AlertState` (raw message)
- **Logic:** Uses an LLM to extract structured fields (severity, alert_type, service).
- **Output:** Updates `severity`, `alert_type`, and `service` in `AlertState`.

### 2.2. Retriever Agent
- **Input:** `AlertState` (alert_type, service)
- **Logic:** Queries a vector database or historical logs to find similar past incidents.
- **Output:** Updates `similar_incidents`.

### 2.3. Decision Agent
- **Input:** `AlertState` (severity, similar_incidents)
- **Logic:** Evaluates if the incident is safe for automatic remediation based on confidence and policy.
- **Output:** Sets `decision` to "auto_remediate" or "escalate".

### 2.4. Planner Agent
- **Input:** `AlertState` (root_cause, similar_incidents)
- **Logic:** Generates a list of commands or API calls to fix the issue.
- **Output:** Updates `remediation_plan`.

### 2.5. Executor Agent
- **Input:** `AlertState` (remediation_plan)
- **Logic:** Iterates through the plan and executes actions (e.g., via Kubernetes API or SSH).
- **Output:** Sets `execution_status`.

### 2.6. Validator Agent
- **Input:** `AlertState` (service, alert_type)
- **Logic:** Checks metrics or health endpoints to confirm the issue is resolved.
- **Output:** Sets `validation_status`.

## 3. Workflow Graph (LangGraph)
Defined in `app/agents/graph.py`:
- **Nodes:** `classifier`, `retriever`, `decision`, `planner`, `approval`, `executor`, `validator`, `learning`.
- **Edges:**
  - `classifier` -> `retriever`
  - `retriever` -> `decision`
  - `decision` -> `planner` (if decision == "auto_remediate")
  - `decision` -> `learning` (if decision != "auto_remediate")
  - `planner` -> `approval`
  - `approval` -> `executor`
  - `executor` -> `validator`
  - `validator` -> `learning`

## 4. API Endpoints

### 4.1. `POST /alert`
- **Payload:** `{"message": "..."}`
- **Response:** `{"status": "processed", "result": {...}}`
- **Internal:** Calls `app.workers.agent_worker.process_alert`.

## 5. Infrastructure Details

### 5.1. AWS Module (`infra/modules/compute/aws`)
- `aws_eks_cluster`: Managed Kubernetes cluster.
- `aws_eks_node_group`: Uses `t3.medium` instances.
- `aws_iam_role`: Cluster and Node roles with necessary policies.

### 5.2. GCP Module (`infra/modules/compute/gcp`)
- `google_container_cluster`: GKE cluster.
- `google_container_node_pool`: Uses `e2-medium` preemptible nodes to reduce costs.

## 6. Observability
- **Prometheus Metrics:**
  - `processed_alerts_total`: Counter for successful/failed alerts.
  - `alert_processing_duration_seconds`: Histogram for latency.
- **Jaeger Tracing:** Instrumented via OpenTelemetry to track agent execution time and errors.
