# backend/database.py

import sqlite3
import csv
from pathlib import Path


DB_PATH = "database/safegate.db"


def create_database():
    """
    Creates the database and logs table if they do not exist.
    """

    Path("database").mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnostic_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL,
            problem TEXT NOT NULL,
            suggestion TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_log(result):
    """
    Saves a diagnostic result dictionary to SQLite.

    Expected format:
    {
        "timestamp": "",
        "message": "",
        "status": "",
        "problem": "",
        "suggestion": ""
    }
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO diagnostic_logs
        (
            timestamp,
            message,
            status,
            problem,
            suggestion
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        result["timestamp"],
        result["message"],
        result["status"],
        result["problem"],
        result["suggestion"]
    ))

    conn.commit()
    conn.close()


def get_logs():
    """
    Returns all logs.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM diagnostic_logs
        ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return logs


def clear_logs():
    """
    Deletes all logs.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM diagnostic_logs")

    conn.commit()
    conn.close()


def export_csv(file_path="exports/diagnostic_logs.csv"):
    """
    Exports logs to CSV.
    """

    Path("exports").mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM diagnostic_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "ID",
            "Timestamp",
            "Message",
            "Status",
            "Problem",
            "Suggestion"
        ])

        writer.writerows(rows)

    return file_path

# ----------------------------
# TESTING
# ----------------------------

if __name__ == "__main__":

    print("Creating database...")
    create_database()
    print("Database created.")

    dummy_results = [
        {
            "timestamp": "2024-01-01 10:00:00",
            "message": "MSG: VOID DETECTED",
            "status": "FAIL",
            "problem": "Broken/Open Connection",
            "suggestion": "Check breadboard track continuity or replace the faulty section."
        },
        {
            "timestamp": "2024-01-01 10:01:00",
            "message": "MSG: HEALTHY TRACK",
            "status": "PASS",
            "problem": "None",
            "suggestion": "No action required."
        },
        {
            "timestamp": "2024-01-01 10:02:00",
            "message": "ALERT: MAIN POWER DISCONNECTED OR REVERSED",
            "status": "CRITICAL",
            "problem": "Power Supply Issue",
            "suggestion": "Check power polarity, supply voltage, and wiring."
        }
    ]

    print("\nSaving dummy logs...")
    for result in dummy_results:
        save_log(result)
    print("Logs saved.")

    print("\nFetching logs from database:")
    logs = get_logs()
    for log in logs:
        print(log)

    print("\nExporting to CSV...")
    path = export_csv()
    print(f"Exported to: {path}")

    print("\nClearing logs...")
    clear_logs()
    print("Logs cleared.")

    print("\nFetching after clear (should be empty):")
    logs = get_logs()
    print(logs)