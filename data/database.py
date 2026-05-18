import sqlite3
from pathlib import Path
# database.py - module quản lý kết nối đến cơ sở dữ liệu SQLite
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "nhatkysuckhoe.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
