import os
import sys
import argparse
import time
import requests
from requests.auth import HTTPDigestAuth
import urllib3
import hashlib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#this script is intentionally broken; specifically it does not contain a valid
#username. also, the script was developed for older EG30xx meters, which only
#support HTTP (a few simple changes to the hardcoded URLs will make this
#compatible with EG4xxx meters using HTTPS)

parser = argparse.ArgumentParser(description='Push a username and password to an eGauge meter.')
parser.add_argument('meterlist', metavar='meterlist', type=str, nargs='+', help='list of meters.')
args = parser.parse_args()

#username is left blank here, the actual username was hard coded for this case
username = ''

#script accepts a list of passwords and meter names in the format
#"password  metername" without quotes (note the double space)
#this file is usually automatically generated using fetch-passwords.sh
file = open(args.meterlist[0], 'r')
for i in file:
    meterinfo = i.split(' ')
    pw = meterinfo[0]
    pw = pw.rstrip()
    meter = meterinfo[2]
    meter = meter.rstrip()
    meternum = meter[5:]
    print(meter)
    print("username: newuser")
    print("password: default"+meternum)

    #add username owner
    headers = {'Connection': 'close'}
    payload = ("sitePW=no\n user2=newuser\n priv2=unlimited_save, view_settings")
    url = "http://" + meter + ".d.eauge.net/cgi-bin/protected/egauge-cfg"
    userresult = requests.post(url, headers=headers, data=payload, auth=HTTPDigestAuth(username, pw))

    #add password default(meterid)
    hash = 'owner:eGauge Administration:default' + str(meternum)
    result = hashlib.md5(hash.encode())
    payload = ("user=newuser\n hash=" + result.hexdigest())
    url = "http://" + meter + ".d.egauge.net/cgi-bin/protected/egauge-cfg?setpw"
    passresult = requests.post(url, headers=headers, data=payload, auth=HTTPDigestAuth(username, pw))
