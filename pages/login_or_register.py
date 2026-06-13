import streamlit as st
from supabase import create_client
from supabase_utils import try_to_add_user, try_to_login
from css_utils import css_style_str

st.set_page_config(page_title="Login or Register", page_icon="🐃")

st.markdown(css_style_str(), unsafe_allow_html=True)
# --- Callbacks (only set state, never call switch_page/rerun) ---

if 'supabase_client' not in st.session_state:
    url = st.secrets["sb_url"]
    key = st.secrets["sb_key"]
    with st.spinner("Connecting to database..."):
        st.session_state.supabase_client = create_client(url, key)

def register_to_login(xbool):
    st.session_state.login_or_register = xbool

def register_new_account(username, pswd1, pswd2):
    if check_registration_validity(username, pswd1, pswd2):
        res = try_to_add_user(username=username, password=pswd1, myclient=st.session_state.supabase_client)
        success = res.data
        if success:
            st.session_state.register_success = True
        else:
            st.session_state.register_success = False
            st.session_state.form_error = "Username already taken"

def check_registration_validity(username, pswd1, pswd2):
    if not username or not pswd1 or not pswd2:
        st.session_state.form_error = "All fields are required"
        return False
    if pswd1 != pswd2:
        st.session_state.form_error = "Passwords do not match"
        return False
    if len(pswd1) < 4:
        st.session_state.form_error = "Password must be at least 4 characters long"
        return False
    if len(username) < 3:
        st.session_state.form_error = "Username must be at least 3 characters long"
        return False
    st.session_state.form_error = None
    return True

def user_login(username, password):
    res = try_to_login(username=username, password=password, myclient=st.session_state.supabase_client).data[0]
    if res['success']:
        st.session_state.logged_in = True   # ✅ only set state here
        st.session_state.my_username = username
    else:
        st.session_state.logged_in = False
        st.session_state.login_error = res['message']

# --- Initialize session state ---

if "login_or_register" not in st.session_state:
    st.session_state.login_or_register = True
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = None
if "form_error" not in st.session_state:
    st.session_state.form_error = None
if "register_success" not in st.session_state:
    st.session_state.register_success = False

# --- Redirect AFTER rerun, outside any callback ---

if st.session_state.logged_in:
    st.switch_page("pages/01_contacts.py")   # ✅ called in main body, works fine

# --- UI ---

if st.session_state.login_or_register:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_login(username, password)
        st.rerun()
    st.button("Don't have an account? Register here",
              on_click=register_to_login, args=(False,))
    if st.session_state.login_error:
        st.error(st.session_state.login_error)
        st.session_state.login_error = None
else:
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    st.button("Register", on_click=register_new_account,
              args=(username, password, confirm_password))
    st.button("Already have an account? Login here",
              on_click=register_to_login, args=(True,))
    if st.session_state.form_error:
        st.error(st.session_state.form_error)
        st.session_state.form_error = None
    if st.session_state.register_success:
        st.success("Account created successfully")
        st.session_state.register_success = False
