


# ==========================================================
# AI Powered Face Recognition Attendance System
# Professional Dashboard
# ==========================================================

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

from database import *
from utils import *

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="AI Powered Face Recognition Attendance System",
    layout="wide",
    initial_sidebar_state="collapsed" # 👈 यह साइडबार को ऑटोमैटिक बंद रखेगा जिससे पेज फुल खुलेगा
)
st.markdown("""
<style>

/* 🌌 पूरे मुख्य पेज का बैकग्राउंड और लेआउट */
.stApp {
    background-color: #E0E0E0 !important; 
}

.stMain, .main, [data-testid="stMain"] {
    pointer-events: auto !important;
    display: block !important;
}

/* 🔵 साइडबार का बैकग्राउंड */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important; 
}

/* 🎨 मुख्य हेडिंग का कलर */
.main h1, h1 span {
    color: #1A237E !important; 
}

/* ==========================================================
   🚨 फिक्स्ड टॉप बार और बटन्स (3-DOTS REMOVED)
   ========================================================== */

/* ⚙️ सफेद हेडर बार */
div[data-testid="stHeader"], header {
    background-color: #E3F2FD !important; 
    height: 3.8rem !important; 
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    pointer-events: none !important; 
    z-index: 99999 !important; 
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1) !important; 
}

/* 📄 हॉरिजॉन्टल नेविगेशन बटन्स - अब इन्हें थोड़ा और दाईं तरफ (right: 120px) खिसका दिया है क्योंकि 3-dots हट गया है */
div[data-testid="stSidebarNav"] {
    position: fixed !important; 
    top: 14px !important;       
    right: 125px !important;    /* 👈 Deploy बटन के ठीक बाईं तरफ परफेक्ट स्पेसिंग */
    left: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    width: auto !important;
    z-index: 100000 !important;
    pointer-events: auto !important; 
}

/* पेजों की लिस्ट को एक लाइन में करना */
div[data-testid="stSidebarNav"] ul {
    display: flex !important;
    flex-direction: row !important; 
    gap: 8px !important; 
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* बटन्स का सुंदर लेआउट */
div[data-testid="stSidebarNav"] ul li {
    padding: 5px 12px !important;
    background-color: #F1F3F4 !important; 
    border: 1px solid #DADCE0 !important;
    border-radius: 4px !important;
    white-space: nowrap !important; 
}

div[data-testid="stSidebarNav"] ul li a span {
    color: #202124 !important; 
    font-weight: 500 !important;
}

/* 🔘 Deploy बटन की सेटिंग्स - इसे अब कोने के पास (right: 20px) सेट किया है */
div[data-testid="stAppDeployButton"], 
div[data-testid="stActionButton"],
.stAppDeployButton {
    position: fixed !important;
    top: 14px !important;
    right: 20px !important; /* 👈 बिल्कुल कोने में फिक्स */
    left: auto !important;
    z-index: 100000 !important;
    pointer-events: auto !important;
}

div[data-testid="stAppDeployButton"] button,
.stAppDeployButton button {
    background-color: #1A237E !important; 
    color: #E3F2FD !important;            
    border: none !important;
    border-radius: 4px !important;
    font-weight: bold !important;
    height: 32px !important;
}

/* 🔘 3-Dots (Menu Button) को पूरी तरह छुपाया */
div[data-testid="stToolbar"] {
    display: none !important; /* 👈 3-dots अब नहीं दिखेगा */
}

/* 📦 मुख्य कंटेंट का स्पेसिंग */
.block-container {
    padding-top: 5rem !important; 
    padding-bottom: 1rem !important;
    pointer-events: auto !important; 
}

</style>
""", unsafe_allow_html=True)



# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image("assets/logo.png", width=150)

    st.title("AI Attendance")

    st.markdown("---")

    st.success("System Ready")

    st.markdown("### Modules")

    st.page_link("streamlit_app.py", label="🏠 Dashboard")
    st.page_link("pages/Student_Details.py", label="👨‍🎓 Students")
    st.page_link("pages/Face_Dataset.py", label="📷 Dataset")
    st.page_link("pages/Train_Model.py", label="🧠 Train Model")
    st.page_link("pages/Face_Recognition.py", label="🎥 Recognition")
    st.page_link("pages/Attendance_Report.py", label="📋 Reports")
    st.page_link("pages/Developer.py", label="👨‍💻 Developer")

# ==========================================================
# HEADER
# ==========================================================

st.title("🎓 AI Powered Face Recognition Attendance System")

st.caption(
    "Professional Attendance Management Dashboard"
)

st.divider()

# ==========================================================
# KPI CARDS
# ==========================================================

students = total_students()

