# Email Alert Management System

This system uses a multi-agent architecture with LangGraph to process and remediate email alerts.

## Getting Started

1. Install requirements: `pip install -r requirements.txt`
2. Run the application (using FastAPI): `uvicorn app.main:app --reload`
## Infrastructure Deployment

We use profile-based Terraform environments to deploy to various cloud providers.

### 1. Authentication via OIDC (Recommended for CI/CD)
For automated deployments via GitHub Actions, we leverage OpenID Connect (OIDC) to securely authenticate with cloud providers without storing long-lived credentials.

*   **AWS:** Configure an [IAM OIDC Provider and an IAM Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html) that your GitHub repository can assume. The ARN of this role should be stored as a GitHub Secret: `AWS_OIDC_ROLE_ARN`.
*   **GCP:** Refer to `docs/GCP_Deployment.md` for detailed instructions on setting up [Workload Identity Federation (OIDC)](https://cloud.google.com/iam/docs/workload-identity-federation-github) and linking your GitHub repository to a GCP Service Account. The required secrets (`GCP_PROJECT_ID`, `GCP_PROJECT_NUMBER`, `GCP_SERVICE_ACCOUNT`) are used in the OIDC configuration, not stored as direct credentials.
*   **Azure:** Configure an [Azure AD App Registration and federated credential](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure?tabs=azure-portal%2Cwindows) that your GitHub repository can use. The Client ID, Tenant ID, and Subscription ID should be stored as GitHub Secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`.

### 2. Prerequisites (for Local Development/Manual Deployment)
-   **Terraform:** [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) (v1.0+)
-   **AWS CLI:** [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and configure with `aws configure`.
-   **Google Cloud SDK (`gcloud`):** [Install gcloud CLI](https://cloud.google.com/sdk/docs/install) and authenticate locally with `gcloud auth login`.
-   **Azure CLI:** [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and authenticate locally with `az login`.
-   **kubectl:** [Install kubectl](https://kubernetes.io/docs/tasks/tools/) to interact with clusters.

### 3. AWS Deployment (EKS)
```bash
cd infra/environments/awsprod
terraform init
terraform apply
```
-   **Post-Deployment:** Update your kubeconfig:
    `aws eks update-kubeconfig --region <region> --name ai-sre-cluster`

### 4. GCP Deployment (GKE)
```bash
cd infra/environments/gcpprod
terraform init
terraform apply
```
-   **Post-Deployment:** Update your kubeconfig:
    `gcloud container clusters get-credentials ai-sre-cluster --region <region>`

### 5. Azure Deployment (AKS)
*Note: You need to create `infra/environments/azureprod` directory and Terraform files.* 
```bash
cd infra/environments/azureprod
terraform init
terraform apply
```
-   **Post-Deployment:** Update your kubeconfig:
    `az aks get-credentials --resource-group <your-rg> --name <your-aks-cluster>`

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
# Run the local-only integration test script (Requires Docker Desktop)
python scripts/test_local.py
```

---

## CI/CD Pipeline Workflow

The project uses GitHub Actions to automate the entire lifecycle from code commit to multi-cloud deployment.

### 1. Continuous Integration (CI) - `.github/workflows/ci.yml`
Triggered on: **Push to any branch** and **Pull Requests**.
- **Linting:** Checks code style using `flake8`.
- **Unit Testing:** Executes tests in `tests/` using `pytest`.

### 2. Integration Testing - `.github/workflows/integration-tests.yml`
Triggered on: **Push to `main`** or `workflow_dispatch`.
- **Default Environment:** `gcpprod`.
- **Purpose:** Validates that provisioned infrastructure (GCS, Pub/Sub, S3, SQS) is accessible and correctly configured.
- **Local Testing:** Local integration testing (using LocalStack) is handled via **Docker Desktop** on the developer's machine (see "Local Testing" section below).

### 3. Continuous Deployment (CD) - `.github/workflows/cd-*.yml`
Triggered on: **Merge/Push to `release/*` branches** or `workflow_dispatch`.
-   **Multi-Cloud Infrastructure:** Uses Terraform environment profiles (`infra/environments/awsprod`, `gcpprod`, `azureprod`) to provision resources.
-   **Authentication:** Leverages **GitHub OIDC** for secure, keyless authentication with AWS, GCP, and Azure. Cloud credentials are *not* stored as GitHub Secrets directly.
-   **Application Secrets:** Application-specific secrets (e.g., `GEMINI_API_KEY`) are fetched at runtime from **HashiCorp Vault**.
-   **Manual Trigger:** Can be manually triggered via `workflow_dispatch` to choose a specific cloud environment.

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
-   **Secrets:** Cloud credentials are managed via **GitHub OIDC**. Application-specific secrets (e.g., `GEMINI_API_KEY`) are stored in **HashiCorp Vault** and fetched at runtime by CI/CD workflows. Never commit `.env` or secret files to the repository.
