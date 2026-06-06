# backend/diagnostic_engine.py

from datetime import datetime


MESSAGE_MAP = {
    "MSG: VOID DETECTED": {
        "status": "FAIL",
        "problem": "Broken/Open Connection",
        "suggestion": "Check breadboard track continuity or replace the faulty section."
    },

    "MSG: HEALTHY TRACK": {
        "status": "PASS",
        "problem": "None",
        "suggestion": "No action required."
    },

    "MSG: COMPONENT OK / HEALTHY RESISTOR": {
        "status": "PASS",
        "problem": "None",
        "suggestion": "Component is functioning correctly."
    },

    "ALERT: MAIN POWER DISCONNECTED OR REVERSED": {
        "status": "CRITICAL",
        "problem": "Power Supply Issue",
        "suggestion": "Check power polarity, supply voltage, and wiring."
    },

    "--- SAFE-GATE SYSTEM ONLINE ---": {
        "status": "INFO",
        "problem": "System Startup",
        "suggestion": "Device successfully initialized."
    }
}


def process_message(message):
    """
    Converts raw Arduino message into structured diagnostic data.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if message in MESSAGE_MAP:
        data = MESSAGE_MAP[message]

        return {
            "timestamp": timestamp,
            "message": message,
            "status": data["status"],
            "problem": data["problem"],
            "suggestion": data["suggestion"]
        }

    return {
        "timestamp": timestamp,
        "message": message,
        "status": "UNKNOWN",
        "problem": "Unknown Event",
        "suggestion": "Review Arduino output."
    }


# ----------------------------
# TESTING
# ----------------------------

if __name__ == "__main__":

    test_messages = [
        "MSG: VOID DETECTED",
        "MSG: HEALTHY TRACK",
        "MSG: COMPONENT OK / HEALTHY RESISTOR",
        "ALERT: MAIN POWER DISCONNECTED OR REVERSED",
        "--- SAFE-GATE SYSTEM ONLINE ---",
        "RANDOM MESSAGE"
    ]

    for msg in test_messages:
        result = process_message(msg)

        print("\n--------------------")
        print(result)