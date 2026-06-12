import streamlit as st

st.set_page_config(page_title="Logout")

st.session_state.logged_in = False

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login_or_register.py")



