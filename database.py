"""
==========================================================
AI Powered Face Recognition Attendance System
Database Module (Version 2.0)
==========================================================
"""

import sqlite3
import logging
from pathlib import Path
from contextlib import contextmanager
import pandas as pd

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DB_DIR = BASE_DIR / "data" / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "attendance.db"

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    filename=LOG_DIR / "database.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

@contextmanager
def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    try:

        yield conn

        conn.commit()

    except Exception:

        conn.rollback()

        raise

    finally:

        conn.close()

# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_database():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""

        PRAGMA foreign_keys = ON;

        """)

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS students(

            student_id TEXT PRIMARY KEY,

            roll_no TEXT UNIQUE,

            name TEXT NOT NULL,

            department TEXT,

            course TEXT,

            year TEXT,

            semester TEXT,

            division TEXT,

            gender TEXT,

            dob TEXT,

            email TEXT,

            phone TEXT,

            address TEXT,

            teacher TEXT,

            photo_sample TEXT DEFAULT 'No',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS attendance(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id TEXT,

            roll_no TEXT,

            name TEXT,

            department TEXT,

            date TEXT,

            time TEXT,

            status TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(student_id)

            REFERENCES students(student_id)

            ON DELETE CASCADE

        )

        """)


 # ==========================================================
# FACE DATASET TABLE
# ==========================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS face_dataset(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id TEXT NOT NULL,

            image_path TEXT NOT NULL,

            image_no INTEGER,

             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(student_id)
            REFERENCES students(student_id)
            ON DELETE CASCADE

        )
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_face_student
        ON face_dataset(student_id)
        """)

        # ==========================================================
# TRAINED MODEL TABLE
# ==========================================================

        cursor.execute("""
         CREATE TABLE IF NOT EXISTS trained_models(

         id INTEGER PRIMARY KEY AUTOINCREMENT,

         model_name TEXT,

          model_path TEXT,

         algorithm TEXT,

         accuracy REAL,

         trained_images INTEGER,

         trained_students INTEGER,

         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ==========================================================
# SYSTEM LOGS
# ==========================================================

        cursor.execute("""
           CREATE TABLE IF NOT EXISTS system_logs(

          id INTEGER PRIMARY KEY AUTOINCREMENT,

          module TEXT,

          level TEXT,

          message TEXT,

          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)


# ==========================================================
# SAVE SYSTEM LOG
# ==========================================================

        def save_log(module, level, message):

            with get_connection() as conn:

                conn.execute(

                    """

                   INSERT INTO system_logs(

                     module,

                     level,

                      message

                )

              VALUES(?,?,?)

               """,

              (

                module,

                level,

                message

            )

        )

           # ==========================================================
# SAVE FACE DATASET
# ==========================================================

        def save_dataset_image(
           student_id,
           image_path,
          image_no
       ):

         with get_connection() as conn:

           conn.execute(

            """

            INSERT INTO face_dataset(

                student_id,

                image_path,

                image_no

            )

            VALUES(

                ?,?,?

            )

            """,

            (

                student_id,

                image_path,

                image_no

            )

        )

        def dataset_image_count():

             with get_connection() as conn:

              cursor = conn.cursor()

              cursor.execute(

                 """

            SELECT COUNT(*)

            FROM face_dataset

            """

        )

      #  return cursor.fetchone()[0]



        def save_model(

            model_name,

            model_path,

            algorithm,

            accuracy,

            images,

           students

         ):

          with get_connection() as conn:

            conn.execute(

             """

            INSERT INTO trained_models(

                model_name,

                model_path,

                algorithm,

                accuracy,

                trained_images,

                trained_students

            )

            VALUES(

                ?,?,?,?,?,?

            )

            """,

            (

                model_name,

                model_path,

                algorithm,

                accuracy,

                images,

                students

            )

        )


        def latest_model():

           with get_connection() as conn:

             return pd.read_sql_query(

              """

            SELECT *

            FROM trained_models

            ORDER BY id DESC

            LIMIT 1

            """,

            conn

        )












        # Performance Indexes

        cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_student_name

        ON students(name)

        """)

        cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_roll

        ON students(roll_no)

        """)

        cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_attendance_date

        ON attendance(date)

        """)

        logging.info("Database Initialized")

# ==========================================================
# VALIDATION
# ==========================================================

