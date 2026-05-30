# GCP Deployment Guide - Email Alert Management System

This guide provides step-by-step instructions for deploying the Email Alert Management System to Google Cloud Platform (GCP). It includes comparisons to AWS services to aid understanding for users familiar with AWS.

## GCP vs. AWS Concept Mapping
- **GCP Project** = AWS Account (The isolated boundary for your resources and billing).
- **GKE (Google Kubernetes Engine)** = EKS (Elastic Kubernetes Service).
- **Google Cloud IAM** = AWS IAM.
- **gcloud CLI** = AWS CLI.
- **Workload Identity Federation** = AWS IAM Roles for Service Accounts (IRSA) / OIDC Providers.

---

## Step-by-Step GCP Deployment Plan

### Step 1: Initial GCP Setup and OIDC Configuration
Before deploying, you need to set up your Google Cloud environment and configure OIDC for secure, keyless authentication from GitHub Actions.

1.  **Create a GCP Project:**
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Click the project dropdown at the top left and select **New Project**. Name it `ai-learning-495017` (or your chosen project ID: `ai-learning-495017`).
2.  **Enable Billing:**
    *   Go to **Billing** in the left menu and link your project to a billing account.
3.  **Enable Required APIs:**
    *   Go to **APIs & Services > Library** and search for/enable:
        *   `Kubernetes Engine API`
        *   `Artifact Registry API`
4.  **Create a GCP Service Account for Deployment:**
    *   Go to **IAM & Admin > Service Accounts**.
    *   Click **+ CREATE SERVICE ACCOUNT**.
    *   **Service account name:** `github-actions-deployer`
    *   **Description:** "Service account for GitHub Actions to deploy the AI SRE application"
    *   Click **CREATE AND CONTINUE**.
    *   **Grant roles:** Add the following roles to this service account:
        *   `Kubernetes Engine Admin`
        *   `Artifact Registry Admin`
        *   `Service Account User`
        *   `Editor` (or more granular roles for production)
    *   Click **CONTINUE**, then **DONE**.
5.  **Configure Workload Identity Federation (OIDC) for GitHub Actions:**
    This allows GitHub Actions to securely impersonate the `github-actions-deployer` service account without needing long-lived keys.

    *   **Create a Workload Identity Pool:**
        ```bash
        gcloud iam workload-identity-pools create "github-pool" \
          --project="ai-learning-495017" \
          --location="global" \
          --display-name="GitHub Actions Pool"
        ```

    *   **Create an OIDC Provider in the Pool:**
        This explicitly maps GitHub's repository claim.
        ```bash
        gcloud iam workload-identity-pools providers create-oidc "github-provider" \
          --project="ai-learning-495017" \
          --location="global" \
          --workload-identity-pool="github-pool" \
          --issuer-uri="https://token.actions.githubusercontent.com" \
          --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository"
        ```

    *   **Link Your Service Account to Your GitHub Repo:**
        This grants your specific GitHub repository (`ersansingh/email-alert-management`) permission to impersonate the `github-actions-deployer` service account.
        ```bash
        gcloud iam service-accounts add-iam-policy-binding "github-actions-deployer@ai-learning-495017.iam.gserviceaccount.com" \
          --project="ai-learning-495017" \
          --role="roles/iam.workloadIdentityUser" \
          --member="principalSet://iam.googleapis.com/projects/663314858590/locations/global/workloadIdentityPools/github-pool/attribute.repository/ersansingh/email-alert-management"
        ```
        *(Replace `663314858590` with your actual GCP Project Number if it differs).*

