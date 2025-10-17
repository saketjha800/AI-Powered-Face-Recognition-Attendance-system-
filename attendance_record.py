from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Record System")
        self.root.geometry("1000x600+100+50")

        # Variables
        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_department = StringVar()
        self.var_status = StringVar(value="Present")

        # Title
        title_lbl = Label(self.root, text="Attendance Record System", font=("times new roman", 30, "bold"), bg="navy", fg="white")
        title_lbl.pack(side=TOP, fill=X)

        # Entry Frame
        frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        frame.place(x=20, y=80, width=960, height=150)

        Label(frame, text="Student ID:", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=5)
        Entry(frame, textvariable=self.var_id, font=("times new roman", 12), width=15).grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Name:", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=2, padx=10, pady=5)
        Entry(frame, textvariable=self.var_name, font=("times new roman", 12), width=15).grid(row=0, column=3, padx=10, pady=5)

        Label(frame, text="Department:", font=("times new roman", 12, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=5)
        Entry(frame, textvariable=self.var_department, font=("times new roman", 12), width=15).grid(row=1, column=1, padx=10, pady=5)

        Label(frame, text="Status:", font=("times new roman", 12, "bold"), bg="white").grid(row=1, column=2, padx=10, pady=5)
        combo_status = ttk.Combobox(frame, textvariable=self.var_status, font=("times new roman", 12), width=12, state="readonly")
        combo_status["values"] = ("Present", "Absent", "Late")
        combo_status.current(0)
        combo_status.grid(row=1, column=3, padx=10, pady=5)

        Button(frame, text="Mark Attendance", command=self.mark_attendance, font=("times new roman", 12, "bold"), bg="green", fg="white", width=15).grid(row=0, column=4, padx=10, pady=5)
        Button(frame, text="Clear", command=self.clear, font=("times new roman", 12, "bold"), bg="red", fg="white", width=10).grid(row=1, column=4, padx=10, pady=5)

        # Table Frame
        table_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=20, y=250, width=960, height=320)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.AttendanceReportTable = ttk.Treeview(table_frame, columns=("id", "name", "department", "date", "time", "status"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        for col in ("id", "name", "department", "date", "time", "status"):
            self.AttendanceReportTable.heading(col, text=col.capitalize())
            self.AttendanceReportTable.column(col, width=150)

        self.AttendanceReportTable["show"] = "headings"
        self.AttendanceReportTable.pack(fill=BOTH, expand=1)

        self.attendance_file = "attendance.csv"
        self.load_attendance()

    def mark_attendance(self):
        if self.var_id.get() == "" or self.var_name.get() == "" or self.var_department.get() == "":
            messagebox.showerror("Error", "All fields are required!")
            return

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        # Prevent duplicate entry for same student on same date
        if self.check_duplicate(self.var_id.get(), date_str):
            messagebox.showwarning("Duplicate Entry", "Attendance already marked for this student today.")
            return

        data = [self.var_id.get(), self.var_name.get(), self.var_department.get(), date_str, time_str, self.var_status.get()]
        with open(self.attendance_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data)

        self.AttendanceReportTable.insert("", END, values=data)
        messagebox.showinfo("Success", "Attendance Marked Successfully!")
        self.clear()

    def check_duplicate(self, student_id, date):
        if not os.path.exists(self.attendance_file):
            return False
        with open(self.attendance_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4 and row[0] == student_id and row[3] == date:
                    return True
        return False

    def load_attendance(self):
        if not os.path.exists(self.attendance_file):
            open(self.attendance_file, "w").close()
        with open(self.attendance_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    self.AttendanceReportTable.insert("", END, values=row)

    def clear(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_department.set("")
        self.var_status.set("Present")


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
