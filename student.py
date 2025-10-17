
from tkinter import*
from tkinter import ttk           
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2

class student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face recognitation system")
        
#------------variables------------
    
        self.var_department=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_sem=StringVar()
        self.var_id=StringVar()
        self.var_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()
        self.var_photo=StringVar()

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
        bg_label5.place(x=0, y=140, width=1540, height=650)



#main lable
        title_lbl = Label(bg_label5, text="STUDENT MANAGEMENT SYSTEM", font=("times new roman", 35, "bold"),bg= "skyblue", fg="black")
        title_lbl.place(x=0, y=0, width=1530, height=40)





        main_frame=Frame(bg_label5,bd=2)
        main_frame.place(x=0,y=40,width=1550,height=700)


       #left side

        Left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Details",
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=5, y=10, width=740, height=580)




        img_left = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\four.jpeg")   
        img_left= img_left.resize((720, 130), Image.Resampling.LANCZOS)

        self.photoing_left= ImageTk.PhotoImage(img_left)
        f_lbl = Label(Left_frame, image=self.photoing_left)    
        f_lbl.place(x=5, y=0, width=720, height=130)


# Current course

        current_course_frame = LabelFrame(Left_frame, bd=2, relief=RIDGE, text="Current Course Information",
                                font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=135, width=720, height=110)

#Department
        dep_lable=Label(current_course_frame,text="Department",font=("times new roman",12,"bold"))
        dep_lable.grid(row=0,column=0,padx=10)
        dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_department,font=("times new roman",12,"bold"),state="read only")
        dep_combo["values"]=("Select Department","CSE","IT","AIML(CSE)","DS","civil","Mechnical","EE")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10)


#Course
        course_label=Label(current_course_frame,text="Course",font=("times new roman",12,"bold"))
        course_label.grid(row=0,column=0,padx=10,sticky=W)
        course_combo=ttk.Combobox(current_course_frame,textvariable=self.var_course,font=("times new roman",12,"bold"),state="readonly")
        course_combo["values"]=("Select Course","Btech","Bsc","ITI","B.pharama","D.pharma","BE")
        course_combo.current(0)
        course_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)


#year
        year_label=Label(current_course_frame,text="Year",font=("times new roman",12,"bold"))
        year_label.grid(row=0,column=0,padx=10,sticky=W)
        year_combo=ttk.Combobox(current_course_frame,textvariable=self.var_year,font=("times new roman",12,"bold"),state="readonly")
        year_combo["values"]=("Select Year","2020-21","2021-22","2022-23","2023-24","2024-25","2025-26")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)


#samester
        samester_label=Label(current_course_frame,text="Semester",font=("times new roman",12,"bold"))
        samester_label.grid(row=0,column=0,padx=10,sticky=W)
        samester_combo=ttk.Combobox(current_course_frame,textvariable=self.var_sem,font=("times new roman",12,"bold"),state="readonly")
        samester_combo["values"]=("Select Semester","semester-1","semester-2")
        samester_combo.current(0)
        samester_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)




# Class student information

        class_student_frame = LabelFrame(Left_frame, bd=2, relief=RIDGE, text="Class Student Information",
                                font=("times new roman", 12, "bold"))
        class_student_frame.place(x=5, y=250, width=720, height=340)
# student id
        studentid_label=Label(class_student_frame,text="StudentId :",font=("times new roman",12,"bold"))
        studentid_label.grid(row=0,column=0,padx=10,sticky=W)
        studentid_entry=ttk.Entry(class_student_frame,textvariable=self.var_id,width=20,font=("times new roman",12,"bold"))
        studentid_entry.grid(row=0,column=1,padx=8,pady=5,sticky=W)



# Student name


        studentname_label=Label(class_student_frame,text="Student Name :",font=("times new roman",12,"bold"))
        studentname_label.grid(row=0,column=2,padx=10,sticky=W)
        studentname_entry=ttk.Entry(class_student_frame,textvariable=self.var_name,width=20,font=("times new roman",12,"bold"))
        studentname_entry.grid(row=0,column=3,padx=10,pady=5,sticky=W)


