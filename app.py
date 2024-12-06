import gradio as gr

import os
import requests
import json
import utils

from dotenv import load_dotenv, find_dotenv

# List of ML models
list_models = ["facebook/detr-resnet-50", "facebook/detr-resnet-101", "hustvl/yolos-tiny", "hustvl/yolos-small"]
list_models_simple = [os.path.basename(model) for model in list_models]

# ECS APIs
AWS_DETR_URL = None
AWS_YOLOS_URL = None


# Initialize API URLs from env file or global settings
def initialize_api_endpoints():

    env_path = find_dotenv('config_api.env')
    if env_path:
        load_dotenv(dotenv_path=env_path)
        print("config_api.env file loaded successfully.")
    else:
        print("config_api.env file not found.")

    # Use of AWS ECS endpoint or local container by default
    global AWS_DETR_URL,  AWS_YOLOS_URL
    AWS_DETR_URL = os.getenv("AWS_DETR_URL", default="http://0.0.0.0:8000")
    AWS_YOLOS_URL = os.getenv("AWS_YOLOS_URL", default="http://0.0.0.0:8001")


# Retrieve correct endpoint based on model_type
def retrieve_api_endpoint(model_type):
    if "detr" in model_type:
        API_URL = AWS_DETR_URL
    else:
        API_URL = AWS_YOLOS_URL

    return API_URL


#@spaces.GPU
def detect(image_path, model_id, threshold):
    print("\n Object detection...")
    print("\t ML model:", list_models[model_id])

    with open(image_path, 'rb') as image_file:
       image_bytes = image_file.read()

    API_URL = retrieve_api_endpoint(list_models_simple[model_id])

    # API Call for object prediction with model type as query parameter
    API_Endpoint = API_URL + "/api/v1/detect" + "?model=" + list_models_simple[model_id]
    print("\t API_Endpoint: ", API_Endpoint)

    response = requests.post(API_Endpoint, files={"image": image_bytes})
    if response.status_code == 200:
        # Process the response
        response_string = response.json()
        response_dict = json.loads(response_string)
        print('\t API response', response_string)
    else:
        response_dict = {"Error": response.status_code}
        gr.Error(f"\t API Error: {response.status_code}")

    # Generate gradio output components: image and json
    output_json, output_pil_img = utils.generate_gradio_outputs(image_path, response_dict, threshold)

    return output_json, output_pil_img


def demo():
    initialize_api_endpoints()
    with gr.Blocks(theme="base") as demo:
        gr.Markdown("# Object detection task - use of ECS endpoints")
        gr.Markdown(
            """
            This web application uses transformer models to detect objects on images.
            Machine learning models were trained on the COCO dataset.
            You can load an image and see the predictions for the objects detected.
            
            Note: This web application uses AWS ECS endpoints as a back-end APIs to run these ML models.
            """
        )

        with gr.Row():
            with gr.Column():
                model_id = gr.Radio(list_models, \
                               label="Detection models", value=list_models[0], type="index", info="Choose your detection model")
            with gr.Column():
                threshold = gr.Slider(0, 1.0, value=0.9, label='Detection threshold', info="Choose your detection threshold")

        with gr.Row():
            input_image = gr.Image(label="Input image", type="filepath")
            output_image = gr.Image(label="Output image", type="pil")
            output_json = gr.JSON(label="JSON output", min_height=240, max_height=300)

        with gr.Row():
            submit_btn = gr.Button("Submit")
            clear_button = gr.ClearButton()

        gr.Examples(['samples/savanna.jpg', 'samples/boats.jpg'], inputs=input_image)

        submit_btn.click(fn=detect, inputs=[input_image, model_id, threshold], outputs=[output_json, output_image])
        clear_button.click(lambda: [None, None, None], \
                        inputs=None, \
                        outputs=[input_image, output_image, output_json], \
                        queue=False)

    demo.queue().launch(debug=True)

if __name__ == "__main__":
    demo()