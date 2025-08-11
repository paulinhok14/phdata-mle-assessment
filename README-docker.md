# Sound Realty API - Docker Instructions

This guide explains how to build and run the Sound Realty House Price Prediction API using Docker.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed on your system.

## Build the Docker Image

Build the Docker image using the following command:

```bash
docker build --no-cache -t sound-realty-api:latest .
```

## Run the Docker Container

Start the API server with:

```bash
docker run -p 8000:8000 sound-realty-api:latest
```

This will map port 8000 of your local machine to port 8000 in the container.

## Access the API

Once the container is running, access the API at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)

## Notes
- Make sure your model files and required data are available in the Docker build context if needed.
- For development or troubleshooting, you can add `-it --rm` to the `docker run` command for interactive mode and automatic cleanup.
