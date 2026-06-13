import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
from css_utils import css_style_str

from supabase_utils import (
    get_all_users_info,
    get_following,
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Graph",
    layout="wide",
    page_icon=':water_buffalo:'
)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.switch_page("pages/login_or_register.py")

st.markdown(css_style_str(), unsafe_allow_html=True)


st.markdown('<div class="sec-header">🌐 Social Network Graph 🐃</div>', unsafe_allow_html=True)

# =====================================================
# SUPABASE CLIENT
# =====================================================

# Replace this with your own initialization
client = st.session_state["supabase_client"]


# =====================================================
# GRAPH BUILDING
# =====================================================

@st.cache_data(ttl=60)
def build_graph0():
    return build_graph()


def build_graph():

    G = nx.DiGraph()

    users = get_all_users_info(client).data

    if users is None:
        return G

    # Add nodes
    descriptions_dict = {}

    for user in users:

        username = (
            user.get("username")
            or user.get("userid")
            or user.get("name")
        )


        if username:
            descriptions_dict[username] = {}
            descriptions_dict[username]["description"] = user.get("description", "")
            descriptions_dict[username]["food"] = user.get("food", "")
            descriptions_dict[username]["animal"] = user.get("animal", "")
            G.add_node(username)

    # Add edges
    for user in users:

        username = (
            user.get("username")
            or user.get("userid")
            or user.get("name")
        )

        if not username:
            continue

        try:
            following = get_following(
                username,
                client
            ).data

            if following is None:
                continue

            for target_user in following:

                target = (
                    target_user.get("username")
                    or target_user.get("userid")
                    or target_user.get("name")
                )

                if target:
                    G.add_edge(
                        username,
                        target
                    )

        except Exception as e:
            print(e)

    return G, descriptions_dict


# =====================================================
# SUBGRAPH EXTRACTION
# =====================================================

def get_neighborhood(
    G,
    center_user,
    depth
):
    nodes = {center_user}
    frontier = {center_user}

    for _ in range(depth):

        new_frontier = set()

        for node in frontier:

            new_frontier.update(
                G.successors(node)
            )

            new_frontier.update(
                G.predecessors(node)
            )

        nodes.update(new_frontier)
        frontier = new_frontier

    return G.subgraph(nodes).copy()


# =====================================================
# GRAPH VISUALIZATION
# =====================================================

def render_graph(G, descriptions_dict):

    net = Network(
        height="850px",
        width="100%",
        directed=True,
        bgcolor="#111111",
        font_color="white"
    )


    for node in G.nodes():

        degree = G.degree(node)

        size = 15 + degree * 3

        if descriptions_dict[node]['description']:
            d1 = f'\ndescription: {descriptions_dict[node].get("description", "")}'
        else:
            d1 = ""


        if descriptions_dict[node]['food']:
            d2 = f'\nfood: {descriptions_dict[node]["food"][0]}'
        else:
            d2 = ""

        if descriptions_dict[node]['animal']:
            d3 = f'\nanimal: {descriptions_dict[node]["animal"][0]}'
        else:
            d3 = ""

        net.add_node(
            node,
            label=node,
            title=f"""{node}
Degree: {degree}{d1}{d3}{d2}
""",
            size=size
        )

    for source, target in G.edges():
        net.add_edge(
            source,
            target
        )

    net.force_atlas_2based(
        gravity=-50,
        central_gravity=0.01,
        spring_length=120,
        spring_strength=0.08
    )

    net.show_buttons(filter_=["physics"])

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".html"
    ) as tmp:

        net.save_graph(tmp.name)

        html = open(
            tmp.name,
            "r",
            encoding="utf8"
        ).read()

    st.iframe(
        html,
        height=900,
        #scrolling=True
    )


# =====================================================
# LOAD GRAPH
# =====================================================

with st.spinner("Loading graph..."):
    G, descriptions_dict = build_graph0()

if st.sidebar.button("Refresh graph"):
    with st.spinner("Loading graph..."):
        G, descriptions_dict = build_graph()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

all_users = sorted(G.nodes())

selected_user = st.sidebar.selectbox(
    "Focus on user",
    [""] + all_users,
    index=all_users.index(st.session_state.my_username)+1
)

depth = st.sidebar.slider(
    "Neighborhood depth",
    min_value=1,
    max_value=5,
    value=2
)

hide_isolated = st.sidebar.checkbox(
    "Hide isolated nodes",
    value=True
)

# =====================================================
# APPLY FILTERS
# =====================================================

filtered_graph = G.copy()

if selected_user:
    filtered_graph = get_neighborhood(
        filtered_graph,
        selected_user,
        depth
    )

if hide_isolated:

    isolated_nodes = list(
        nx.isolates(filtered_graph)
    )

    filtered_graph.remove_nodes_from(
        isolated_nodes
    )

# =====================================================
# METRICS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Users",
    filtered_graph.number_of_nodes()
)

col2.metric(
    "Connections",
    filtered_graph.number_of_edges()
)

avg_degree = (
    sum(
        dict(
            filtered_graph.degree()
        ).values()
    )
    / max(
        filtered_graph.number_of_nodes(),
        1
    )
)

col3.metric(
    "Average Degree",
    f"{avg_degree:.2f}"
)

density = (
    nx.density(filtered_graph)
    if filtered_graph.number_of_nodes() > 1
    else 0
)

col4.metric(
    "Density",
    f"{density:.4f}"
)

# =====================================================
# GRAPH
# =====================================================

render_graph(filtered_graph, descriptions_dict)