import streamlit as st
from css_utils import css_style_str

st.set_page_config(
    page_title="Social Graph",
    page_icon="👋",
)

st.markdown(css_style_str(), unsafe_allow_html=True)

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
    if st.button('Login or register Now', type="primary"):
        st.switch_page("pages/login_or_register.py")
else:
    if st.button('Logout'):
        st.session_state.logged_in = False


if st.toggle("about"):

    st.markdown("""
## About the code

This project is built with Streamlit and Supabase, showcasing a simple social network app with user profiles, posts, and a social graph.
        
It includes a simple interactive graph based on networkx and pyvis.

The source code is available on [GitHub](https://github.com/Fede-Rausa/CyberBull#cyberbull)
""")
    
if st.toggle("disclaimer"):

    st.markdown("""
## Disclaimer

This project is for educational purposes only and does not promote or endorse any form of cyberbullying or harassment.
Your privacy gets here the best protection possible.
""")
