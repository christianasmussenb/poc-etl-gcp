#!/bin/bash
gcloud config list

gcloud run deploy pipeline \
  --image us-central1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/poc/pipeline:0.1 \
  --region us-central1 \
  --service-account sa-pipeline@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
  --vpc-connector fn-to-pg \
  --egress-settings all \
  --max-instances 3 \
  --memory 512Mi \
  --timeout 900s \
  --set-env-vars PG_HOST=10.128.0.2,PG_DB=pocdb,PG_USER=postgres,PG_PWD=TU_PASS
