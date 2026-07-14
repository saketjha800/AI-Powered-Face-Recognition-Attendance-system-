# ==========================================================
# AI Powered Face Recognition Attendance System
# Developer Information
# pages/6_Developer.py
# ==========================================================

import streamlit as st
from database import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Developer",
    page_icon="👨‍💻",
    layout="wide"
)

initialize_database()

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* 🌌 पूरे मुख्य पेज का बैकग्राउंड */
.stApp, .main {
    background-color: #E0E0E0 !important; 
}

/* 🔵 साइडबार का बैकग्राउंड कलर */
[data-testid="stSidebar"] {
    background-color: #E0F7FA !important; 
}

/* 🎨 मुख्य हेडिंग का कलर */
.main h1, h1 span {
    color: #1A237E !important;
}

/* ⚙️ हेडर बार की सेटिंग्स */
div[data-testid="stHeader"], header {
    background-color: transparent !important; /* हेडर को बैकग्राउंड में मिला दिया */
}

/* 🔘 Deploy बटन को ग्रे कलर करना */
div[data-testid="stActionButton"] button,
button[data-testid="stDeployButton"] {
    background-color: #757575 !important; /* मीडियम ग्रे */
    color: #FFFFFF !important;            /* सफेद टेक्स्ट */
    border: 1px solid #616161 !important;
    border-radius: 6px !important;
}

/* 🔘 3-Dots (Menu Button) को ग्रे करना */
#MainMenu button, 
header button[aria-label="Manage app"],
header button svg {
    color: #757575 !important;            /* ग्रे आइकॉन */
    fill: #757575 !important;
}

/* 🟢 सिस्टम स्टेटस वाले कार्ड्स का स्टाइल */
div[data-testid="element-container"] .stAlert,
div[data-testid="stNotificationBody"] {
    background-color: #E0F2F1 !important; 
    color: #1A237E !important; 
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

.metric-card{
    background:white;
    border-radius:15px;
    padding:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,.08);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.title("👨‍💻 Developer Profile")

st.caption(
    "AI Powered Face Recognition Attendance System"
)

st.divider()

# ==========================================================
# PROFILE
# ==========================================================

col1, col2 = st.columns([1, 3])

with col1:
    st.image(
        "assets/profile.jpeg",
        width=220
    )

with col2:
    st.markdown("## Saket Jha")
    st.write("🎓 B.Tech CSE Student")
    st.write("🏫 Buddha Institute of Technology, Gorakhpur")
    st.write("💻 Full Stack Developer")
    st.write("🤖 AI & Machine Learning Enthusiast")
    st.write("🌐 Python | Streamlit | OpenCV | MySQL | React | Node.js")
    
    # 🔗 पोर्टफोलियो और सोशल मीडिया लिंक्स
    st.write("") # थोड़ा सा स्पेस देने के लिए
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        st.link_button(
            "🌐 My Portfolio", 
            "https://saketjha800.github.io/portfolio/?utm_source=chatgpt.com", # यहाँ अपनी असली लिंक डालें
            use_container_width=True
        )
        
    with btn_col2:
        st.link_button(
            "🐙 GitHub", 
            "https://github.com/saketjha800", # यहाँ अपनी गिटहब लिंक डालें
            use_container_width=True
        )
        
    with btn_col3:
        st.link_button(
            "💼 LinkedIn", 
            "https://www.linkedin.com/in/saket-jha-03b167391/", # यहाँ अपनी लिंक्डइन लिंक डालें
            use_container_width=True
        )

st.divider()

# ==========================================================
# CONTACT
# ==========================================================

st.subheader("📞 Contact Information")

c1,c2 = st.columns(2)

with c1:

    st.info("""
📧 Email

jhasaket30@gmail.com
""")

    st.info("""
📱 Mobile

+91-xxxxxx7307
""")

with c2:

    st.info("""
🌐 GitHub

https://github.com/saketjha800
""")

    st.info("""
💼 LinkedIn

https://www.linkedin.com/in/saket-jha-03b167391/
""")

st.divider()

# ==========================================================
# PROJECT
# ==========================================================

st.subheader("📂 Project Information")

st.markdown("""

### AI Powered Face Recognition Attendance System

This Project is developed using

- Python
- Streamlit
- OpenCV
- SQLite
- Pandas
- Plotly
- Pillow

Features

- Student Management

- Face Dataset Collection

- Face Model Training

- Face Recognition

- Automatic Attendance

- Attendance Reports

- Dashboard Analytics

- CSV & Excel Export

""")

st.divider()

# ==========================================================
# TECHNOLOGY
# ==========================================================

st.subheader("🛠 Technology Stack")

col1,col2,col3=st.columns(3)

with col1:

    st.success("Python")

    st.success("Streamlit")

    st.success("OpenCV")

with col2:

    st.success("SQLite")

    st.success("NumPy")

    st.success("Pandas")

with col3:

    st.success("Plotly")

    st.success("Pillow")

    st.success("GitHub")

st.divider()

# ==========================================================
# PROJECT STATISTICS
# ==========================================================

st.subheader("📊 Project Statistics")

c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(

        "Students",

        total_students()

    )

with c2:

    st.metric(

        "Attendance",

        total_attendance()

    )

with c3:

    st.metric(

        "Dataset",

        dataset_image_count()

    )

with c4:

    latest = latest_model()

    if latest.empty:

        st.metric(

            "Model",

            "Not Trained"

        )

    else:

        st.metric(

            "Model",

            "Ready"

        )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
"""
---
<center>

© 2026 AI Powered Face Recognition Attendance System

Developed by <b>Saket Jha</b>

Version 2.0

</center>
""",
unsafe_allow_html=True
)