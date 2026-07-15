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
# CUSTOM CSS (FORCED NAVBAR FOR DEPLOYED LINK)
# ==========================================================
st.markdown("""
<style>

/* 🌌 पूरे मुख्य पेज का बैकग्राउंड और लेआउट */
.stApp {
    background-color: #E0E0E0 !important; 
}

.stMain, .main, [data-testid="stMain"] {
    pointer-events: auto !important;
    display: block !important;
}

/* 🔵 साइडबार का बैकग्राउंड */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important; 
}

/* 🎨 मुख्य हेडिंग का कलर */
.main h1, h1 span {
    color: #1A237E !important; 
}

/* ==========================================================
   🚨 फिक्स्ड टॉप बार और बटन्स (3-DOTS REMOVED)
   ========================================================== */

/* ⚙️ सफेद हेडर बार */
div[data-testid="stHeader"], header {
    background-color: #E3F2FD !important; 
    height: 3.8rem !important; 
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    pointer-events: none !important; 
    z-index: 99999 !important; 
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1) !important; 
}

/* 📄 हॉरिजॉन्टल नेविगेशन बटन्स - अब इन्हें थोड़ा और दाईं तरफ (right: 120px) खिसका दिया है क्योंकि 3-dots हट गया है */
div[data-testid="stSidebarNav"] {
    position: fixed !important; 
    top: 14px !important;       
    right: 125px !important;    /* 👈 Deploy बटन के ठीक बाईं तरफ परफेक्ट स्पेसिंग */
    left: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    width: auto !important;
    z-index: 100000 !important;
    pointer-events: auto !important; 
}

/* पेजों की लिस्ट को एक लाइन में करना */
div[data-testid="stSidebarNav"] ul {
    display: flex !important;
    flex-direction: row !important; 
    gap: 8px !important; 
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* बटन्स का सुंदर लेआउट */
div[data-testid="stSidebarNav"] ul li {
    padding: 5px 12px !important;
    background-color: #F1F3F4 !important; 
    border: 1px solid #DADCE0 !important;
    border-radius: 4px !important;
    white-space: nowrap !important; 
}

div[data-testid="stSidebarNav"] ul li a span {
    color: #202124 !important; 
    font-weight: 500 !important;
}

/* 🔘 Deploy बटन की सेटिंग्स - इसे अब कोने के पास (right: 20px) सेट किया है */
div[data-testid="stAppDeployButton"], 
div[data-testid="stActionButton"],
.stAppDeployButton {
    position: fixed !important;
    top: 14px !important;
    right: 20px !important; /* 👈 बिल्कुल कोने में फिक्स */
    left: auto !important;
    z-index: 100000 !important;
    pointer-events: auto !important;
}

div[data-testid="stAppDeployButton"] button,
.stAppDeployButton button {
    background-color: #1A237E !important; 
    color: #E3F2FD !important;            
    border: none !important;
    border-radius: 4px !important;
    font-weight: bold !important;
    height: 32px !important;
}

/* 🔘 3-Dots (Menu Button) को पूरी तरह छुपाया */
div[data-testid="stToolbar"] {
    display: none !important; /* 👈 3-dots अब नहीं दिखेगा */
}

/* 📦 मुख्य कंटेंट का स्पेसिंग */
.block-container {
    padding-top: 5rem !important; 
    padding-bottom: 1rem !important;
    pointer-events: auto !important; 
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
        ["All"] + sorted(attendance_df["department"].unique().tolist())
    )

with col3:
    status_filter = st.selectbox(
        "Status",
        ["All"] + sorted(attendance_df["status"].unique().tolist())
    )

filtered_df = attendance_df.copy()

# ==========================================================
# APPLY FILTERS
# ==========================================================

if date_filter:
    filtered_df = filtered_df[filtered_df["date"] == date_filter]

if department_filter != "All":
    filtered_df = filtered_df[filtered_df["department"] == department_filter]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

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
        len(filtered_df[filtered_df["status"] == "Present"])
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

# Daily Attendance Chart
daily_data = filtered_df.groupby("date").size().reset_index(name="Total")

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

# Department Attendance
dept_data = filtered_df.groupby("department").size().reset_index(name="Total")

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
        list(range(1, 13))
    )

with c2:
    year = st.selectbox(
        "Year",
        [2025, 2026, 2027, 2028]
    )

if st.button("Generate Monthly Report"):
    report = monthly_attendance(month, year)
    if report.empty:
        st.warning("No Attendance Found")
    else:
        st.success(f"{len(report)} Records Found")
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
csv = filtered_df.to_csv(index=False).encode()

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
filtered_df.to_excel(excel_file, index=False)

with open(excel_file, "rb") as f:
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

if st.button("Delete Record"):
    delete_attendance(record_id)
    st.success("Attendance Record Deleted Successfully.")
    st.rerun()

# ==========================================================
# BOTTOM NAVIGATION (DEVELOPER PAGE BUTTON)
# ==========================================================
st.write("---")

if st.button("📊 DEVELOPER PAGE ओपन करें", use_container_width=True):
    st.switch_page("pages/Developer.py")