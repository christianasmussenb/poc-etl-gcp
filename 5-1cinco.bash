#!/bin/bash
gcloud config list

gcloud eventarc triggers create gs-trigger \
  --location=us-central1 \
  --destination-run-service=pipeline \
  --destination-run-region=us-central1 \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=poc-data-staging" \
  --service-account=sa-pipeline@poc-etl-gcp.iam.gserviceaccount.com
  