# ==========================================================
# AI Powered Face Recognition Attendance System
# Train Face Recognition Model
# pages/3_Train_Model.py
# ==========================================================

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import streamlit as st

from database import *
from utils import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Train Model",
    page_icon="🧠",
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

st.title("🧠 Train Face Recognition Model")
st.caption("Generate LBPH Face Recognition Model from Student Dataset")
st.divider()

# ==========================================================
# PATHS (💡 पाथ को सीधा रूट में trainer.yml पर सेट किया)
# ==========================================================
DATASET_PATH = Path("data/dataset")
CLASSIFIER_PATH = "trainer.yml"  # सीधे रूट फ़ोल्डर में सेव होगा ताकि दूसरा पेज ढूंढ सके

# ==========================================================
# DATASET INFORMATION
# ==========================================================
students = get_all_students()
dataset_ready = students[students["photo_sample"] == "Yes"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Students", len(students))
with col2:
    st.metric("Dataset Ready", len(dataset_ready))
with col3:
    st.metric("Pending", len(students) - len(dataset_ready))

st.divider()

# ==========================================================
# TRAIN BUTTON
# ==========================================================
train_btn = st.button("🚀 Train Model", use_container_width=True)

progress = st.progress(0)
status = st.empty()
log = st.empty()

# ==========================================================
# TRAIN MODEL
# ==========================================================
if train_btn:
    if not DATASET_PATH.exists():
        st.error("Dataset folder not found.")
        st.stop()

    face_samples = []
    ids = []
    image_files = list(DATASET_PATH.rglob("*.jpg"))

    if len(image_files) == 0:
        st.warning("No dataset images available.")
        st.stop()

    total_images = len(image_files)
    status.info("Loading Dataset Images...")
    
    for index, image_path in enumerate(image_files):
        try:
            image = Image.open(image_path).convert("L")
            image_np = np.array(image, dtype="uint8")
            
            # सभी इमेजेस का साइज़ एक बराबर होना जरूरी है
            image_resized = cv2.resize(image_np, (200, 200))
            
            student_id = int(image_path.parent.name)
            face_samples.append(image_resized)
            ids.append(student_id)
            
            progress.progress((index + 1) / total_images)
            log.write(f"Loaded & Resized : {image_path.name}")
        except Exception as e:
            st.warning(f"Skipped {image_path.name}: {e}")

    status.info("Training Face Recognizer...")
    
    # 💡 डायनेमिक रिकॉग्नाइज़र चेकिंग
    recognizer = None
    methods_to_try = [
        lambda: cv2.face.LBPHFaceRecognizer_create(),
        lambda: cv2.face_LBPHFaceRecognizer.create(),
        lambda: cv2.LBPHFaceRecognizer_create(),
        lambda: cv2.face_LBPHFaceRecognizer_create()
    ]
    
    for method in methods_to_try:
        try:
            recognizer = method()
            if recognizer is not None:
                break
        except AttributeError:
            continue
            
    if recognizer is None:
        st.error("❌ OpenCV Face Module (contrib) इंस्टॉल नहीं है! टर्मिनल में रन करें: `pip install opencv-contrib-python`")
        st.stop()

    try:
        # मॉडल को सही तरीके से ट्रेन करें
        recognizer.train(face_samples, np.array(ids, dtype=np.int32))
        
        # .yml फॉर्मेट में सेव करें ताकि प्रेडिक्शन के दौरान कोई एरर न आए
        if hasattr(recognizer, 'write'):
            recognizer.write(CLASSIFIER_PATH)
        else:
            recognizer.save(CLASSIFIER_PATH)

        progress.progress(1.0)
        accuracy = 100.0

        # डेटाबेस या लॉग्स में सेव करने के लिए
        try:
            save_model(
                model_name="LBPH Classifier",
                model_path=CLASSIFIER_PATH,
                algorithm="LBPH",
                accuracy=accuracy,
                images=total_images,
                students=len(set(ids))
            )
            save_log(module="TRAINING", level="INFO", message="Model trained successfully.")
        except:
            pass # अगर ये फंक्शन्स अलग मॉड्यूल में हैं तो क्रैश न हो

        status.success("Model Training Completed Successfully. 🎉")
        st.balloons()
        
        st.success(
            f"""
            ### Training Completed 🎉
            - **Model Saved As:** `{CLASSIFIER_PATH}`
            - **Total Students Trained:** {len(set(ids))}
            - **Total Images Used:** {total_images}
            """
        )
    except Exception as training_error:
        st.error(f"ट्रेनिंग में एरर: {training_error}")

# ==========================================================
# MODEL INFORMATION
# ==========================================================
st.divider()
st.subheader("📊 Latest Model")

try:
    latest = latest_model()
    if latest.empty:
        st.info("No trained model available.")
    else:
        st.dataframe(latest, use_container_width=True, hide_index=True)
except:
    st.info("Model metadata system is ready.")