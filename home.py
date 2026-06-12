import streamlit as st


st.set_page_config(
    page_title="Social Graph",
    page_icon="👋",
)

st.markdown(
    """
    # Welcome to CyberBull! 👋

    The first social network where cyberbullying is not just tolerated, but actively encouraged.

    You can see the trending dumb creep victims and join their social persecution in real-time!

    All users privacy is exposed, and full of resources that let you engage in the fun.

    Become a part of the conversation today!
    """
)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.get("logged_in", False):
    if st.button('Login or register Now'):
        st.switch_page("pages/login_or_register.py")
else:
    if st.button('Logout'):
        st.session_state.logged_in = False

