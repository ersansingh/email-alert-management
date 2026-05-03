# Email Alert Management System

This system uses a multi-agent architecture orchestrated by **n8n** to process and remediate email alerts.

## Getting Started

1. Install requirements: `pip install -r requirements.txt`
2. Run the application (using FastAPI): `uvicorn app.main:app --reload`
3. Infrastructure deployment:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

---

## Local Testing with Docker Desktop

This project is optimized for local testing using Docker Desktop, providing a complete replica of the cloud environment including mocked services and observability tools.

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- (Optional) `docker-compose` CLI.

### 2. Launch the Local Stack
To spin up the application, database, local mocks, and monitoring tools, run:
```bash
docker-compose -f docker-compose.local.yml up --build
```

### 3. Service Access
Once running, you can access the following services:
- **FastAPI Application:** `http://localhost:8000` (Individual Agent Endpoints)
- **n8n (Orchestration):** `http://localhost:5678`
- **Prometheus (Metrics):** `http://localhost:9090`
- **Grafana (Dashboards):** `http://localhost:3000` (Default: admin/admin)
- **Jaeger (Tracing):** `http://localhost:16686`
- **LocalStack (Cloud Mocks):** `http://localhost:4566`
- **Mock LLM:** `http://localhost:5000`

### 5. n8n Workflow Setup
1. Open n8n at `http://localhost:5678`.
2. Import the `n8n_workflow.json` file from the root directory.
3. Activate the workflow.
4. Send a test alert to the Webhook URL (visible in the Webhook node).

---

## CI/CD Pipeline Workflow

The project uses GitHub Actions to automate the entire lifecycle from code commit to multi-cloud deployment.

### 1. Continuous Integration (CI) - `.github/workflows/ci.yml`
Triggered on: **Push to any branch** and **Pull Requests**.
- **Linting:** Checks code style using `flake8`.
- **Unit Testing:** Executes tests in `tests/` using `pytest`.
- **Verification:** Ensures the application and agent services are functional.

### 2. Continuous Deployment (CD) - `.github/workflows/deploy.yml`
Triggered on: **Merge/Push to `main`**.
- **Multi-Cloud Infrastructure:** Uses Terraform to provision resources.
- **n8n Hosting:** Deploys n8n as the central orchestrator (containerized on ECS/GKE).
- **Provider Selection:** Supports both **AWS** and **GCP**.

---

# Project Guidelines

This section outlines the architectural standards and conventions.

## Architectural Guidelines
- **Core Orchestration:** n8n is used as the central engine for workflow automation and coordination (as per design doc).
- **Agent Services:** AI Agents are exposed as discrete REST endpoints via FastAPI, allowing n8n to call them as part of the pipeline.
- **State Management:** Strict use of `Pydantic` `BaseModel` (`AlertState`) for data exchange between n8n and agents.

## Coding Conventions
- **Type Safety:** Mandatory type hints for all function signatures.
- **Observability:** Instrument all new endpoints with Prometheus metrics and OpenTelemetry traces.
- **Testing:** New features must include unit tests.

## Development Workflows
- **Branching:** Feature branches only. Merge to `main` only after CI success.
- **Secrets:** Use GitHub Secrets for all sensitive keys. Never commit `.env` or secret files.
