import streamlit as st
import os
import base64
from src.database import create_users_table, create_chat_table
from streamlit_pdf_viewer import pdf_viewer
from src.auth import register_user, login_user
from src.rag_pipeline import generate_answer
from src.memory import add_message

# ==========================================================
# DATABASE
# ==========================================================

create_users_table()
create_chat_table()


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Research Insights Chatbot", page_icon="🧠", layout="wide"
)

# ==========================================================
# RESPONSIVE BACKGROUND IMAGE
# ==========================================================

def set_background():

    with open("assets/background.jpg", "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        /* Full Background */
        .stApp {{
            background:
                linear-gradient(
                    rgba(0,0,0,0.80),
                    rgba(0,0,0,0.80)
                ),
                url("data:image/jpg;base64,{encoded}");

            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        

        /* Titles */
        .main-title {{
            color: white !important;
            font-weight: 800 !important;
        }}

        .sub-title {{
            color: white !important;
        }}
 
        label, p, h1,h2, h3, h4, h5, h6 {{
            color: white !important;
        }}
        
        /* Chat Area */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        /* Mobile Responsive */
        @media (max-width:768px) {{

            .main-title {{
                font-size: 30px !important;
            }}

            .sub-title {{
                font-size: 15px !important;
            }}

            .auth-card {{
                padding: 20px !important;
                border-radius: 15px !important;
            }}

            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .stApp {{
                background-position: center;
                background-size: cover;
            }}
        }}
     
         /* =========================
         GLASS SIDEBAR
         ========================= */

         section[data-testid="stSidebar"] {{
            background: rgba(0, 0, 0, 0.25) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);

             border-right: 1px solid rgba(255,255,255,0.15);
        }}

        /* Sidebar text */
        section[data-testid="stSidebar"] *{{
            color: white !important;
        }}

        /* Sidebar buttons */
        section[data-testid="stSidebar"] .stButton button {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            color: white !important;
            border-radius: 12px;
        }}

        
        div[data-testid="stDownloadButton"] button {{
           background: rgba(59,130,246,0.20) !important;
           backdrop-filter: blur(20px) !important;
           border: 1px solid rgba(255,255,255,0.25) !important;
           color: white !important;
        }}
        
     
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# ==========================================================
# SESSION STATE
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


# ==========================================================
# LOGIN / REGISTER PAGE
# ==========================================================

if not st.session_state.logged_in:

    st.markdown(
        """
    <style>

    .main {
        padding-top: 2rem;
    }

    /* Hide Sidebar */
    section[data-testid="stSidebar"]{
        display:none;
    }

    /* Main Title */
    .main-title{
        text-align:center;
        font-size:42px;
        font-weight:700;
        margin-top:20px;
        margin-bottom:10px;
    }

    .sub-title{
        text-align:center;
        opacity:0.8;
        margin-bottom:40px;
        font-size:18px;
    }

    /* Login Box */


    /* Inputs */
    .stTextInput input{
        border-radius: 12px !important;
        height: 48px !important;
    }

    /* Buttons */
    .stButton button{
        width:100%;
        border-radius:12px;
        height:48px;
        font-size:16px;
        font-weight:600;
    }

    /* Radio buttons */
    div[role="radiogroup"]{
        justify-content:center;
        gap:10px;
        margin-bottom:20px;
    }

    /* Mobile Responsive */
    @media (max-width:768px){

        .main-title{
            font-size:32px;
        }

    }

    </style>
    """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # TITLE
    # ======================================================

    st.markdown(
        """
    <div class="main-title">
        🧠 Research Chatbot
    </div>

    <div class="sub-title">
        AI Powered Research Assistant
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # CENTER LOGIN BOX
    # ======================================================

    left, center, right = st.columns([1, 1.2, 1])

    with center:

        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        auth_mode = st.radio("", ["Login", "Register"], horizontal=True)

        # ==================================================
        # LOGIN
        # ==================================================

        if auth_mode == "Login":

            username = st.text_input("Username", key="login_username")

            password = st.text_input("Password", type="password", key="login_password")

            if st.button("🔐 Login"):

                if username.strip() == "" or password.strip() == "":

                    st.warning("Please enter username and password")

                else:

                    result = login_user(username, password)

                    if result == "admin":

                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = "admin"
                        st.success("Admin Login Success")
                        print("Admin Login Success")
                        st.rerun()

                    elif result == "user":

                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = "user"

                        st.rerun()

                    elif result == "blocked":

                        st.error("🚫 Your account has been blocked by admin.")

                    else:

                        st.error("Invalid username or password")

        # ==================================================
        # REGISTER
        # ==================================================

        else:

            username = st.text_input("Create Username", key="register_username")

            password = st.text_input(
                "Create Password", type="password", key="register_password"
            )

            if st.button("📝 Register"):

                if username.strip() == "" or password.strip() == "":

                    st.warning("Please fill all fields")

                elif len(password) < 4:

                    st.warning("Password must be at least 4 characters")

                else:

                    success = register_user(username, password)

                    if success:

                        st.success("Registration Successful")

                        st.info("Now login using your credentials")

                    else:

                        st.error("Username already exists")

        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# CHATBOT PAGE
# ==========================================================

else:

    # ======================================================
    # SIDEBAR PROFILE
    # ======================================================

    username = st.session_state.username or "User"
    initial = username[0].upper() if username else "U"

    # Avatar circle using columns (Streamlit native)
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])

    with col2:
        st.markdown(
            f"""
            <div style="
               width:120px;
               height:120px;
               border-radius:50%;
               background: rgba(255,255,255,0.15);
               backdrop-filter: blur(20px);
               display:flex;
               align-items:center;
               justify-content:center;
               margin:auto;
               font-size:36px;
               font-weight:bold;
               color:white;
               border:1px solid rgba(255,255,255,0.2);
            ">
               {initial}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.sidebar.markdown(
        f"""
    <div style="
        text-align:center;
        width: 250px;
        margin-top:15px;
        margin-bottom:200px;
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(15px);
        padding: 10px;
        border-radius:15px;
        border:1px solid rgba(255,255,255,0.15);
    ">
        <b style="color:white;">{username}</b>
        <br>
        <span style="color:white;">Role: {st.session_state.role}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # ADMIN INFO
    # ======================================================

    if st.session_state.role == "admin":
        st.sidebar.success("Admin Login Successful")

        st.switch_page("pages/admin_panel.py")

    # ======================================================
    # LOGOUT
    # ======================================================

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()

    # ======================================================
    # TITLE
    # ======================================================

    st.title("🧠 Research Insights Chatbot")

    # ======================================================
    # QUESTION INPUT
    # ======================================================

    question = st.text_input("Ask a research question")

    # ======================================================
    # GENERATE ANSWER
    # ======================================================

    if question:

        with st.spinner("Searching research papers..."):

            answer, sources = generate_answer(st.session_state.username, question)

            add_message(st.session_state.username, question, answer)

            st.subheader("Answer")

            st.write(answer)

            st.subheader("📄 Sources")

            shown = set()

            if len(sources) > 0:

                for s in sources:

                    paper = s.get("paper", "Unknown Paper")

                    page = s.get("page", "N/A")

                    pdf = s.get("pdf", "")

                    if paper not in shown:

                        shown.add(paper)

                        paper_name = paper.replace("_", " ").replace(".pdf", "")

                        st.markdown(f"📄 **{paper_name}** | Page: {page}")

                        st.write("PDF:",pdf)
                        #st.write("Exists:", os.path.exists(pdf))

                        if os.path.exists(pdf):
                            
                            col1, col2 = st.columns([1, 1])
                            
                            with col1: 
                                 with open(pdf, "rb") as f:
                                    st.download_button(
                                        label="📥 Download PDF",
                                        data=f,
                                        file_name=paper,
                                        mime="application/pdf",
                                        key=f"download_{paper}"
                                    )
                                
                                #View pdf inside app
                            with col2:
                                if st.button(
                                   "View Paper",
                                   key=f"view_{paper}" 
                                ):
                                    pdf_viewer(
                                       pdf,
                                       width="100%",
                                       height=1000
                                    )

                        st.markdown("---")

            else:

                st.warning("No research papers found.")


from src.database import create_connection

conn = create_connection()
cursor = conn.cursor()

cursor.execute("""
UPDATE users
SET role='admin'
WHERE username='admin'
""")

conn.commit()
conn.close()

print("Admin updated")


st.write(os.path.exists("pages/admin_panel.py"))
