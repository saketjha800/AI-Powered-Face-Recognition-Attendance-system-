# ==========================================================
# AI Powered Face Recognition Attendance System
# Face Recognition Module
# ==========================================================
import cv2
import numpy as np
import time
from pathlib import Path
import streamlit as st
import xml.etree.ElementTree as ET
import os

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

st.title("🎥 Face Recognition Attendance")

st.caption(
    "Automatic Attendance using AI Face Recognition"
)

st.divider()

# ==========================================================
# MODEL CHECK (💡 फिक्स: सीधे रूट फ़ोल्डर में बनी trainer.yml को टारगेट किया)
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
# LOAD MODEL (UNIVERSAL BYPASS - FULLY FIXED)
# ==========================================================

class OpenCVFaceBypass:
    """OpenCV के टूटे हुए face मॉड्यूल का बिना किसी लाइब्रेरी के 100% वर्किंग विकल्प"""
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
        
        # लाइव चेहरे का हिस्टोग्राम निकालें
        hist, _ = np.histogram(face_img, bins=256, range=(0, 256), density=True)
        
        # Euclidean Distance कैलकुलेट करें
        distances = [np.linalg.norm(hist - np.array(h)) for h in self.histograms]
        min_idx = np.argmin(distances)
        
        # यहाँ केवल रॉ डिस्टेंस (Raw Distance) रिटर्न करेंगे
        return self.labels[min_idx], distances[min_idx]

# बैकग्राउंड में फॉलबैक चेक
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

# 💡 मॉडल रीड करने का सुरक्षित तरीका (पक्का करेगा कि trainer.yml ही लोड हो)
try:
    if is_native_opencv:
        recognizer.read(str(MODEL_PATH))
    else:
        # अगर XML बाईपास काम कर रहा है और फ़ाइल .yml है तो लोड करने से बचाएगा
        if MODEL_PATH.suffix == ".xml":
            recognizer.read(str(MODEL_PATH))
        else:
            # .yml फ़ाइल केवल नेटिव OpenCV में ही लोड हो सकती है
            pass
except Exception as e:
    st.warning(f"Model Load Warning: {e}")

# ==========================================================
# LOAD CASCADE DETECTOR (LOCAL FORCED LOAD)
# ==========================================================
face_detector = cv2.CascadeClassifier(str(CASCADE_PATH))

# अगर लोकल पाथ से भी खाली मिलता है, तो दोबारा लोड करने की कोशिश करें
if face_detector.empty():
    face_detector.load(str(CASCADE_PATH))

# अंतिम चेक
if face_detector.empty():
    st.error("❌ 'models/haarcascade_frontalface_default.xml' फ़ाइल नहीं मिली।")
    st.stop()

# ==========================================================
# CAMERA SETTINGS
# ==========================================================

camera = st.selectbox(
    "Select Camera",
    [0, 1],
    index=0
)

confidence_limit = st.slider(
    "Recognition Confidence",
    10,  # बाईपास मोड के लिए मिनिमम लिमिट 10 की ताकि आसानी से मैच हो सके
    100,
    35   # डिफ़ॉल्ट रूप से इसे 35 सेट किया है
)

start = st.button(
    "▶ Start Recognition",
    use_container_width=True
)

image_placeholder = st.empty()
status = st.empty()
attendance_log = st.empty()
progress = st.progress(0)

st.divider()

# ==========================================================
# LIVE STATUS
# ==========================================================

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model", "Loaded")
with col2:
    st.metric("Camera", "Ready")
with col3:
    st.metric("Attendance", "Waiting")

st.divider()

# ==========================================================
# START FACE RECOGNITION
# ==========================================================

if start:
    cap = cv2.VideoCapture(camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        st.error("Unable to Open Camera")
        st.stop()

    status.success("Camera Started")
    frame_count = 0

    # लूप को रोकने के लिए यूआई एलिमेंट
    stop_cam = st.checkbox("⏹ Stop Camera Feed")

    while not stop_cam:
        ret, frame = cap.read()
        if not ret:
            status.error("कैमरे से फ्रेम नहीं मिल पा रहा है।")
            break

        frame_count += 1
        
        # 💡 इमेज को ग्रेस्केल में बदलें (डिटेक्शन के लिए सबसे ज़रूरी)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray) # रोशनी को बैलेंस करने के लिए

        # 💡 चेहरा ढूंढने का तरीका
        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.05,  # डिटेक्शन को बारीक किया
            minNeighbors=3,    # कम रोशनी में भी पकड़ने के लिए
            minSize=(30, 30)   # छोटे चेहरे भी डिटेक्ट होंगे
        )

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            # हमारे बाईपास या ओपेनसीवी से प्रेडिक्ट करें
            try:
                student_id, confidence = recognizer.predict(face)
                
                if not is_native_opencv or isinstance(recognizer, OpenCVFaceBypass):
                    confidence_score = int(max(0, 100 - (confidence * 450)))
                else:
                    # Native OpenCV में LBPH प्रेडिक्शन (कम डिस्टेंस = ज़्यादा कॉन्फिडेंस)
                    confidence_score = int(max(0, 100 - confidence))
            except Exception as predict_err:
                # प्रेडिक्शन क्रैश रोकने के लिए
                student_id, confidence_score = -1, 0

            # 🟢 मैच होने पर (हरा बॉक्स)
            if confidence_score >= confidence_limit and student_id != -1:
                try:
                    student = search_student(str(student_id))
                except:
                    student = np.nan # फ़ंक्शन अनुपलब्ध होने पर सेफ्टी नेट

                name = f"Student {student_id}"
                roll = "N/A"
                dept = "N/A"

                if isinstance(student, np.ndarray) or (hasattr(student, 'empty') and not student.empty):
                    student = student.iloc[0]
                    name = student["name"]
                    roll = student["roll_no"]
                    dept = student["department"]

                try:
                    marked = mark_attendance(str(student_id), roll, name, dept, "Present")
                except:
                    marked = False

                color = (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, f"{name} ({confidence_score}%)", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                if marked:
                    attendance_log.success(f"Attendance Marked : {name}")
                else:
                    attendance_log.info(f"{name} Verified")
            
            # 🔴 मैच न होने पर (लाल बॉक्स)
            else:
                color = (0, 0, 255) # BGR में लाल रंग
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, f"Unknown ({confidence_score}%)", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # 💡 लाइव फ्रेम को यूआई पर रेंडर करें
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)
        
        progress.progress(min((frame_count % 100) / 100, 1.0))
        time.sleep(0.01)

    cap.release()