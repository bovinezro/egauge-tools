#this script was written to automate the creation of a very complex configuration
#file for a group of devices. the script took about an hour to write; mannual
#configuration (accomplished through dropdown menus) would have taken at least
#a couple hours per device.


#don't just run this, double check the register id mapping first
#script to add multiple remote devices (Modbus TCP) and multiple registers
#per remote device. No provision for CTs/register based on physical measurements
#EG4xxx only

#required config info for PTs (never blank even if voltage refs aren't used)
cc = 0
while cc <= 2:
    print('ch'+str(cc)+'=-74.014,0,,,,1:1')
    cc += 1

#add a bit more info required by the config file, do not modify!
print('ch3=459.705,0,,,,')
print('highGain=no')
print('team=')
print('member="local"')
print(' link="local"')

#two sunspec devices with registers we want to keep, this could be dynamically
#generated but for a single register each it's easier to just hardcode
print('member="Inverter 15"')
print(' link="slowd"')
print(' addr="modbus://sunspec.15@USB2:9600/8n1"')
print('  name="Inverter 15"')
print('   id="0"')
print('   val="inverter.W"')
print('   type="P"')
print('member="Inverter 16"')
print(' link="slowd"')
print(' addr="modbus://sunspec.16@USB2:9600/8n1"')
print('  name="Inverter 16"')
print('   id="1"')
print('   val="inverter.W"')
print('   type="P"')

#define Modbus slave address, we'll be using 1-16 for this inverter set
slave_addr = 1
addr = 'modbus://AC_power=29,!u16*100,W;AC_daily_cumulative=24,!u16*.1,kWh;DC_current_1=38,!u16*.1,A;DC_current_2=40,!u16*.1,A;DC_current_3=42,!u16*.1,A;AB_voltage=31,!u16*.1,V;BC_voltage=32,!u16*.1,V;CA_voltage=33,!u16*.1,V.'+str(slave_addr)+'@USB1:9600/8n1'

#max 127, we start at 16 because 0-15 are reserved for the sunspec devices
id = 16
#max 7, there are eight registers per inverter (0-7)
valcounter = 0
#max 14, there are 14 inverters with this addressing
inv = 1

#lists to contain our unit types and register names as text strings
#these get reused a lot
type = ["P", "P", "I", "I", "I", "V", "V", "V"]
vallist = ["AC_power", "AC_daily_cumulative", "DC_current_1", "DC_current_2", "DC_current_3", "AB_voltage", "BC_voltage", "CA_voltage"]

#this is a risky way to increment register ids but it works since we know there
#are 16 register (0-15) used by the sunspec devices and 128 regs available
#don't use this for just any config, CHECK RANGE FIRST
while id <= 127:

    print('member="Inverter '+str(slave_addr)+'"')
    print(' link="slowd"')
    print(' addr="'+str(addr)+'"')
    slave_addr += 1
    addr = 'modbus://AC_power=29,!u16*100,W;AC_daily_cumulative=24,!u16*.1,kWh;DC_current_1=38,!u16*.1,A;DC_current_2=40,!u16*.1,A;DC_current_3=42,!u16*.1,A;AB_voltage=31,!u16*.1,V;BC_voltage=32,!u16*.1,V;CA_voltage=33,!u16*.1,V.'+str(slave_addr)+'@USB1:9600/8n1'

    while valcounter <= 7:

        print('  name="Inverter '+str(inv)+' '+str(vallist[valcounter])+'"')
        print('   id="'+str(id)+'"')
        print('   val="'+str(vallist[valcounter])+'"')
        print('   type="'+str(type[valcounter])+'"')
        valcounter += 1
        id += 1

    if valcounter == 8:
        valcounter = 0
        inv += 1
    else:
        pass

#last bit of configuration that needs to be present. Don't modify!
print('team_end=')
print('totals=')
print('map0="use"=')
print('map1="gen"=')
