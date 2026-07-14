# ==========================================================
# AI Powered Face Recognition Attendance System
# Attendance Report Module
# ==========================================================

import streamlit as st
import pandas as pd
from datetime import datetime

from database import *
from utils import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Attendance Report",
    page_icon="📋",
    layout="wide"
)

initialize_database()



# ==========================================================
# CUSTOM CSS (RED TITLE, SKY BLUE BACKGROUND & DARK BLUE SIDEBAR)
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

st.title("📋 Attendance Report")

st.caption(
    "View, Search and Export Attendance Records"
)

st.divider()

# ==========================================================
# LOAD DATA
# ==========================================================

attendance_df = get_attendance()

if attendance_df.empty:

    st.info("No Attendance Records Found")

    st.stop()

# ==========================================================
# FILTER SECTION
# ==========================================================

st.subheader("🔍 Filter Attendance")

col1, col2, col3 = st.columns(3)

with col1:

    date_filter = st.text_input(
        "Date (DD-MM-YYYY)"
    )

with col2:

    department_filter = st.selectbox(

        "Department",

        ["All"] +
        sorted(
            attendance_df["department"].unique().tolist()
        )

    )

with col3:

    status_filter = st.selectbox(

        "Status",

        ["All"] +
        sorted(
            attendance_df["status"].unique().tolist()
        )

    )

filtered_df = attendance_df.copy()

# ==========================================================
# APPLY FILTERS
# ==========================================================

if date_filter:

    filtered_df = filtered_df[
        filtered_df["date"] == date_filter
    ]

if department_filter != "All":

    filtered_df = filtered_df[
        filtered_df["department"] == department_filter
    ]

if status_filter != "All":

    filtered_df = filtered_df[
        filtered_df["status"] == status_filter
    ]

st.divider()

# ==========================================================
# DASHBOARD METRICS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Total Records",
        len(filtered_df)
    )

with c2:

    st.metric(
        "Present",
        len(
            filtered_df[
                filtered_df["status"] == "Present"
            ]
        )
    )

with c3:

    st.metric(
        "Departments",
        filtered_df["department"].nunique()
    )

with c4:

    st.metric(
        "Today's Attendance",
        today_attendance_count()
    )

st.divider()

# ==========================================================
# ATTENDANCE TABLE
# ==========================================================

st.subheader("📄 Attendance Records")

st.dataframe(

    filtered_df,

    use_container_width=True,

    hide_index=True,

    height=550

)

# ==========================================================
# ATTENDANCE ANALYTICS
# ==========================================================

import plotly.express as px

st.divider()

st.subheader("📊 Attendance Analytics")

# ----------------------------------------------------------
# Daily Attendance Chart
# ----------------------------------------------------------

daily_data = (
    filtered_df.groupby("date")
    .size()
    .reset_index(name="Total")
)

if not daily_data.empty:

    fig = px.bar(

        daily_data,

        x="date",

        y="Total",

        title="Daily Attendance",

        text="Total"

    )

    fig.update_layout(

        xaxis_title="Date",

        yaxis_title="Students",

        height=450

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ----------------------------------------------------------
# Department Attendance
# ----------------------------------------------------------

dept_data = (
    filtered_df.groupby("department")
    .size()
    .reset_index(name="Total")
)

if not dept_data.empty:

    fig2 = px.pie(

        dept_data,

        names="department",

        values="Total",

        title="Department-wise Attendance"

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

st.divider()

# ==========================================================
# MONTHLY REPORT
# ==========================================================

st.subheader("📅 Monthly Attendance")

c1, c2 = st.columns(2)

with c1:

    month = st.selectbox(

        "Month",

        list(range(1,13))

    )

with c2:

    year = st.selectbox(

        "Year",

        [

            2025,

            2026,

            2027,

            2028

        ]

    )

if st.button(

    "Generate Monthly Report"

):

    report = monthly_attendance(

        month,

        year

    )

    if report.empty:

        st.warning(

            "No Attendance Found"

        )

    else:

        st.success(

            f"{len(report)} Records Found"

        )

        st.dataframe(

            report,

            use_container_width=True,

            hide_index=True

        )

st.divider()

# ==========================================================
# EXPORT REPORT
# ==========================================================

st.subheader("📥 Export Attendance")

col1, col2 = st.columns(2)

# CSV

csv = filtered_df.to_csv(

    index=False

).encode()

with col1:

    st.download_button(

        "⬇ Download CSV",

        csv,

        file_name="attendance.csv",

        mime="text/csv",

        use_container_width=True

    )

# Excel

excel_file = "attendance_report.xlsx"

filtered_df.to_excel(

    excel_file,

    index=False

)

with open(

    excel_file,

    "rb"

) as f:

    with col2:

        st.download_button(

            "⬇ Download Excel",

            data=f,

            file_name="attendance_report.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )

st.divider()

# ==========================================================
# DELETE RECORD
# ==========================================================

st.subheader("🗑 Delete Attendance Record")

record_id = st.number_input(

    "Attendance Record ID",

    min_value=1,

    step=1

)

if st.button(

    "Delete Record"

):

    delete_attendance(

        record_id

    )

    st.success(

        "Attendance Record Deleted Successfully."

    )

    st.rerun()