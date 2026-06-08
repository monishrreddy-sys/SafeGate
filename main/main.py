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
from backend.serial_handler import SerialHandler
import tkinter as tk
from tkinter import messagebox

# Create database automatically
create_database()
serial_handler = SerialHandler()
root = tk.Tk()
root.title("Safe-Gate Dashboard")
root.geometry("900x700")  
root.config(bg="#f4f6f9")

# =====================================================================
# EVENT FUNCTIONS
# =====================================================================

def connect_device():

    ports = serial_handler.list_available_ports()

    if not ports:

        messagebox.showerror(
            "Connection Error",
            "No Arduino detected."
        )

        return

    port = "COM9"

    if serial_handler.connect(port):

        status_label.config(
            text=f"Status: Connected ({port})",
            fg="#27ae60"
        )

        diagnosis_button.config(state="normal")

    else:

        messagebox.showerror(
            "Connection Error",
            f"Could not connect to {port}"
        )
def run_diagnosis():

    message = serial_handler.read_message()

    if not message:

        messagebox.showwarning(
            "No Data",
            "No Arduino data received."
        )

        return

    message_label.config(text=message)

    result = process_message(message)

    if result["status"] == "PASS":
        result_label.config(
            text="🟢 PASS",
            fg="#27ae60",
            bg="#e8f8f5"
        )

    elif result["status"] == "FAIL":
        result_label.config(
            text="🔴 FAIL",
            fg="#c0392b",
            bg="#f9ebea"
        )

    elif result["status"] == "CRITICAL":
        result_label.config(
            text="🚨 CRITICAL",
            fg="#ffffff",
            bg="#922b21"
        )

    else:
        result_label.config(
            text=result["status"],
            fg="#2c3e50",
            bg="#f8f9fa"
        )

    problem_label.config(
        text=f"Problem: {result['problem']}"
    )

    suggestion_label.config(
        text=f"Suggestion: {result['suggestion']}"
    )

    save_log(result)

def reset_dashboard():
    status_label.config(text="Status: Disconnected", fg="#c0392b")
    result_label.config(text="Result: Waiting...", fg="#7f8c8d", bg="#f8f9fa") # Reset card to neutral gray/white
    problem_label.config(text="Problem: None")
    suggestion_label.config(text="Suggestion: Waiting for diagnosis")
    message_label.config(
    text="Waiting for data...")
    diagnosis_button.config(state="disabled")
    

def export_logs():
    path = export_csv()
    messagebox.showinfo(
        "Export Complete",
        f"Logs exported to:\n{path}"
    )

def clear_all_logs():
    if messagebox.askyesno("Confirm Clear", "Are you sure you want to delete all logs?"):
        clear_logs()
        messagebox.showinfo("Logs Cleared", "All logs removed successfully.")

def view_logs():
    logs = get_logs()
    log_window = tk.Toplevel(root)
    log_window.title("Diagnostic Logs")
    log_window.geometry("750x450")
    
    text_area = tk.Text(log_window, font=("Courier New", 10), padx=10, pady=10)
    text_area.pack(fill="both", expand=True)
    
    # Show logs in popup window
    for log in logs:
        text_area.insert(
            tk.END,
            f"Timestamp:  {log[1]}\nStatus:     {log[3]}\nProblem:    {log[4]}\nSuggestion: {log[5]}\n"
            f"{'-'*50}\n\n"
        )
    
    text_area.config(state="disabled")

# =====================================================================
# UI LAYOUT FRAME STRUCTURE
# =====================================================================

# Title
header_frame = tk.Frame(root, bg="#2c3e50", height=80)
header_frame.pack(fill="x", side="top")

title_label = tk.Label(
    header_frame,
    text="SAFE-GATE DIAGNOSTIC DASHBOARD",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#2c3e50"
)
title_label.pack(pady=20)

