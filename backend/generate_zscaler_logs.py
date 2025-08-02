import csv
import random
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
uaclasses = ['curl/7.68.0', 'Mozilla/5.0', 'Chrome/92.0', 'Safari/605.1.15']
companies = ['YouTube', 'Gmail', 'Ebay', 'Dropbox', 'Facebook']
logins = ['user1@gmail.com', 'user2@gmail.com', 'user3@gmail.com', 'user4@gmail.com', 'user5@gmail.com', 'user6@gmail.com']
activities = ['view', 'edit', 'upload', 'download', 'buy', 'sell']
protocols = ['HTTP', 'HTTPS', 'TCP', 'UDP']
actions = ['Allowed', 'Allowed', 'Allowed', 'Blocked']
categories = ['Productivity Loss', 'Security Risk', 'Online Shopping', 'Social Media', 'Streaming Media', 'File Sharing', 'Shopping and Auctions']
respcodes = ['200', '204', '403', '404', '500']
urls = ['ebay.com/', 'youtube.com/', 'dropbox.com/', 'gmail.com/', 'facebook.com/']
countries = ['US', 'CA', 'GB', 'AU', 'IN', 'DE', 'FR', 'JP', 'MX']

def generate_sample_logs(filename="zscaler_logs.csv", num_entries=20):
    logs = []
    now = datetime.now()
    for i in range(num_entries):
        timestamp = (now - timedelta(minutes=i)).strftime("%a %b %d %H:%M:%S %Y")
        selected_cloud = random.choice(cloud_names)
        selected_protocol = random.choice(protocols)
        selected_url = random.choice(urls)
        selected_action = random.choice(actions)
        selected_company = random.choice(companies)
        selected_login = random.choice(logins)
        selected_activity = random.choice(activities)
        selected_category = random.choice(categories)
        selected_riskscore = random.randint(0, 100)

        if selected_riskscore == 0:
            threatseverity = 'None'
        elif selected_riskscore < 46:
            threatseverity = 'Low'
        elif selected_riskscore < 75:
            threatseverity = 'Medium'
        elif selected_riskscore < 90:
            threatseverity = 'High'
        else:
            threatseverity = 'Critical'

        selected_reqmethod = random.choice(reqmethods)
        selected_respcode = random.choice(respcodes)
        selected_uaclass = random.choice(uaclasses)
        selected_cpubip = f"198.51.100.{random.randint(1, 255)}"
        selected_src_country = random.choice(countries)
        selected_dst_country = random.choice(countries)
        reqsize = random.randint(100, 10000)
        respsize = random.randint(100, 10000)

        log = [
            timestamp, selected_cloud, selected_protocol, selected_url, selected_action,
            selected_company, selected_login, selected_activity, reqsize, respsize,
            selected_category, selected_category, selected_category,
            selected_riskscore, threatseverity, selected_cpubip,
            selected_src_country, selected_dst_country,
            selected_uaclass, selected_reqmethod, selected_respcode
        ]
        logs.append(log)
    return logs

def write_logs_to_file(filename="zscaler_logs.csv", num_entries=20):
    logs = generate_sample_logs(filename, num_entries)
    print("Saving to:", os.path.abspath(filename))
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(logs)
    print(f"{num_entries} sample Zscaler logs written to {filename}")

if __name__ == "__main__":
    write_logs_to_file()
    print("Current working directory:", os.getcwd())