def student_exists(student_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(

            "SELECT 1 FROM students WHERE student_id=?",

            (student_id,)

        )

        return cursor.fetchone() is not None

def roll_exists(roll_no):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(

            "SELECT 1 FROM students WHERE roll_no=?",

            (roll_no,)

        )

        return cursor.fetchone() is not None

# ==========================================================
# DASHBOARD COUNTS
# ==========================================================

def total_students():

    with get_connection() as conn:

        return pd.read_sql_query(

            "SELECT COUNT(*) AS total FROM students",

            conn

        ).iloc[0]["total"]

def total_attendance():

    with get_connection() as conn:

        return pd.read_sql_query(

            "SELECT COUNT(*) AS total FROM attendance",

            conn

        ).iloc[0]["total"]

# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

initialize_database()


    # ==========================================================
# SAVE SYSTEM LOG
# ==========================================================

def save_log(module, level, message):

    with get_connection() as conn:

        conn.execute(

            """

            INSERT INTO system_logs(

                module,

                level,

                message

            )

            VALUES(?,?,?)

            """,

            (

                module,

                level,

                message

            )

        )





# ==========================================================
# SAVE FACE DATASET
# ==========================================================

def save_dataset_image(student_id, image_path, image_no):

    with get_connection() as conn:

        conn.execute(
            """
            INSERT INTO face_dataset(
                student_id,
                image_path,
                image_no
            )
            VALUES(?,?,?)
            """,
            (
                student_id,
                image_path,
                image_no
            )
        )


# ==========================================================
# DATASET IMAGE COUNT
# ==========================================================

def dataset_image_count():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM face_dataset
        """)

        return cursor.fetchone()[0]

def save_model(

    model_name,

    model_path,

    algorithm,

    accuracy,

    images,

    students

):

    with get_connection() as conn:

        conn.execute(

            """

            INSERT INTO trained_models(

                model_name,

                model_path,

                algorithm,

                accuracy,

                trained_images,

                trained_students

            )

            VALUES(

                ?,?,?,?,?,?

            )

            """,

            (

                model_name,

                model_path,

                algorithm,

                accuracy,

                images,

                students

            )

        )





def latest_model():

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM trained_models

            ORDER BY id DESC

            LIMIT 1

            """,

            conn

        )














# ==========================================================
# STUDENT CRUD OPERATIONS
# ==========================================================

def add_student(student_data):
    """
    student_data =
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
        dob,
        email,
        phone,
        address,
        teacher,
        photo_sample
    )
    """

    student_id = student_data[0]
    roll_no = student_data[1]

    if student_exists(student_id):
        raise ValueError(
            f"Student ID '{student_id}' already exists."
        )

    if roll_exists(roll_no):
        raise ValueError(
            f"Roll Number '{roll_no}' already exists."
        )

    with get_connection() as conn:

        conn.execute(
            """
            INSERT INTO students(
                student_id,
                roll_no,
                name,
                department,
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
                photo_sample
            )

            VALUES(
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?
            )
            """,
            student_data
        )

    logging.info(
        f"Student Added : {student_id}"
    )


# ==========================================================
# UPDATE STUDENT
# ==========================================================

def update_student(student_data):

    student_id = student_data[0]

    if not student_exists(student_id):
        raise ValueError(
            "Student does not exist."
        )

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE students

            SET

            roll_no=?,
            name=?,
            department=?,
            course=?,
            year=?,
            semester=?,
            division=?,
            gender=?,
            dob=?,
            email=?,
            phone=?,
            address=?,
            teacher=?,
            photo_sample=?

            WHERE student_id=?

            """,

            (

                student_data[1],
                student_data[2],
                student_data[3],
                student_data[4],
                student_data[5],
                student_data[6],
                student_data[7],
                student_data[8],
                student_data[9],
                student_data[10],
                student_data[11],
                student_data[12],
                student_data[13],
                student_data[14],

                student_id

            )

        )

    logging.info(
        f"Student Updated : {student_id}"
    )


# ==========================================================
# DELETE STUDENT
# ==========================================================

def delete_student(student_id):

    if not student_exists(student_id):
        return False

    with get_connection() as conn:

        conn.execute(

            "DELETE FROM students WHERE student_id=?",

            (student_id,)

        )

    logging.info(

        f"Student Deleted : {student_id}"

    )

    return True


# ==========================================================
# SEARCH STUDENT
# ==========================================================

def search_student(student_id):

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM students

            WHERE student_id=?

            """,

            conn,

            params=(student_id,)

        )