attendance = total_attendance()

today = today_attendance_count()

dataset = dataset_image_count()

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(
        "👨‍🎓 Students",
        students
    )

with col2:

    st.metric(
        "✅ Attendance",
        attendance
    )

with col3:

    st.metric(
        "📅 Today",
        today
    )

with col4:

    st.metric(
        "📷 Dataset",
        dataset
    )

st.divider()

# ==========================================================
# SYSTEM STATUS
# ==========================================================

status = system_status()

st.subheader("⚡ System Status")

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.success("Camera") if status["Camera"] else st.error("Camera")

with c2:
    st.success("Cascade") if status["Cascade"] else st.error("Cascade")

with c3:
    st.success("Model") if status["Model"] else st.error("Model")

with c4:
    st.success("Dataset") if status["Dataset"] else st.error("Dataset")

with c5:
    st.success("Database")

    # ==========================================================
# RECENT ATTENDANCE
# ==========================================================

st.divider()

st.subheader("📋 Today's Attendance")

today_df = today_attendance()

if today_df.empty:

    st.info("No Attendance Today")

else:

    st.dataframe(

        today_df,

        use_container_width=True,

        hide_index=True,

        height=350

    )
    # ==========================================================
# DEPARTMENT CHART
# ==========================================================

dept = department_statistics()

if not dept.empty:

    fig = px.pie(

        dept,

        names="department",

        values="Total",

        title="Department Wise Students"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ==========================================================
# ATTENDANCE ANALYTICS
# ==========================================================

st.divider()

st.subheader("📈 Attendance Analytics")

attendance_data = attendance_statistics()

if not attendance_data.empty:

    fig = px.line(

        attendance_data,

        x="date",

        y="Total",

        markers=True,

        title="Daily Attendance Trend"

    )

    fig.update_layout(

        height=450,

        xaxis_title="Date",

        yaxis_title="Attendance"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

else:

    st.info("No attendance analytics available.")

    # ==========================================================
# MONTHLY ANALYTICS
# ==========================================================

st.divider()

st.subheader("📅 Monthly Analytics")

attendance_df = get_attendance()

if not attendance_df.empty:

    monthly = attendance_df.groupby("department").size().reset_index(name="Students")

    fig = px.bar(

        monthly,

        x="department",

        y="Students",

        text="Students",

        title="Department Attendance"

    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(

        fig,

        use_container_width=True

    )
    # ==========================================================
# DATASET PROGRESS
# ==========================================================

st.divider()

st.subheader("📷 Dataset Progress")

students = total_students()

images = dataset_image_count()

if students == 0:

    percent = 0

else:

    percent = min(

        round(images/(students*100)*100),

        100

    )

st.progress(percent/100)

st.write(f"Dataset Completion : **{percent}%**")
# ==========================================================
# MODEL INFORMATION
# ==========================================================

st.divider()

st.subheader("🤖 Trained Model")

model = latest_model()

if model.empty:

    st.warning("No Model Available")

else:

    st.dataframe(

        model,

        use_container_width=True,

        hide_index=True

    )
    # ==========================================================
# DATE & TIME
# ==========================================================

st.divider()

col1,col2 = st.columns(2)

with col1:

    st.info(

        f"📅 Date : {datetime.now().strftime('%d-%m-%Y')}"

    )

with col2:

    st.info(

        f"🕒 Time : {datetime.now().strftime('%H:%M:%S')}"

    )
    # ==========================================================
# TOP DEPARTMENT
# ==========================================================

st.divider()

dept = department_statistics()

if not dept.empty:

    top = dept.sort_values(

        "Total",

        ascending=False

    ).iloc[0]

    st.success(

        f"🏆 Top Department : {top['department']} ({top['Total']} Students)"

    )
    # ==========================================================
# RECENT LOGS
# ==========================================================

st.divider()

st.subheader("📝 Recent Activity")

try:

    with get_connection() as conn:

        logs = pd.read_sql_query(

            """

            SELECT *

            FROM system_logs

            ORDER BY id DESC

            LIMIT 10

            """,

            conn

        )

    if logs.empty:

        st.info("No Logs Available")

    else:

        st.dataframe(

            logs,

            use_container_width=True,

            hide_index=True

        )

except:

    st.warning("System Logs Table Not Found")
    # ==========================================================
# AUTO REFRESH
# ==========================================================

st.divider()

if st.button(

    "🔄 Refresh Dashboard",

    use_container_width=True

):

    st.rerun()
    # ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(

"""

<center>

<h4>AI Powered Face Recognition Attendance System</h4>

Version 2.0

Developed by <b>Saket Jha</b>

</center>

""",

unsafe_allow_html=True

)