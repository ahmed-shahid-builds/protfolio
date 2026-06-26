import sqlite3
from datetime import datetime

DB_PATH = "reservations.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the reservations table if it doesn't exist yet."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            service TEXT NOT NULL,
            message TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_booked_times_for_today():
    """Return a set of time-slot strings that are already taken today (active only)."""
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    rows = conn.execute(
        "SELECT time FROM reservations WHERE date = ? AND status = 'active'",
        (today,)
    ).fetchall()
    conn.close()
    return {row["time"] for row in rows}


def is_slot_taken(date, time):
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM reservations WHERE date = ? AND time = ? AND status = 'active'",
        (date, time)
    ).fetchone()
    conn.close()
    return row is not None


def create_reservation(name, phone, date, time, service, message):
    conn = get_connection()
    conn.execute("""
        INSERT INTO reservations (name, phone, date, time, service, message, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'active', ?)
    """, (name, phone, date, time, service, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def get_all_reservations():
    """Return all reservations, most recent first, for the admin dashboard."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM reservations ORDER BY date DESC, created_at DESC"
    ).fetchall()
    conn.close()
    return rows


def cancel_reservation(reservation_id):
    """Mark a reservation cancelled, which frees up that slot again."""
    conn = get_connection()
    conn.execute(
        "UPDATE reservations SET status = 'cancelled' WHERE id = ?",
        (reservation_id,)
    )
    conn.commit()
    conn.close()
