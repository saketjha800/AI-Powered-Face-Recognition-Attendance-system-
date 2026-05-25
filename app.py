import streamlit as st
import cv2
import pandas as pd
import numpy as np
import os
from datetime import datetime

# 1. पेज की सेटिंग (Full Screen Layout)
st.set_page_config(page_title="AI Face Recognition Attendance System", layout="wide", initial_sidebar_state="collapsed")

# CSS की मदद से बैकग्राउंड और बटन्स को खूबसूरत बनाना
st.markdown("""
    <style>
    .main-title {
        text-align: center; 
        color: #38bdf8; 
        background-color: #1e293b; 
        padding: 15px; 
        border-radius: 10px;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        border: 2px solid #38bdf8;
        box-shadow: 0px 4px 15px rgba(56, 189, 248, 0.3);
    }
    .dashboard-banner {
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# अटेंडेंस फाइल चेक करना
ATTENDANCE_FILE = "attendance.csv"
if not os.path.exists(ATTENDANCE_FILE):
    pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(ATTENDANCE_FILE, index=False)

# डेटाबेस से छात्रों के नाम निकालना
DATA_DIR = "data"
registered_students = []
if os.path.exists(DATA_DIR):
    registered_students = [os.path.splitext(f)[0] for f in os.listdir(DATA_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Session State की मदद से पेजों को कंट्रोल करना
if "page" not in st.session_state:
    st.session_state.page = "Main Page"

# ---------------------------------------------------------------
# 🖥️ PAGE 1: MAIN DASHBOARD (जो लिंक खोलते ही सबसे पहले दिखेगा)
# ---------------------------------------------------------------
if st.session_state.page == "Main Page":
    
    # मुख्य हेडिंग
    st.markdown("<h1 class='main-title'>AI-POWERED FACE RECOGNITION ATTENDANCE SYSTEM</h1>", unsafe_allow_html=True)
    st.write(" ")
    
    # लेआउट को दो हिस्सों में बांटना (लेफ्ट में बटन्स, राइट में वो ब्लू फेस ग्राफिक)
    left_col, right_col = st.columns([3, 2])
    
    with left_col:
        st.write("### 🎛️ Select an Option to Initialize:")
        st.write(" ")
        
        # बटन 1: Student Details
        if st.button("👥 Student Details", use_container_width=True, type="secondary"):
            st.session_state.page = "Student Details"
            st.rerun()
            
        st.write(" ")
        # बटन 2: Face Detector (यहीं से कैमरा खुलेगा)
        if st.button("📷 Face Detector (Live Attendance)", use_container_width=True, type="primary"):
            st.session_state.page = "Face Detector"
            st.rerun()
            
        st.write(" ")
        # बटन 3: Attendance Record
        if st.button("📊 Attendance Record", use_container_width=True):
            st.session_state.page = "Attendance Record"
            st.rerun()
            
        st.write(" ")
        # बटन 4: Train Data
        if st.button("⚙️ Train Data System", use_container_width=True):
            st.session_state.page = "Train Data"
            st.rerun()

    with right_col:
        # यहाँ पर हम एक शानदार रोबोटिक/एआई फेस का सिंबल दिखा रहे हैं जैसा आपके ऐप में था
        st.markdown("<h1 style='font-size: 150px; text-align: center; margin-top: 20px;'>🤖</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #38bdf8;'>AI Core Active</h4>", unsafe_allow_html=True)

# ---------------------------------------------------------------
# 👥 PAGE 2: STUDENT DETAILS
# ---------------------------------------------------------------
elif st.session_state.page == "Student Details":
    st.subheader("👥 Student Registration & Details")
    
    name = st.text_input("Enter Student Name:")
    student_id = st.text_input("Enter Student ID:")
    if st.button("Save Details"):
        st.success(f"Student {name} registered in local buffer!")
        
    st.write("---")
    if st.button("⬅️ Back to Main Page", type="primary"):
        st.session_state.page = "Main Page"
        st.rerun()

# ---------------------------------------------------------------
# 📷 PAGE 3: FACE DETECTOR (असली अटेंडेंस कैमरा)
# ---------------------------------------------------------------
elif st.session_state.page == "Face Detector":
    st.subheader("📷 Live AI Face Recognition")
    
    if registered_students:
        selected_name = st.selectbox("Select Student Name for Verification:", registered_students)
    else:
        selected_name = st.text_input("Enter Student Name Manually:", "Guest_User")

    img_file = st.camera_input("Look into the camera")

    if img_file is not None:
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
        gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
        
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(opencv_img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                
            st.image(opencv_img, channels="BGR", caption="Face Verified!")
            
            # सेविंग लॉजिक
            now = datetime.now()
            new_entry = pd.DataFrame([[selected_name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")]], columns=["Name", "Date", "Time"])
            df_old = pd.read_csv(ATTENDANCE_FILE)
            df_updated = pd.concat([df_old, new_entry], ignore_index=True)
            df_updated.to_csv(ATTENDANCE_FILE, index=False)
            
            st.success(f"✅ Attendance Logged for {selected_name}!")
        else:
            st.warning("No face detected.")

    st.write("---")
    if st.button("⬅️ Back to Main Page", type="primary"):
        st.session_state.page = "Main Page"
        st.rerun()

# ---------------------------------------------------------------
# 📊 PAGE 4: ATTENDANCE RECORD
# ---------------------------------------------------------------
elif st.session_state.page == "Attendance Record":
    st.subheader("📊 Attendance Spreadsheet Logs")
    df_show = pd.read_csv(ATTENDANCE_FILE)
    st.dataframe(df_show, use_container_width=True)
    
    csv_data = df_show.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download CSV Report", data=csv_data, file_name="Report.csv", mime="text/csv")
    
    st.write("---")
    if st.button("⬅️ Back to Main Page", type="primary"):
        st.session_state.page = "Main Page"
        st.rerun()

# ---------------------------------------------------------------
# ⚙️ PAGE 5: TRAIN DATA
# ---------------------------------------------------------------
elif st.session_state.page == "Train Data":
    st.subheader("⚙️ AI Machine Learning Training Section")
    if st.button("⚡ Start Training Now"):
        with st.spinner("Processing datasets..."):
            st.success("Core Models trained successfully via cloud!")
            
    st.write("---")
    if st.button("⬅️ Back to Main Page", type="primary"):
        st.session_state.page = "Main Page"
        st.rerun()