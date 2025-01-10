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

[![](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker Pulls](https://img.shields.io/docker/pulls/cvachet/object-detection-ecs)](https://hub.docker.com/repository/docker/cvachet/object-detection-ecs)

![example workflow](https://github.com/clementsan/object_detection_ecs/actions/workflows/publish_docker_image.yml/badge.svg)
![example workflow](https://github.com/clementsan/object_detection_ecs/actions/workflows/sync_HFSpace.yml/badge.svg)

**Aim: AI-driven object detection task**
 - Front-end: user interface via Gradio library
 - Back-end: use of AWS ECS endpoints to run Machine Learning models

----
**Table of contents:**
- [Front-end user interface](#1-front-end-user-interface)
  - [Environment variables](#11-environment-variables)
  - [Local execution](#12-local-execution)
- [Back-end Machine Learning models](#2-back-end-machine-learning-models)
  - [Information on ML models](#21-information-on-ml-models)
  - [Deployment on AWS ECS](#22-information-on-aws-ecs-deployment)
- [Deployment on Hugging Face](#3-deployment-on-hugging-face)
- [Deployment on Docker Hub](#4-deployment-on-docker-hub)
----

## 1. Front-end user interface

### 1.1. Environment variables

This web app uses two environment variables, corresponding to the endpoints for the deployed machine learning models
(cf. [Section 2 - Back-end ML models](#2-back-end-ml-models))

Environment variables:
 - AWS_DETR_URL: endpoint for DETR model
 - AWS_YOLOS_URL: endpoint for YOLOS model

### 1.2. Local execution
Use of Gradio library for web interface

Command line:
> python3 app.py

<b>Note:</b> The Gradio app should now be accessible at http://localhost:7860



## 2. Back-end machine learning models

Machine Learning (ML) models are available on Docker Hub and have been deployed to AWS ECS (Elastic Container Service)

### 2.1. Information on ML models
**Github repos:**
 - DETR API: https://github.com/clementsan/object_detection_detr_api
 - YOLOS API: https://github.com/clementsan/object_detection_yolos_api

**Docker hub containers:**
 - DETR API: https://hub.docker.com/r/cvachet/object-detection-detr-api
 - YOLOS API: https://hub.docker.com/r/cvachet/object-detection-yolos-api

### 2.2 Information on AWS ECS deployment

ECS: Elastic Container Service

<details>

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

</details>


### 3. Deployment on Hugging Face

This web application has been deployed on Hugging Face. 

HF Space URL: https://huggingface.co/spaces/cvachet/object_detection_ecs


### 4. Deployment on Docker Hub

This web application has been deployed on Docker Hub. 

URL: https://hub.docker.com/r/cvachet/object-detection-ecs
