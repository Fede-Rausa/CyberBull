import streamlit as st
from supabase_utils import get_all_posts
from css_utils import css_style_str

st.set_page_config(page_title="Posts", page_icon=':water_buffalo:', layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login_or_register.py")

client   = st.session_state.supabase_client
username = st.session_state.get("my_username", "")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(css_style_str(), unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-header">📰 Posts Feed 🐃</div>', unsafe_allow_html=True)

# ── Filter bar ────────────────────────────────────────────────────────────────
col_search, col_filter = st.columns([3, 2])
with col_search:
    search_query = st.text_input("", placeholder="🔍  Search posts…", label_visibility="collapsed")
with col_filter:
    filter_mine = st.checkbox("Only my posts", value=False)

# ── Load posts ────────────────────────────────────────────────────────────────
with st.spinner("Loading posts…"):
    posts = get_all_posts(client).data or []

# Sort newest first — assumes datetime field is ISO-sortable
posts = sorted(posts, key=lambda p: p.get("datetime", p.get("created_at", "")), reverse=True)

# Apply filters
if filter_mine:
    posts = [p for p in posts if p.get("sender", p.get("username", "")) == username]
if search_query:
    q = search_query.lower()
    posts = [p for p in posts if
             q in p.get("message", "").lower() or
             q in p.get("sender", p.get("username", "")).lower()]

# ── Render ────────────────────────────────────────────────────────────────────
if not posts:
    st.markdown('<div class="empty-state">No posts found.</div>', unsafe_allow_html=True)
else:
    for post in posts:
        author  = post.get("sender", post.get("username", "unknown"))
        content = post.get("message", "")
        ts      = post.get("datetime", post.get("created_at", ""))
        initial = author[0].upper() if author else "?"
        is_mine = author == username

        # Card header via HTML
        mine_tag = ' style="border-color:#4c3fb5"' if is_mine else ""
        st.markdown(
            f'  <div class="bubble-meta"{mine_tag}>'
            f'    <span class="author-avatar">{initial}</span>'
            f'    <span class="post-author">{author}</span>'
            f'    &nbsp;·&nbsp;{ts}'
            f'  <hr class="post-divider">',
            unsafe_allow_html=True,
        )
        # Markdown content rendered natively by Streamlit
        st.markdown(content)
        st.markdown("</div>", unsafe_allow_html=True)