# Despliegue del Proyecto con Docker Compose

Este proyecto utiliza Docker y Docker Compose para desplegar Apache Airflow con un ejecutor Celery. A continuación, se describen los pasos necesarios para configurar y ejecutar el entorno.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes en tu sistema:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuración

1. **Crear el archivo `.env`**

   En el directorio del proyecto, crea un archivo llamado `.env` y agrega las siguientes variables de entorno:

   ```env
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DB=
   LOAD_EX=
   FERNET_KEY=
   EXECUTOR=
   AZURE_STORAGE_ACCOUNT_NAME=
   AZURE_STORAGE_ACCOUNT_KEY=
   AZURE_STORAGE_CONNECTION_STRING=
   AZURE_STORAGE_CONTAINER_NAME=
   ```

2. **Construir los contenedores**

   En el directorio del proyecto, ejecuta el siguiente comando para construir las imágenes necesarias:

   ```sh
   docker-compose build
   ```

3. **Levantar los servicios**

   Una vez completada la construcción, inicia los contenedores con:

   ```sh
   docker-compose up
   ```

4. **Acceder a la interfaz de Airflow**

   Una vez que los contenedores estén en ejecución, puedes acceder a la interfaz de Apache Airflow en tu navegador en la siguiente dirección:

   - [Airflow UI](http://localhost:8080)

5. **Monitorear los workers con Flower**

   También puedes supervisar el estado de los workers de Celery a través de la interfaz de Flower en:

   - [Flower UI](http://localhost:5555)



## Visualización de Datos

En el proyecto se incluye el archivo `DataVisualization.ipynb`, un notebook diseñado para la visualización de datos provenientes de Azure Blob Storage.

## Notas

- Para detener los contenedores, usa `Ctrl + C` o ejecuta:
  
  ```sh
  docker-compose down
  ```

- Si deseas reconstruir las imágenes sin utilizar la caché, ejecuta:
  
  ```sh
  docker-compose build --no-cache
  ```

¡Listo! Ahora tienes Apache Airflow ejecutándose con Docker Compose.