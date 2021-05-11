
#!/usr/bin/env python3
#
# * Installation:
# apt-get install python3 python3-pip
# pip3 install minimalmodbus pyserial
# chmod +x smart-meter.py
#
# Read all registers
# python3 smart-meter.py


import io
import minimalmodbus
import struct
import serial
import time
import os
import sys
import urllib.request, urllib.error, urllib.parse

registers = {
    "L1 Voltage":               {"r": 0x000E, "w": 2, "t": "float"}, # alternative to 
    "L2 Voltage":               {"r": 0x0010, "w": 2, "t": "float"}, # below notation
    "L3 Voltage":               {"r": 0x0012}, # default float, width 2
    #"Grid Frequency":           {"r": 0x0014},
    "L1 Current":               {"r": 0x0016},
    "L2 Current":               {"r": 0x0018},
    "L3 Current":               {"r": 0x001A},
    "Total Active Power":       {"r": 0x001C},
    "L1 Active Power":          {"r": 0x001E},
    "L2 Active Power":          {"r": 0x0020},
    "L3 Active Power":          {"r": 0x0022},
    #"Total reactive power":     {"r": 0x0024},
    #"L1 reactive power":        {"r": 0x0026},
    #"L2 reactive power":        {"r": 0x0028},
    #"L3 reactive power":        {"r": 0x002A},
    #"Total Apparent Power":     {"r": 0x002C},
    #"L1 Apparent Power":        {"r": 0x002E},
    #"L2 Apparent Power":        {"r": 0x0030},
    #"L3 Apparent Power":        {"r": 0x0032},
    #"Total Power Factor":       {"r": 0x0034},
    #"L1 Power Factor":          {"r": 0x0036},
    #"L2 Power Factor":          {"r": 0x0038},
    #"L3 Power Factor":          {"r": 0x003A},
    "Total Active Energy":      {"r": 0x0100},
    "L1 Total Active Energy":   {"r": 0x0102},
    "L2 Total Active Energy":   {"r": 0x0104},
    "L3 Total Active Energy":   {"r": 0x0106},
    "Forward Active Energy":    {"r": 0x0108},
    "L1 Forward Active Energy": {"r": 0x010A},
    "L2 Forward Active Energy": {"r": 0x010C},
    "L3 Forward Active Energy": {"r": 0x010E},
    "Reverse Active Energy":    {"r": 0x0110},
    "L1 Reverse Active Energy": {"r": 0x0112},
    "L2 Reverse Active Energy": {"r": 0x0114},
    "L3 Reverse Active Energy": {"r": 0x0116},
}



smartmeter = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, meter address (in decimal)
smartmeter.serial.baudrate = 9600         # Baud
smartmeter.serial.bytesize = 8
smartmeter.serial.parity   = serial.PARITY_EVEN # vendor default is EVEN
smartmeter.serial.stopbits = 1
smartmeter.serial.timeout  = .7        # seconds
smartmeter.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
smartmeter.clear_buffers_before_each_transaction = True
smartmeter.debug = False # set to "True" for debug mode

register_list_str = ""
register_list_arr = None

for x in range(12):
    time.sleep(5)
    #Volty
    v1 = smartmeter.read_float(0x000E, functioncode=3, number_of_registers=2, byteorder=0)
    v2 = smartmeter.read_float(0x0010, functioncode=3, number_of_registers=2, byteorder=0)
    v3 = smartmeter.read_float(0x0012, functioncode=3, number_of_registers=2, byteorder=0)
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=423&svalue=%.3f" % (v1)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=424&svalue=%.3f" % (v2)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=425&svalue=%.3f" % (v3)))

    #Ampery
    a1 = smartmeter.read_float(0x0016, functioncode=3, number_of_registers=2, byteorder=0)
    a2 = smartmeter.read_float(0x0018, functioncode=3, number_of_registers=2, byteorder=0)
    a3 = smartmeter.read_float(0x001A, functioncode=3, number_of_registers=2, byteorder=0)
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=426&svalue=%.3f;%.3f;%.3f" % (a1,a2,a3)))

    #Wolty + licznik
    w = smartmeter.read_float(0x001C, functioncode=3, number_of_registers=2, byteorder=0)*1000
    w1 = smartmeter.read_float(0x001E, functioncode=3, number_of_registers=2, byteorder=0)*1000
    w2 = smartmeter.read_float(0x0020, functioncode=3, number_of_registers=2, byteorder=0)*1000
    w3 = smartmeter.read_float(0x0022, functioncode=3, number_of_registers=2, byteorder=0)*1000
    e = smartmeter.read_float(0x0100, functioncode=3, number_of_registers=2, byteorder=0)*1000
    e1 = smartmeter.read_float(0x0102, functioncode=3, number_of_registers=2, byteorder=0)*1000
    e2 = smartmeter.read_float(0x0104, functioncode=3, number_of_registers=2, byteorder=0)*1000
    e3 = smartmeter.read_float(0x0106, functioncode=3, number_of_registers=2, byteorder=0)*1000
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=427&svalue=%.3f;%.3f" % (w,e)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=428&svalue=%.3f;%.3f" % (w1,e1)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=429&svalue=%.3f;%.3f" % (w2,e2)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=430&svalue=%.3f;%.3f" % (w3,e3)))

    #Pobrana
    p = smartmeter.read_float(0x0108, functioncode=3, number_of_registers=2, byteorder=0)*1000
    p1 = smartmeter.read_float(0x010A, functioncode=3, number_of_registers=2, byteorder=0)*1000
    p2 = smartmeter.read_float(0x010C, functioncode=3, number_of_registers=2, byteorder=0)*1000
    p3 = smartmeter.read_float(0x010E, functioncode=3, number_of_registers=2, byteorder=0)*1000
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=1328&svalue=%.3f" % (p)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=1329&svalue=%.3f" % (p1)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=1330&svalue=%.3f" % (p2)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=1331&svalue=%.3f" % (p3)))

    #Oddana
    o = smartmeter.read_float(0x0110, functioncode=3, number_of_registers=2, byteorder=0)*1000
    o1 = smartmeter.read_float(0x0112, functioncode=3, number_of_registers=2, byteorder=0)*1000
    o2 = smartmeter.read_float(0x0114, functioncode=3, number_of_registers=2, byteorder=0)*1000
    o3 = smartmeter.read_float(0x0116, functioncode=3, number_of_registers=2, byteorder=0)*1000
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=1332&svalue=%.3f" % (o)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=1333&svalue=%.3f" % (o1)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=1334&svalue=%.3f" % (o2)))
    urllib.request.urlopen(urllib.request.Request("http://192.168.1.5:8080/json.htm?type=command&param=udevice&idx=1335&svalue=%.3f" % (o3)))


   # for name in registers:
   #     if register_list_arr and not name in register_list_arr:
   #          continue
   #     rconf = registers[name]
   #     #print(name, rconf)
   #     register = rconf["r"]
   #     rwidth = rconf["w"] if "w" in rconf else 2
   #     value = smartmeter.read_float(register, functioncode=3, number_of_registers=rwidth, byteorder=0)
   #     print ("%s: %.3f" % (name, value))

