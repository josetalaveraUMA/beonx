from datetime import datetime, timedelta
from time import sleep
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import azure.storage.blob
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Azure Blob Storage configuration
CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')

# Create Blob Storage client
blob_service_client = azure.storage.blob.BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

class FileProcessor:
    def __init__(self, container_client):
        self.container_client = container_client

    def download_convert_and_upload(self, extract: datetime, date: datetime):
        # Using the _download_rates function to download the CSV file
        csv_path = self._download_rates(extract, date)
        parquet_path = self.csv_to_parquet_conversion(csv_path)
        self.upload_parquet_to_blob(parquet_path)

    # Method to simulate downloading a CSV file (renamed as _download_rates)
    def _download_rates(self, extract: datetime, date: datetime) -> str:
        """Download file and return local file path where file is downloaded."""
        sleep(1)  # Simulates the download time of the API
        return 'storage/{}/{}.csv'.format(extract.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d'))

    # Method to convert CSV to Parquet
    def csv_to_parquet_conversion(self, csv_path: str) -> str:
        df = pd.read_csv(csv_path)
        parquet_path = csv_path.replace(".csv", ".parquet")
        df.to_parquet(parquet_path, engine="pyarrow", index=False)
        return parquet_path

    # Method to upload a Parquet file to Azure Blob Storage
    def upload_parquet_to_blob(self, parquet_path: str):
        if not os.path.exists(parquet_path):
            raise FileNotFoundError(f"The file {parquet_path} does not exist.")

        folder_name = os.path.basename(os.path.dirname(parquet_path))
        blob_name = f"{folder_name}/{os.path.basename(parquet_path)}"
        blob_client = self.container_client.get_blob_client(blob_name)

        try:
            # Upload the file
            with open(parquet_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"File {parquet_path} successfully uploaded to Azure Blob Storage as {blob_name}.")
        except Exception as e:
            print(f"Error uploading {parquet_path}: {str(e)}")


# DAG configuration
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 19),
    'retries': 1,
}

dag = DAG(
    'download_and_upload_text',
    default_args=default_args,
    description='DAG to download csv files and upload parquet files to Azure Blob Storage',
    schedule_interval='@daily',
    catchup=False,
)

# Create an instance of the FileProcessor class
file_processor = FileProcessor(container_client)

# Create DAG tasks
extract_date = datetime(2023, 7, 2)

tasks = []
for i in range(7):
    check_in_date = extract_date + timedelta(days=i)

    task = PythonOperator(
        task_id=f"download_convert_and_upload_file_{i}",
        python_callable=file_processor.download_convert_and_upload,
        op_args=[extract_date, check_in_date],
        dag=dag,
    )
    tasks.append(task)
