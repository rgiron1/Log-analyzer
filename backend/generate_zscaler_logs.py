import csv
import random
import argparse
from datetime import datetime, timedelta
import os

headers = [
    "timestamp", "cloud_name", "proto", "url", "action", "company",
    "login", "activity", "reqsize", "respsize",
    "primary_category", "secondary_category", "tertiary_category",
    "riskscore", "threatseverity", "cpubip", "srcip_country", "dstip_country",
    "uaclass", "reqmethod", "respcode"
]

reqmethods = ['GET', 'POST', 'PUT', 'DELETE']
cloud_names = ['Zscaler', 'AWS', 'Azure', 'Google Cloud']
uaclasses = ['Mozilla/5.0', 'Chrome/92.0', 'Safari/605.1.15']
companies = ['YouTube', 'Gmail', 'Ebay', 'Dropbox', 'Facebook']
logins = ['user1@gmail.com', 'user2@gmail.com', 'user3@gmail.com', 'user4@gmail.com']
activities = ['view', 'edit', 'upload', 'download', 'buy', 'sell']
protocols = ['HTTP', 'HTTPS', 'TCP', 'UDP']
actions = ['Allowed', 'Blocked']
categories = ['Productivity Loss', 'Security Risk', 'Online Shopping', 'Social Media', 'Streaming Media']
respcodes_normal = ['200']
respcodes_threat = ['403', '500']
urls = ['ebay.com/', 'youtube.com/', 'dropbox.com/', 'gmail.com/', 'facebook.com/']
countries = ['US', 'CA', 'GB', 'AU', 'IN', 'DE', 'FR', 'JP', 'MX']

def generate_log(entry_type="normal", minutes_offset=0):
    now = datetime.now()
    timestamp = (now - timedelta(minutes=minutes_offset)).strftime("%Y-%m-%dT%H:%M:%S")
    base = {
        "timestamp": timestamp,
        "cloud_name": random.choice(cloud_names),
        "proto": random.choice(protocols),
        "url": random.choice(urls),
        "company": random.choice(companies),
        "login": random.choice(logins),
        "activity": random.choice(activities),
        "primary_category": random.choice(categories),
        "secondary_category": random.choice(categories),
        "tertiary_category": random.choice(categories),
        "cpubip": f"198.51.100.{random.randint(1, 255)}",
        "srcip_country": random.choice(countries),
        "dstip_country": random.choice(countries),
        "uaclass": random.choice(uaclasses),
        "reqmethod": random.choice(reqmethods),
        "action": "Allowed",
        "respcode": random.choice(respcodes_normal),
        "reqsize": random.randint(500, 3000),
        "respsize": random.randint(500, 3000),
        "riskscore": random.randint(0, 45),
        "threatseverity": "Low"
    }

    if entry_type == "threat":
        base.update({
            "action": "Blocked",
            "respcode": random.choice(respcodes_threat),
            "reqsize": random.randint(40000, 100000),
            "respsize": random.randint(100, 1000),
            "uaclass": "curl/7.68.0",
            "riskscore": random.randint(75, 100),
            "activity": random.choice(['download', 'upload']),
            "threatseverity": random.choice(["High", "Critical"])
        })

    elif entry_type == "normal":
        base.update({
            "reqsize": random.randint(500, 3000),
            "respsize": random.randint(500, 3000),
            "riskscore": random.randint(0, 45),
            "threatseverity": random.choice(["Low", "Medium"]),
            "respcode": random.choice(respcodes_normal),
            "action": "Allowed"
        })

    return [base[h] for h in headers]

def generate_sample_logs(mode="normal", num_entries=20, normal_ratio=0.8):
    logs = []
    for i in range(num_entries):
        if mode == "normal":
            entry_type = "normal"
        elif mode == "threat":
            entry_type = "threat"
        elif mode == "mixed":
            entry_type = "normal" if random.random() < normal_ratio else "threat"
        else:
            raise ValueError(f"Unknown mode '{mode}'. Choose from 'normal', 'threat', 'mixed'.")
        logs.append(generate_log(entry_type=entry_type, minutes_offset=i))
    return logs

def write_logs_to_file(filename="zscaler_logs.csv", mode="normal", num_entries=20):
    logs = generate_sample_logs(mode=mode, num_entries=num_entries)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(logs)
    print(f" {num_entries} '{mode}' logs saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zscaler log generator")
    parser.add_argument("--mode", choices=["normal", "threat", "mixed"], default="normal", help="Type of logs to generate")
    parser.add_argument("--count", type=int, default=50, help="Number of log entries")
    parser.add_argument("--out", type=str, default="logs/zscaler_logs.csv", help="Output CSV file")
    args = parser.parse_args()

    write_logs_to_file(filename=args.out, mode=args.mode, num_entries=args.count)
