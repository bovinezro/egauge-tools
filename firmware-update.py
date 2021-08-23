import requests
from requests.auth import HTTPDigestAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = ""
password = ""

url = "https://egaugexxxxx.egaug.es/cgi-bin/protected/sw-upgrade?"
xml_output = requests.get(url, verify=False, auth=HTTPDigestAuth(username,password))
url = "https://egaugexxxxx.egaug.es/cgi-bin/protected/reboot?"
xml_output = requests.get(url, verify=False, auth=HTTPDigestAuth(username,password))
