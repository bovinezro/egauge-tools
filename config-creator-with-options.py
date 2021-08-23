#creates a variety of configuration files for a customer's predefined config
#needs. wrote this before I'd figured out argparse.


#script to create complete configuration files for meters with complex or
#tedious configuration requirements.
#expects two arguments
#enter '15' or '30' for EG4115 or EG4130
#enter 1, 2, 3 for single/split/three phase
#example 'python this-script.py 15 2'

import sys

#check to make sure user specified a valid model
idlist = []
model = 0

try:
    int(sys.argv[1])
    if int(sys.argv[1]) == 30:
        idlist = [29, 59, 89, 119]
        model = 4130
    elif int(sys.argv[1]) == 15:
        idlist = [14, 29, 44, 59]
        model = 4115
    else:
        print('Enter either 15 or 30 depending on number of sensor ports.')
        sys.exit()
except ValueError:
    print('Enter either 15 or 30 depending on number of sensor ports.')
    sys.exit()

#check to make sure user specified a valid phase value
phase = 1

try:
    int(sys.argv[2])
    if int(sys.argv[2]) == 1:
        phase = 1
    elif int(sys.argv[2]) == 2:
        phase = 2
    elif int(sys.argv[2]) == 3:
        phase = 3
    else:
        print('Enter 1 for single ph, 2 for split ph, 3 for 3 ph.')
        sys.exit()
except ValueError:
    print('Enter 1 for single ph, 2 for split ph, 3 for 3 ph.')
    sys.exit()

#Define sensors (CTs) here
#sensor definitions must be pulled from an existing meter
A100 = '-206.8012,0,,,.08@1.5:.08@3:.06@6:.02@15:-.05@50:-.05@100,CC-ACT-020-0100'
A2775 = '7.5081,0,int,0,0@50,AE-RCT-178-2775'

#start printing the config file. Do not change these values!
cc = 0
while cc <= 2:
    print('ch'+str(cc)+'=-74.014,0,,,,1:1')
    cc += 1
print('ch3=459.705,0,,,,')
print('highGain=no')
cc += 1

#these values can be changed to use the correct sensor type based on config
while cc <= 6:
    print('ch'+str(cc)+'='+A2775)
    cc += 1

while cc <= 18:
    print('ch'+str(cc)+'='+A100)
    cc += 1

#add additional sensors for the 30 port model
if int(sys.argv[1]) == 30:
    while cc <= 33:
        print('ch'+str(cc)+'='+A100)
        cc += 1
else:
    pass

#add a bit more info required by the config file. Do not modify this!
print('team=')
print('member="local"')
print(' link="local"')

#setting up some variables for incrementing components of the register config
i = 1
id = 0
L = 1

#create registers. This isn't documented anywhere.
while id <= idlist[0]:
    print('  name="Pos Real Energy S'+str(i)+'+"')
    print('   id="'+str(id)+'"')
    print('   val="S'+str(i)+'*L'+str(L)+'"')
    print('')
    print('type="P"')
    i += 1
    id += 1
    L += 1
    if L > phase:
        L = 1
    else:
        pass
i = 1
L = 1
while id <= idlist[1]:
    print('  name="Neg Real Energy S'+str(i)+'-"')
    print('   id="'+str(id)+'"')
    print('   val="S'+str(i)+'*L'+str(L)+'"')
    print('')
    print('type="P"')
    i += 1
    id += 1
    L += 1
    if L > phase:
        L = 1
    else:
        pass
i = 1
L = 1
while id <= idlist[2]:
    print('  name="App Energy S'+str(i)+'*"')
    print('   id="'+str(id)+'"')
    print('   val="S'+str(i)+'*L'+str(L)+'"')
    print('')
    print('type="P"')
    i += 1
    id += 1
    L += 1
    if L > phase:
        L = 1
    else:
        pass

i = 1
while id <= idlist[3]:
    print('  name="Power Factor S'+str(i)+'"')
    print('   id="'+str(id)+'"')
    print('   val="=($\\"Pos Real Energy S'+str(i)+'+\\" + abs($\\"Neg Real Energy S'+str(i)+'-\\")) / $\\"App Energy S'+str(i)+'*\\""')
    print('   type="#3"')
    i += 1
    id += 1

#last bit of configuration that needs to be present. Don't modify!
print('  name="Model number"')
print('   id="'+str(id)+'"')
print('   val="='+str(model)+'"')
print('   type="#"')
print('team_end=')
print('totals=')
print('map0="use"=')
print('map1="gen"=')
