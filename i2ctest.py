import smbus                                #import necessary libraries
import time

PCF1 = 0x20                                 #i2c device address
#D1 = 0b11111111                            #8pins of i2c module 1 means relay turned off

PCF2 = 0x21                                 #i2c device address
#D2 = 0b11111111                            #8pins of i2c module o means relay turned on

b = smbus.SMBus(1)                          #specific i2c but to manage

while True:
    b.write_byte(PCF1, 0xFE)                #sending command to i2c bus
    time.sleep(2)                           #command format is
    b.write_byte(PCF1, 0xFF)                #write into the bus (device address, data to write)
    time.sleep(2)
"""
    b.write_byte(PCF2, 0xFF)
    time.sleep(2)
    b.write_byte(PCF2, 0xF0)
    time.sleep(2)
"""
