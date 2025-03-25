FROM puckel/docker-airflow:latest

# Switch to root user for installing dependencies
USER root

# Upgrade pip and install required dependencies in a single RUN command
RUN pip install --upgrade pip && \
    pip install --no-cache-dir azure-storage-blob pandas==1.3.5 pyarrow python-dotenv

# Copy the .env file first to leverage Docker caching for unchanged files
COPY .env /usr/local/airflow/.env

# Copy the storage folder into the container
COPY storage /usr/local/airflow/storage

# Change the permissions of the files and directories inside `storage`
RUN chmod -R 777 /usr/local/airflow/storage


# Switch back to airflow user
USER airflow
