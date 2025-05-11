import time
import json
from urllib.parse import urlparse
from ping3 import ping
import requests

results = []

with open("urls.txt") as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    if not url.startswith("http"):
        url = "http://" + url
    parsed_url = urlparse(url)
    host = parsed_url.hostname

    entry = {
        "url": url,
        "host": host,
        "ping_up": 0,
        "ping_latency": None,
        "http_up": 0,
        "http_status": None,
        "http_latency": None
    }

    # Ping
    try:
        ping_latency = ping(host, timeout=2)
        if ping_latency:
            entry["ping_up"] = 1
            entry["ping_latency"] = round(ping_latency, 4)
    except:
        entry["ping_up"] = 0

    # HTTP GET
    try:
        start = time.time()
        response = requests.get(url, timeout=3)
        end = time.time()
        entry["http_up"] = 1
        entry["http_status"] = response.status_code
        entry["http_latency"] = round(end - start, 4)
    except:
        entry["http_up"] = 0

    results.append(entry)

with open("health_log.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ health_log.json created.")

