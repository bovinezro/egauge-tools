import datetime
import time
import requests
import argparse
from requests.auth import HTTPDigestAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#getting the necessary items to query a meter: meter name, username, password
parser = argparse.ArgumentParser(description='Read and store the eGauge syslog file externally.')
parser.add_argument('meter_name', metavar='meter_name', type=str, nargs='+', help='device name of meter.')
parser.add_argument('username', metavar='username', type=str, nargs='+', help='valid meter username')
parser.add_argument('password', metavar='username', type=str, nargs='+', help='value meter password')
args = parser.parse_args()

#setting a few parameters needed later
headers = {'Connection': 'close'}
url = "https://" + args.meter_name[0] + ".d.egauge.net/cgi-bin/protected/set?logread"
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
current_date = datetime.datetime.now()
most_recent = 0


while True:
    #makes the actual request to the meter, which should return the syslog contents if it works
    xml_output = requests.get(url, headers, verify=False, auth=HTTPDigestAuth(args.username[0], args.password[0]))
    lines = xml_output.text.split("\n")
    #check to see if syslog is even running (may need to be started manually)
    if len(lines) == 3:
        print("Syslog is not running. Start with <metername>.d.egauge.net/cgi-bin/protected/set?log")
        exit()
    #handles invalid username/password combo
    try:
        if "401" in lines[5]:
            print("Invalid Username or Password.")
            exit()
    except IndexError:
        pass
    #trim some leading and trailing junk
    lines = lines[1:-2]
    #convert the date and time at the start of each line into a unix timestamp for easy comparison
    for i in lines:
        date_time = i[0:15]
        if i[0:3] in months:
            date_time = (str(int(months.index(i[0:3])) + 1)) + i[4:15]
        chunks = date_time.split(":")
        date_time = " ".join(chunks)
        chunks = date_time.split(" 0")
        date_time = " ".join(chunks)
        chunks = date_time.split(" ")
        date_time = datetime.datetime(current_date.year, int(chunks[0]), int(chunks[1]), int(chunks[2]), int(chunks[3]), int(chunks[4]))
        latest_value = int(time.mktime(date_time.timetuple()))
        #if the timestamp of any values in the most recent pull contains a newer value, write to file
        if latest_value > most_recent:
            with open("output.txt", mode="a") as f:
                f.write(i + "\n")
    #handle meters which aren't connected to the proxy server gracefully
    try:
        most_recent = latest_value
    except NameError:
        print("Meter is not connected to the d.egauge.net proxy server.")
        exit()
    #wait five seconds before checking syslog again. In all but the most extreme cases this should be fine.
    time.sleep(5)
