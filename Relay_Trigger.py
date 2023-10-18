'''
This is a working code & not all exceptions are handled.
The final working code is linked below
https://github.com/tenxer-roy/i2c-relay-chain/blob/main/Relay_Test_F.py
'''

import smbus                #importing libraries
import time

bus = smbus.SMBus(1)        #creating i2c bus object for sending commands

max_device = int(input("Enter the number of I2C devices: "))        #total number of devices
D = []                      #create device address array, max 8 for PCF8574 IO expander
V = []                      #create array to contain corresponding value/ state of the IO bus

for i in range(max_device):
    d = input("Enter the address for device no. {}: ".format(i + 1))
    v = 0xFF                #set all relays off initially, by sending 1111 1111 to each device
    D.append(d)
    V.append(v)
    bus.write_byte(int(D[i], 16), V[i])         #write the address and value in SMbus

print("Addresses:", D)
print("Values:", V)

while True:                 #infinite loop, for embedded applications
    try:
        command = input("Enter Relay command (format: RxxN or RxxF): ")
        print(command)

        if len(command) < 3:                    #relay command cannot be less than 3 elements
            print("Wrong instruction! Please review the command format.")
        else:
            fst_ltr = command[0]
            rly_num = command[1:-1]             #relay number extracted from user command
            lst_ltr = command[-1]               #relay command O(N) or OF(F)

            if not (fst_ltr.lower() == "r" and (lst_ltr.lower() in ["n", "f"])):    #check for N,F and lower case
                print("Wrong instruction! Please review the command format.")
            else:
                rly_num = int(rly_num)          #convert string to int
                
                if rly_num==0:                  #patch if relay number 0 is given
                    print("Failed! Relay number out of range.")
                    continue                    #skip & continue to while loop if relay number=0

                module_num = rly_num // 8       #getting device index for D[] array
                pin_num = rly_num % 8           #getting pin number for V[] array
                if pin_num == 0:                #patch for pin no 8, it should turn on the last 7th bit of i2c pins
                    module_num-=1
                    pin_num = 8
                

                if module_num >= max_device:                        #when module number is greater than i2c devices
                    print("Failed! Relay number out of range.")
                else:
                    print("module_num:", (module_num+1))            #quotent starts from 0, i2c module starts from 1
                    print("pin_num:", pin_num)

                    if lst_ltr.lower() == "n":                      #checking ON instruction
                        print("old", bin(V[module_num]))
                        V[module_num] &= ~(1 << (pin_num - 1))      #leftshift 0 is done using shiftin inverted 1, AND
                        print("new", bin(V[module_num]))
                        bus.write_byte(int(D[module_num], 16), V[module_num])   #sending instruction to i2c module

                    if lst_ltr.lower() == "f":                      #checking ON instruction
                        print("old", bin(V[module_num]))
                        V[module_num] |= (1 << (pin_num - 1))       #leftshift 1 is done using shiftin inverted 1, OR
                        print("new", bin(V[module_num]))
                        bus.write_byte(int(D[module_num], 16), V[module_num])   #sending instruction to i2c module

    except KeyboardInterrupt:                       #handling exception when program interrupted
        for i in range(max_device):
            bus.write_byte(int(D[i], 16), 0xFF)     #turn OFF all the relays before closing the program
            time.sleep(0.3)                         #delay between turn off each module 300ms
        print("\nInterrupted")
        break
