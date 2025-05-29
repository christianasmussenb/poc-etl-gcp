FROM python:3.12-slim
RUN apt-get update && apt-get install -y libmagic1 file && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
# gunicorn escuchará en 8080 como exige Cloud Run
CMD ["gunicorn", "-b", ":8080", "main:app"]
