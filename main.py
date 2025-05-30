import os, json, magic, pandas as pd, psycopg2, flask
from google.cloud import pubsub_v1, logging as gcp_logging

app = flask.Flask(__name__)
publisher = pubsub_v1.PublisherClient()
gcp_logging.Client().setup_logging()

PG_CONN = psycopg2.connect(
    host=os.environ["PG_HOST"],
    dbname=os.environ["PG_DB"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PWD"])

def load(df):
    with PG_CONN, PG_CONN.cursor() as cur:
        for row in df.itertuples(index=False):
            cur.execute("INSERT INTO raw_data VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", row)

@app.route("/", methods=["POST"])
def ingest():
    data = flask.request.get_json()
    bucket, name = data["bucket"], data["name"]
    tmp = f"/tmp/{os.path.basename(name)}"
    os.system(f"gsutil cp gs://{bucket}/{name} {tmp}")

    try:
        mt = magic.from_file(tmp, mime=True)
        if mt in ("text/csv", "text/plain"):
            df = pd.read_csv(tmp)
        elif "spreadsheet" in mt or "ms-excel" in mt:
            df = pd.read_excel(tmp)
        else:
            raise ValueError(f"Tipo no soportado {mt}")

        # Reglas de calidad mínimas
        assert not df.isna().any().any()
        load(df)

        publisher.publish("projects/poc-etl-gcp/topics/pipeline-success",
                          json.dumps({"file": name}).encode())
        return "OK", 200

    except Exception as e:
        publisher.publish("projects/poc-etl-gcp/topics/pipeline-error",
                          json.dumps({"file": name, "error": str(e)}).encode())
        flask.current_app.logger.error(str(e))
        return "FAIL", 500
@app.route("/health", methods=["GET"])
def health():
    try:
        with PG_CONN.cursor() as cur:
            cur.execute("SELECT 1")
        return "OK", 200
    except Exception as e:
        flask.current_app.logger.error(str(e))
        return "FAIL", 500
