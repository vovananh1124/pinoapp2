from flask import Flask, jsonify
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from datetime import datetime

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "backend-02")
STORAGE_ACCOUNT_URL = os.getenv("STORAGE_ACCOUNT_URL")
CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "appdata")

credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
    account_url=STORAGE_ACCOUNT_URL,
    credential=credential
)

container_client = blob_service_client.get_container_client(CONTAINER_NAME)


@app.route("/")
def home():
    return jsonify({
        "message": f"Hello from {APP_NAME}"
    })


@app.route("/health")
def health():
    return "OK", 200


@app.route("/upload-sample")
def upload_sample():
    blob_name = f"{APP_NAME}-{datetime.utcnow().isoformat()}.txt"
    content = f"File created by {APP_NAME}"

    container_client.upload_blob(name=blob_name, data=content)
    return jsonify({
        "uploaded": blob_name
    })


@app.route("/blobs")
def list_blobs():
    blobs = [b.name for b in container_client.list_blobs()]
    return jsonify({
        "app": APP_NAME,
        "blobs": blobs
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
