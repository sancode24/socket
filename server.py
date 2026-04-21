from flask import Flask, request
import csv
import os
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "centralized_network_log.csv"

@app.route('/report', methods=['POST'])
def report_speed():
    # 1. Get the data sent by the client
    data = request.json
    client_id = data.get("client_id", "Unknown")
    speed = data.get("speed", 0)
    timestamp = data.get("timestamp", datetime.now().strftime("%H:%M:%S"))

    # 2. PRINT MESSAGE TO TERMINAL (This is what you asked for)
    print(f"[#] RECEIVING PACKET from {client_id} | Speed: {speed} Mbps | Time: {timestamp}")

    # 3. Save to CSV
    file_exists = os.path.isfile(LOG_FILE)
    try:
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Client_ID", "Speed_Mbps"])
            writer.writerow([timestamp, client_id, speed])
        
        # 4. Confirm it was saved
        print(f"    >>> Success: Data logged to {LOG_FILE}")
        return {"status": "success"}, 200
        
    except Exception as e:
        print(f"    [!] ERROR saving data: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    print("--- SERVER INITIALIZED ---")
    print(f"Listening for clients on: http://172.20.225.8:5000")
    print("Waiting for incoming network packets...\n")
    app.run(host='0.0.0.0', port=5000)
