import os, json, magic, pandas as pd, psycopg2, functions_framework
from google.cloud import pubsub_v1, logging as gcp_logging

publisher = pubsub_v1.PublisherClient()
log_client = gcp_logging.Client()
log_client.setup_logging()

PG_CONN = psycopg2.connect(
    host=os.environ["PG_HOST"],
    dbname=os.environ["PG_DB"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PWD"])

def load_df_to_pg(df, table):
    with PG_CONN, PG_CONN.cursor() as cur:
        # upsert simplificado
        for _, row in df.iterrows():
            cur.execute("INSERT INTO ...", tuple(row))

@functions_framework.cloud_event
def ingest(cloud_event):
    bucket = cloud_event.data["bucket"]
    name   = cloud_event.data["name"]
    uri    = f"gs://{bucket}/{name}"

    df, table = None, "raw_data"
    try:
        tmp = f"/tmp/{os.path.basename(name)}"
        os.system(f"gsutil cp {uri} {tmp}")
        mimetype = magic.from_file(tmp, mime=True)

        if mimetype in ["text/csv", "text/plain"]:
            df = pd.read_csv(tmp)
        elif mimetype in ["application/vnd.ms-excel",
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            df = pd.read_excel(tmp)
        else:
            raise ValueError(f"Tipo no soportado: {mimetype}")

        # --- VALIDACIONES BÁSICAS ----
        assert not df.isnull().any().any(), "Nulls detectados"
        assert len(df.columns) >= 3, "Demasiadas pocas columnas"
        # más reglas de negocio …

        load_df_to_pg(df, table)
        publisher.publish("projects/$PROJECT_ID/topics/pipeline-success",
                          json.dumps({"file": name}).encode())
        print("Carga exitosa", extra={"severity": "INFO"})

    except Exception as e:
        publisher.publish("projects/$PROJECT_ID/topics/pipeline-error",
                          json.dumps({"file": name, "error": str(e)}).encode())
        print(f"ERROR {e}", extra={"severity": "ERROR"})
        raise
    