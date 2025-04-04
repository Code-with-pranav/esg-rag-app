# data_simulator.py
import json
import time
import random
import os

# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Output file for streaming
ESG_OUTPUT_FILE = "esg_stream_output.jsonl"

# Simulate ESG reports every 2 minutes
while True:
    # Generate random emissions data for CoalCo
    data = {
        "company": "CoalCo",
        "emissions": random.randint(50, 200),  # Random emissions between 50-200 tons
        "date": "2025-03-28"
    }
    # Write to coalco.json
    with open("data/coalco.json", "w") as f:
        json.dump(data, f)
    print(f"Generated ESG report: {data}")

    # Append to JSONL for streaming
    with open(ESG_OUTPUT_FILE, "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")
    print(f"Appended ESG report to {ESG_OUTPUT_FILE}")

    time.sleep(120)  # Wait 2 minutes