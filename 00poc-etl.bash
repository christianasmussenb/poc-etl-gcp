gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/poc/pipeline:0.1
gcloud run deploy pipeline \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/poc/pipeline:0.1 \
  --region us-central1 --service-account sa-pipeline@$PROJECT_ID.iam.gserviceaccount.com \
  --max-instances 3 --memory 1Gi --timeout 900s --ingress internal
  