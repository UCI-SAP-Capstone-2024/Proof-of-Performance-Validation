import streamlit as st
import pandas as pd
import os
import bcrypt

# File path for the database (this is a simple storage for demonstration)
DB_FILE_PATH = "users_db.csv"

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

def check_login(username, password):
    df = pd.read_csv(DB_FILE_PATH)
    user = df[df['username'] == username]
    if not user.empty:
        stored_password = user.iloc[0]['password']
        return check_password(stored_password, password)
    return False

def main():
    st.title("Simple Login and Registration App")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login Section")
        username = st.text_input("Username", key='login_username_input')
        password = st.text_input("Password", type='password', key='login_password_input')
        
        if st.button("Login"):
            if check_login(username, password):
                st.success(f"Welcome {username}")
            else:
                st.error("Incorrect Username/Password")

    elif choice == "Register":
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

if __name__ == '__main__':
    main()
