import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from pymongo import MongoClient
import time

def connect_to_db():
    # Connect to your MongoDB Atlas cluster
    client = MongoClient("mongodb+srv://sapsuser:3dUEbY0ijMlL81vF@sap-pv.bdcccxg.mongodb.net/?retryWrites=true&w=majority&appName=SAP-PV")
    db = client["SAPPV"]
    # st.session_state.db = db
    return db


def main():
    if(not st.session_state.get("username")):
        st.error("You need to login first!")
        switch_page("login_screen")

    # Title of the application
    st.title('Current Promotions')

    db = connect_to_db()

    # message_placeholder = st.empty()
    # message_placeholder.success(f"Welcome to the Promotions Page, {st.session_state.username}!")
    # time.sleep(5)
    # message_placeholder.empty()
    st.success(f"Welcome to the Promotions Page, {st.session_state.username}!")

    # Filepath to your CSV file
    # csv_file_path = 'promotions.csv'
    
    # Read the CSV file into a pandas DataFrame
    # df = pd.read_csv(csv_file_path)

    # Display the DataFrame
    # st.write("### Displaying the CSV file:")
    # st.dataframe(df)

    collection = db["promotions"] 

    documents = list(collection.find())

    collection_name = collection.name

    if documents:
        df = pd.DataFrame(documents)
        # st.write("### Documents in the '{}' collection:".format(collection_name))
        st.dataframe(df)
    else:
        st.write("No documents found in the '{}' collection.".format(collection_name))

    if st.button("Validate Promotions"):
        switch_page("promotion_seg")

if __name__ == "__main__":
    main()