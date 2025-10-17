from tkinter import*
from tkinter import ttk           
from PIL import Image,ImageTk
import os
from tkinter import messagebox
from student import student
from traindata import Train
from facedata import Face_Recognition
from attendance_record import Attendance
class Face_Recognition_System:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("face Recogniton System")
      


     #add img0

        img0 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\four.jpeg")   
        img0 = img0.resize((550, 155), Image.Resampling.LANCZOS)

        self.bg_image4= ImageTk.PhotoImage(img0)
        bg_label4 = Label(self.root, image=self.bg_image4)    
        bg_label4.place(x=0, y=0, width=500, height=150)





    
     #add img1

        img = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\firstpic.jpeg")   
        img = img.resize((550, 155), Image.Resampling.LANCZOS)

        self.bg_image = ImageTk.PhotoImage(img)
        bg_label = Label(self.root, image=self.bg_image)    
        bg_label.place(x=500, y=0, width=350, height=150)

       #addimg2


        img1 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\sis.jpeg")   
        img1 = img1.resize((550, 155), Image.Resampling.LANCZOS)

        self.bg_image1 = ImageTk.PhotoImage(img1)

        bg_label = Label(self.root, image=self.bg_image1)    
        bg_label.place(x=850, y=0, width=350, height=150)

          
   #add img3

        img3 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\third.jpeg")   
        img3 = img3.resize((550, 155), Image.Resampling.LANCZOS)

        self.bg_image3 = ImageTk.PhotoImage(img3)
        bg_label3 = Label(self.root, image=self.bg_image3,cursor="hand2")    
        bg_label3.place(x=1200, y=0, width=350, height=150)


    #bag img4

         

        img5 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\fift.jpeg")   
        img5 = img5.resize((1530, 710), Image.Resampling.LANCZOS)

        self.bg_image5 = ImageTk.PhotoImage(img5)
        bg_label5 = Label(self.root, image=self.bg_image5)    
        bg_label5.place(x=0, y=140, width=1530, height=650)

#main lable
        title_lbl = Label(bg_label5, text="AI-POWER  FACE RECOGNITION ATTENDANCE SYSTEM", font=("times new roman", 35, "bold"),bg= "skyblue", fg="black")
        title_lbl.place(x=0, y=0, width=1530, height=45)


#student button
       
         
        img6 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\love2.jpeg")   
        img6= img6.resize((250, 100), Image.Resampling.LANCZOS)
        self.bg_image6 = ImageTk.PhotoImage(img6)

        b1=Button(bg_label5,image=self.bg_image6,command=self.student_details,cursor="hand2")
        b1.place(x=10,y=60,width=250,height=100)


        b1=Button(bg_label5,text="Student Details",command=self.student_details,cursor="hand2",font=("times new roman", 20, "bold"), bg="skyblue", fg="blue")
        b1.place(x=10,y=150,width=250,height=30)




# DETECT FACE button
       
         
        img7 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\seven.jpeg")   
        img7= img7.resize((250, 100), Image.Resampling.LANCZOS)

        self.bg_image7 = ImageTk.PhotoImage(img7)

        b1=Button(bg_label5,image=self.bg_image7,cursor="hand2",command=self.face_data)
        b1.place(x=300,y=60,width=250,height=100)


        b1=Button(bg_label5,text="Face Detector",cursor="hand2",command=self.face_data,font=("times new roman", 20, "bold"), bg="skyblue", fg="blue")
        b1.place(x=300,y=150,width=250,height=30)




# Attendance record button
       
         
        img8 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\anu.jpeg")   
        img8= img8.resize((250, 100), Image.Resampling.LANCZOS)

        self.bg_image8 = ImageTk.PhotoImage(img8)

        b1=Button(bg_label5,image=self.bg_image8,cursor="hand2", command=self.attendance_record_data)
        b1.place(x=10,y=250,width=250,height=100)


        b1=Button(bg_label5,text="Attendance Record",cursor="hand2", command=self.attendance_record_data,font=("times new roman", 20, "bold"), bg="skyblue", fg="blue")
        b1.place(x=10,y=350,width=250,height=30)






# HELP DESK button
       
         
        img9 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\shiv.jpeg")   
        img9= img9.resize((250, 100), Image.Resampling.LANCZOS)

        self.bg_image9 = ImageTk.PhotoImage(img9)

        b1=Button(bg_label5,image=self.bg_image9,cursor="hand2",command=self.help_desk)
        b1.place(x=300,y=250,width=250,height=100)


        b1=Button(bg_label5,text="Help Desk",cursor="hand2",command=self.help_desk,font=("times new roman", 20, "bold"), bg="skyblue", fg="blue")
        b1.place(x=300,y=350,width=250,height=30)








# train data button
       
         
        img10 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\shiv2.jpeg")   
        img10= img10.resize((250, 100), Image.Resampling.LANCZOS)

        self.bg_image10= ImageTk.PhotoImage(img10)

        b1=Button(bg_label5,image=self.bg_image10,cursor="hand2",command=self.train_data)
        b1.place(x=10,y=450,width=250,height=100)


        b1=Button(bg_label5,text="Train Data",cursor="hand2",command=self.train_data,font=("times new roman", 20, "bold"), bg="skyblue", fg="blue")
        b1.place(x=10,y=550,width=250,height=30)






