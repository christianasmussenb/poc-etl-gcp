#!/bin/bash
gcloud config list

gcloud pubsub topics create pipeline-success 

gcloud pubsub topics create pipeline-error

gcloud pubsub subscriptions create pipeline-success \
  --topic=pipeline-success \
  --ack-deadline=20

gcloud pubsub subscriptions create pipeline-error \
  --topic=pipeline-error \
  --ack-deadline=20
