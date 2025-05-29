#!/bin/bash
gcloud config list

gcloud auth login

gcloud config set project poc-etl-gcp

gcloud services enable \
  compute.googleapis.com \
  run.googleapis.com \
  storage.googleapis.com \
  pubsub.googleapis.com \
  cloudfunctions.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com

gsutil mb -l us-central1 gs://poc-data-staging
