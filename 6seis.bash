#!/bin/bash
# This script creates a Google Cloud Artifact Registry repository and submits a Docker image to it.
gcloud config list

gcloud artifacts repositories create poc --repository-format=docker --location=us-central1

gcloud builds submit \
  --tag us-central1-docker.pkg.dev/poc-etl-gcp/poc/pipeline:0.1
