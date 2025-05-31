import os, pathlib, pandas as pd, psycopg2
from google.cloud import storage

# ↓ parámetros fijos vía env-vars
PG = dict(
    host=os.environ["PG_HOST"],
    dbname=os.environ["PG_DB"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PWD"],
    connect_timeout=5,
)

storage_client = storage.Client()

def ingest(event, context):
    bucket, name = event["bucket"], event["name"]
    tmp_path = f"/tmp/{pathlib.Path(name).name}"

    # 1. descarga
    storage_client.bucket(bucket).blob(name).download_to_filename(tmp_path)

    # 2. lectura + mini ETL
    if name.endswith(".csv") or name.endswith(".txt"):
        df = pd.read_csv(tmp_path)
    else:  # xlsx
        df = pd.read_excel(tmp_path)

    # 3. reglas de calidad
    assert not df.isna().any().any(), "Nulls detectados"
    assert len(df.columns) >= 3, "Se requieren ≥3 columnas"

    # 4. carga incremental
    with psycopg2.connect(**PG) as conn, conn.cursor() as cur:
        for row in df.itertuples(index=False):
            cur.execute(
                """
                INSERT INTO raw_data (col1,col2,col3)
                VALUES (%s,%s,%s)
                ON CONFLICT DO NOTHING
                """,
                row[:3],
            )

    return f"Rows inserted: {len(df)}", 200