#class division

        studentdid_label=Label(class_student_frame,text="Class Division :",font=("times new roman",12,"bold"))
        studentdid_label.grid(row=1,column=0,padx=8,sticky=W)
     

        div_combo=ttk.Combobox(class_student_frame,textvariable=self.var_div,font=("times new roman",12,"bold"),state="readonly",width=18)
        div_combo["values"]=("A","B","C")
        div_combo.current(0)
        div_combo.grid(row=1,column=1,padx=2,pady=5,sticky=W)



#Roll no


        roll_label=Label(class_student_frame,text="Roll No :",font=("times new roman",12,"bold"))
        roll_label.grid(row=1,column=2,padx=10,sticky=W)
        roll_entry=ttk.Entry(class_student_frame,textvariable=self.var_roll,width=20,font=("times new roman",12,"bold"))
        roll_entry.grid(row=1,column=3,padx=10,pady=5,sticky=W)

#gender

        gender_label=Label(class_student_frame,text="Gender :",font=("times new roman",12,"bold"))
        gender_label.grid(row=2,column=0,padx=10,sticky=W)


        gender_combo=ttk.Combobox(class_student_frame,textvariable=self.var_gender,font=("times new roman",12,"bold"),state="readonly",width=18)
        gender_combo["values"]=("Male","Female","other")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=2,pady=5,sticky=W)


#dob

        dob_label=Label(class_student_frame,text="DOB :",font=("times new roman",12,"bold"))
        dob_label.grid(row=2,column=2,padx=10,sticky=W)
        dob_entry=ttk.Entry(class_student_frame,textvariable=self.var_dob,width=20,font=("times new roman",12,"bold"))
        dob_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)



# EMAIL

        email_label=Label(class_student_frame,text="Email :",font=("times new roman",12,"bold"))
        email_label.grid(row=3,column=0,padx=10,sticky=W)
        self.var_email.set("@gmail.com")

        email_entry=ttk.Entry(class_student_frame,textvariable=self.var_email,width=20,font=("times new roman",12,"bold"))
        email_entry.grid(row=3,column=1,padx=10,pady=5,sticky=W)

  


#Phone no

        pho_label=Label(class_student_frame,text="Phone NO :",font=("times new roman",12,"bold"))
        pho_label.grid(row=3,column=2,padx=10,sticky=W)
        pho_entry=ttk.Entry(class_student_frame,textvariable=self.var_phone,width=20,font=("times new roman",12,"bold"))
        pho_entry.grid(row=3,column=3,padx=10,pady=5,sticky=W)


#ADDRESS

        add_label=Label(class_student_frame,text="Address:",font=("times new roman",12,"bold"))
        add_label.grid(row=4,column=0,padx=10,sticky=W)
        add_entry=ttk.Entry(class_student_frame,textvariable=self.var_address,width=20,font=("times new roman",12,"bold"))
        add_entry.grid(row=4,column=1,padx=10,pady=5,sticky=W)






#Teacher name

        tea_label=Label(class_student_frame,text="Teacher Name :",font=("times new roman",12,"bold"))
        tea_label.grid(row=4,column=2,padx=10,sticky=W)
        tea_entry=ttk.Entry(class_student_frame,textvariable=self.var_teacher,width=20,font=("times new roman",12,"bold"))
        tea_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)

#radio button
  
  
   #     self.var_radio1=StringVar()
    #    radionbtn1=ttk.Radiobutton(class_student_frame,textvariable=self.var_radio1,text="Take Photo Sample",value="yes")
   #     radionbtn1.grid(row=5,column=0)

   #     self.var_radio2=StringVar()
    #    radionbtn1=ttk.Radiobutton(class_student_frame,textvariable=self.var_radio2,text="NO Photo Sample",value="no")
    #    radionbtn1.grid(row=5,column=1)



       
        self.var_radio = StringVar(value="yes")  
        radio_btn1 = ttk.Radiobutton(class_student_frame, text="Take Photo Sample", variable=self.var_radio, value="yes")
        radio_btn1.grid(row=5, column=0)

        radio_btn2 = ttk.Radiobutton(class_student_frame, text="NO Photo Sample", variable=self.var_radio, value="no")
        radio_btn2.grid(row=5, column=1)





