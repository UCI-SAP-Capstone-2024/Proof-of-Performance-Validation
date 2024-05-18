import streamlit as st
from PIL import Image
import io
import os

VONS_DIR = "C:\Code Files\Python Codes\Capstone\Proof-of-Performance-Validation\\assets\\vons"
ALBERTSONS_DIR = "C:\Code Files\Python Codes\Capstone\Proof-of-Performance-Validation\\assets\\albertsons"
TARGET_DIR = "C:\Code Files\Python Codes\Capstone\Proof-of-Performance-Validation\\assets\\target"
KROGER_DIR = "C:\Code Files\Python Codes\Capstone\Proof-of-Performance-Validation\\assets\\kroger"

def make_dirs():
    if not os.path.exists(os.getcwd() + "\\assets\\images"):
        os.makedirs(os.getcwd() + "\\assets\\images")
    if not os.path.exists(os.getcwd() + "\\assets\\invoices"):
        os.makedirs(os.getcwd() + "\\assets\\invoices")

def save_uploaded_file(retailer_choice, uploaded_file, file_name):
    if retailer_choice == "VONS":
        filepath = VONS_DIR
    elif retailer_choice == "ALBERTSONS":
        filepath = ALBERTSONS_DIR
    elif retailer_choice == "TARGET":
        filepath = TARGET_DIR
    elif retailer_choice == "KROGER":
        filepath = KROGER_DIR
    if uploaded_file.type == "application/pdf":
        filepath = os.path.join(filepath + "\\invoices", uploaded_file.name)
    else:
        filepath = os.path.join(filepath + "\\images", file_name)
    print(filepath)
    try:
        with open(filepath, "wb") as f:
            # print(filepath)
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        print(e)
        return False
    
def main():
    st.title("Upload Files and Select Options")
    # make_dirs()

    # promotion_id = st.text_input("Promotion ID", key='promotion_id_ip')


    # Multiple Image Upload
    uploaded_images = st.file_uploader("Choose images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    images_to_display = []

    # Display uploaded images
    if uploaded_images:
        for uploaded_image in uploaded_images:
            image = Image.open(uploaded_image)
            images_to_display.append(image)
            # print(uploaded_image.name, uploaded_image.type, uploaded_image.size)
        st.image(images_to_display, width=200, caption=["Uploaded Image"] * len(images_to_display))


    # PDF Upload
    uploaded_pdf = st.file_uploader("Choose a PDF file", type='pdf')

    # If a PDF is uploaded, show a message (processing the PDF would depend on requirements)
    if uploaded_pdf:
        st.success("PDF Uploaded Successfully!")

    # Dropdown menu for retailer
    retailer_choices = ["VONS", "KROGER", "ALBERTSONS", "TARGET"]
    retailer_choice = st.selectbox("Select a Retailer:", retailer_choices)

    # Submit button
    if st.button("Submit"):
        st.write("You selected:", retailer_choice)
        for image in uploaded_images:
            save_uploaded_file(retailer_choice, image, image.name  )
        save_uploaded_file(retailer_choice, uploaded_pdf, uploaded_pdf.name)
        
        st.write("Images and PDF processed.")

if __name__ == "__main__":
    main()
