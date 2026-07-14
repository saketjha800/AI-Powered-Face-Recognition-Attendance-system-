# ==========================================================
# AI Powered Face Recognition Attendance System
# Student Details Module
# pages/1_Student_Details.py
# ==========================================================

import streamlit as st
import pandas as pd
from database import *
from utils import *

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Student Details",
    page_icon="🎓",
    layout="wide"
)

initialize_database()

# ----------------------------------------------------------
# Custom CSS
# ----------------------------------------------------------

st.markdown("""
<style>

/* 🌌 पूरे मुख्य पेज का बैकग्राउंड */
.stApp, .main {
    background-color: #E0E0E0 !important; 
}

/* 🔵 साइडबार का बैकग्राउंड... */
[data-testid="stSidebar"] {
    background-color: #E0F7FA !important; 
}

/* 🎨 मुख्य हेडिंग का कलर */
.main h1, h1 span {
    color:   #B71C1C !important;
}

/* ==========================================================
   🚨 क्लिक करने की समस्या को फिक्स करने का कोड (Z-INDEX & POINTER EVENTS)
   ========================================================== */

/* ⚙️ हेडर बार की क्लिक-थ्रू सेटिंग्स ताकि इसके नीचे के बटन क्लिक हो सकें */
div[data-testid="stHeader"], header {
    background-color: #1A237E !important;
    display: flex !important;
    flex-direction: row !important;
    justify-content: space-between !important; 
    align-items: center !important;
    height: 3.5rem !important;
    pointer-events: none !important; /* 👈 हेडर खुद माउस क्लिक नहीं रोकेगा */
    z-index: 999 !important;
}

/* 📄 पेजों की लिस्ट - इसे सबसे ऊपर (Front) लाएंगे ताकि क्लिक हो सके */
div[data-testid="stSidebarNav"] {
    position: fixed !important;
    top: 8px !important;
    left: 350px !important; 
    z-index: 999999 !important; /* 👈 सबसे ऊपर की परत */
    background: transparent !important;
    width: auto !important;
    pointer-events: auto !important; /* 👈 इसपर माउस क्लिक काम करेगा */
}

/* पेजों के अंदर के <ul> (List) को हॉरिजॉन्टल अरेंज करना */
div[data-testid="stSidebarNav"] ul {
    display: flex !important;
    flex-direction: row !important; 
    gap: 15px !important;          
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
    pointer-events: auto !important;
}

/* पेजों के लिंक्स और बटन्स */
div[data-testid="stSidebarNav"] ul li {
    padding: 5px 10px !important;
    background-color: #F8F9FA !important;
    border-radius: 5px !important;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.05) !important;
    pointer-events: auto !important;
}

/* बटन के अंदर के टेक्स्ट/लिंक को भी क्लिकेबल बनाना */
div[data-testid="stSidebarNav"] ul li a {
    pointer-events: auto !important;
    display: block !important;
}

/* 🔘 Deploy बटन को टॉप-राइट हेडर लाइन में फिक्स करना */
div[data-testid="stAppDeployButton"], 
div[data-testid="stActionButton"],
.stAppDeployButton {
    position: fixed !important;
    top: 10px !important;
    right: 70px !important; 
    z-index: 999999 !important; /* 👈 डिप्लॉय बटन को भी ऊपर लाया */
    pointer-events: auto !important;
}

/* 🔘 Deploy बटन का ग्रे कलर स्टाइल */
div[data-testid="stAppDeployButton"] button,
.stAppDeployButton button {
    background-color: #757575 !important; 
    color: #FFFFFF !important;            
    border: 1px solid #616161 !important;
    border-radius: 6px !important;
}

/* 🔘 3-Dots (Menu Button) */
div[data-testid="stToolbar"] {
    position: fixed !important;
    top: 10px !important;
    right: 15px !important;
    z-index: 999999 !important;
    pointer-events: auto !important;
}

/* 🪟 साइडबार के टॉप गैप को हटाना */
div[data-testid="stSidebarUserContent"] {
    padding-top: 0rem !important;
}

/* ========================================================== */

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


# ----------------------------------------------------------
# Header
# ----------------------------------------------------------

st.title("👨‍🎓 Student Management")

st.caption(
    "Add, Update, Search and Delete Student Records"
)

st.divider()

# ----------------------------------------------------------
# Student Form
# ----------------------------------------------------------

with st.form("student_form"):

    c1, c2 = st.columns(2)

    with c1:

        student_id = st.text_input(
            "Student ID"
        )

        roll_no = st.text_input(
            "Roll Number"
        )

        name = st.text_input(
            "Student Name"
        )

        department = st.selectbox(

            "Department",

            [

                "CSE",

                "IT",

                "ECE",

                "EEE",

                "Civil",

                "Mechanical"

            ]

        )

        course = st.text_input(
            "Course"
        )

        year = st.selectbox(

            "Year",

            [

                "1",

                "2",

                "3",

                "4"

            ]

        )

        semester = st.selectbox(

            "Semester",

            [

                "1","2","3","4",

                "5","6","7","8"

            ]

        )

    with c2:

        division = st.text_input(
            "Division"
        )

        gender = st.selectbox(

            "Gender",

            [

                "Male",

                "Female",

                "Other"

            ]

        )

        dob = st.date_input(
            "Date of Birth"
        )

        email = st.text_input(
            "Email"
        )

        phone = st.text_input(
            "Phone"
        )

        address = st.text_area(
            "Address"
        )

        teacher = st.text_input(
            "Teacher Name"
        )

    submitted = st.form_submit_button(
        "💾 Save Student"
    )

# ----------------------------------------------------------
# Save Student
# ----------------------------------------------------------

if submitted:

    if student_id.strip() == "":

        st.error(
            "Student ID Required"
        )

    elif name.strip() == "":

        st.error(
            "Student Name Required"
        )

    else:

        try:

            add_student(

                (

                    student_id,

                    roll_no,

                    name,

                    department,

                    course,

                    year,

                    semester,

                    division,

                    gender,

                    str(dob),

                    email,

                    phone,

                    address,

                    teacher,

                    "No"

                )

            )

            st.success(
                "Student Added Successfully"
            )

        except Exception as e:

            st.error(e)

st.divider()

# ==========================================================
# SEARCH STUDENT
# ==========================================================

st.subheader("🔍 Search Student")

col1, col2 = st.columns([3,1])

with col1:
    search_id = st.text_input(
        "Enter Student ID",
        key="search_student"
    )

with col2:
    search_btn = st.button(
        "Search Student",
        use_container_width=True
    )

if search_btn:

    if search_id.strip() == "":

        st.warning("Enter Student ID")

    else:

        student = search_student(search_id)

        if student.empty:

            st.error("Student Not Found")

        else:

            st.success("Student Found")

            st.dataframe(
                student,
                use_container_width=True,
                hide_index=True
            )

st.divider()

# ==========================================================
# UPDATE STUDENT
# ==========================================================

st.subheader("✏ Update Student")

update_id = st.text_input(
    "Student ID To Update"
)

if st.button("Load Student"):

    df = search_student(update_id)

    if df.empty:

        st.error("Student Not Found")

    else:

        st.session_state.student = df.iloc[0].to_dict()

if "student" in st.session_state:

    s = st.session_state.student

    with st.form("update_form"):

        roll = st.text_input(
            "Roll No",
            value=s["roll_no"]
        )

        name = st.text_input(
            "Name",
            value=s["name"]
        )

        dept = st.text_input(
            "Department",
            value=s["department"]
        )

        course = st.text_input(
            "Course",
            value=s["course"]
        )

        year = st.text_input(
            "Year",
            value=s["year"]
        )

        semester = st.text_input(
            "Semester",
            value=s["semester"]
        )

        division = st.text_input(
            "Division",
            value=s["division"]
        )

        gender = st.text_input(
            "Gender",
            value=s["gender"]
        )

        dob = st.text_input(
            "DOB",
            value=s["dob"]
        )

        email = st.text_input(
            "Email",
            value=s["email"]
        )

        phone = st.text_input(
            "Phone",
            value=s["phone"]
        )

        address = st.text_area(
            "Address",
            value=s["address"]
        )

        teacher = st.text_input(
            "Teacher",
            value=s["teacher"]
        )

        photo = st.text_input(
            "Photo Sample",
            value=s["photo_sample"]
        )

        if st.form_submit_button(
            "Update Student"
        ):

            update_student(

                (

                    update_id,

                    roll,

                    name,

                    dept,

                    course,

                    year,

                    semester,

                    division,

                    gender,

                    dob,

                    email,

                    phone,

                    address,

                    teacher,

                    photo

                )

            )

            st.success(
                "Student Updated Successfully"
            )

            del st.session_state.student

st.divider()

# ==========================================================
# DELETE STUDENT
# ==========================================================

st.subheader("❌ Delete Student")

delete_id = st.text_input(
    "Student ID",
    key="delete_student"
)

if st.button(
    "Delete Student"
):

    if delete_id.strip()=="":

        st.warning("Enter Student ID")

    else:

        delete_student(delete_id)

        st.success("Student Deleted Successfully")

st.divider()
# ==========================================================
# VIEW ALL STUDENTS
# ==========================================================

st.subheader("📋 Student Records")

students_df = get_all_students()

if students_df.empty:

    st.info("No student records found.")

else:

    # ------------------------------------------------------
    # FILTERS
    # ------------------------------------------------------

    f1, f2, f3 = st.columns(3)

    with f1:

        dept_filter = st.selectbox(

            "Department",

            ["All"] + sorted(
                students_df["department"].dropna().unique().tolist()
            )

        )

    with f2:

        year_filter = st.selectbox(

            "Year",

            ["All"] + sorted(
                students_df["year"].astype(str).unique().tolist()
            )

        )

    with f3:

        semester_filter = st.selectbox(

            "Semester",

            ["All"] + sorted(
                students_df["semester"].astype(str).unique().tolist()
            )

        )

    # ------------------------------------------------------
    # APPLY FILTER
    # ------------------------------------------------------

    filtered = students_df.copy()

    if dept_filter != "All":

        filtered = filtered[
            filtered["department"] == dept_filter
        ]

    if year_filter != "All":

        filtered = filtered[
            filtered["year"].astype(str) == year_filter
        ]

    if semester_filter != "All":

        filtered = filtered[
            filtered["semester"].astype(str) == semester_filter
        ]

    st.success(f"Showing {len(filtered)} Students")

    st.dataframe(

        filtered,

        use_container_width=True,

        hide_index=True,

        height=500

    )

st.divider()

# ==========================================================
# STUDENT STATISTICS
# ==========================================================

st.subheader("📊 Student Statistics")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(

        "Total Students",

        len(students_df)

    )

with c2:

    st.metric(

        "Departments",

        students_df["department"].nunique()

    )

with c3:

    st.metric(

        "Courses",

        students_df["course"].nunique()

    )

st.divider()

# ==========================================================
# EXPORT (FIXED: NameError Resolved)
# ==========================================================

st.subheader("📥 Export Student Records")

col1, col2 = st.columns(2)

with col1:
    # CSV एक्सपोर्ट (यह पहले से सही था)
    csv = students_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇ Download CSV",
        data=csv,
        file_name="students.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    try:
        import io
        
        # 💡 फ़िक्स: बिना किसी बाहरी फ़ंक्शन के सीधे Pandas DataFrame को Excel (Bytes) में बदलना
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            students_df.to_excel(writer, index=False, sheet_name='Students')
        
        excel_data = buffer.getvalue()

        st.download_button(
            "⬇ Download Excel",
            data=excel_data,
            file_name="students.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Excel Export Error: {e}")