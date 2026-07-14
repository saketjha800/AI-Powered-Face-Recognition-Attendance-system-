# ==========================================================
# AI Powered Face Recognition Attendance System
# Face Dataset Module
# ==========================================================

import cv2
import time
from pathlib import Path

import streamlit as st

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

st.title("📷 Face Dataset Collection")

st.caption(
    "Capture face images for model training."
)

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

student = students[
    students["name"] == student_name
].iloc[0]

student_id = student["student_id"]

roll_no = student["roll_no"]

st.info(

    f"""

Student ID : {student_id}

Roll No : {roll_no}

Department : {student['department']}

"""

)

st.divider()

# ==========================================================
# CAMERA SETTINGS
# ==========================================================

TOTAL_IMAGES = 100

camera_index = st.selectbox(

    "Camera",

    [0,1],

    index=0

)

capture_btn = st.button(

    "📸 Start Capture",

    use_container_width=True

)

image_placeholder = st.empty()

progress_bar = st.progress(0)

status = st.empty()


# ==========================================================
# START FACE CAPTURE
# ==========================================================

if capture_btn:

    detector = load_face_detector()

    save_folder = student_dataset_folder(student_id)

    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():

        st.error("Unable to Open Camera")

        st.stop()

    image_count = 0

    status.info("Starting Camera...")

    while True:

        ret, frame = cap.read()

        if not ret:

            status.error("Camera Frame Error")

            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = detector.detectMultiScale(

            gray,

            scaleFactor=1.2,

            minNeighbors=5,

            minSize=(100,100)

        )

        for (x,y,w,h) in faces:

            face = frame[y:y+h, x:x+w]

            face = cv2.resize(

                face,

                (200,200)

            )

            image_count += 1

            filename = save_folder / f"{image_count}.jpg"

            cv2.imwrite(

                str(filename),

                face

            )

            save_dataset_image(

                student_id,

                str(filename),

                image_count

            )

            cv2.rectangle(

                frame,

                (x,y),

                (x+w,y+h),

                (0,255,0),

                2

            )

            cv2.putText(

                frame,

                f"{image_count}/{TOTAL_IMAGES}",

                (x,y-10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                (0,255,0),

                2

            )

            progress_bar.progress(

                image_count / TOTAL_IMAGES

            )

            status.success(

                f"Captured {image_count} Images"

            )

        image_placeholder.image(

            bgr_to_rgb(frame),

            channels="RGB",

            use_container_width=True

        )

        if image_count >= TOTAL_IMAGES:

            break

        time.sleep(0.03)

    cap.release()

    progress_bar.progress(1.0)

    status.success(

        "Dataset Collection Completed Successfully."

    )

    try:

        with get_connection() as conn:

            conn.execute(

                """

                UPDATE students

                SET photo_sample='Yes'

                WHERE student_id=?

                """,

                (student_id,)

            )

    except Exception as e:

        st.error(e)

    st.balloons()

    st.success(

        f"{TOTAL_IMAGES} Images Saved Successfully."

    )

st.divider()




# ==========================================================
# DATASET SUMMARY
# ==========================================================

st.subheader("📊 Dataset Summary")

summary = get_all_students()

if not summary.empty:

    total_students = len(summary)

    completed = len(

        summary[
            summary["photo_sample"] == "Yes"
        ]

    )

    pending = total_students - completed

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Students",

            total_students

        )

    with c2:

        st.metric(

            "Dataset Ready",

            completed

        )

    with c3:

        st.metric(

            "Pending",

            pending

        )