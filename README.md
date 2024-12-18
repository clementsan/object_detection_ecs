---
title: Object Detection ECS
emoji: 🌖
colorFrom: purple
colorTo: green
sdk: gradio
sdk_version: 5.5.0
app_file: app.py
pinned: false
short_description: Object detection ECS
---

# Object detection via ECS endpoints

<b>Aim: AI-driven object detection task</b>
 - Front-end: user interface via Gradio library
 - Back-end: use of ECS endpoints to run ML models


## Front-end user interface
Use of Gradio library for web interface

Command line:
> python3 app.py

<b>Note:</b> The Gradio app should now be accessible at http://localhost:7860


## Back-end ML models

Machine Learning (ML) models are available on Docker Hub and have been deployed on AWS ECS

**Docker hub containers:**
 - DETR model: https://hub.docker.com/r/cvachet/object-detection-detr-api
 - YOLOS model: https://hub.docker.com/r/cvachet/object-detection-yolos-api

## AWS ECS deployment steps: 

ECS: Elastic Container Service
Steps after docker images are available on Docker Hub

### Step 1. Create a new ECS task definition
   - Task name (e.g. ObjectDetectionDETRTask)
   - Infrastructure requirement: 
     - Launch type: ```AWS Fargate```
     - Architecture: ```Linux/X86_64```
     - Task size: ```0.5 CPU, 3GB memory```
   - Container:
     - Container name:  (e.g. ```object-detection-detr```)
     - Image uri: point to Docker image URI (e.g. ```cvachet/object-detection-detr-api```)
     - Port mapping: assess port number (e.g. ```port 8000, TCP protocol```)
     

### Step 2. Create a new ECS cluster
   - Cluster name (e.g. ```ObjectDetectionCluster```)


### Step 3. Add a new service to the cluster
 - Compute configuration
   - Use capacity provider strategy (e.g. using Fargate or Fargate_spot)
 - Deployment configuration
   - Application Type: Service
   - Task Family: Select task definition family from prior instance (e.g. ```ObjectDetectionDETRTask```)
   - Assign a Service Name: (e.g. ```object-detection-detr-api```)


### Step 4. Update security group for new service
 - Go to Cluster -> service -> task -> configuration and networking
 - Click on ```Security Group```
 - Adjust rules for inbound traffic (e.g. traffic only from my_ip)