# Photo Face button
       
         
        img11 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\love.jpeg")   
        img11= img11.resize((250, 100), Image.Resampling.LANCZOS)

        self.bg_image11 = ImageTk.PhotoImage(img11)

        b1=Button(bg_label5,image=self.bg_image11,cursor="hand2")
        b1.place(x=300,y=450,width=250,height=100)


        b1=Button(bg_label5,text="Photos",cursor="hand2",command=self.open_img,font=("times new roman", 20, "bold"), bg="skyblue", fg="blue")
        b1.place(x=300,y=550,width=250,height=30)






# developer face button
       
         
        img12 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\yes.jpeg")   
        img12= img12.resize((250, 100), Image.Resampling.LANCZOS)

        self.bg_image12 = ImageTk.PhotoImage(img12)

        b1=Button(bg_label5,image=self.bg_image12,cursor="hand2",command=self.developer_info,)
        b1.place(x=1260,y=60,width=250,height=100)


        b1=Button(bg_label5,text="Developer",cursor="hand2",command=self.developer_info,font=("times new roman", 20, "bold"), bg="skyblue", fg="blue")
        b1.place(x=1260,y=160,width=250,height=30)





# Exit button
       
         
        img13 = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\exit.jpeg")   
        img13= img13.resize((250, 100), Image.Resampling.LANCZOS)

        self.bg_image13 = ImageTk.PhotoImage(img13)

        b1=Button(bg_label5,image=self.bg_image13,cursor="hand2",command=self.close_window,)
        b1.place(x=1260,y=450,width=250,height=100)


        b1=Button(bg_label5,text="Exit",cursor="hand2",command=self.close_window,font=("times new roman", 20, "bold"), bg="skyblue", fg="blue")
        b1.place(x=1260,y=550,width=250,height=30)

#===============open img in data file=============

    def open_img(self):
       os.startfile("data")

#--------------------Function button---------
    def student_details(self):
     self.new_window=Toplevel(self.root)
     self.app=student(self.new_window)


    def train_data (self):
     self.new_window=Toplevel(self.root)
     self.app=Train(self.new_window)

    def face_data (self):
     self.new_window=Toplevel(self.root)
     self.app=Face_Recognition(self.new_window)

    def attendance_record_data (self):
     self.new_window=Toplevel(self.root)
     self.app=Attendance(self.new_window)
   

       # -------------------- Help Desk Window --------------------
    def help_desk(self):
        help_win = Toplevel(self.root)
        help_win.title("Help Desk")
        help_win.geometry("600x400+650+300")
        help_win.config(bg="#EAF6F6")

        # Title Label
        title = Label(help_win, text="Help Desk", font=("times new roman", 25, "bold"), bg="#EAF6F6", fg="#4D1A1C")
        title.pack(pady=10)

        # Logo Image (optional)
        try:
            from PIL import Image, ImageTk
            img = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\boss.jpeg")  # <-- अपना logo यहाँ डालें
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            logo_label = Label(help_win, image=photo, bg="#EAF6F6")
            logo_label.image = photo
            logo_label.pack(pady=10)
        except:
            pass

        # Info Labels
        info_text = """📞 Contact Information

Email: jhasaket30@gmail.com
Phone: +91 8009207307
Address: BUDDHA INSTITUTE OF TECHNOLOGY, GORAKHAPUR

For any technical issue or training support,
please contact our team using the details above.
        """
        info_label = Label(help_win, text=info_text, font=("times new roman", 14), bg="#EAF6F6", fg="#1A374D", justify=LEFT)
        info_label.pack(padx=20, pady=10)

        # Close Button
        close_btn = Button(help_win, text="Close", command=help_win.destroy, bg="#1A374D", fg="white", font=("Arial", 12, "bold"), relief=RIDGE)
        close_btn.pack(pady=20)
  

     
    # -------------------- Developer Information --------------------
    def developer_info(self):
        dev_win = Toplevel(self.root)
        dev_win.title("Developer Information")
        dev_win.geometry("600x500+650+250")
        dev_win.config(bg="#F0F4F7")

        # Title Label
        title = Label(dev_win, text="Developer", font=("times new roman", 25, "bold"), bg="#F0F4F7", fg="#0F3460")
        title.pack(pady=10)

        # Developer Image (optional)
        try:
            img = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\developer.jpeg")  # अपना फोटो path दें
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            logo_label = Label(dev_win, image=photo, bg="#F0F4F7")
            logo_label.image = photo
            logo_label.pack(pady=10)
        except:
            pass

        # Developer Info
        info = """👤 Name: SAKET JHA
🏫 College: Buddha Institute of Technology
📧 Email: jhasaket30@gmail.com
📱 Phone: +91 8009207307

This Face Recognition Attendance System
is developed using Python, Tkinter & OpenCV.
"""
        info_label = Label(dev_win, text=info, font=("times new roman", 14), bg="#F0F4F7", fg="#0F3460", justify=LEFT)
        info_label.pack(padx=20, pady=10)

        # Resume Button
        def open_resume():
            resume_path = r"C:\Users\ritik\Desktop\CV of saket jha.pdf"  # अपना resume path दें
            if os.path.exists(resume_path):
                os.startfile(resume_path)  # resume open होगा
            else:
                messagebox.showerror("Error", "Resume file not found!")

        resume_btn = Button(dev_win, text="Open Resume", command=open_resume, bg="#0F3460", fg="white",
                            font=("Arial", 12, "bold"), relief=RIDGE)
        resume_btn.pack(pady=10)

        # Close Button
        close_btn = Button(dev_win, text="Close", command=dev_win.destroy, bg="#0F3460", fg="white",
                           font=("Arial", 12, "bold"), relief=RIDGE)
        close_btn.pack(pady=10)


        # -------------------- Close Function --------------------
    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition_System(root)
    root.mainloop()