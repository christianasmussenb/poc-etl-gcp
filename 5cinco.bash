#!/bin/bash
gcloud config list

gcloud pubsub topics create pipeline-success 

gcloud pubsub topics create pipeline-error
