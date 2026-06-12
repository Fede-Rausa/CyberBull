# import streamlit as st
# from supabase_utils import get_user_profile, set_user_profile, delete_user

# st.set_page_config(page_title="My Profile")

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if "deleting" not in st.session_state:
#     st.session_state.deleting = False

# if 'profile_editing' not in st.session_state:
#     st.session_state.profile_editing = False

# if not st.session_state.get("logged_in", False):
#     st.switch_page("pages/login_or_register.py")


# st.title("My Profile")
# with st.spinner("querying profile data..."):
#     if st.session_state.logged_in:

#         if not st.session_state.deleting:
#             old_description = get_user_profile(st.session_state.my_username, st.session_state.supabase_client).data
#             st.markdown(st.session_state.my_username)
#             st.markdown(old_description)

#             if st.session_state.profile_editing:
#                 new_description = st.text_area("Edit Description", old_description)
#                 c1, c2 = st.columns([1, 1])
#                 with c1:
#                     if st.button("Save", type="primary"):
#                         set_user_profile(st.session_state.my_username, new_description, st.session_state.supabase_client)
#                         st.session_state.profile_editing = False
#                         st.rerun()
#                 with c2:
#                     if st.button("Cancel", type="secondary"):
#                         st.session_state.profile_editing = False
#                         st.rerun()
#             else:
#                 if st.button("Edit Profile", type="secondary"):
#                     st.session_state.profile_editing = True
#                     st.rerun()

#             if st.button("Delete Account", type="primary"):
#                 st.session_state.deleting = True
#                 st.rerun()

#         else:
#             st.warning("Are you sure you want to delete your account? This action cannot be undone.")

#             c1, c2 = st.columns([1, 1])

#             with c1:
#                 if st.button("Confirm and delete my virtual life", type="primary"):
#                     delete_user(st.session_state.my_username, st.session_state.supabase_client)
#                     st.session_state.logged_in = False
#                     st.session_state.my_username = None
#                     st.session_state.profile_editing = False
#                     st.success("Account deleted successfully. You have successfully killed yourself.")

#             with c2:
#                 if st.button("No, I want to keep being alive", type="secondary"):
#                     st.session_state.deleting = False
#                     st.rerun()




import streamlit as st
from css_utils import css_style_str
from supabase_utils import (
    get_user_profile,
    set_user_profile,
    get_user_preferences,
    set_user_preferences,
    send_post,
    get_user_posts,
    delete_user
)

st.set_page_config(page_title="My Profile", page_icon="👤")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login_or_register.py")

if "profile_editing" not in st.session_state:
    st.session_state.profile_editing = False
if "prefs_editing" not in st.session_state:
    st.session_state.prefs_editing = False
if "post_key" not in st.session_state:
    st.session_state.post_key = 0

if "deleting" not in st.session_state:
    st.session_state.deleting = False

client   = st.session_state.supabase_client
username = st.session_state.my_username

# ── Options ──────────────────────────────────────────────────────────────────
ANIMALS = [
    # --- Original ---
    "🐶 Dog", "🐱 Cat", "🐺 Wolf", "🦊 Fox", "🐻 Bear", "🐼 Panda",
    "🦁 Lion", "🐯 Tiger", "🐸 Frog", "🦅 Eagle", "🐬 Dolphin",
    "🐙 Octopus", "🦄 Unicorn", "🐲 Dragon",
    
    # --- Mammals & Woodlands ---
    "🐨 Koala", "🐯 Leopard", "🐵 Monkey", "🦍 Gorilla", "🦧 Orangutan", 
    "🦌 Deer", "🦬 Bison", "🦏 Rhinoceros", "🦛 Hippopotamus", "🐘 Elephant", 
    "🐫 Camel", "🦒 Giraffe", "🦘 Kangaroo", "🦥 Sloth", "🦦 Otter", 
    "🦫 Beaver", "🦡 Badger", "🦔 Hedgehog", "🦇 Bat", "🐿️ Chipmunk",
    
    # --- Birds ---
    "🦉 Owl", "🦜 Parrot", "🦚 Peacock", "🦩 Flamingo", "🦢 Swan", 
    "🐧 Penguin", "🦆 Duck", "🐓 Rooster",
    
    # --- Marine & Aquatic ---
    "🦈 Shark", "🐳 Whale", " Seal", "🐊 Crocodile", "🐢 Turtle", 
    "🦞 Lobster", "🦀 Crab", "🦑 Squid", "🐠 Tropical Fish",
    
    # --- Reptiles & Bugs ---
    "🦎 Lizard", "🐍 Snake", "🐝 Honeybee", "🦋 Butterfly", "🐞 Ladybug"
]


FOODS = [
    # --- Original ---
    "🍕 Pizza", "🍣 Sushi", "🍜 Ramen", "🌮 Tacos", "🍔 Burger",
    "🥗 Salad", "🍝 Pasta", "🥘 Curry", "🦧 Falafel", "🍱 Bento",
    "🫕 Fondue", "🥩 Steak", "🍦 Ice Cream", "🍫 Chocolate",
    
    # --- Savory Meals & Street Food ---
    "🍗 Fried Chicken", "🌭 Hot Dog", "🍟 Fries", "🥪 Sandwich", "🫔 Tamale", 
    "🫓 Flatbread", "🥟 Dumpling", "🍤 Tempura", "🥮 Mooncake", "🥨 Pretzel", 
    "🥯 Bagel", "🧀 Cheese", "🍳 Eggs", "🥞 Pancakes", "🧇 Waffles",
    
    # --- Bakery & Desserts ---
    "🍰 Shortcake", "🍩 Donut", "🍪 Cookie", "🧁 Cupcake", "🥧 Pie", 
    "🥐 Croissant", "🥖 Baguette", "🍯 Honey", "🍿 Popcorn",
    
    # --- Fruits & Vegetables (Fresh Foods) ---
    "🍓 Strawberry", "🥑 Avocado", "🍉 Watermelon", "🍍 Pineapple", "🥭 Mango", 
    "🍑 Peach", "🍒 Cherries", "🍌 Banana", "🍎 Apple", "🥦 Broccoli", 
    "🌽 Corn", "🥕 Carrot", "🌶️ Hot Pepper", "🍄 Mushroom"
]


# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(css_style_str(), unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading profile…"):
    bio       = get_user_profile(username, client).data or ""
    prefs_raw = get_user_preferences(username, client).data
    prefs     = prefs_raw[0] if prefs_raw else {}
    posts     = get_user_posts(username, client).data or []

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="sec-header">👤 My Profile</div>'
    f'<div class="avatar-lg">{username[0].upper()}</div>'
    f'<div style="font-size:1.3rem;font-weight:700;color:var(--text);margin-bottom:20px">{username}</div>',
    unsafe_allow_html=True,
)

if not st.session_state.deleting:

    # ══════════════════════════════════════════════════════════════════════════════
    # BIO SECTION
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-label">📝 Bio</div>', unsafe_allow_html=True)

    with st.container():
        if st.session_state.profile_editing:
            new_bio = st.text_area("Edit bio", value=bio, height=120, label_visibility="collapsed",
                                placeholder="Tell people about yourself…")
            c1, c2 = st.columns([1, 5])
            with c1:
                if st.button("💾 Save bio", type="primary"):
                    set_user_profile(username, new_bio, client)
                    st.session_state.profile_editing = False
                    st.rerun()
            with c2:
                if st.button("Cancel", type="secondary"):
                    st.session_state.profile_editing = False
                    st.rerun()
        else:
            st.markdown(
                f'<div class="profile-desc">{bio if bio else "<em>No bio yet — add one!</em>"}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("")
            if st.button("✏️ Edit bio"):
                st.session_state.profile_editing = True
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════════════
    # PREFERENCES SECTION
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-label">⭐ Favourites</div>', unsafe_allow_html=True)

    current_animal = prefs.get("animal", ANIMALS[0])
    current_food   = prefs.get("food", FOODS[0])

    if st.session_state.prefs_editing:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Favourite animal**")
            new_animal = st.selectbox(
                "animal", ANIMALS,
                index=ANIMALS.index(current_animal) if current_animal in ANIMALS else 0,
                label_visibility="collapsed",
            )
        with col2:
            st.markdown("**Favourite food**")
            new_food = st.selectbox(
                "food", FOODS,
                index=FOODS.index(current_food) if current_food in FOODS else 0,
                label_visibility="collapsed",
            )
        st.markdown("")
        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("💾 Save preferences", type="primary"):
                set_user_preferences(username, animal=new_animal, food=new_food, myclient=client)
                st.session_state.prefs_editing = False
                st.rerun()
        with c2:
            if st.button("Cancel ", type="secondary"):   # trailing space to avoid key clash
                st.session_state.prefs_editing = False
                st.rerun()
    else:
        pills = ""
        if current_animal: pills += f'<span class="pref-pill">🐾 {current_animal}</span>'
        if current_food:   pills += f'<span class="pref-pill">🍽️ {current_food}</span>'
        st.markdown(pills or '<span class="pref-pill">Not set yet</span>', unsafe_allow_html=True)
        st.markdown("")
        if st.button("✏️ Edit preferences"):
            st.session_state.prefs_editing = True
            st.rerun()

    if st.button("Delete Account", type="primary"):
        st.session_state.deleting = True
        st.rerun()

    # ══════════════════════════════════════════════════════════════════════════════
    # PUBLISH A POST
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-label">📣 New Post</div>', unsafe_allow_html=True)

    with st.form(key=f"post_form_{st.session_state.post_key}", clear_on_submit=True):
        post_text = st.text_area(
            "", height=100, label_visibility="collapsed",
            placeholder="Write something… (Markdown supported: **bold**, _italic_, `code`, etc.)",
        )
        if st.form_submit_button("Publish ↑", type="primary") and post_text.strip():
            send_post(username, post_text.strip(), client)
            st.session_state.post_key += 1
            st.success("Post published!")
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════════
    # MY POSTS
    # ══════════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-label">🗂️ My Posts</div>', unsafe_allow_html=True)

    if posts:
        for post in posts:
            content = post.get("content", "")
            ts      = post.get("datetime", post.get("created_at", ""))
            st.markdown(
                f'<div class="bubble-meta">{ts}',
                unsafe_allow_html=True,
            )
            st.markdown(content)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:var(--text-dim);font-size:.88rem">No posts yet.</p>', unsafe_allow_html=True)

else:
            st.warning("Are you sure you want to delete your account? This action cannot be undone.")

            c1, c2 = st.columns([1, 1])

            with c1:
                if st.button("Confirm and delete my virtual life", type="primary"):
                    delete_user(st.session_state.my_username, st.session_state.supabase_client)
                    st.session_state.logged_in = False
                    st.session_state.my_username = None
                    st.session_state.profile_editing = False
                    st.success("Account deleted successfully. You have successfully killed yourself.")

            with c2:
                if st.button("No, I want to keep being alive", type="secondary"):
                    st.session_state.deleting = False
                    st.rerun()