import streamlit as st
import bcrypt

st.set_page_config(initial_sidebar_state="collapsed")
users_collection = st.session_state.db["users"]

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(username, password):
    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        st.error("Username already exists.")
        return False
    else:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert the new user into the database
        users_collection.insert_one({"username": username, "password": hashed_password})
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