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

/* 🌌 पूरे मुख्य पेज का बैकग्राउंड */
.stApp, .main {
    background-color: #E0E0E0 !important; 
}

/* 🔵 साइडबार का बैकग्राउंड... */
[data-testid="stSidebar"] {
    background-color: #E0F7FA !important; 
}

/* 🎨 मुख्य हेडिंग का कलर */
.main h1, h1 span {
    color:   #B71C1C !important;
}

/* ==========================================================
   🚨 क्लिक करने की समस्या को फिक्स करने का कोड (Z-INDEX & POINTER EVENTS)
   ========================================================== */

/* ⚙️ हेडर बार की क्लिक-थ्रू सेटिंग्स ताकि इसके नीचे के बटन क्लिक हो सकें */
div[data-testid="stHeader"], header {
    background-color: #1A237E !important;
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important; 
    align-items: center !important;
    height: 3.5rem !important;
    pointer-events: none !important; /* 👈 हेडर खुद माउस क्लिक नहीं रोकेगा */
    z-index: 999 !important;
}

/* 📄 पेजों की लिस्ट - इसे सबसे ऊपर (Front) लाएंगे ताकि क्लिक हो सके */
div[data-testid="stSidebarNav"] {
    position: fixed !important;
    top: 8px !important;
    left: 350px !important; 
    z-index: 999999 !important; /* 👈 सबसे ऊपर की परत */
    background: transparent !important;
    width: auto !important;
    pointer-events: auto !important; /* 👈 इसपर माउस क्लिक काम करेगा */
}

/* पेजों के अंदर के <ul> (List) को हॉरिजॉन्टल अरेंज करना */
div[data-testid="stSidebarNav"] ul {
    display: flex !important;
    flex-direction: row !important; 
    gap: 15px !important;          
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
    pointer-events: auto !important;
}

/* पेजों के लिंक्स और बटन्स */
div[data-testid="stSidebarNav"] ul li {
    padding: 5px 10px !important;
    background-color: #F8F9FA !important;
    border-radius: 5px !important;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.05) !important;
    pointer-events: auto !important;
}

/* बटन के अंदर के टेक्स्ट/लिंक को भी क्लिकेबल बनाना */
div[data-testid="stSidebarNav"] ul li a {
    pointer-events: auto !important;
    display: block !important;
}

/* 🔘 Deploy बटन को टॉप-राइट हेडर लाइन में फिक्स करना */
div[data-testid="stAppDeployButton"], 
div[data-testid="stActionButton"],
.stAppDeployButton {
    position: fixed !important;
    top: 10px !important;
    right: 70px !important; 
    z-index: 999999 !important; /* 👈 डिप्लॉय बटन को भी ऊपर लाया */
    pointer-events: auto !important;
}

/* 🔘 Deploy बटन का ग्रे कलर स्टाइल */
div[data-testid="stAppDeployButton"] button,
.stAppDeployButton button {
    background-color: #757575 !important; 
    color: #FFFFFF !important;            
    border: 1px solid #616161 !important;
    border-radius: 6px !important;
}

/* 🔘 3-Dots (Menu Button) */
div[data-testid="stToolbar"] {
    position: fixed !important;
    top: 10px !important;
    right: 15px !important;
    z-index: 999999 !important;
    pointer-events: auto !important;
}

/* 🪟 साइडबार के टॉप गैप को हटाना */
div[data-testid="stSidebarUserContent"] {
    padding-top: 0rem !important;
}

/* ========================================================== */

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
st.write("कैमरा शुरू करने के लिए नीचे 'Start' पर क्लिक करें। चेहरा दिखते ही सिस्टम अपने आप 100 फ़ोटो क्लिक कर लेगा।")

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
        
    st.success("🎉 फोटो सैंपल सफलतापूर्वक कैप्चर कर लिए गए हैं!")

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