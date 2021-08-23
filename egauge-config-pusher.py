import requests
from requests.auth import HTTPDigestAuth
import sys
import argparse

#used to push a configuration file to a single eGauge meter. assumes the meter
#is on the d.egauge.net proxy (standard). the format of configuration files
#is not described here, but the most common use case would be to manually copy
#/cgi-bin/protected/egauge-cfg from one meter and use this script to push it to
#another meter. 

#gather up a config filename, meter name, username, and password
parser = argparse.ArgumentParser(description='Push a configuration file to an eGauge meter.')
parser.add_argument('filename', metavar='filename', type=str, nargs='+', help='filename of the eGauge configuration file.')
parser.add_argument('meter', metavar='meter', type=str, nargs='+', help='eGauge device name.')
parser.add_argument('user', metavar='user', type=str, nargs='+', help='valid username for the eGauge meter.')
parser.add_argument('pw', metavar='pw', type=str, nargs='+', help='value password for the eGauge meter.')
args = parser.parse_args()

#create the meter url (assumes egaug.es proxy server)
meter_url = 'http://' + args.meter[0] + '.d.egauge.net/cgi-bin/protected/egauge-cfg'

#fetch info from the config file
file = open(args.filename[0], "r")
payload = (file.read())

#pass this to ensure the connection is closed
headers={'Connection': 'close'}

#post contents of the configuration file
result = requests.post(meter_url, headers=headers, data=payload, auth=HTTPDigestAuth(args.user[0], args.pw[0]))
print(result)
