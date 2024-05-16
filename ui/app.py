import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from pymongo import MongoClient
st.set_page_config(initial_sidebar_state="collapsed")

@st.cache_resource
def connect_to_db():
    # Connect to your MongoDB Atlas cluster
    client = MongoClient("mongodb+srv://sapsuser:3dUEbY0ijMlL81vF@sap-pv.bdcccxg.mongodb.net/?retryWrites=true&w=majority&appName=SAP-PV")
    db = client["SAPPV"]
    st.session_state.db = db
    return db

def main():
    st.title("SAP PromoteSync")
    st.markdown("Welcome to SAP PromoteSync! This is a tool to validate the proof of performance of your promotions.")
    # st.markdown('<div><a href="/login_screen" target="_self">Login page</a></div>', unsafe_allow_html=True)
    # st.markdown('<div><a href="/register_screen" target="_self">Register page</a></div>', unsafe_allow_html=True)
    # st.markdown('<div><a href="/upload_proof_screen" target="_self">Proof Upload page</a></div>', unsafe_allow_html=True)
    connect_to_db()
    print("Connected to DB")
    want_to_contribute = st.button("Log In!")
    if want_to_contribute:
        switch_page("login_screen")
    

if __name__ == '__main__':
    main()
