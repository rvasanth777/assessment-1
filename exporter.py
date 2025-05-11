from prometheus_client import start_http_server, Gauge
from urllib.parse import urlparse
from ping3 import ping
import requests
import time

# Metrics
url_latency = Gauge('url_latency_seconds', 'Latency in seconds', ['url'])
url_up = Gauge('url_up', 'Availability (1=up, 0=down)', ['url'])

# Load URLs
with open("urls.txt") as f:
    urls = [line.strip() for line in f if line.strip()]

def check_urls():
    for url in urls:
        if not url.startswith("http"):
            url = "http://" + url
        parsed = urlparse(url)
        host = parsed.hostname

        try:
            ping_time = ping(host, timeout=2)
            if ping_time:
                url_up.labels(url).set(1)
            else:
                url_up.labels(url).set(0)
        except:
            url_up.labels(url).set(0)

        try:
            start = time.time()
            resp = requests.get(url, timeout=3)
            latency = time.time() - start
            url_latency.labels(url).set(latency)
        except:
            url_latency.labels(url).set(0)

if __name__ == "__main__":
    print("Starting exporter at http://localhost:9100/metrics")
    start_http_server(9100)
    while True:
        check_urls()
        time.sleep(30)