#button frame

        btn_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=200,width=715,height=35)

      
        save_btn=Button(btn_frame,text="Save",command=self.add_data,width=19,font=("times new roman",12,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0,)


        update_btn=Button(btn_frame,text="Update",command=self.update_data,width=19,font=("times new roman",12,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1,)


       




        delete_btn=Button(btn_frame,text="Delete",command=self.delete_data,width=19,font=("times new roman",12,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2,)


        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,width=19,font=("times new roman",12,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3,)

   #button frame1
   
        btn_frame1=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame1.place(x=0,y=235,width=715,height=35)

        take_pho_btn=Button(btn_frame1,command=self.generate_dataset,text="Take Photo Sample",width=40,font=("times new roman",12,"bold"),bg="blue",fg="white")
        take_pho_btn.grid(row=0,column=0,)


        up_btn=Button(btn_frame1,text="Update Photo Sample ",width=40,font=("times new roman",12,"bold"),bg="blue",fg="white")
        up_btn.grid(row=0,column=1,)


 #right side

        RIGHT_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Details",
                                font=("times new roman", 12, "bold"))
        RIGHT_frame.place(x=760, y=10, width=750, height=580)



        img_right = Image.open(r"C:\Users\ritik\Desktop\face recognijection\collageimage\four.jpeg")   
        img_right= img_right.resize((720, 130), Image.Resampling.LANCZOS)

        self.photoing_right= ImageTk.PhotoImage(img_right)
        f_lbl = Label(RIGHT_frame, image=self.photoing_right)    
        f_lbl.place(x=5, y=0, width=730, height=130)

# ----------   SEarch frame-------------------

        search_frame = LabelFrame(RIGHT_frame, bd=2, relief=RIDGE, text="Search System",
                                font=("times new roman", 12, "bold"))
        search_frame.place(x=5, y=135, width=730, height=80)


        search_label=Label(search_frame,text="Search By:",font=("times new roman",12,"bold"),bg="red",fg="white")
        search_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)



        search_combo=ttk.Combobox(search_frame,font=("times new roman",12,"bold"),state="readonly")
        search_combo["values"]=("Select ","Roll No","Phone_ No")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)



        search_entry=ttk.Entry(search_frame,width=15,font=("times new roman",12,"bold"))
        search_entry.grid(row=0,column=2,padx=10,pady=5,sticky=W,)



        search_btn=Button(search_frame,text="Search",width=15,font=("times new roman",12,"bold"),bg="blue",fg="white")
        search_btn.grid(row=0,column=3,padx=3)


        showall_btn=Button(search_frame,text="ShowAll ",width=13,font=("times new roman",12,"bold"),bg="blue",fg="white")
        showall_btn.grid(row=0,column=4,padx=3)

