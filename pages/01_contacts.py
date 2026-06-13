import streamlit as st
from css_utils import css_style_str

st.set_page_config(page_title="Contacts", layout="wide", page_icon=':water_buffalo:')

# ── Auth guard ────────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login_or_register.py")

# ── Supabase client ───────────────────────────────────────────────────────────
client = st.session_state.get("supabase_client")
me = st.session_state.get("my_username", "")

from supabase_utils import (
    get_all_users_info,
    get_friends_of,
    get_follower,
    get_following,
    follow,
    unfollow,
    get_chat,
    send_message,
    get_user_profile,
    get_user_preferences,
    get_user_posts,
)

# ── Session-state defaults ────────────────────────────────────────────────────
if "contacts_view" not in st.session_state:
    st.session_state.contacts_view = "list"
if "selected_user" not in st.session_state:
    st.session_state.selected_user = None
if "chat_input_key" not in st.session_state:
    st.session_state.chat_input_key = 0


def go(view, user=None):
    st.session_state.contacts_view = view
    if user:
        st.session_state.selected_user = user


def go_list():
    st.session_state.contacts_view = "list"
    st.session_state.selected_user = None


# ── Shared CSS ────────────────────────────────────────────────────────────────
st.markdown(css_style_str(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=30, show_spinner=False)
def cached_all_users(_client):
    data = get_all_users_info(_client).data or []
    return [u for u in data if u.get("username") != me]


@st.cache_data(ttl=15, show_spinner=False)
def cached_friends(_client, username):
    data = get_friends_of(username, _client).data or []
    return set(u["username"] for u in data)

@st.cache_data(ttl=15, show_spinner=False)
def cached_followers(_client, username):
    """People who follow ME (i.e. my followers)."""
    data = get_follower(username, _client).data or []
    return set(u["username"] for u in data)

@st.cache_data(ttl=15, show_spinner=False)
def cached_following(_client, username):
    """People I am following."""
    data = get_following(username, _client).data or []
    return set(u["username"] for u in data)



def avatar_letter(name):
    return name[0].upper() if name else "?"


# ═══════════════════════════════════════════════════════════════════════════════
# VIEW: CONTACTS LIST
# ═══════════════════════════════════════════════════════════════════════════════

def view_list():
    st.markdown('<div class="sec-header">👥 Contacts</div>', unsafe_allow_html=True)

    col_search, _ = st.columns([2, 3])
    with col_search:
        query = st.text_input("", placeholder="🔍  Search by name…", label_visibility="collapsed")

    with st.spinner("Loading…"):
        all_users_info = cached_all_users(client)
        all_users = [u["username"] for u in all_users_info]
        all_users_details = {u["username"]: {'food': u.get("food", ""), 'animal': u.get("animal", "")} for u in all_users_info}
        #friends = cached_friends(client, me)
        followeds = cached_following(client, me)  # people I follow
        followers = cached_followers(client, me)  # people who follow me

    filtered = [u for u in all_users if query.lower() in u.lower()] if query else all_users

    if not filtered:
        st.markdown('<p class="sub-text">No users found.</p>', unsafe_allow_html=True)
        return

    for user in filtered:
        is_following = user in followeds   # am I following this person?
        is_follower = user in followers     # is this person following me?
        is_friend = is_following and is_follower # mutual following = friends
        if is_friend:
            badge = '<span class="friend-badge">✓ Friends</span>'
        elif is_follower:
            badge = '<span class="friend-badge">✓ Follower</span>'
        elif is_following:
            badge = '<span class="friend-badge">✓ Following</span>'
        else:
            badge = ""

        with st.container():

            if all_users_details[user]["animal"]:
                v1 = all_users_details[user]["animal"][0]
            else:
                v1 = ""

            if all_users_details[user]["food"]:
                v2 = all_users_details[user]["food"][0]
            else:
                v2 = ""

            st.markdown(
                f'<div class="contact-card">'
                f'  <span class="contact-name">{user}{badge}</span>'
                #f'  <div class="avatar">{avatar_letter(user)}</div>'
                f'  <span class="pref-pill">{v1}</span>'
                f'  <span class="pref-pill">{v2}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            c1, c2, c3, _ = st.columns([1, 1, 1, 4])

           
            with c1:
                if is_following:
                    if st.button("Unfollow", key=f"unf_{user}", type="secondary"):
                        unfollow(me, user, client)
                        cached_followers.clear()
                        cached_following.clear()
                        cached_friends.clear()
                        st.rerun()
                else:
                    if st.button("Follow", key=f"fol_{user}", type="primary"):
                        follow(me, user, client)
                        cached_followers.clear()
                        cached_following.clear()
                        cached_friends.clear()
                        st.rerun()
            with c2:
                if st.button("💬 Chat", key=f"chat_{user}"):
                    go("chat", user)
                    st.rerun()
            with c3:
                if st.button("👤 Profile", key=f"prof_{user}"):
                    go("profile", user)
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# VIEW: CHAT
# ═══════════════════════════════════════════════════════════════════════════════

def view_chat():
    user = st.session_state.selected_user
    if not user:
        go_list(); st.rerun(); return

    if st.button("← Back to contacts", type="secondary"):
        go_list(); st.rerun()

    st.markdown(f'<div class="sec-header">💬 Chat with {user}</div>', unsafe_allow_html=True)

    messages = get_chat(me, user, client).data or []

    chat_html = '<div class="chat-wrap">'
    for msg in messages:
        sender  = msg['sender']
        content = msg['message']
        ts      = msg['datetime']
        side    = "me" if sender == me else "them"
        chat_html += (
            f'<div class="bubble-row {side}">'
            f'  <div>'
            f'    <div class="bubble {side}">{content}</div>'
            f'    <div class="bubble-meta">{ts}</div>'
            f'  </div>'
            f'</div>'
        )
    chat_html += "</div>"

    if messages:
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown('<p class="sub-text">No messages yet. Say hello!</p>', unsafe_allow_html=True)

    with st.form(key=f"msg_form_{st.session_state.chat_input_key}", clear_on_submit=True):
        text = st.text_input("", placeholder="Type a message…", label_visibility="collapsed")
        if st.form_submit_button("Send ↑") and text.strip():
            send_message(me, user, text.strip(), client)
            st.session_state.chat_input_key += 1
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# VIEW: PROFILE
# ═══════════════════════════════════════════════════════════════════════════════

def view_profile():
    user = st.session_state.selected_user
    if not user:
        go_list(); st.rerun(); return

    if st.button("← Back to contacts", type="secondary"):
        go_list(); st.rerun()

    description  = get_user_profile(user, client).data or ""
    prefs_raw    = get_user_preferences(user, client).data
    prefs        = prefs_raw[0] if prefs_raw else {}
    posts        = get_user_posts(user, client).data or []
    friends      = cached_friends(client, me)
    is_friend    = user in friends
    badge        = '<span class="friend-badge">✓ Friends</span>' if is_friend else ""

    # ── Header card ──
    st.markdown(
        f'<div class="profile-box">'
        f'  <div class="profile-avatar">{avatar_letter(user)}</div>'
        f'  <div class="contact-name" style="font-size:1.4rem">{user} {badge}</div>'
        f'  <div class="section-label">Bio</div>'
        f'  <div class="profile-desc">{description if description else "<em>No bio yet.</em>"}</div>',
        unsafe_allow_html=True,
    )

    # ── Preferences pills ──
    if prefs:
        animal = prefs.get("animal", "")
        food   = prefs.get("food", "")
        pills  = ""
        if animal: pills += f'<span class="pref-pill">🐾 {animal}</span>'
        if food:   pills += f'<span class="pref-pill">🍽️ {food}</span>'
        if pills:
            st.markdown(
                f'<div class="section-label" style="margin-top:16px">Favourites</div>{pills}',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Action buttons ──
    st.markdown("")
    c1, c2 = st.columns([1, 5])
    with c1:
        if is_friend:
            if st.button("Unfollow", type="secondary"):
                unfollow(me, user, client)
                cached_followers.clear()
                cached_following.clear()
                cached_friends.clear()
                st.rerun()
        else:
            if st.button("Follow", type="primary"):
                follow(me, user, client)
                cached_followers.clear()
                cached_following.clear()
                cached_friends.clear()
                st.rerun()
    with c2:
        if st.button(f"💬 Chat with {user}"):
            go("chat", user)
            st.rerun()

    # ── Posts ──
    st.markdown(f'<div class="section-label" style="margin-top:24px">📝 Posts by {user}</div>', unsafe_allow_html=True)
    if posts:
        for post in posts:
            content = post.get("content", "")
            ts      = post.get("datetime", post.get("created_at", ""))
            st.markdown(
                f'<div class="post-card">'
                f'  <div class="post-meta">{ts}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(content)   # render as markdown
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="sub-text">No posts yet.</p>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════

view = st.session_state.contacts_view

if view == "list":
    view_list()
elif view == "chat":
    view_chat()
elif view == "profile":
    view_profile()
else:
    go_list()
    st.rerun()
