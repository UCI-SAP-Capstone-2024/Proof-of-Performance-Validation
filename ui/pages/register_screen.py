import streamlit as st
import pandas as pd
import os
import bcrypt

# File path for the database (this is a simple storage for demonstration)
DB_FILE_PATH = "users_db.csv"

st.set_page_config(initial_sidebar_state="collapsed")

# Initialize the database if it does not exist
if not os.path.isfile(DB_FILE_PATH):
    df = pd.DataFrame(columns=['username', 'password'])
    df.to_csv(DB_FILE_PATH, index=False)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(username, password):
    df = pd.read_csv(DB_FILE_PATH)
    if username in df['username'].values:
        st.error("Username already exists.")
        return False
    else:
        hashed_password = hash_password(password)  # Hash the password
        df = pd.concat([pd.DataFrame([[username, hashed_password.decode('utf-8')]], columns = df.columns), df], ignore_index=True)
        df.to_csv(DB_FILE_PATH, index=False)
        return True

st.subheader("Create New Account")
new_user = st.text_input("Username")
new_password = st.text_input("Password", type='password')

if st.button("Signup"):
    if register_user(new_user, new_password):
        st.success("You have successfully created a valid account!")
        st.info("Go to the Login Menu to login")
        st.session_state.user_input = ""
    else:
        st.error("A user with that username already exists.")