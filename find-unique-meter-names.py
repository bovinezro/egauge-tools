import argparse

#users commonly submit large lists of device names with many duplicate entries
#however, most automated tasks will either take extra time or not run at all
#with duplicate device names. this script accepts a list of device names and
#returns only unique entries. 

parser = argparse.ArgumentParser(description='sort a list of meter names for unique entries.')
parser.add_argument('meterlist', metavar='meterlist', type=str, nargs='+', help='list of meters.')
args = parser.parse_args()

file = open(args.meterlist[0], 'r')
meters = set()
for i in file:
    meters.add(i)

for i in meters:
    print(i.rstrip("\n"))
