from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500+200+100")
        self.root.title("Face Recognition System - Train Data")

        title_lbl = Label(self.root, text="TRAIN FACE DATA", font=("times new roman", 30, "bold"), bg="green", fg="white")
        title_lbl.pack(fill=X)

        train_btn = Button(self.root, text="START TRAINING", command=self.train_classifier,
                           font=("times new roman", 20, "bold"), bg="skyblue", fg="black", cursor="hand2")
        train_btn.pack(pady=150)

    # ================= TRAIN FUNCTION =================
    def train_classifier(self):
        try:
            data_dir = "data"
            if not os.path.exists(data_dir):
                messagebox.showerror("Error", "Data folder not found!")
                return

            # Step 1: Fix filenames if invalid
            for filename in os.listdir(data_dir):
                if filename.startswith("user..") and filename.endswith(".jpg"):
                    name_parts = filename.split("..")
                    if len(name_parts) == 2:
                        number_part = name_parts[1].split('.')[0]
                        new_name = f"user.1.{number_part}.jpg"
                        os.rename(os.path.join(data_dir, filename), os.path.join(data_dir, new_name))
                        print(f"Renamed: {filename} -> {new_name}")

            # Step 2: Prepare training data
            path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
            faces = []
            ids = []

            for image_path in path:
                try:
                    img = Image.open(image_path).convert('L')  # grayscale
                    image_np = np.array(img, 'uint8')
                    filename = os.path.split(image_path)[1]
                    parts = filename.split('.')

                    if len(parts) < 3 or not parts[1].isdigit():
                        print(f"Skipping invalid file: {filename}")
                        continue

                    id = int(parts[1])
                    faces.append(image_np)
                    ids.append(id)

                    cv2.imshow("Training", image_np)
                    cv2.waitKey(1)

                except Exception as e:
                    print(f"Error reading {image_path}: {str(e)}")

            if len(faces) < 2:
                messagebox.showerror("Error", "At least 2 valid images required for training.")
                cv2.destroyAllWindows()
                return

            # Step 3: Train the recognizer
            ids = np.array(ids)
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, ids)
            recognizer.write("classifier.xml")

            cv2.destroyAllWindows()
            messagebox.showinfo("Success", "Training completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}")

# ================= MAIN =================
if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