### Step 2: Set Up Local Tools (The "AWS CLI" Configuration)
1.  **Install the Google Cloud SDK (`gcloud`):**
    *   Download it from the [Google Cloud CLI page](https://cloud.google.com/sdk/docs/install).
2.  **Authenticate Locally:**
    Open your terminal and run:
    ```bash
    gcloud auth login
    ```
    This will open a browser to log you in.
3.  **Set Your Default Project:**
    ```bash
    gcloud config set project [YOUR_PROJECT_ID]
    ```
    *(Note: The Project ID is usually your project name plus some random numbers, visible in the GCP Console).*


### Step 3: Deploy the Infrastructure using Terraform
The project already contains the required Terraform scripts for GCP under `infra/environments/gcpprod`.

1.  **Navigate to the GCP environment directory:**
    ```bash
    cd infra/environments/gcpprod
    ```
2.  **Initialize Terraform:**
    ```bash
    terraform init
    ```
3.  **Review and Apply:**
    Run the following command. It will show you a plan (similar to AWS CloudFormation Change Sets).
    ```bash
    terraform apply
    ```
    - Type `yes` when prompted.
    - *Cost Note:* This deploys a GKE cluster with "Preemptible VMs" (similar to AWS Spot Instances) which drastically reduces your costs.

### Step 4: Configure `kubectl` to Access the GKE Cluster
Just like you run `aws eks update-kubeconfig`, you need to configure your local Kubernetes CLI to communicate with the newly created GKE cluster.

```bash
gcloud container clusters get-credentials ai-sre-cluster --region us-central1
```
*(Make sure to match the region to what was outputted by Terraform, usually `us-central1` by default).*

### Step 5: Build and Push the Docker Image
To run your FastAPI app on Kubernetes, Google Cloud needs access to your Docker image. For CI/CD, images are pushed to Docker Hub by the CI workflow and pulled from there. For local testing or direct pushes, you can use Artifact Registry:

1.  **Create an Artifact Registry Repository (like ECR):**
    ```bash
    gcloud artifacts repositories create ai-sre-repo --repository-format=docker --location=us-central1
    ```
2.  **Authenticate Docker with Artifact Registry:**
    ```bash
    gcloud auth configure-docker us-central1-docker.pkg.dev
    ```
3.  **Build the Image (from project root):**
    ```bash
    docker build -t us-central1-docker.pkg.dev/ai-learning-495017/ai-sre-repo/email-alert-app:latest .
    ```
4.  **Push the Image:**
    ```bash
    docker push us-central1-docker.pkg.dev/ai-learning-495017/ai-sre-repo/email-alert-app:latest
    ```

### Step 6: Deploy the Application to GKE (Manual / Local Test)
For CI/CD, the `cd-gcp.yml` workflow handles this. For manual deployment or testing after local image push:

1.  Ensure you have your `kubernetes/deployment-template.yaml` file (or a custom deployment manifest) ready.
    The `cd-gcp.yml` workflow will use the image `dedoc22/email-alert-app:${{ github.sha }}` from Docker Hub.
    If deploying manually using an image from Artifact Registry, update your `deployment.yaml` with the correct image path:
    `image: us-central1-docker.pkg.dev/ai-learning-495017/ai-sre-repo/email-alert-app:latest`

2.  Apply the deployment (ensure `GEMINI_API_KEY` is set in your environment if not using Kubernetes secrets):
    ```bash
    kubectl apply -f deployment.yaml
    ```
3.  Get the external IP of your application:
    ```bash
    kubectl get services
    ```

You can now send POST requests to `http://<EXTERNAL-IP>/alert` to test your live, Gemini-powered system!

---

### Step 7: Teardown and Cleanup
To avoid ongoing charges, it's crucial to delete all the resources you've created. Follow these steps in order.

1.  **Delete the Kubernetes Application and Service:**
    First, remove the application from your GKE cluster. This will also de-provision the external Load Balancer.
    ```bash
    kubectl delete -f deployment.yaml
    ```

2.  **Delete the Docker Image from Artifact Registry:**
    Next, remove the container image you pushed.
    ```bash
    gcloud artifacts docker images delete us-central1-docker.pkg.dev/[YOUR_PROJECT_ID]/ai-sre-repo/email-alert-app:latest --delete-tags
    ```
    *(Note: You may be prompted to confirm; type 'Y').*

3.  **Delete the Artifact Registry Repository:**
    Now, delete the repository that housed the image.
    ```bash
    gcloud artifacts repositories delete ai-sre-repo --location=us-central1
    ```
    *(Note: You may be prompted to confirm; type 'Y').*

4.  **Destroy the Terraform Infrastructure:**
    This is the most critical step and will delete the GKE cluster and all associated networking resources.
    - Navigate back to the Terraform directory:
      ```bash
      cd infra/environments/gcpprod
      ```
    - Run the destroy command:
      ```bash
      terraform destroy
      ```
      - Type `yes` when prompted to confirm the deletion.

5.  **Delete Workload Identity Pool and Provider:**
    Finally, clean up the OIDC configuration.
    ```bash
    gcloud iam workload-identity-pools providers delete "github-provider" \
          --project="ai-learning-495017" \
          --location="global" \
          --workload-identity-pool="github-pool" --quiet
    ```
    ```bash
    gcloud iam workload-identity-pools delete "github-pool" \
          --project="ai-learning-495017" \
          --location="global" --quiet
    ```

By following these steps, you ensure that all billable services created during the deployment are properly removed.
