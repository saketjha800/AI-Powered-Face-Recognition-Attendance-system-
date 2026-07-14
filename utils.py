"""
=========================================================
AI Powered Face Recognition Attendance System
Utility Functions
=========================================================
"""

from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATASET_DIR = DATA_DIR / "dataset"
ATTENDANCE_DIR = DATA_DIR / "attendance"

MODEL_DIR = BASE_DIR / "models"

DATASET_DIR.mkdir(parents=True, exist_ok=True)
ATTENDANCE_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# HAAR CASCADE
# ==========================================================

CASCADE_PATH = Path("models/haarcascade_frontalface_default.xml")

# ==========================================================
# LOAD FACE DETECTOR
# ==========================================================

@st.cache_resource
def load_face_detector():

    detector = cv2.CascadeClassifier(str(CASCADE_PATH))

    if detector.empty():
        raise FileNotFoundError(
            f"Haar Cascade not found:\n{CASCADE_PATH}"
        )

    return detector

# ==========================================================
# LOAD TRAINED MODEL
# ==========================================================

@st.cache_resource
def load_classifier():

    model = cv2.face.LBPHFaceRecognizer_create()

    classifier = MODEL_DIR / "classifier.xml"

    if classifier.exists():

        model.read(str(classifier))

    return model

# ==========================================================
# STUDENT DATASET FOLDER
# ==========================================================

def student_dataset_folder(student_id):

    folder = DATASET_DIR / str(student_id)

    folder.mkdir(parents=True, exist_ok=True)

    return folder

# ==========================================================
# IMAGE UTILITIES
# ==========================================================

def bgr_to_rgb(image):

    return cv2.cvtColor(

        image,

        cv2.COLOR_BGR2RGB

    )


def rgb_to_bgr(image):

    return cv2.cvtColor(

        image,

        cv2.COLOR_RGB2BGR

    )


def gray(image):

    return cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )


def resize(image, width=200, height=200):

    return cv2.resize(

        image,

        (width, height)

    )

# ==========================================================
# FACE DETECTION
# ==========================================================

def detect_faces(image):

    detector = load_face_detector()

    gray_image = gray(image)

    faces = detector.detectMultiScale(

        gray_image,

        scaleFactor=1.2,

        minNeighbors=5,

        minSize=(100,100)

    )

    return faces

# ==========================================================
# EXPORT FUNCTIONS
# ==========================================================

def export_dataframe_excel(df, file_name):

    df.to_excel(

        file_name,

        index=False

    )

    return file_name


def export_dataframe_csv(df, file_name):

    df.to_csv(

        file_name,

        index=False

    )

    return file_name

# ==========================================================
# CAMERA CHECK
# ==========================================================

def camera_available(index=0):

    cap = cv2.VideoCapture(index)

    status = cap.isOpened()

    cap.release()

    return status

# ==========================================================
# FILE CHECK
# ==========================================================

def model_exists():

    return (MODEL_DIR / "classifier.xml").exists()


def cascade_exists():

    return CASCADE_PATH.exists()

# ==========================================================
# STREAMLIT HELPERS
# ==========================================================

def success(message):

    st.success(message)


def warning(message):

    st.warning(message)


def error(message):

    st.error(message)


def info(message):

    st.info(message)

# ==========================================================
# SYSTEM STATUS
# ==========================================================

def system_status():

    return {

        "Camera": camera_available(),

        "Cascade": cascade_exists(),

        "Model": model_exists(),

        "Dataset": DATASET_DIR.exists(),

        "Attendance": ATTENDANCE_DIR.exists()

    }