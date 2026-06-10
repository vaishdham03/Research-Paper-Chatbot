import streamlit as st
import pandas as pd
import plotly.express as px

if "logged_in" not in st.session_state:
    st.error("Please login first.")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("⛔ Access Denied. Admins only.")
    st.stop()

# Logout Button
if st.sidebar.button(" Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    st.switch_page("app.py")

from src.database import create_users_table, create_chat_table
from src.admin_utils import (
    get_all_users,
    get_all_chats,
    block_user,
    unblock_user,
    delete_user,
)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Admin Dashboard", page_icon="🛠", layout="wide")

create_users_table()
create_chat_table()

st.markdown(
    """
<style>
.main-title {
    font-size:42px;
    font-weight:800;
    text-align:center;
    margin-bottom:10px;
}

.card {
    background:#0f172a;
    padding:16px;
    border-radius:14px;
    color:white;
    box-shadow:0px 4px 20px rgba(0,0,0,0.3);
}

.small {
    opacity:0.7;
    font-size:13px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🛠 Admin Dashboard</div>', unsafe_allow_html=True)

# ---------------- DATA ----------------
users = get_all_users()
chats = get_all_chats()

df_users = pd.DataFrame(users, columns=["id", "username", "role", "blocked"])
df_chats = pd.DataFrame(chats, columns=["username", "question", "answer"])

# ---------------- KPIs ----------------
total_users = len(df_users)
blocked_users = df_users["blocked"].sum()
active_users = total_users - blocked_users
total_chats = len(df_chats)

c1, c2, c3, c4 = st.columns(4)

card_style = """
background: rgba(255,255,255,0.07);
padding:14px;
border-radius:14px;
text-align:center;
backdrop-filter: blur(10px);
border:1px solid rgba(255,255,255,0.08);
box-shadow:0 2px 10px rgba(0,0,0,15);
height:140px;
"""

# ---------------- USERS ----------------
with c1:
    st.markdown(
        f"""
    <div style="{card_style}">
        <div style="font-size:28px;">👥</div>
        <div style="font-size:30px;font-weight:bold;">
            {total_users}
        </div>
        <div style="font-size:14px;opacity:0.8;">
            Total Users
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ---------------- ACTIVE ----------------
with c2:
    st.markdown(
        f"""
    <div style="{card_style}">
        <div style="font-size:28px;">🟢</div>
        <div style="font-size:30px;font-weight:bold;">
            {active_users}
        </div>
        <div style="font-size:14px;opacity:0.8;">
            Active Users
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ---------------- BLOCKED ----------------
with c3:
    st.markdown(
        f"""
    <div style="{card_style}">
        <div style="font-size:28px;">🔴</div>
        <div style="font-size:30px;font-weight:bold;">
            {blocked_users}
        </div>
        <div style="font-size:14px;opacity:0.8;">
            Blocked Users
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ---------------- CHATS ----------------
with c4:
    st.markdown(
        f"""
    <div style="{card_style}">
        <div style="font-size:28px;">💬</div>
        <div style="font-size:30px;font-weight:bold;">
            {total_chats}
        </div>
        <div style="font-size:14px;opacity:0.8;">
            Total Chats
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
st.subheader("📊 Analytics Overview")

col1, col2 = st.columns(2)

# ---------------- PIE CHART CARD ----------------
with col1:

    st.markdown(
        """
    <div style="
        background: rgba(255,255,255,0.07);
        padding:12px;
        border-radius:14px;
        backdrop-filter: blur(10px);
        border:1px solid rgba(255,255,255,0.08);
        box-shadow:0 2px 10px rgba(0,0,0,10);
        margin-bottom:10px;
    ">
    <h4 style="text-align:center;">
        👥 User Status Distribution
    </h4>
    </div>
    """,
        unsafe_allow_html=True,
    )

    fig = px.pie(
        df_users, names=df_users["blocked"].map({0: "Active", 1: "Blocked"}), hole=0.5
    )

    fig.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10))

    st.plotly_chart(fig, use_container_width=True)

# ---------------- BAR CHART CARD ----------------
with col2:

    st.markdown(
        """
    <div style="
        background: rgba(255,255,255,0.07);
        padding:12px;
        border-radius:14px;
        backdrop-filter: blur(10px);
        border:1px solid rgba(255,255,255,0.08);
        box-shadow:0 2px 10px rgba(0,0,0,10);
        margin-bottom:10px;
    ">
    <h4 style="text-align:center;">
        💬 Top Active Users
    </h4>
    </div>
    """,
        unsafe_allow_html=True,
    )

    chat_counts = df_chats["username"].value_counts().reset_index()

    chat_counts.columns = ["username", "messages"]

    fig2 = px.bar(chat_counts, x="username", y="messages")

    fig2.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10))

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- EXPORT ----------------
st.subheader("📤 Export Data")

col1, col2 = st.columns(2)

with col1:

    csv_users = df_users.to_csv(index=False).encode("utf-8")

    st.download_button("⬇️ Download Users CSV", csv_users, "users.csv", "text/csv")

with col2:

    csv_chats = df_chats.to_csv(index=False).encode("utf-8")

    st.download_button("⬇️ Download Chats CSV", csv_chats, "chats.csv", "text/csv")

st.markdown("---")

uploaded_pdf = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)

if uploaded_pdf:

    save_path = os.path.join("data", uploaded_pdf.name)

    with open(save_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())

    st.success("PDF uploaded")

    if st.button("🔄 Index Research Paper"):
        with st.spinner("Creating embeddings..."):
            ingest_documents()

        st.success("Paper indexed successfully")

# ---------------- SEARCH ----------------
st.subheader("🔎 Search Panel")

search_users = st.text_input("Search Users")

filtered_users = df_users.copy()
filtered_chats = df_chats.copy()

if search_users:
    filtered_users = filtered_users[
        filtered_users["username"].str.contains(search_users, case=False)
    ]


# ---------------- USERS ----------------
st.subheader("👤 User Management")

for _, user in filtered_users.iterrows():

    status = "BLOCKED" if user["blocked"] == 1 else "ACTIVE"

    st.markdown(
        f"""
    <div class="card">
        <h4>👤 {user['username']}</h4>
        <p class="small">Role: {user['role']}</p>
        <p class="small">Status: {status}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if user["blocked"] == 0:
            if st.button("🚫 Block", key=f"b_{user['id']}"):
                block_user(user["username"])
                st.rerun()
        else:
            if st.button("✅ Unblock", key=f"u_{user['id']}"):
                unblock_user(user["username"])
                st.rerun()

    with col2:
        if st.button("🗑 Delete", key=f"d_{user['id']}"):
            delete_user(user["username"])
            st.rerun()

    st.markdown("---")

# ---------------- CHAT ANALYTICS ----------------
st.subheader("💬 Chat Analytics")

import pandas as pd

df_chats = pd.DataFrame(chats, columns=["username", "question", "answer"])

if df_chats.empty:
    st.info("No chats found.")
    st.stop()

# ---------------- FILTERS ----------------
col1, col2 = st.columns(2)

with col1:
    users_list = ["All"] + list(df_chats["username"].unique())
    selected_user = st.selectbox("👤 Filter by User", users_list)

with col2:
    min_chats = st.slider("📊 Minimum chats per user", 1, 30, 1)

# ---------------- APPLY FILTERS ----------------
filtered = df_chats.copy()

if selected_user != "All":
    filtered = filtered[filtered["username"] == selected_user]
st.dataframe(filtered)
# ---------------- KPIs ----------------
st.markdown("### 📊 Insights")

user_counts = df_chats["username"].value_counts()

top_user = user_counts.idxmax()
top_count = user_counts.max()

c1, c2, c3 = st.columns(3)

c1.metric("🔥 Most Active User", top_user, f"{top_count} chats")
c2.metric("💬 Total Chats", len(df_chats))
c3.metric("👥 Active Users", df_chats["username"].nunique())

st.markdown("---")

# ---------------- TOP QUESTIONS ----------------
st.subheader("🔥 Top Questions")

top_questions = df_chats["question"].value_counts().head(5)

for q, count in top_questions.items():
    st.markdown(
        f"""
                <br>
    <div class="card">
        ❓ {q}<br>
        <small>Asked {count} times</small>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------------- USER ACTIVITY ----------------
st.subheader("📈 User Activity")

activity_df = user_counts.reset_index()
activity_df.columns = ["username", "chats"]

activity_df = activity_df[activity_df["chats"] >= min_chats]

st.bar_chart(activity_df.set_index("username"))

st.markdown("---")

# ---------------- CHAT FEED ----------------
st.subheader("💬 Chat Feed")

for idx, chat in filtered.tail(20).iloc[::-1].iterrows():

    full_answer = chat["answer"]

    is_long = len(full_answer) > 120

    short_answer = full_answer[:120] if is_long else full_answer

    # ---------------- CARD ----------------
    with st.container():

        st.markdown(
            f"""
        <div style="
            background: rgba(255,255,255,0.08);
            padding: 18px;
            border-radius: 16px;
            backdrop-filter: blur(12px);
            margin-bottom: 12px;
            border:1px solid rgba(255,255,255,0.1);
        ">

        <div style="
            font-size:18px;
            font-weight:600;
            margin-bottom:10px;
        ">
            👤 {chat['username']}
        </div>

        <b>❓ Question:</b><br>
        {chat['question']}<br><br>

        <b>🤖 Answer:</b><br>
        {short_answer}
        </div>
        """,
            unsafe_allow_html=True,
        )

        # ---------------- MORE BUTTON ----------------
        if is_long:

            if st.button("...more", key=f"more_{idx}"):

                st.info(full_answer)
