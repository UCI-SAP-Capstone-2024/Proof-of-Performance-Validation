import streamlit as st
from PIL import Image
import io
import os

def make_dirs():
    if not os.path.exists(os.getcwd() + "\\assets\\images"):
        os.makedirs(os.getcwd() + "\\assets\\images")
    if not os.path.exists(os.getcwd() + "\\assets\\invoices"):
        os.makedirs(os.getcwd() + "\\assets\\invoices")

def save_uploaded_file(uploaded_file, file_name):
    filepath = ""
    if uploaded_file.type == "application/pdf":
        filepath = os.path.join(os.getcwd() + "\\assets\\invoices", uploaded_file.name)
    else:
        filepath = os.path.join(os.getcwd() + "\\assets\\images", file_name)
    print(filepath)
    try:
        with open(filepath, "w+") as f:
            print(filepath)
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        print(e)
        return False
    
def main():
    st.title("Upload Files and Select Options")
    make_dirs()

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
    retailer_choices = ["Vons", "Kroger", "Albertsons", "Costco", "Target", "Walmart"]
    retialer_choice = st.selectbox("Select a Retailer:", retailer_choices)

    # Submit button
    if st.button("Submit"):
        st.write("You selected:", retialer_choice)
        for image in images_to_display:
            save_uploaded_file(uploaded_image, str(uploaded_images.index(uploaded_image)) + "_" + uploaded_image.name  )
        save_uploaded_file(uploaded_pdf, uploaded_pdf.name)
        
        st.write("Images and PDF processed.")

if __name__ == "__main__":
    main()
