import streamlit as st
import bcrypt
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(initial_sidebar_state="collapsed")
users_collection = st.session_state.db["users"]

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_login(username, password):
    # Retrieve the user from the database
    user = users_collection.find_one({"username": username})
    if user:
        # Check if the password matches
        if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return True
    return False

if st.session_state.get("username"):
    switch_page("promotions")

st.subheader("Login Section")

# Add image after the subheading
st.image("C:/Code Files/Python Codes/Capstone/Proof-of-Performance-Validation/ui/pages/promo.png")

username = st.text_input("Username", key='login_username_input')
password = st.text_input("Password", type='password', key='login_password_input')
# st.write("Don't have an account? [Sign Up](/register_screen)")
if st.button("Login"):
    if check_login(username, password):
        st.success(f"Welcome {username}")
        st.session_state.username = username
        switch_page("promotions")
    else:
        st.error("Incorrect Username/Password")