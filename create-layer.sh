#!/bin/bash

# Build the Docker image
docker build -t lambda-layer -f Dockerfile-layer .

# Run the Docker container to create the layer
docker run --name lambda-layer-container  lambda-layer

# Move the zip file in layers directory.

docker cp lambda-layer-container:/app/lambda-layer.zip ./dist

# Stop the conainer
docker stop lambda-layer-container

# Remove the running conainer
docker rm lambda-layer-container

# Cleanup: remove the Docker image
docker rmi --force lambda-layer