import requests
from requests.auth import HTTPDigestAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = ""
password = ""
suffix = ["/cgi-bin/netcfg?live"]

for i in suffix:
    url = "https://egaugexxxxx.d.egauge.net/" + i
    xml_output = requests.get(url, verify=False, auth=HTTPDigestAuth(username,password))
    print(xml_output.text)
