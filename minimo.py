import os, pandas as pd, psycopg2, pathlib
from google.cloud import storage

def ingest(event, context):
    bucket, name = event['bucket'], event['name']
    tmp = f"/tmp/{pathlib.Path(name).name}"
    storage.Client().bucket(bucket).blob(name).download_to_filename(tmp)

    df = pd.read_csv(tmp) if name.endswith('.csv') else pd.read_excel(tmp)
    assert not df.isna().any().any(), "Nulls!"

    with psycopg2.connect(
        host=os.environ['PG_HOST'], dbname=os.environ['PG_DB'],
        user=os.environ['PG_USER'], password=os.environ['PG_PWD']) as conn, conn.cursor() as cur:
        for row in df.itertuples(index=False):
            cur.execute("INSERT INTO raw_data VALUES (%s,%s,%s)", row)
        print(f"Processed {name} successfully.")