# Control panel frame
control_frame = tk.LabelFrame(
    root, 
    text=" Control & Scenarios ", 
    font=("Arial", 11, "bold"), 
    padx=15, 
    pady=15, 
    bg="white"
)
control_frame.place(x=20, y=110, width=360, height=360) # Tucked to the x=20 line

status_label = tk.Label(
    control_frame,
    text="Status: Disconnected",
    font=("Arial", 12, "bold"),
    fg="#c0392b",
    bg="white"
)
status_label.pack(pady=(5, 15))

connect_button = tk.Button(
    control_frame,
    text="🔌 Connect Device",
    font=("Arial", 11),
    bg="#34495e",
    fg="white",
    activebackground="#2c3e50",
    command=connect_device
)
connect_button.pack(fill="x", pady=5)

data_label = tk.Label(
    control_frame,
    text="Live Arduino Data",
    font=("Arial", 10),
    bg="white"
)

data_label.pack(pady=(20,5), anchor="w")

message_label = tk.Label(
    control_frame,
    text="Waiting for data...",
    font=("Arial",10),
    bg="#ecf0f1",
    relief="sunken",
    anchor="w"
)

message_label.pack(fill="x", pady=5)

diagnosis_button = tk.Button(
    control_frame,
    text="⚡ Run Diagnosis",
    font=("Arial", 11, "bold"),
    bg="#2980b9",
    fg="white",
    activebackground="#2471a3",
    state="disabled",
    command=run_diagnosis
)
diagnosis_button.pack(fill="x", pady=(20, 5))

# Results panel
display_frame = tk.LabelFrame(
    root, 
    text=" Active Measurement Telemetry ", 
    font=("Arial", 11, "bold"), 
    padx=15, 
    pady=15, 
    bg="white"
)
display_frame.place(x=400, y=110, width=480, height=360) # Balanced to close the gap perfectly

result_heading = tk.Label(
    display_frame,
    text="Diagnostic Result:",
    font=("Arial", 11, "bold"),
    bg="white"
)
result_heading.pack(anchor="w", pady=(5, 5))

result_label = tk.Label(
    display_frame,
    text="Result: Waiting...",
    font=("Arial", 14, "bold"),
    fg="#7f8c8d",
    bg="#f8f9fa",
    height=2,
    relief="solid",
    bd=1
)
result_label.pack(fill="x", pady=5)

problem_label = tk.Label(
    display_frame,
    text="Problem: None",
    font=("Arial", 11),
    bg="white",
    wraplength=440,
    justify="left"
)
problem_label.pack(anchor="w", pady=15)

suggestion_label = tk.Label(
    display_frame,
    text="Suggestion: Waiting for diagnosis",
    font=("Arial", 11),
    fg="#34495e",
    bg="white",
    wraplength=440,
    justify="left"
)
suggestion_label.pack(anchor="w", pady=5)

# Management utilities panel
management_frame = tk.LabelFrame(
    root, 
    text=" Maintenance Utilities ", 
    font=("Arial", 11, "bold"), 
    padx=15, 
    pady=15, 
    bg="white"
)
management_frame.place(x=20, y=490, width=860, height=140) # Spans the full width frame cleanly 

view_button = tk.Button(management_frame, text="📋 View Logs", font=("Arial", 11), command=view_logs, width=15)
view_button.pack(side="left", expand=True, padx=5)

export_button = tk.Button(management_frame, text="📥 Export CSV", font=("Arial", 11), command=export_logs, width=15)
export_button.pack(side="left", expand=True, padx=5)

clear_button = tk.Button(management_frame, text="🗑️ Clear Logs", font=("Arial", 11), command=clear_all_logs, width=15)
clear_button.pack(side="left", expand=True, padx=5)

reset_button = tk.Button(management_frame, text="🔄 Reset Unit", font=("Arial", 11), command=reset_dashboard, width=15)
reset_button.pack(side="left", expand=True, padx=5)

root.mainloop()