#  table frame----------

        table_frame =Frame(RIGHT_frame, bd=2, relief=RIDGE, )
        table_frame.place(x=5, y=210, width=730, height=350)


        Scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        Scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,column=("department","course","year","sem","id","name","div","roll","gender","dob","email","phone","address","teacher","photo",),xscrollcommand=Scroll_x.set,yscrollcommand=Scroll_y.set)
        Scroll_x.pack(side=BOTTOM,fill=X)
        Scroll_y.pack(side=RIGHT,fill=Y)
        Scroll_x.config(command=self.student_table.xview)
        Scroll_y.config(command=self.student_table.yview)
       
       
        self.student_table.heading("department",text="Department")
        self.student_table.heading("course",text="Course")
        self.student_table.heading("year",text="Year")
        self.student_table.heading("sem",text="Samester")
        self.student_table.heading("id",text="StudentId")
        self.student_table.heading("name",text="Name")
        self.student_table.heading("div",text="Division")
        self.student_table.heading("roll",text="Roll NO")
        self.student_table.heading("gender",text="Gender")
        self.student_table.heading("dob",text="DOB")
        self.student_table.heading("email",text="Email")
        self.student_table.heading("phone",text="Phone NO")
        self.student_table.heading("address",text="Address")
        self.student_table.heading("teacher",text="Teacher")
        self.student_table.heading("photo",text="PhotoSampleStatus")
        self.student_table["show"]="headings"
        



        self.student_table.column("department",width=100)
        self.student_table.column("course",width=100)
        self.student_table.column("year",width=100)
        self.student_table.column("sem",width=100)
        self.student_table.column("id",width=100)
        self.student_table.column("name",width=100)
        self.student_table.column("div",width=100)
        self.student_table.column("roll",width=100)
        self.student_table.column("gender",width=100)
        self.student_table.column("dob",width=100)
        self.student_table.column("email",width=100)
        self.student_table.column("phone",width=100)
        self.student_table.column("address",width=100)
        self.student_table.column("teacher",width=100)
        self.student_table.column("photo",width=100)
       


        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()


        


    #-----------function declration------     
    def add_data(self):
         if self.var_department.get() == "Select Department" or self.var_name.get() == "" or self.var_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
  
         elif len(self.var_phone.get()) != 10 or not self.var_phone.get().isdigit():
            messagebox.showerror("Error", "The mobile number must be exactly 10 digits & not alphabets!!!", parent=self.root)
            return
         else:
             try:
                 
                 # अगर user ने सिर्फ नाम लिखा है (जैसे 'ritik'), तो अपने आप '@gmail.com' जुड़ जाए
                 email_text = self.var_email.get()
                 if "@gmail.com" not in email_text:
                    email_text = email_text + "@gmail.com"
                 self.var_email.set(email_text)

                 
                 conn=mysql.connector.connect(host='localhost',username='root',password='Saket@123',database='face_recognition')
                 my_cursor=conn.cursor()
                 my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                 
                                                                                                               self.var_department.get(),
                                                                                                               self.var_course.get(),
                                                                                                               self.var_year.get(),
                                                                                                               self.var_sem.get(),
                                                                                                               self.var_id.get(),
                                                                                                               self.var_name.get(),
                                                                                                               self.var_div.get(),
                                                                                                               self.var_roll.get(),
                                                                                                               self.var_gender.get(),
                                                                                                               self.var_dob.get(),
                                                                                                               self.var_email.get(),
                                                                                                             

                                                                                                               self.var_phone.get(),
                                                                                                               self.var_address.get(),
                                                                                                               self.var_teacher.get(),
                                                                                                               self.var_photo.get(),


                                                                                                              ))


                 conn.commit()
                 self.fetch_data()
                 conn.close()
                 messagebox.showinfo("success","student details has been added Successfully",parent=self.root)                                                                                            

             except Exception as es:
              messagebox.showerror("Error",f"Due TO:{str(es)}",parent=self.root)

            
   
#==========Fatch Data=====================#


    def fetch_data(self):
        conn = mysql.connector.connect(host='localhost', username='root', password='Saket@123', database='face_recognition')
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM student")
        data = my_cursor.fetchall()

        if len(data) != 0:
          self.student_table.delete(*self.student_table.get_children())  # FIXED here
          for i in data:
              self.student_table.insert("", END, values=i)
        conn.commit()
        conn.close()

        
   #========================get cursor=================

    def get_cursor(self,even=" "):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]

        self.var_department.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_sem.set(data[3]),
        self.var_id.set(data[4]),
        self.var_name.set(data[5]),
        self.var_div.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_teacher.set(data[13]),
        self.var_radio.set(data[14]),



