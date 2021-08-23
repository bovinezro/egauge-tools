import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://egaugexxxxx.egaug.es/status.xml"

print(requests.get(url, verify=False))
