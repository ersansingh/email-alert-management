# Email Alert Management System

This system uses a multi-agent architecture with LangGraph to process and remediate email alerts.

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
- **FastAPI Application:** `http://localhost:8000` (Endpoint: `POST /alert`)
- **Prometheus (Metrics):** `http://localhost:9090`
- **Grafana (Dashboards):** `http://localhost:3000` (Default: admin/admin)
- **Jaeger (Tracing):** `http://localhost:16686`
- **LocalStack (Cloud Mocks):** `http://localhost:4566`
- **Mock LLM:** `http://localhost:5000`

### 4. Running Integration Tests
To run tests against the LocalStack instance programmatically:
```bash
pytest tests/test_integration_localstack.py
```

---

## CI/CD Pipeline Workflow

The project uses GitHub Actions to automate the entire lifecycle from code commit to multi-cloud deployment.

### 1. Continuous Integration (CI) - `.github/workflows/ci.yml`
Triggered on: **Push to any branch** and **Pull Requests**.
- **Linting:** Checks code style using `flake8`.
- **Unit Testing:** Executes tests in `tests/` using `pytest` to ensure logic correctness.
- **Verification:** Ensures the application can build and dependencies are resolved.

### 2. Continuous Deployment (CD) - `.github/workflows/deploy.yml`
Triggered on: **Merge/Push to `main`**.
- **Multi-Cloud Infrastructure:** Uses Terraform to provision resources.
- **Provider Selection:** Supports both **AWS** and **GCP** via the `cloud_provider` variable.
- **Manual Trigger:** Can be manually triggered via `workflow_dispatch` to choose a specific cloud provider.
- **Security:** Injects `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `GOOGLE_CREDENTIALS` from GitHub Secrets.

---

# Project Guidelines

This section outlines the architectural standards and conventions.

## Architectural Guidelines
- **Agent-Oriented:** Multi-agent approach orchestrated via `LangGraph`. Each agent is a discrete module in `app/agents/`.
- **State Management:** Strict use of `Pydantic` `BaseModel` (`AlertState`) for workflow states.
- **Multi-Cloud:** Infrastructure is modularized in `infra/modules/`. Avoid cloud-specific hardcoding in the application core.

## Coding Conventions
- **Type Safety:** Mandatory type hints for all function signatures.
- **Observability:** Instrument all new endpoints with Prometheus metrics and OpenTelemetry traces.
- **Testing:** New features must include unit tests.

## Development Workflows
- **Branching:** Feature branches only. Merge to `main` only after CI success.
- **Secrets:** Use GitHub Secrets for all sensitive keys. Never commit `.env` or secret files.
