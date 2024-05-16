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

@st.cache_data
def process_image_and_get_predictions(image):
    # Process your image and get predictions here
    model = pickle.load(open('savedModel.sav', 'rb'))
    outputsRaw = model(image)  # Assuming model is already loaded
    v = Visualizer(image[:, :, ::-1],
                   metadata=MetadataCatalog.get("my_dataset_train"), 
                   scale=0.5, 
                   instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
    )
    x = outputsRaw["instances"].pred_classes.cpu().numpy()
    most_frequent_class = np.bincount(x).argmax()
    if most_frequent_class == 7:
        most_frequent_class = "Red Bull"
    out = v.draw_instance_predictions(outputsRaw["instances"].to("cpu"))
    plt.imshow(cv2.cvtColor(out.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
    plt.show()
    return out.get_image(), most_frequent_class

st.title('Proof of Performance - Validation')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert PIL image to numpy array
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    if st.button('Process Image'):
        processed_image, detected_class = process_image_and_get_predictions(image_np)
        # matched_store = utils.match_promotion_to_retailer(image, detected_class)
        # st.markdown(matched_store["store"] + ": " + matched_store["address"])
        # st.success("Promotion matched to store: " + matched_store["store_id"] + " at " + matched_store["address"] + " with product: " + matched_store["product"])
        st.image(processed_image, caption='Processed Image.', use_column_width=True)

