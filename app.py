import streamlit as st
import cv2
import pandas as pd
import numpy as np

st.title("AI Face Recognition Attendance System")

img_file = st.camera_input("Take a photo")

if img_file is not None:
    
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    opencv_img = cv2.imdecode(file_bytes, 1)
    
    
    gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
    
    
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
   
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) > 0:
        st.success(f"Image Captured Successfully! फोटो में {len(faces)} चेहरा मिला।")
        
        
        for (x, y, w, h) in faces:
            cv2.rectangle(opencv_img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        st.image(opencv_img, channels="BGR", caption="Processed Image")
        
       
        
    else:
        st.warning("फोटो तो खींच गई, लेकिन कोई चेहरा नहीं मिला। कृपया सीधे कैमरे में देखें।")