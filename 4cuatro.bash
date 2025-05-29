gcloud compute networks vpc-access connectors create fn-to-pg --region us-central1 --range 10.8.0.0/28
gcloud compute instances delete-access-config poc-pg-vm --zone us-central1-a --access-config-name="external-nat"
