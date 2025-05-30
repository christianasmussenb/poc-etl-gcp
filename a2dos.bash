#!/bin/bash
gcloud config list

gcloud compute firewall-rules create allow-fn-pg \
  --network=default --direction=INGRESS --priority=1000 \
  --action=ALLOW --rules=tcp:5432 --source-ranges=10.8.0.0/28 \
  --target-tags=postgres
