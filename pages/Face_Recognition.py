# ==========================================================
# AI Powered Face Recognition Attendance System
# Face Recognition Module
# ==========================================================
import os
import cv2
import numpy as np
import time
from pathlib import Path
import streamlit as st
import xml.etree.ElementTree as ET
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

from database import *
from utils import *

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Face Recognition",
    page_icon="🎥",
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
st.title("🎥 Face Recognition Attendance")
st.caption("Automatic Attendance using AI Face Recognition")
st.divider()

# ==========================================================
# MODEL CHECK
# ==========================================================
MODEL_PATH = Path("trainer.yml")
CASCADE_PATH = Path("models/haarcascade_frontalface_default.xml")

if not MODEL_PATH.exists():
    st.error("Train Model First (trainer.yml missing).")
    st.stop()

if not CASCADE_PATH.exists():
    st.error("Haar Cascade File Missing.")
    st.stop()

# ==========================================================
# LOAD MODEL (UNIVERSAL BYPASS)
# ==========================================================
class OpenCVFaceBypass:
    def __init__(self):
        self.histograms = []
        self.labels = []

    def read(self, xml_path):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            hist_node = root.find(".//histograms")
            labels_node = root.find(".//labels")
            
            if hist_node is not None and labels_node is not None:
                self.histograms = []
                for hist in hist_node.findall("data"):
                    text_data = hist.text.strip().split()
                    self.histograms.append([float(x) for x in text_data])
                
                labels_text = labels_node.text.strip().split()
                self.labels = [int(x) for x in labels_text]
        except Exception as e:
            print(f"XML Read Error: {e}")

    def predict(self, face_img):
        if not self.histograms:
            return -1, 999.0
        
        hist, _ = np.histogram(face_img, bins=256, range=(0, 256), density=True)
        distances = [np.linalg.norm(hist - np.array(h)) for h in self.histograms]
        min_idx = np.argmin(distances)
        return self.labels[min_idx], distances[min_idx]

# बैकग्राउंड में फॉलबैक चेक और इनिशियलाइज़ेशन
recognizer = OpenCVFaceBypass()
is_native_opencv = False

try:
    if hasattr(cv2, 'face') and hasattr(cv2.face, 'LBPHFaceRecognizer_create'):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        is_native_opencv = True
    elif hasattr(cv2, 'face_LBPHFaceRecognizer'):
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        is_native_opencv = True
except:
    pass

try:
    if is_native_opencv:
        recognizer.read(str(MODEL_PATH))
    else:
        if MODEL_PATH.suffix == ".xml":
            recognizer.read(str(MODEL_PATH))
except Exception as e:
    st.warning(f"Model Load Warning: {e}")

# Haar Cascade डिटेक्टर लोड करना
face_detector = cv2.CascadeClassifier(str(CASCADE_PATH))
if face_detector.empty():
    face_detector.load(str(CASCADE_PATH))

if face_detector.empty():
    st.error("❌ 'models/haarcascade_frontalface_default.xml' फ़ाइल नहीं मिली।")
    st.stop()

# ==========================================================
# SETTINGS & CONTROLS
# ==========================================================
confidence_limit = st.slider(
    "Recognition Confidence",
    10,  
    100,
    35   
)

# रीयल-टाइम अटेंडेंस लॉग के लिए UI प्लेसहोल्डर
attendance_log = st.empty()

# ==========================================================
# WEBRTC PROCESSOR CLASS
# ==========================================================
class FaceRecognizerProcessor(VideoProcessorBase):
    def __init__(self, detector, recognizer, is_native, conf_limit):
        self.detector = detector
        self.recognizer = recognizer
        self.is_native = is_native
        self.conf_limit = conf_limit
        self.last_marked_student = None
        self.last_marked_time = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        # चेहरे डिटेक्ट करें
        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            try:
                student_id, confidence = self.recognizer.predict(face)
                if not self.is_native or isinstance(self.recognizer, OpenCVFaceBypass):
                    confidence_score = int(max(0, 100 - (confidence * 450)))
                else:
                    confidence_score = int(max(0, 100 - confidence))
            except Exception:
                student_id, confidence_score = -1, 0

            # 🟢 चेहरा मैच होने पर
            if confidence_score >= self.conf_limit and student_id != -1:
                try:
                    student = search_student(str(student_id))
                except Exception:
                    student = np.nan

                name = f"Student {student_id}"
                roll = "N/A"
                dept = "N/A"

                if isinstance(student, np.ndarray) or (hasattr(student, 'empty') and not student.empty):
                    student = student.iloc[0]
                    name = student["name"]
                    roll = student["roll_no"]
                    dept = student["department"]

                # स्पैमिंग को रोकने के लिए टाइम-लॉक (5 सेकंड का अंतर)
                current_time = time.time()
                if self.last_marked_student != student_id or (current_time - self.last_marked_time) > 5:
                    try:
                        mark_attendance(str(student_id), roll, name, dept, "Present")
                        self.last_marked_student = student_id
                        self.last_marked_time = current_time
                    except Exception:
                        pass

                color = (0, 255, 0) # हरा रंग
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                cv2.putText(img, f"{name} ({confidence_score}%)", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # 🔴 अननोन चेहरा होने पर
            else:
                color = (0, 0, 255) # लाल रंग
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                cv2.putText(img, f"Unknown ({confidence_score}%)", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# ==========================================================
# STREAMER UI IN STREAMLIT
# ==========================================================
st.subheader("🎥 Live Face Recognition Scanner")
st.write("Please Press  **Start** Button for Start Camra")

ctx = webrtc_streamer(
    key="face-recognition-scan",
    video_processor_factory=lambda: FaceRecognizerProcessor(
        face_detector, recognizer, is_native_opencv, confidence_limit
    ),
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    media_stream_constraints={"video": True, "audio": False}
)

if ctx.state.playing:
    st.success("सफलतापूर्वक कैमरा कनेक्ट हो गया है। स्कैनर लाइव है! 🟢")
else:
    st.info("📷 **Camera is on standby. Please click the 'Start' button above.**")

st.divider()

# ==========================================================
# LIVE METRICS / STATUS CARD
# ==========================================================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model Status", "Loaded" if MODEL_PATH.exists() else "Missing")
with col2:
    st.metric("Webcam Mode", "WebRTC (Cloud Optimized)")
with col3:
    st.metric("Bypass Classifier", "Active" if not is_native_opencv else "Inactive")






    # streamlit_app.py के बिल्कुल नीचे (आखिरी लाइनों में) लिखें:

st.write("---") # एक पतली डिवाइडर लाइन बनाने के लिए

# यह बटन मुख्य पेज पर दिखेगा
if st.button("📊ATTENDANCE REPORT PAGE OPEN", use_container_width=True):
    st.switch_page("pages/Attendance_Report.py")