#!/bin/bash

# Variables
echo "Setting up deployment variables..."
PROJECT_ID="potent-result-414004"
SERVICE_NAME="dev-globant-api"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
SERVICE_ACCOUNT_EMAIL="globant-api-de@potent-result-414004.iam.gserviceaccount.com"
REGION="us-central1"
CPU="1"
MIN_INSTANCES="0"
MAX_INSTANCES="10"
# Set to "--allow-unauthenticated" to allow unauthenticated access, or "--no-allow-unauthenticated" to require authentication
AUTHENTICATION="--allow-unauthenticated"

gcloud config set project ${PROJECT_ID}

# Build and submit the container image to Container Registry
echo ${IMAGE}
echo "Starting build and submit to Container Registry..."
gcloud builds submit --tag ${IMAGE}
echo "Build and submit completed."
echo "----------------------"

# Deploy to Cloud Run
echo "Starting deployment to Cloud Run..."
gcloud beta run deploy ${SERVICE_NAME} \
    --image ${IMAGE} \
    --cpu ${CPU} \
    --min-instances ${MIN_INSTANCES} \
    --max-instances ${MAX_INSTANCES} \
    --service-account ${SERVICE_ACCOUNT_EMAIL} \
    --region ${REGION} \
    ${AUTHENTICATION}
echo "Deployment to Cloud Run completed."