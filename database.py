import sqlite3
from pathlib import Path

DB_NAME = "flights.db"

def get_db_path():
    # Store DB in the same directory as this file
    # return Path(__file__).resolve().parent / DB_NAME
    return Path.cwd() / DB_NAME

def get_connection():
    return sqlite3.connect(get_db_path())

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                date TEXT NOT NULL,
                seat_number TEXT NOT NULL
            )
            """
        )
        conn.commit()

def create_reservation(name, flight_number, departure, destination, date, seat_number):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, flight_number, departure, destination, date, seat_number),
        )
        conn.commit()
        return cur.lastrowid

def list_reservations():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, flight_number, departure, destination, date, seat_number FROM reservations ORDER BY id DESC")
        return cur.fetchall()

def get_reservation(res_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, flight_number, departure, destination, date, seat_number FROM reservations WHERE id = ?", (res_id,))
        return cur.fetchone()

def update_reservation(res_id, name, flight_number, departure, destination, date, seat_number):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE reservations
            SET name=?, flight_number=?, departure=?, destination=?, date=?, seat_number=?
            WHERE id=?
            """,
            (name, flight_number, departure, destination, date, seat_number, res_id),
        )
        conn.commit()
        return cur.rowcount

def delete_reservation(res_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE id = ?", (res_id,))
        conn.commit()
        return cur.rowcount
