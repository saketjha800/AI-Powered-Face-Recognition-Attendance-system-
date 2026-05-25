import streamlit as st
import cv2
import pandas as pd

st.title("AI Face Recognition Attendance System")

img_file = st.camera_input("Take a photo")

if img_file is not None:
    file_bytes = img_file.getvalue()

    with open("capture.jpg", "wb") as f:
        f.write(file_bytes)

    st.success("Image Captured Successfully")