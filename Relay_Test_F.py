import smbus                                                                #import necessary libraries
import time

class RelayController:                                                      #create class RelayController
    def __init__(self):       
        self.bus = smbus.SMBus(1)                                           #Initializing i2cbus
        self.D = []
        self.V = []

    def initialize(self, num_devices):                                      #Initializing the relay module
        self.D = []
        self.V = []
        for i in range(num_devices):   
            address = input(f"Enter the address for device no. {i + 1}: ")  #enter the address of all i2c devices
            self.D.append(address)                                          #append the addresses in D[] array 
            self.V.append(0xFF)                                             #fill the values with 11111111, initial condition OFF
            self.bus.write_byte(int(self.D[i], 16), self.V[i])              #write into the bus (device address, data to write)

    def process_command(self, command):
        if len(command) < 3:
            print("Wrong instruction! Please review the command format.")   #Address value length must be >=3
            return

        fst_ltr = command[0]                                                    #index 0 determines relay
        rly_num = command[1:-1]                                                 #index 1 to (length of list-1) determines the relay number
        lst_ltr = command[-1]                                                   #last index determines ON and OFF instruction
        if not (fst_ltr.lower() == "r" and (lst_ltr.lower() in ["n", "f"])):    #enter "r" followed by relay number to turn on or turn off relay.
            print("Wrong instruction! Please review the command format.")
            return
        
        if(rly_num.isnumeric()==False):
            print("Failed! Relay number out of range.")                         #if entered relay value is not a numeric value
            return                                                              # continue to 

        rly_num = int(rly_num)
        if (rly_num == 0):
            print("Failed! Relay number out of range.")                        #if entered relay value is 0
            return

        module_num = (rly_num - 1) // 8                                         #To determine the  I2C module to be trigerred
        pin_num = (rly_num - 1) % 8                                             #To determine the pin number.

        if module_num >= len(self.D):
            print("Failed! Relay number out of range.")                        
            return

        print("module_num:", module_num + 1)
        print("pin_num:", pin_num + 1)

        if lst_ltr.lower() == "n":                                               #checking for turn ON  input
            print("old", bin(self.V[module_num]))
            self.V[module_num] &= ~(1 << pin_num)                                #leftshift 0 is done using shifting  1 and inverting and followed by AND operation
            print("new", bin(self.V[module_num]))
            self.bus.write_byte(int(self.D[module_num], 16), self.V[module_num]) #sending instruction to i2c module

        if lst_ltr.lower() == "f":                                               #checking for turn OFF input
            print("old", bin(self.V[module_num]))
            self.V[module_num] |= (1 << pin_num)                                 #l#leftshift 0 is done using shifting  1 and inverting and followed by OR operation
            self.bus.write_byte(int(self.D[module_num], 16), self.V[module_num]) #sending instruction to i2c module

    def cleanup(self):                                                           #turn OFF all the relays before closing the program
        for i in range(len(self.D)):
            self.bus.write_byte(int(self.D[i], 16), 0xFF)
            time.sleep(0.3)                                                      #delay between turn off each module 300ms

if __name__ == "__main__":
    controller = RelayController()
    num_devices = int(input("Enter the number of I2C devices: "))
    controller.initialize(num_devices)

    try:                                                                       #handling exception when program interrupted
        while True:
            command = input("Enter Relay command (format: RxxN or RxxF): ")
            print(command)
            controller.process_command(command)

    except KeyboardInterrupt:
        controller.cleanup()
        print("\nInterrupted")