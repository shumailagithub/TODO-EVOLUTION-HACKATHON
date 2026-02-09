# CI/CD Pipeline Setup

This project includes a CI/CD pipeline using GitHub Actions to automatically deploy the application to cloud Kubernetes services (AKS or GKE) after each push to the repository.

## Prerequisites

Before setting up the CI/CD pipeline, you need to configure the following:

### For AKS Deployment

1. **Azure Credentials Secret**:
   - Create an Azure service principal with contributor access to your AKS cluster
   - Add the JSON output as a GitHub secret named `AZURE_CREDENTIALS`

2. **Repository Variables**:
   - `AKS_CLUSTER_NAME`: Your AKS cluster name
   - `AKS_RESOURCE_GROUP`: The resource group containing your AKS cluster
   - `DEPLOY_TO_AKS`: Set to `true` to enable AKS deployment

### For GKE Deployment

1. **GKE Service Account Key Secret**:
   - Create a GCP service account with appropriate permissions
   - Download the JSON key file
   - Add the JSON content as a GitHub secret named `GKE_SA_KEY`

2. **Repository Variables**:
   - `GKE_PROJECT_ID`: Your GCP project ID
   - `GKE_CLUSTER_NAME`: Your GKE cluster name
   - `GKE_ZONE`: The zone where your cluster is located
   - `DEPLOY_TO_GKE`: Set to `true` to enable GKE deployment

## GitHub Secrets Required

- `AZURE_CREDENTIALS`: JSON credentials for Azure service principal (for AKS)
- `GKE_SA_KEY`: JSON key for GCP service account (for GKE)

## GitHub Variables Required

For AKS deployment:
- `AKS_CLUSTER_NAME`
- `AKS_RESOURCE_GROUP`
- `DEPLOY_TO_AKS` (set to `true`)

For GKE deployment:
- `GKE_PROJECT_ID`
- `GKE_CLUSTER_NAME`
- `GKE_ZONE`
- `DEPLOY_TO_GKE` (set to `true`)

## Pipeline Workflow

The CI/CD pipeline performs the following steps:

1. **Build Phase**:
   - Checks out the code
   - Builds Docker images for the application
   - Pushes images to the container registry (GitHub Container Registry)

2. **Test Phase**:
   - Runs automated tests to validate the application

3. **Deploy Phase**:
   - Authenticates with the target Kubernetes cluster (AKS or GKE)
   - Updates the Kubernetes deployment manifests with the new image tags
   - Applies the updated manifests to the cluster
   - Waits for the rollout to complete successfully

## Enabling the Pipeline

1. Commit and push the `.github/workflows/ci-cd.yml` file to your repository
2. Configure the required secrets and variables in your GitHub repository settings
3. The pipeline will automatically trigger on pushes to the main/master branch

## Manual Trigger

You can also manually trigger the workflow from the GitHub Actions tab in your repository.

## Rollback Process

If needed, you can rollback to a previous version by:
1. Identifying the previous image tag in the container registry
2. Updating the deployment manifest with the previous image tag
3. Applying the updated manifest to the cluster