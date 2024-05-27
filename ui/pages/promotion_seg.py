import streamlit as st 
import matplotlib.pyplot as plt
from PIL import Image
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

class_list = [
        {
            "id": 0,
            "name": "redbull_cans-cocacola_cans",
            "supercategory": "none"
        },
        {
            "id": 1,
            "name": "Coca Cola Bottles",
            "supercategory": "Coca Cola"
        },
        {
            "id": 2,
            "name": "Coca Cola Cans",
            "supercategory": "Coca Cola"
        },
        {
            "id": 3,
            "name": "Coca Cola Logo",
            "supercategory": "Coca Cola"
        },
        {
            "id": 4,
            "name": "Fridge Display",
            "supercategory": "None"
        },
        {
            "id": 5,
            "name": "Other Bottles",
            "supercategory": "None"
        },
        {
            "id": 6,
            "name": "Other Cans",
            "supercategory": "None"
        },
        {
            "id": 7,
            "name": "Red Bull Cans",
            "supercategory": "Red Bull"
        },
        {
            "id": 8,
            "name": "Red Bull Logo",
            "supercategory": "Red Bull"
        }
    ]


def process_detected_class(index):
    return class_list[index]["supercategory"]

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
    most_frequent_class = np.bincount(x).argmax()
    most_frequent_class = process_detected_class(most_frequent_class)
    out = v.draw_instance_predictions(outputsRaw["instances"].to("cpu"))
    plt.imshow(cv2.cvtColor(out.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
    plt.show()
    return out.get_image(), most_frequent_class


def resize_image(image, width, height):
    # return np.asarray(image.thumbnail((width,height)))
    return image.resize((width, height))

st.title('Proof of Performance - Validation')

st.sidebar.title("Image Categories")
for cls in class_list[1:]:
    st.sidebar.markdown(f"**ID {cls['id']}**: {cls['name']}")

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
        matched_stores = []

        # Process and store each uploaded image
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert PIL image to numpy array
            
            processed_image, detected_class = process_image_and_get_predictions(image_np)
            processed_images.append(processed_image)
            detected_classes.append(detected_class)

            matched_store = utils.match_promotion_to_retailer(image, detected_class)
            matched_stores.append(matched_store)
            # st.markdown(matched_store["store"] + ": " + matched_store["address"])
        
            # Resize the image for display in the grid
            resized_image = resize_image(Image.fromarray(processed_image), 340, 340)
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
                        st.image(resized_images[idx], caption=detected_classes[idx], use_column_width=False)
                        if len(matched_stores) > 0 and matched_stores[idx] is not None:
                            st.success("Promotion Matched!\n\nPromotion ID: "+ matched_stores[idx]["promotion_id"]+ "\n\nStore: " + matched_stores[idx]["store_retailer"] + " at " + matched_stores[idx]["address"] + "\n\nProduct: " + matched_stores[idx]["product"])
                        else:
                            st.error("No promotion matched")
