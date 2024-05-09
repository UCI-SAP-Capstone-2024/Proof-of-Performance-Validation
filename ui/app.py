import streamlit as st
from streamlit_extras.switch_page_button import switch_page
st.set_page_config(initial_sidebar_state="collapsed")


def main():
    st.title("Simple Login and Registration App")
    # st.markdown('<div><a href="/login_screen" target="_self">Login page</a></div>', unsafe_allow_html=True)
    # st.markdown('<div><a href="/register_screen" target="_self">Register page</a></div>', unsafe_allow_html=True)
    # st.markdown('<div><a href="/upload_proof_screen" target="_self">Proof Upload page</a></div>', unsafe_allow_html=True)
    want_to_contribute = st.button("I want to contribute!")
    if want_to_contribute:
        switch_page("login_screen")
    

if __name__ == '__main__':
    main()
