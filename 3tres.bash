gcloud compute ssh --zone "us-central1-a" "poc-pg-vm" --project "poc-etl-gcp"
sudo growpart /dev/sda 1
sudo resize2fs /dev/sda1
# Install PostgreSQL and set up the database
sudo apt update
sudo apt -y install postgresql
sudo systemctl enable --now postgresql
sudo -i -u postgres psql -c "ALTER USER postgres PASSWORD 'Mayo2025';"
sudo apt install -y cron
