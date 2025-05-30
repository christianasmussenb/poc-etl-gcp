#!/bin/bash
gcloud config list

gcloud compute ssh --zone "us-central1-a" "poc-pg-vm" --project "poc-etl-gcp"
sudo growpart /dev/sda 1
sudo resize2fs /dev/sda1
# Install PostgreSQL and set up the database
sudo apt update
sudo apt -y install postgresql
sudo systemctl enable --now postgresql
sudo -i -u postgres psql -c "ALTER USER postgres PASSWORD 'Mayo2025';"
sudo apt install -y cron

# Create the database
sudo -i -u postgres psql -c "CREATE DATABASE pocdb;"
sudo -i -u postgres psql -c "CREATE USER pocuser WITH PASSWORD 'Mayo2025';"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE pocdb TO pocuser;"

# Create the table
sudo -i -u postgres psql -d pocdb -c "CREATE TABLE raw_data (
  col1        text,
  col2        text,
  col3        text,
  created_at  timestamptz DEFAULT now()
);"
# Insert sample data
sudo -i -u postgres psql -d pocdb -c "INSERT INTO raw_data (col1, col2, col3) VALUES ('value1', 'value2', 'value3');"
sudo -i -u postgres psql -d pocdb -c "SELECT COUNT(*) FROM raw_data;"
