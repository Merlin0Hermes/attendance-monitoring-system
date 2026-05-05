import uuid
from PIL import Image
import sqlite3
from datetime import datetime

# Database name
DB_PATH = "attendance.db"
IMG_DIR = "database/"


# Connect to database
def connect():
    return sqlite3.connect(DB_PATH)


# Create table
def create_table():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            filepath TEXT NOT NULL
        )
        """)



def save_image(name: str, image: Image.Image):
    filename = uuid.uuid4().hex
    filepath = f"{IMG_DIR}/{filename}.png"
    image.save(filepath, "PNG")
    with connect() as conn:
        conn.execute("INSERT INTO images (name, filepath) VALUES (?, ?)", (name.title(), filepath))


def load_name_imgpath():
    with connect() as conn:
        data = conn.execute("SELECT name, filepath FROM images").fetchall()
        return [
            {"name": row[0], "filepath": row[1]}
            for row in data 
        ]

# Mark attendance
def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    try:
        with connect() as conn:
            conn.execute(
                "INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
                (name, date, time)
            )
    except sqlite3.IntegrityError:
        return f"{name} already marked today"


# Get attendance
def get_attendance():
    with connect() as conn:
        data = conn.execute(
            "SELECT name, date, time FROM attendance ORDER BY date DESC, time DESC"
        ).fetchall()

    return [
        {"name": row[0], "date": row[1], "time": row[2]}
        for row in data
    ]


def clear_attendance():
    with connect() as conn:
        conn.execute(
            "DELETE FROM attendance"
        )