from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import mysql.connector
import numpy as np
import os
import csv
from datetime import datetime

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System - Identify Student")

        title_lbl = Label(self.root, text="FACE RECOGNITION SYSTEM",
                          font=("times new roman", 35, "bold"), bg="green", fg="white")
        title_lbl.place(x=0, y=0, width=1530, height=60)

        img_top = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\four.jpeg")
        img_top = img_top.resize((650, 700), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=650, height=700)

        b1 = Button(self.root, text="RECOGNIZE FACE", cursor="hand2",
                    command=self.face_recog,
                    font=("times new roman", 25, "bold"), bg="skyblue", fg="black")
        b1.place(x=700, y=100, width=600, height=60)

        self.text_label = Label(self.root, text="", font=("times new roman", 20, "bold"),
                                bg="white", fg="black")
        self.text_label.place(x=700, y=200, width=600, height=400)

    def mark_attendance(self, i, n, r, d):
        date_today = datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H:%M:%S")
        file_exists = os.path.exists("attendance.csv")

        # Duplicate check for same day
        if file_exists:
            with open("attendance.csv", "r") as f:
                lines = f.readlines()
                for line in lines:
                    entry = line.strip().split(",")
                    if len(entry) >= 5 and entry[0] == str(i) and entry[4] == date_today:
                        return

        with open("attendance.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists or os.path.getsize("attendance.csv") == 0:
                writer.writerow(["ID", "Name", "Roll", "Dept", "Date", "Time", "Status"])
            writer.writerow([i, n, r, d, date_today, time_now, "Present"])
            print(f"Attendance marked: {i}, {n}, {date_today}, {time_now}")

    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coords = []

            for (x, y, w, h) in features:
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int((100 * (1 - predict /300)))

                conn = mysql.connector.connect(host="localhost", user="root", password="Saket@123",
                                               database="face_recognition")
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT Name FROM student WHERE Student_id=" + str(id))
                n = my_cursor.fetchone()
                n = "+".join(n) if n else "Unknown"

                my_cursor.execute("SELECT Roll FROM student WHERE Student_id=" + str(id))
                r = my_cursor.fetchone()
                r = "+".join(r) if r else "N/A"

                my_cursor.execute("SELECT Dep FROM student WHERE Student_id=" + str(id))
                d = my_cursor.fetchone()
                d = "+".join(d) if d else "N/A"

                conn.close()

                if confidence > 80:
                    cv2.putText(img, f"ID: {id}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)
                    cv2.putText(img, f"Name: {n}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)
                    cv2.putText(img, f"Roll: {r}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)
                    cv2.putText(img, f"Dep: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 2)
                    cv2.rectangle(img, (x, y), (x+w, y+h), color, 3)

                    self.text_label.config(
                        text=f"Recognized Student:\n\nID: {id}\nName: {n}\nRoll: {r}\nDept: {d}")

                    # Automatic Attendance
                    self.mark_attendance(id, n, r, d)

                else:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 150), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 3),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 150), 2)
                    self.text_label.config(text="Unknown Face Detected")

                coords = [x, y, w, h]

            return coords

        def recognize(img, clf, faceCascade):
            coords = draw_boundary(img, faceCascade, 1.1, 8,
                                   (150, 150, 0), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read(r"C:\Users\ritik\Desktop\face recognijection\classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
