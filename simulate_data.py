# simulate_data.py
import json
import time
from datetime import datetime

while True:
    # Generate a new ESG report
    new_report = {
        "company": "CoalCo",
        "emissions": 150 + int(time.time() % 50),  # Vary emissions slightly
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    # Append to the file
    with open("esg_stream_output.jsonl", "a") as f:
        f.write(json.dumps(new_report) + "\n")
    print(f"Added new report: {new_report}")
    time.sleep(120)  # Wait 2 minutes