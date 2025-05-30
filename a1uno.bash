#!/bin/bash
gcloud config list

gcloud functions deploy load_to_pg \
  --gen2 --runtime=python312 --entry-point=ingest \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=poc-data-staging" \
  --region=us-central1 \
  --service-account=sa-pipeline@poc-etl-gcp.iam.gserviceaccount.com \
  --vpc-connector=fn-to-pg \
  --set-env-vars=PG_HOST=10.128.0.2,PG_DB=pocdb,PG_USER=postgres,PG_PWD=Mayo2025
