import streamlit as st 
import matplotlib.pyplot as plt
from PIL import Image, ExifTags, ImageOps
import pickle
import pandas as pd
import sys
import os

from pprint import pprint
import cv2

from matplotlib import pyplot as plt
import numpy as np

# import utils
# utils.print_HI()

from datetime import datetime

# DATA SET PREPARATION AND LOADING
from detectron2.data import DatasetCatalog, MetadataCatalog

# VISUALIZATION
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode

sys.path.insert(1, os.path.abspath("./coordinate_utils/"))


import utils
utils.print_HI()

def process_detected_class(index):
    class_list = [
        {
            "id": 0,
            "name": "redbull_cans-cocacola_cans",
            "supercategory": "none"
        },
        {
            "id": 1,
            "name": "Coca Cola",
            "supercategory": "redbull_cans-cocacola_cans"
        },
        {
            "id": 2,
            "name": "Coca Cola",
            "supercategory": "redbull_cans-cocacola_cans"
        },
        {
            "id": 3,
            "name": "Coca Cola",
            "supercategory": "redbull_cans-cocacola_cans"
        },
        {
            "id": 4,
            "name": "Fridge Display",
            "supercategory": "redbull_cans-cocacola_cans"
        },
        {
            "id": 5,
            "name": "Other",
            "supercategory": "redbull_cans-cocacola_cans"
        },
        {
            "id": 6,
            "name": "Others",
            "supercategory": "redbull_cans-cocacola_cans"
        },
        {
            "id": 7,
            "name": "Red Bull",
            "supercategory": "redbull_cans-cocacola_cans"
        },
        {
            "id": 8,
            "name": "Red Bull",
            "supercategory": "redbull_cans-cocacola_cans"
        }
    ]

    return class_list[index]["name"]

def resize_with_padding(img, expected_size=(1024, 1024)):
    img.thumbnail((expected_size[0], expected_size[1]))
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    new_img = ImageOps.expand(img, padding)
    return new_img

@st.cache_data
def process_image_and_get_predictions(image):
    # Process your image and get predictions here
    model = pickle.load(open('savedModel.sav', 'rb'))
    outputsRaw = model(image)  # Assuming model is already loaded
    v = Visualizer(image[:, :, ::-1],
                   metadata=MetadataCatalog.get("my_dataset_train"), 
                   scale=0.5, 
                #    instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
    )
    x = outputsRaw["instances"].pred_classes.cpu().numpy()
    print(x)
    if (len(x) == 0):
        most_frequent_class = "No Class Detected"
    else:
        most_frequent_class = np.bincount(x).argmax()
        most_frequent_class = process_detected_class(most_frequent_class)
    out = v.draw_instance_predictions(outputsRaw["instances"].to("cpu"))
    plt.imshow(cv2.cvtColor(out.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
    plt.show()
    return out.get_image(), most_frequent_class

def resize_image(image, width, height):
    return image.resize((width, height))

st.title('Proof of Performance - Validation')

uploaded_files = st.file_uploader("Choose multiple images...", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if uploaded_files:
    if st.button('Process Images'):
        num_columns = 2  # Number of columns in the grid
        num_images = len(uploaded_files)
        num_rows = (num_images + num_columns - 1) // num_columns  # Calculate the number of rows needed
        
        # Create an empty list to store the processed images
        processed_images = []
        detected_classes = []
        resized_images = []

        # Process and store each uploaded image
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image = image.rotate(270, expand=True)
            
            image = resize_with_padding(image)
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert PIL image to numpy array

            processed_image, detected_class = process_image_and_get_predictions(image_np)
            processed_images.append(processed_image)
            detected_classes.append(detected_class)

            # Resize the image for display in the grid
            resized_image = resize_image(Image.fromarray(processed_image), 330, 330)
            resized_images.append(resized_image)
        
        # Display the processed images in a grid
        for i in range(num_rows):
            cols = st.columns(num_columns)  # Create columns for each image in the row
            for j in range(num_columns):
                idx = i * num_columns + j
                if idx < num_images:
                    # Display the image in the column
                    with cols[j]:
                        # Show the image with its caption
                        st.image(processed_images[idx], caption=detected_classes[idx], use_column_width=False) 