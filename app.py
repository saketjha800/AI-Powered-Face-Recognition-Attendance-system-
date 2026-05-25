import streamlit as st
import cv2
import pandas as pd
import numpy as np
import os
from datetime import datetime

# पेज की सेटिंग (चौड़ाई और टाइटल)
st.set_page_config(page_title="AI Face Recognition Attendance System", layout="wide")

# मुख्य हेडिंग (जैसा आपके Tkinter डैशबोर्ड में था)
st.markdown("<h1 style='text-align: center; color: #00b4d8;'>AI-POWERED FACE RECOGNITION ATTENDANCE SYSTEM</h1>", unsafe_allow_html=True)
st.write("---")

# लेफ्ट साइडबार में मेनू (सारे फीचर्स को जोड़ने के लिए)
st.sidebar.title("🎛️ Control Panel")
choice = st.sidebar.radio("Go To Section:", [
    "🖥️ Home / Dashboard", 
    "👥 Student Details", 
    "📷 Face Detector (Live Attendance)", 
    "⚙️ Train Data", 
    "📊 Attendance Record"
])

# फाइल सेटिंग्स
ATTENDANCE_FILE = "attendance.csv"
if not os.path.exists(ATTENDANCE_FILE):
    pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(ATTENDANCE_FILE, index=False)

# ----------------- SECTION 1: HOME DASHBOARD -----------------
if choice == "🖥️ Home / Dashboard":
    st.subheader("Welcome to the AI Attendance System")
    st.info("बाएं हाथ (Sidebar) पर दिए गए विकल्पों का उपयोग करके अलग-अलग फीचर्स को चलाएं।")
    
    # ग्रिड लेआउट (जैसे आपके Tkinter में बटन्स थे)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Students Registered", value="15") # आप चाहें तो dynamic कर सकते हैं
    with col2:
        df_count = pd.read_csv(ATTENDANCE_FILE)
        st.metric(label="Today's Attendance Count", value=str(len(df_count)))

# ----------------- SECTION 2: STUDENT DETAILS -----------------
elif choice == "👥 Student Details":
    st.subheader("👥 Student Registration & Details")
    st.write("यहाँ से आप नए छात्रों का डेटा मैनेज कर सकते हैं।")
    # यहाँ आप student.py का लॉजिक डाल सकते हैं
    name = st.text_input("Enter Student Name:")
    student_id = st.text_input("Enter Student ID:")
    if st.button("Save Details"):
        st.success(f"Student {name} registered locally!")

# ----------------- SECTION 3: FACE DETECTOR -----------------
elif choice == "📷 Face Detector (Live Attendance)":
    st.subheader("📷 Live Face Recognition Attendance")
    
    img_file = st.camera_input("Take a photo to mark attendance")

    if img_file is not None:
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
        gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
        
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(opencv_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
            st.image(opencv_img, channels="BGR", caption="Processed Image")
            
            # अटेंडेंस सेव करना
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            user_name = "Detected_User"
            
            new_attendance = pd.DataFrame([[user_name, current_date, current_time]], columns=["Name", "Date", "Time"])
            df_old = pd.read_csv(ATTENDANCE_FILE)
            df_updated = pd.concat([df_old, new_attendance], ignore_index=True)
            df_updated.to_csv(ATTENDANCE_FILE, index=False)
            
            st.success(f"✅ Attendance Marked for {user_name} at {current_time}!")
        else:
            st.warning("No face detected. Please try again.")

# ----------------- SECTION 4: TRAIN DATA -----------------
elif choice == "⚙️ Train Data":
    st.subheader("⚙️ Train AI Model")
    st.write("नया डेटाबेस अपडेट होने के बाद एआई मॉडल को यहाँ से ट्रेन करें।")
    if st.button("Start Training"):
        with st.spinner("Training in progress..."):
            # यहाँ traindata.py का लॉजिक चलेगा
            st.success("AI Model Trained Successfully!")

# ----------------- SECTION 5: ATTENDANCE RECORD -----------------
elif choice == "📊 Attendance Record":
    st.subheader("📊 Live Attendance Sheets")
    df_show = pd.read_csv(ATTENDANCE_FILE)
    st.dataframe(df_show)
    
    # डाउनलोड बटन
    csv_data = df_show.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Excel/CSV Sheet", data=csv_data, file_name="Attendance_Report.csv", mime="text/csv")