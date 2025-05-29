#!/bin/bash
gcloud config list

gcloud run deploy pipeline \
  --image us-central1-docker.pkg.dev/poc-etl-gcp/poc/pipeline:0.1 \
  --region us-central1 \
  --service-account=sa-pipeline@poc-etl-gcp.iam.gserviceaccount.com \
  --vpc-connector=fn-to-pg \
  --vpc-egress=private-ranges-only \
  --memory=512Mi \
  --timeout=900s \
  --max-instances=3 \
  --set-env-vars=PG_HOST=10.128.0.2,PG_DB=pocdb,PG_USER=postgres,PG_PWD=Mayo2025
