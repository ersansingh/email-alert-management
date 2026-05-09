# Email Alert Management System

This system uses a multi-agent architecture with LangGraph to process and remediate email alerts.

## Getting Started

1. Install requirements: `pip install -r requirements.txt`
2. Run the application (using FastAPI): `uvicorn app.main:app --reload`
## Infrastructure Deployment

We use profile-based Terraform environments. Choose your target profile:

### 1. Prerequisites
- **Terraform:** [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) (v1.0+)
- **AWS CLI:** [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and configure with `aws configure`.
- **Google Cloud SDK:** [Install gcloud CLI](https://cloud.google.com/sdk/docs/install) and run `gcloud auth application-default login`.
- **kubectl:** [Install kubectl](https://kubernetes.io/docs/tasks/tools/) to interact with clusters.

### 2. AWS Deployment (EKS)
```bash
cd infra/environments/awsprod
terraform init
terraform apply
```
- **Post-Deployment:** Update your kubeconfig:
  `aws eks update-kubeconfig --region <region> --name ai-sre-cluster`

### 3. GCP Deployment (GKE)
```bash
cd infra/environments/gcpprod
terraform init
terraform apply
```
- **Post-Deployment:** Update your kubeconfig:
  `gcloud container clusters get-credentials ai-sre-cluster --region <region>`

---

## Deployment with Minimal Charges

To minimize cloud costs during testing and development, follow these guidelines:

### General Tips
- **Clean Up:** Always run `terraform destroy` when you are finished testing to stop all billing.
- **Region Selection:** Use regions with lower costs (e.g., `us-east-1` for AWS, `us-central1` for GCP).

### AWS Cost Optimization
- **Instance Types:** The default `t3.medium` is chosen for stability. For even lower costs, you can manually change `instance_types` to `t3.small` in `infra/modules/compute/aws/main.tf`, though performance may vary.
- **Node Count:** The scaling config is set to `min_size = 1`. Ensure it stays at 1 for minimal cost.
- **Cleanup:** EKS charges $0.10 per hour for the control plane. **Delete the cluster immediately after use.**

### GCP Cost Optimization
- **Preemptible Nodes:** The GCP setup is already configured to use **Preemptible VMs** (`preemptible = true`), which are up to 80% cheaper than standard VMs.
- **GKE Free Tier:** Google Cloud offers a free tier for GKE that waives the cluster management fee for one zonal cluster per billing account.
- **Machine Type:** Using `e2-medium` provides a good balance of cost and performance for small workloads.

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
- **Multi-Cloud Infrastructure:** Uses Terraform environment profiles (`infra/environments/awsprod` or `infra/environments/gcpprod`) to provision resources.
- **Provider Selection:** The pipeline dynamically targets the specific environment directory based on your deployment strategy.
- **Manual Trigger:** Can be manually triggered via `workflow_dispatch` to choose a specific cloud environment.
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