# ==========================================================
# SEARCH BY NAME
# ==========================================================

def search_student_name(name):

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM students

            WHERE name LIKE ?

            ORDER BY name

            """,

            conn,

            params=(f"%{name}%",)

        )


# ==========================================================
# SEARCH BY ROLL NUMBER
# ==========================================================

def search_roll(roll_no):

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM students

            WHERE roll_no=?

            """,

            conn,

            params=(roll_no,)

        )


# ==========================================================
# GET ALL STUDENTS
# ==========================================================

def get_all_students():

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM students

            ORDER BY name

            """,

            conn

        )


# ==========================================================
# DEPARTMENT FILTER
# ==========================================================

def students_by_department(department):

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM students

            WHERE department=?

            ORDER BY name

            """,

            conn,

            params=(department,)

        )


# ==========================================================
# YEAR FILTER
# ==========================================================

def students_by_year(year):

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM students

            WHERE year=?

            ORDER BY name

            """,

            conn,

            params=(year,)

        )
    

    # ==========================================================
# ATTENDANCE MANAGEMENT
# ==========================================================

from datetime import datetime


# ----------------------------------------------------------
# Mark Attendance
# ----------------------------------------------------------

def mark_attendance(student_id,
                    roll_no,
                    name,
                    department,
                    status="Present"):

    today = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")

    with get_connection() as conn:

        cursor = conn.cursor()

        # Prevent duplicate attendance
        cursor.execute("""

        SELECT id

        FROM attendance

        WHERE student_id=?
        AND date=?

        """,

        (student_id, today))

        if cursor.fetchone():

            return False

        cursor.execute("""

        INSERT INTO attendance(

            student_id,

            roll_no,

            name,

            department,

            date,

            time,

            status

        )

        VALUES(

            ?,?,?,?,?,?,?

        )

        """,

        (

            student_id,

            roll_no,

            name,

            department,

            today,

            current_time,

            status

        ))

    logging.info(f"Attendance Marked : {student_id}")

    return True


# ==========================================================
# TODAY ATTENDANCE
# ==========================================================

def today_attendance():

    today = datetime.now().strftime("%d-%m-%Y")

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM attendance

            WHERE date=?

            ORDER BY time DESC

            """,

            conn,

            params=(today,)

        )


# ==========================================================
# ATTENDANCE BY DATE
# ==========================================================

def attendance_by_date(date):

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM attendance

            WHERE date=?

            ORDER BY time DESC

            """,

            conn,

            params=(date,)

        )


# ==========================================================
# STUDENT ATTENDANCE HISTORY
# ==========================================================

def student_attendance(student_id):

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM attendance

            WHERE student_id=?

            ORDER BY date DESC,time DESC

            """,

            conn,

            params=(student_id,)

        )


# ==========================================================
# ALL ATTENDANCE
# ==========================================================

def get_attendance():

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM attendance

            ORDER BY date DESC,time DESC

            """,

            conn

        )


# ==========================================================
# DELETE ATTENDANCE
# ==========================================================

def delete_attendance(record_id):

    with get_connection() as conn:

        conn.execute(

            """

            DELETE FROM attendance

            WHERE id=?

            """,

            (record_id,)

        )

    logging.info(f"Attendance Deleted : {record_id}")


# ==========================================================
# MONTHLY ATTENDANCE
# ==========================================================

def monthly_attendance(month, year):

    pattern = f"%-{month:02d}-{year}"

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT *

            FROM attendance

            WHERE date LIKE ?

            ORDER BY date DESC

            """,

            conn,

            params=(pattern,)

        )


# ==========================================================
# DASHBOARD ANALYTICS
# ==========================================================

def department_statistics():

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT

                department,

                COUNT(*) AS Total

            FROM students

            GROUP BY department

            ORDER BY department

            """,

            conn

        )


def attendance_statistics():

    with get_connection() as conn:

        return pd.read_sql_query(

            """

            SELECT

                date,

                COUNT(*) AS Total

            FROM attendance

            GROUP BY date

            ORDER BY date

            """,

            conn

        )


# ==========================================================
# TODAY COUNT
# ==========================================================

def today_attendance_count():

    today = datetime.now().strftime("%d-%m-%Y")

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT COUNT(*)

            FROM attendance

            WHERE date=?

            """,

            (today,)

        )

        return cursor.fetchone()[0]