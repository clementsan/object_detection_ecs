---
title: Object Detection ECS
emoji: 🖼
colorFrom: green
colorTo: purple
sdk: gradio
sdk_version: 5.5.0
app_file: app.py
pinned: false
short_description: Object detection ECS
---

# Object detection - ECS 

<b>Aim: AI-driven object detection task</b>
 - Front-end: user interface via Gradio library
 - Back-end: use of ECS endpoints to run ML models


## Front-end user interface
Use of Gradio library for web interface

Command line:
> python3 app.py

<b>Note:</b> The Gradio app should now be accessible at http://localhost:7860


## Back-end ML models

ML models are available on Docker Hub and have been deployed on AWS ECS


Docker hub containers:
 - DETR model: https://hub.docker.com/r/cvachet/object-detection-detr-api
 - YOLOS model: https://hub.docker.com/r/cvachet/object-detection-yolos-api