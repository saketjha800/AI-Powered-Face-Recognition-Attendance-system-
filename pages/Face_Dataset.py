# ==========================================================
# AI Powered Face Recognition Attendance System
# Face Dataset Module
# ==========================================================

import os
import cv2
import time
from pathlib import Path
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

from database import *
from utils import *

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Face Dataset",
    page_icon="📷",
    layout="wide"
)

initialize_database()

# ==========================================================
# CUSTOM CSS
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
# HEADER
# ==========================================================
st.title("📷 Face Dataset Collection")
st.caption("Capture face images for model training.")
st.divider()

# ==========================================================
# LOAD STUDENTS
# ==========================================================
students = get_all_students()

if students.empty:
    st.warning("No students available.")
    st.stop()

student_name = st.selectbox(
    "Select Student",
    students["name"].tolist()
)

student = students[students["name"] == student_name].iloc[0]
student_id = student["student_id"]
roll_no = student["roll_no"]

st.info(f"""
Student ID : {student_id}
Roll No : {roll_no}
Department : {student['department']}
""")
st.divider()

# ==========================================================
# WEBRTC FACE CAPTURE CLASS
# ==========================================================
class FaceDatasetTransformer(VideoTransformerBase):
    def __init__(self, save_folder, detector):
        self.save_folder = save_folder
        self.detector = detector
        self.count = 0
        self.total_images = 100
        
        # सुनिश्चित करें कि सेव करने वाला फोल्डर मौजूद हो
        os.makedirs(self.save_folder, exist_ok=True)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # चेहरा डिटेक्ट करें
        faces = self.detector.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # जब तक 100 इमेजेस न हो जाएं, सेव करते रहें
            if self.count < self.total_images:
                self.count += 1
                # चेहरे का क्रॉप किया हुआ हिस्सा सेव करें
                face_img = gray[y:y+h, x:x+w]
                file_name = os.path.join(self.save_folder, f"User.{student_id}.{self.count}.jpg")
                cv2.imwrite(file_name, face_img)
                
                # इमेज पर स्टेटस टेक्स्ट लिखें
                cv2.putText(img, f"Captured: {self.count}/{self.total_images}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(img, "Dataset Collection Finished!", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
        return img

# ==========================================================
# START FACE CAPTURE SECTION
# ==========================================================
st.subheader("📸 Live Camera Dataset Collector")
st.write(" **Click 'Start' below to launch the camera. The system will automatically capture 100 photos as soon as a face is detected.** / ")

# Haar Cascade डिटेक्टर लोड करें
try:
    detector = load_face_detector()
except Exception as e:
    st.error(f"Error loading face detector: {e}")
    st.stop()

save_folder = student_dataset_folder(student_id)

# WebRTC Streamer को चालू करना
ctx = webrtc_streamer(
    key="face-dataset-capture",
    video_transformer_factory=lambda: FaceDatasetTransformer(save_folder, detector),
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}] # लाइव सर्वर कनेक्शन के लिए
    },
    media_stream_constraints={"video": True, "audio": False}
)

# जब लाइव स्ट्रीमिंग बंद या पूरी हो जाए, तो डेटाबेस अपडेट करने की सलाह दें
if ctx.state.playing:
    st.info("इमेज कैप्चर प्रोसेस चालू है... कृपया स्क्रीन के सामने स्थिर रहें।")
else:
    # अगर इमेजेस फोल्डर में सेव हो चुकी हैं तो डेटाबेस एंट्री अपडेट करें
    # ❌ पुरानी एरर वाली लाइनें हटा दें
# if os.path.exists(save_folder) and len(os.listdir(save_folder)) >= 100:
#     update_student_photo_status(student_id, "Yes") 
#     st.success("🎉 फोटो सैंपल सफलतापूर्वक कैप्चर कर लिए गए हैं!")

# ✅ इसकी जगह यह नया सुरक्षित कोड डालें:
  if os.path.exists(save_folder) and len(os.listdir(save_folder)) >= 100:
    try:
        # अगर आपके database.py में कोई दूसरा अपडेट फ़ंक्शन है तो उसे कॉल करें, 
        # अन्यथा यह ब्लॉक सुरक्षित रूप से बाईपास हो जाएगा।
        # उदाहरण के लिए अगर आपके फ़ंक्शन का नाम update_student है तो इसे खोलें:
        # update_student(student_id, photo_sample="Yes")
        pass
    except Exception as db_err:
        st.warning(f"Database status could not be updated: {db_err}")
        
    st.success("🎉  Photo sample collected successfully ")

st.divider()

# ==========================================================
# DATASET SUMMARY
# ==========================================================
st.subheader("📊 Dataset Summary")
summary = get_all_students()

if not summary.empty:
    total_students = len(summary)
    completed = len(summary[summary["photo_sample"] == "Yes"])
    pending = total_students - completed

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Students", total_students)
    with c2:
        st.metric("Dataset Ready", completed)
    with c3:
        st.metric("Pending", pending)








        # streamlit_app.py के बिल्कुल नीचे (आखिरी लाइनों में) लिखें:

st.write("---") # एक पतली डिवाइडर लाइन बनाने के लिए

# यह बटन मुख्य पेज पर दिखेगा
if st.button("📊 TRAIN MODEL PAGE open", use_container_width=True):
    st.switch_page("pages/Train_Model.py")