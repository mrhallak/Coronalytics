import logging
from google.cloud import storage


class Storage:
    def __init__(self, project_id: str):
        self.project_id = project_id

        self.client = storage.Client(project=project_id)

    def upload_blob(self, source_file_uri: str, destination_file_uri: str, bucket_name: str):
        logging.info(f"Uploading {source_file_uri} to gs://{bucket_name}/{destination_file_uri}")

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_file_uri)
        blob.upload_from_filename(source_file_uri)

        logging.info(f"Uploaded {source_file_uri} to gs://{bucket_name}/{destination_file_uri}")