#!/bin/bash
gcloud config list

gcloud projects add-iam-policy-binding poc-etl-gcp \
  --member="serviceAccount:sa-pipeline@poc-etl-gcp.iam.gserviceaccount.com" \
  --role="roles/eventarc.eventReceiver"

gcloud services enable eventarc.googleapis.com

PROJECT_NUMBER=$(gcloud projects describe poc-etl-gcp --format='value(projectNumber)')
gcloud projects add-iam-policy-binding poc-etl-gcp \
    --member=serviceAccount:service-$PROJECT_NUMBER@gs-project-accounts.iam.gserviceaccount.com \
    --role=roles/pubsub.publisher

gcloud run services add-iam-policy-binding pipeline \
  --region=us-central1 \
  --member="serviceAccount:sa-pipeline@poc-etl-gcp.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
