"""
main.py – Cloud Function Gen 2 handler
Descarga un archivo nuevo del bucket, realiza validaciones
básicas con pandas y lo inserta en PostgreSQL. Publica
un mensaje en Pub/Sub indicando éxito o error.
"""

import os
import pathlib
import json
import pandas as pd
import psycopg2
from google.cloud import storage, pubsub_v1
from flask import abort

# ---------- configuración global (solo se ejecuta en el cold-start) ----------
PROJECT_ID = os.environ["GCP_PROJECT"]
TOPIC_OK   = f"projects/{PROJECT_ID}/topics/pipeline-success"
TOPIC_ERR  = f"projects/{PROJECT_ID}/topics/pipeline-error"

PG_PARAMS = dict(
    host=os.environ["PG_HOST"],
    dbname=os.environ["PG_DB"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PWD"],
    connect_timeout=5,
)

storage_client = storage.Client()
publisher      = pubsub_v1.PublisherClient()

# --------------------------------------------------------------------------- #
def _download_to_tmp(bucket: str, name: str) -> str:
    """Descarga el objeto GCS a /tmp/ y devuelve la ruta local."""
    local_path = f"/tmp/{pathlib.Path(name).name}"
    storage_client.bucket(bucket).blob(name).download_to_filename(local_path)
    return local_path


def _load_dataframe(path: str) -> pd.DataFrame:
    """Lee CSV, TXT o XLSX según extensión sencilla."""
    if path.endswith((".csv", ".txt")):
        return pd.read_csv(path)
    elif path.endswith((".xls", ".xlsx")):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Tipo de archivo no soportado: {path}")


def _basic_qc(df: pd.DataFrame) -> None:
    """Validaciones mínimas para la POC."""
    if df.isna().any().any():
        raise ValueError("Nulls detectados en el dataset")
    if len(df.columns) < 3:
        raise ValueError("Se requieren al menos 3 columnas")


def _insert_df(df: pd.DataFrame) -> int:
    """Inserta el DataFrame en raw_data; devuelve filas insertadas."""
    rows = [tuple(r[:3]) for r in df.itertuples(index=False)]
    with psycopg2.connect(**PG_PARAMS) as conn, conn.cursor() as cur:
        cur.executemany(
            """INSERT INTO raw_data (col1,col2,col3) VALUES (%s,%s,%s)
               ON CONFLICT DO NOTHING""",
            rows,
        )
    return len(rows)


# ================  Cloud Function entry point ===============================
def ingest(event: dict, _context):
    bucket, name = event["bucket"], event["name"]
    if not bucket or not name:
        abort(400, "Bad event payload")

    try:
        local = _download_to_tmp(bucket, name)
        df    = _load_dataframe(local)
        _basic_qc(df)
        inserted = _insert_df(df)

        publisher.publish(TOPIC_OK, json.dumps({
            "file": name,
            "rows": inserted
        }).encode())
        return f"Rows inserted: {inserted}", 200

    except Exception as exc:
        publisher.publish(TOPIC_ERR, json.dumps({
            "file":  name,
            "error": str(exc)
        }).encode())
        # Cloud Functions considera que un 500 provoca re-intento; perfecto
        abort(500, str(exc))
