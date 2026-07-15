# ==========================================================
# AI Powered Face Recognition Attendance System
# Developer Information
# pages/Developer.py
# ==========================================================

import streamlit as st  
import os
from PIL import Image
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
# CUSTOM CSS (FORCED NAVBAR FOR DEPLOYED LINK)
# ==========================================================
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
# PAGE TITLE
# ==========================================================
st.title("👨‍💻 Developer Information")
st.caption("About the Developer, Technology Stack & Dataset Gallery")
st.divider()

# ==========================================================
# 👤 DEVELOPER PROFILE & LINKS (SAFE MODE)
# ==========================================================
st.subheader("👤 Developer Profile & Links")

c1, c2 = st.columns([1, 2])

with c1:
    image_path = "profile.jpeg" 
    
    # 🛡️ अगर फ़ाइल मौजूद होगी तभी लोड करेगा, वरना प्लेसहोल्डर दिखाएगा (क्रैश नहीं होगा)
    if os.path.exists(image_path):
        st.image(image_path, caption="Saket Jha (Lead Developer)", use_container_width=True)
    else:
        st.image("assets/profile.jpeg", 
                 caption="Saket Jha (Photo not found - Showing Placeholder)", use_container_width=True)

with c2:
    st.markdown("""
    ### **Saket Jha**
    **AI & FULL STACK (MERN DEVELOPER)**
    
    I build smart, scalable AI solutions. You can connect with me, view my portfolio, or explore my open-source projects using the quick links below:
    """)
    
    st.markdown("""
    <div style="display: flex; flex-direction: column; gap: 10px; max-width: 350px;">
        <a href="https://github.com/saketjha800" target="_blank" style="text-decoration: none;">
            <div style="background-color: #24292e; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 10px;">
                🐙 View GitHub Portfolio
            </div>
        </a>
        <a href="https://www.linkedin.com/in/saket-jha-03b167391/" target="_blank" style="text-decoration: none;">
            <div style="background-color: #0077b5; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 10px;">
                💼 Connect on LinkedIn
            </div>
        </a>
        <a href="https://saketjha800.github.io/portfolio/?utm_source=chatgpt.com" style="text-decoration: none;">
            <div style="background-color: #d44638; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 10px;">
                📧 Send Email in (Portfolio)
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================================
# PROJECT INFO
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
# TECHNOLOGY STACK
# ==========================================================
st.subheader("🛠 Technology Stack")

col1, col2, col3 = st.columns(3)

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

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Students", total_students())

with c2:
    st.metric("Attendance", total_attendance())

with c3:
    st.metric("Dataset", dataset_image_count())

with c4:
    latest = latest_model()
    if latest.empty:
        st.metric("Model", "Not Trained")
    else:
        st.metric("Model", "Ready")

# ==========================================================
# 📸 IMAGE DATASET GALLERY SECTION
# ==========================================================
st.divider()
st.subheader("📸 Captured Student Dataset (Recent Faces)")

dataset_path = "dataset" 

if os.path.exists(dataset_path):
    all_images = [f for f in os.listdir(dataset_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if len(all_images) == 0:
        st.info("No images found in the dataset folder yet.")
    else:
        recent_images = all_images[-8:] 
        st.write(f"Showing last {len(recent_images)} captured faces in dataset:")
        
        cols = st.columns(4)
        for idx, img_name in enumerate(recent_images):
            img_path = os.path.join(dataset_path, img_name)
            try:
                img = Image.open(img_path)
                col_idx = idx % 4
                with cols[col_idx]:
                    st.image(img, caption=img_name, use_container_width=True)
            except Exception as e:
                pass
else:
    st.warning("Dataset folder not found. Please register students first to generate images.")

# ==========================================================
# FOOTER
# ==========================================================
st.markdown(
"""
<center>
<hr>
© 2026 AI Powered Face Recognition Attendance System

Developed by <b>Saket Jha</b>

Version 2.0
</center>
""",
unsafe_allow_html=True
)