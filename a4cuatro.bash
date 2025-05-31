#!/bin/bash
gcloud config list

gcloud pubsub topics create pipeline-success
gcloud pubsub topics create pipeline-error

gcloud projects add-iam-policy-binding poc-etl-gcp \
  --member="serviceAccount:sa-pipeline@poc-etl-gcp.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"

gcloud pubsub subscriptions create inspect-success \
  --topic=pipeline-success --ack-deadline=20
gcloud pubsub subscriptions create inspect-error \
  --topic=pipeline-error --ack-deadline=20