#==========update function=================

      
    def update_data(self):
         if self.var_department.get() == "Select Department" or self.var_name.get() == "" or self.var_id.get() == "":
             messagebox.showerror("Error", "All Fields are required", parent=self.root)
         else:
             try:
                 Update=messagebox.askyesno("Update","Do u want to change",parent=self.root)
                 if Update>0:
                     conn=mysql.connector.connect(host='localhost',username='root',password='Saket@123',database='face_recognition')
                     my_cursor=conn.cursor()
                     my_cursor.execute("update student set  Dep=%s,Course=%s,Year=%s,Semester=%s,Name=%s,Division=%s,Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,Teacher=%s,PhotoSemple=%s where Student_id=%s",(
                                                                                                                                                                                              self.var_department.get(),
                                                                                                                                                                                              self.var_course.get(),
                                                                                                                                                                                              self.var_year.get(),
                                                                                                                                                                                              self.var_sem.get(),
                                                                                                                                                                                              self.var_name.get(),
                                                                                                                                                                                              self.var_div.get(),
                                                                                                                                                                                              self.var_roll.get(), 
                                                                                                                                                                                              self.var_gender.get(),
                                                                                                                                                                                              self.var_dob.get(),
                                                                                                                                                                                              self.var_email.get(),
                                                                                                                                                                                              self.var_phone.get(),
                                                                                                                                                                                              self.var_address.get(),
                                                                                                                                                                                              self.var_teacher.get(),
                                                                                                                                                                                              self.var_radio.get(), 
                                                                                                                                                                                              self.var_id.get()


                                                                                                                                                                                         ))
                 else:
                        if not Update:
                             return
                 messagebox.showinfo("Success", "Student details successfully updated", parent=self.root)
                 conn.commit()
                 self.fetch_data()
                 conn.close()
             except Exception as es:
                 messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)







##===============delete function======


    def delete_data(self):
         if self.var_id.get() == "" :
             messagebox.showerror("Error", "student id must be required", parent=self.root)
         else:
             try:
                 delete=messagebox.askyesno("student delete page","do you want to delete this student",parent=self.root)
                 if delete>0:
                      conn = mysql.connector.connect(host='localhost', username='root', password='Saket@123', database='face_recognition')
                      my_cursor = conn.cursor()
                      sql="delete from student where student_id=%s"
                      val=(self.var_id.get(),)
                      my_cursor.execute(sql,val)
                 else:
                     if not delete:
                         return
                     
                 conn.commit()
                 
                 self.fetch_data()    
                 conn.close()
                 messagebox.showerror("delete","successfully deleted student details",parent=self.root)

             except Exception as es:
                   messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
  
#=========reset function===================

    def reset_data(self):
        self.var_department.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_sem.set("Select  Samester")
        self.var_id.set("")
        self.var_name.set("")
        self.var_div.set("Select Division")
        self.var_roll.set("")
        self.var_gender.set("male")
        self.var_dob.set("")
        self.var_email.set("")
       
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio.set("")

     

#===================Genrate data set or take photo sample===============

 
      

    
    def generate_dataset(self):
     if self.var_department.get() == "Select Department" or self.var_name.get() == "" or self.var_id.get() == "":
        messagebox.showerror("Error", "All Fields are required", parent=self.root)
     else:
        try:
            conn = mysql.connector.connect(
                host='localhost',
                username='root',
                password='Saket@123',
                database='face_recognition'
            )
            my_cursor = conn.cursor()

            # Update student info
            my_cursor.execute("""
                UPDATE student SET
                    Dep=%s, Course=%s, Year=%s, Semester=%s, Name=%s, Division=%s,
                    Roll=%s, Gender=%s, Dob=%s, Email=%s, Phone=%s, Address=%s,
                    Teacher=%s, PhotoSemple=%s
                WHERE Student_id=%s
            """, (
                self.var_department.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_sem.get(),
                self.var_name.get(),
                self.var_div.get(),
                self.var_roll.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_email.get(),
                self.var_phone.get(),
                self.var_address.get(),
                self.var_teacher.get(),
                self.var_radio.get(),
                self.var_id.get()
            ))

            conn.commit()
            self.fetch_data()
            self.reset_data()
            conn.close()

            # Start face capture
            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y+h, x:x+w]
                return None

            cap = cv2.VideoCapture(0)
            img_id = 0

            if not cap.isOpened():
                messagebox.showerror("Error", "Webcam not accessible.")
                return

            while True:
                ret, my_frame = cap.read()
                if face_cropped(my_frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_cropped(my_frame), (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = f"data/user.{self.var_id.get()}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                    cv2.imshow("Cropped Face", face)

                if cv2.waitKey(1) == 13 or img_id == 100:
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Generating data sets completed !!!!")

        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = student(root)
    root.mainloop()