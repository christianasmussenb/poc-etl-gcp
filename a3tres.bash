#!/bin/bash
gcloud config list

gcloud functions deploy load_to_pg \
  --gen2 --runtime=python312 --entry-point=ingest \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=poc-data-staging" \
  --region=us-central1 \
  --service-account=sa-pipeline@poc-etl-gcp.iam.gserviceaccount.com \
  --vpc-connector=fn-to-pg \
  --env-vars-file=env.yaml \
  --memory=512Mi --timeout=540
