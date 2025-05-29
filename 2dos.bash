#!/bin/bash
gcloud config list

gcloud compute instances create poc-pg-vm \
   --zone=us-central1-a \
   --machine-type=e2-micro \
   --image-family=debian-12 \
   --image-project=debian-cloud \
   --boot-disk-size=20GB \
   --boot-disk-type=pd-standard \
   --tags=postgres \
   --scopes=https://www.googleapis.com/auth/cloud-platform
