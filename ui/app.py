import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")


def main():
    st.title("Simple Login and Registration App")
    st.markdown('<div><a href="/login_screen" target="_self">Login page</a></div>', unsafe_allow_html=True)
    st.markdown('<div><a href="/register_screen" target="_self">Register page</a></div>', unsafe_allow_html=True)
    

if __name__ == '__main__':
    main()
