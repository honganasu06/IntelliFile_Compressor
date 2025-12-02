import os
import json
import csv
import random
import time
from datetime import datetime, timedelta

OUTPUT_DIR = "intelligent_file_compressor/examples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_json(filename, size_mb=1):
    print(f"Generating {filename}...")
    # Create a structure that compresses well:
    # 1. Repetitive keys (Dictionary)
    # 2. Monotonic integers (Delta)
    
    data = []
    base_int = 1000
    target_size = size_mb * 1024 * 1024
    
    while True:
        # Create a batch
        batch = []
        for _ in range(1000):
            base_int += random.randint(1, 5) # Monotonic increase
            item = {
                "id": base_int,
                "category": random.choice(["A", "B", "C", "D", "E"]),
                "status": "active",
                "details": {
                    "timestamp": base_int * 10,
                    "checked": True
                }
            }
            batch.append(item)
        
        data.extend(batch)
        
        # Check size roughly
        current_size = len(json.dumps(data))
        if current_size >= target_size:
            break
            
    with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Done. Size: {os.path.getsize(os.path.join(OUTPUT_DIR, filename)) / 1024:.2f} KB")

def generate_csv(filename, rows=50000):
    print(f"Generating {filename}...")
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Category", "Value", "Description"])
        
        id_counter = 1000
        categories = ["Hardware", "Software", "Service", "Consulting", "Other"] * 5
        descriptions = ["Standard Item", "Premium Item", "Legacy Item", "Refurbished Item"] * 5
        
        for _ in range(rows):
            id_counter += random.randint(1, 3) # Delta friendly
            cat = random.choice(categories) # Dictionary friendly
            val = random.randint(100, 9999)
            desc = random.choice(descriptions)
            
            writer.writerow([id_counter, cat, val, desc])
            
    print(f"Done. Size: {os.path.getsize(filepath) / 1024:.2f} KB")

def generate_log(filename, lines=50000):
    print(f"Generating {filename}...")
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    start_time = datetime.now()
    
    with open(filepath, 'w') as f:
        for i in range(lines):
            ts = start_time + timedelta(seconds=i)
            ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
            
            level = random.choice(["INFO", "INFO", "INFO", "WARN", "ERROR"])
            msg = random.choice([
                "Connection established successfully",
                "User logged in from 192.168.1.1",
                "Database query executed in 0.05s",
                "Cache miss for key user_123",
                "Retrying operation after timeout"
            ])
            
            f.write(f"{ts_str} {level} {msg}\n")
            
    print(f"Done. Size: {os.path.getsize(filepath) / 1024:.2f} KB")

def generate_text(filename, size_mb=1):
    print(f"Generating {filename}...")
    filepath = os.path.join(OUTPUT_DIR, filename)
    target_size = size_mb * 1024 * 1024
    
    words = [
        "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
        "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
        "magna", "aliqua", "ut", "enim", "ad", "minim", "veniam", "quis", "nostrud",
        "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea",
        "commodo", "consequat"
    ]
    
    with open(filepath, 'w') as f:
        while f.tell() < target_size:
            line = " ".join(random.choices(words, k=20)) + ".\n"
            f.write(line)
            
    print(f"Done. Size: {os.path.getsize(filepath) / 1024:.2f} KB")

if __name__ == "__main__":
    generate_json("large_sample.json", size_mb=2) # ~2MB
    generate_csv("large_data.csv", rows=20000)    # ~1MB
    generate_log("server.log", lines=20000)       # ~1.5MB
    generate_text("story.txt", size_mb=1)         # ~1MB
