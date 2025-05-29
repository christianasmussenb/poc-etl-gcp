#!/bin/bash

gcloud run services describe pipeline --region=us-central1 --format='value(status.url)'

gcloud run services logs read pipeline --region=us-central1 --limit 20
