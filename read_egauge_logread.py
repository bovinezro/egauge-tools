import datetime
import time
import requests
import argparse
from requests.auth import HTTPDigestAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description='Read and store the eGauge syslog file externally.')
parser.add_argument('meter_name', metavar='meter_name', type=str, nargs='+', help='device name of meter.')
parser.add_argument('username', metavar='username', type=str, nargs='+', help='valid meter username')
parser.add_argument('password', metavar='username', type=str, nargs='+', help='value meter password')
args = parser.parse_args()

headers = {'Connection': 'close'}
url = "https://" + args.meter_name[0] + ".egaug.es/cgi-bin/protected/set?logread"
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

most_recent = 0
while True:
    xml_output = requests.get(url, headers, verify=False, auth=HTTPDigestAuth(args.username[0], args.password[0]))
    lines = []
    lines = xml_output.text.split("\n")
    lines = lines[1:-2]

    for i in lines:
        date_time = i[0:15]
        if i[0:3] in months:
            date_time = (str(int(months.index(i[0:3])) + 1)) + i[4:15]
        chunks = date_time.split(":")
        date_time = " ".join(chunks)
        chunks = date_time.split(" 0")
        date_time = " ".join(chunks)
        chunks = date_time.split(" ")
        date_time = datetime.datetime(2021, int(chunks[0]), int(chunks[1]), int(chunks[2]), int(chunks[3]), int(chunks[4]))
        latest_value = int(time.mktime(date_time.timetuple()))

        if latest_value > most_recent:
            with open("output.txt", mode="a") as f:
                f.write(i + "\n")

    most_recent = latest_value
    time.sleep(5)
