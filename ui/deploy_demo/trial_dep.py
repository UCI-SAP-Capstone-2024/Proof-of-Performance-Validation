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

def rotate_image(image):
    try:
        # image=Image.open(filepath)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        
        exif = image._getexif()
        if exif is None:
            print("No EXIF metadata found")
            # image=image.transpose(Image.ROTATE_270)
            return image
        if exif[orientation] == 3:
            image=image.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            image=image.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            image=image.transpose(Image.ROTATE_90)
        print("Works fine!")
        # image.save(filepath)
        # image.close()
        return image
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        print("Error in rotation")
        image=image.transpose(Image.ROTATE_270)
        return image

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
    # plt.show()
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
        # matched_stores = []

        # Process and store each uploaded image
        for uploaded_file in uploaded_files:
            image_og = Image.open(uploaded_file)
            # image = image.rotate(270, expand=True)
            image_rt = rotate_image(image_og)
            image = resize_with_padding(image_rt)
            image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert PIL image to numpy array

            processed_image, detected_class = process_image_and_get_predictions(image_np)
            processed_images.append(processed_image)
            detected_classes.append(detected_class)

            # matched_store = utils.match_promotion_to_retailer(image_og, detected_class)
            # if matched_store is not None:
            #     matched_stores.append(matched_store)

            # Resize the image for display in the grid
            resized_image = resize_image(Image.fromarray(processed_image), 300, 300)
            resized_images.append(resized_image)
        print(detected_classes)
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
                        # st.success(f"Promotion Matched!\n\nPromotion ID: 1013 \n\nStore: UCI at 419 Physical Sciences Quad, Irvine, CA 92697\n\nProduct: {set(detected_classes)}")

                        # if len(matched_stores) > 0 and matched_stores[idx] is not None:
                        #     st.success("Promotion Matched!\n\nPromotion ID: "+ matched_stores[idx]["promotion_id"]+ "\n\nStore: " + matched_stores[idx]["store_retailer"] + " at " + matched_stores[idx]["address"] + "\n\nProduct: " + matched_stores[idx]["product"])
                        # else:
                        #     st.error("No promotion matched")