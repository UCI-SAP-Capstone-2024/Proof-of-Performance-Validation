import streamlit as st
import pandas as pd
import os
import bcrypt

# File path for the database (this is a simple storage for demonstration)
DB_FILE_PATH = "users_db.csv"

st.set_page_config(initial_sidebar_state="collapsed")

if not os.path.isfile(DB_FILE_PATH):
    df = pd.DataFrame(columns=['username', 'password'])
    df.to_csv(DB_FILE_PATH, index=False)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_login(username, password):
    df = pd.read_csv(DB_FILE_PATH)
    user = df[df['username'] == username]
    if not user.empty:
        stored_password = user.iloc[0]['password']
        return check_password(stored_password, password)
    return False

st.subheader("Login Section")
username = st.text_input("Username", key='login_username_input')
password = st.text_input("Password", type='password', key='login_password_input')

if st.button("Login"):
    if check_login(username, password):
        st.success(f"Welcome {username}")
    else:
        st.error("Incorrect Username/Password")