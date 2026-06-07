import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from backend.database import (
    create_database,
    save_log,
    get_logs,
    clear_logs,
    export_csv
)

from backend.diagnostic_engine import process_message
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

root.title("Safe-Gate Dashboard")
root.geometry("850x700")

# Title
title_label = tk.Label(
    root,
    text="SAFE-GATE DIAGNOSTIC DASHBOARD",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=15)

# Status Section
status_label = tk.Label(
    root,
    text="Status: Disconnected",
    font=("Arial", 12),
    fg="red"
)
status_label.pack(pady=10)

# Create database automatically
create_database()

# Connect Button
def connect_device():
    status_label.config(
        text="Status: Connected",
        fg="green"
    )

connect_button = tk.Button(
    root,
    text="Connect Device",
    font=("Arial", 12),
    width=20,
    command=connect_device
)

connect_button.pack(pady=10)

def run_diagnosis():

    selected_message = diagnosis_var.get()

    result = process_message(selected_message)

    if result["status"] == "PASS":

        result_label.config(
            text="🟢 PASS",
            fg="green"
        )

    elif result["status"] == "FAIL":

        result_label.config(
            text="🔴 FAIL",
            fg="red"
        )

    elif result["status"] == "CRITICAL":

        result_label.config(
            text="🚨 CRITICAL",
            fg="red"
        )

    else:

        result_label.config(
            text=result["status"],
            fg="black"
        )

    problem_label.config(
        text=f"Problem: {result['problem']}"
    )

    suggestion_label.config(
        text=f"Suggestion: {result['suggestion']}"
    )

    save_log(result)

def reset_dashboard():

    status_label.config(text="Status: Disconnected")

    result_label.config(text="Result: Waiting...")

    problem_label.config(text="Problem: None")

    suggestion_label.config(
        text="Suggestion: Waiting for diagnosis"
    )


def export_logs():

    path = export_csv()

    messagebox.showinfo(
        "Export Complete",
        f"Logs exported to:\n{path}"
    )


def clear_all_logs():

    clear_logs()

    messagebox.showinfo(
        "Logs Cleared",
        "All logs removed successfully."
    )


def view_logs():

    logs = get_logs()

    log_window = tk.Toplevel(root)

    log_window.title("Diagnostic Logs")

    log_window.geometry("900x400")

    text_area = tk.Text(log_window)

    text_area.pack(fill="both", expand=True)

    for log in logs:

       text_area.insert(
          tk.END,
          f"""
Timestamp: {log[1]}
Status: {log[3]}
Problem: {log[4]}
Suggestion: {log[5]}

----------------------------------------

"""
    ) 
# Run Diagnosis Button
diagnosis_label = tk.Label(
    root,
    text="Select Diagnostic Scenario",
    font=("Arial", 11, "bold")
)

diagnosis_label.pack(pady=5)
# Diagnosis Options

diagnosis_var = tk.StringVar()

diagnosis_var.set("MSG: HEALTHY TRACK")

diagnosis_options = [
    "MSG: HEALTHY TRACK",
    "MSG: VOID DETECTED",
    "MSG: COMPONENT OK / HEALTHY RESISTOR",
    "ALERT: MAIN POWER DISCONNECTED OR REVERSED",
    "--- SAFE-GATE SYSTEM ONLINE ---"
]

diagnosis_menu = tk.OptionMenu(
    root,
    diagnosis_var,
    *diagnosis_options
)

diagnosis_menu.pack(pady=10)

diagnosis_button = tk.Button(
    root,
    text="Run Diagnosis",
    font=("Arial", 12),
    width=20,
    command=run_diagnosis
)
diagnosis_button.pack(pady=10) 

result_heading = tk.Label(
    root,
    text="Diagnostic Result:",
    font=("Arial", 11, "bold")
)

result_heading.pack(pady=(10,5))
# Result Section
result_label = tk.Label(
    root,
    text="Result: Waiting...",
    font=("Arial", 12)
)
result_label.pack(pady=10)

problem_label = tk.Label(
    root,
    text="Problem: None",
    font=("Arial", 12)
)
problem_label.pack(pady=5)

suggestion_label = tk.Label(
    root,
    text="Suggestion: Waiting for diagnosis",
    font=("Arial", 12)
)
suggestion_label.pack(pady=5)

view_button = tk.Button(
    root,
    text="View Logs",
    font=("Arial", 11),
    width=15,
    command=view_logs
)

view_button.pack(pady=5)


export_button = tk.Button(
    root,
    text="Export CSV",
    font=("Arial", 11),
    width=15,
    command=export_logs
)

export_button.pack(pady=5)


clear_button = tk.Button(
    root,
    text="Clear Logs",
    font=("Arial", 11),
    width=15,
    command=clear_all_logs
)

clear_button.pack(pady=5)


reset_button = tk.Button(
    root,
    text="Reset",
    font=("Arial", 11),
    width=15,
    command=reset_dashboard
)

reset_button.pack(pady=5)

root.mainloop()
