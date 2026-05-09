# High-Level Design (HLD) - Email Alert Management System

## 1. Overview
The Email Alert Management System is an AI-powered SRE (Site Reliability Engineering) tool designed to autonomously handle incoming email alerts. It uses a multi-agent architecture orchestrated by LangGraph to classify, investigate, and remediate issues, reducing manual intervention and improving response times.

## 2. Architecture Diagram (Textual)
```text
[Incoming Alert] -> [FastAPI Endpoint]
                          |
                          v
                  [LangGraph Workflow]
                          |
        +-----------------+-----------------+
        |                 |                 |
 [Classifier Agent] -> [Retriever Agent] -> [Decision Agent]
                                            |
                                            | (Auto-Remediate?)
                                            v
 [Validator Agent] <--- [Executor Agent] <--- [Planner Agent]
        |                                   ^
        |                                   |
        +------------> [Learning Agent] <---+
```

## 3. Key Components

### 3.1. API Layer (FastAPI)
- Acts as the entry point for alerts.
- Provides a `POST /alert` endpoint.
- Integrates with Prometheus for metrics collection and OpenTelemetry for tracing.

### 3.2. Agent Orchestration (LangGraph)
- Uses `StateGraph` to manage the flow of data between specialized agents.
- Maintains the `AlertState` object throughout the lifecycle of an alert.

### 3.3. Specialized Agents
- **Classifier Agent:** Parses the alert and determines its type and severity.
- **Retriever Agent:** Fetches relevant logs, metrics, or documentation from historical data.
- **Decision Agent:** Determines if the alert can be auto-remediated or needs manual intervention.
- **Planner Agent:** Creates a step-by-step remediation plan.
- **Approval Agent:** (Hooks into workflow) Waits for manual approval if required.
- **Executor Agent:** Executes the remediation steps (e.g., restarting a service, scaling resources).
- **Validator Agent:** Verifies if the remediation was successful.
- **Learning Agent:** Updates the knowledge base with the outcome of the alert.

### 3.4. Infrastructure (Terraform)
- **AWS:** Provisions EKS (Elastic Kubernetes Service) with managed node groups.
- **GCP:** Provisions GKE (Google Kubernetes Engine) with preemptible node pools for cost efficiency.
- **Networking:** VPCs, Subnets, and Security Groups/Firewall rules.

### 3.5. Observability
- **Prometheus:** Metrics collection.
- **Grafana:** Dashboards for visualization.
- **Jaeger:** Distributed tracing for agent execution steps.

## 4. Tech Stack
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Orchestration:** LangGraph (LangChain ecosystem)
- **Infrastructure:** Terraform
- **Cloud Providers:** AWS, GCP
- **Containerization:** Docker, Kubernetes (EKS/GKE)
- **Monitoring:** Prometheus, Grafana, Jaeger

## 5. Data Flow
1. An external system (e.g., monitoring tool) sends an alert payload to the FastAPI `/alert` endpoint.
2. The endpoint invokes the `process_alert` worker.
3. The worker initializes the `AlertState` and triggers the LangGraph.
4. The graph executes agents in sequence or conditionally based on the state.
5. The final result (remediated or escalated) is returned to the API caller.
