import smbus
import time
"""
#interface for directly passing the module number and pin number from other programs into the script.
obj = MultiRelayModule()
obj.add_module(0x20)
obj.add_module(0x21)
obj.turn_on(16)
obj.turn_off(16)

"""
class Relay:
    def __init__(self,i2c_address):                     #intialization of realy class object with i2c address
        self.bus = smbus.SMBus(1)                       #initialize SMBus for I2C communication
        if isinstance(i2c_address,str):
            self.i2c_address = int(i2c_address, 16)     #I2C address HEX from input integer
        else:
            self.i2c_address = i2c_address
        self.channels = 8                               #8 pins per relay
        self.clear_all = 0xFF                           #setting all relays to off
        self.enabled_relays = self.clear_all            #setting the relay status as 0xFF initially
        
        try:
            self.bus.read_byte(self.i2c_address)        #checking for valid I2C response
        except Exception as excp:                       #exception handling, If I2C device not found
            del self.bus
            self.bus = None
            raise OSError("Invalid I2C Address")
        
        self.bus.write_byte(self.i2c_address, self.clear_all)       #writing the I2C pins 
    
    def turn_on(self,channel):                                      #turn on relay function
        if not 1 <= channel <= self.channels:                       #relay pin must be within 1 to 8
            print(f"[ info ] channel should be 1 - {self.channel}")
            return
        pin_num = channel - 1                                       #pin_num 0 to 7, channel 1 to 8
        print("pin",pin_num)
        print("before",bin(self.enabled_relays)) 
        self.enabled_relays &= ~(1 << pin_num)                      #enabled_relays is last state, then AND with 0
        
        print("[ON]",bin(self.enabled_relays))  
        self.bus.write_byte(self.i2c_address, self.enabled_relays)  #turn on specific relay which user will enter


    def turn_off(self,channel):                                     #turn off relay function
        if not 1 <= channel <= self.channels:
            print(f"[ info ] channel should be 1 - {self.channel}")
            return
        pin_num = channel - 1
        print("pin",pin_num)
        print("before",bin(self.enabled_relays)) 
        self.enabled_relays |= (1 << pin_num)                       #enabled_relays is last state, then OR with 1
        
        print("[OFF]",bin(self.enabled_relays))                               
        self.bus.write_byte(self.i2c_address, self.enabled_relays)  #turn off specific relay which user will enter

    def cleanup(self):                                              #setting all relays to off
        self.bus.write_byte(self.i2c_address, self.clear_all)
        del self.bus
        self.bus = None

    def __del__(self):
        if self.bus: self.cleanup()

class MultiRelayModule:
    def __init__(self):
        self.module = []


    def add_module(self,i2c_address):                               #storing relay_module address in to module [] as a list
        try:
            self.module.append(Relay(i2c_address))                  #adding the i2c address to the list.
            return True
        except Exception as excp:                                   #exception handling
            print(f"[ error ] invalid i2c address {i2c_address}")   #will be printed if i2c address not found
            return False
        
    def turn_on(self,channel):                                      #turn on specific relay which user will enter
        module_number = (relay_number - 1) // 8                     #identify the I2C bus
        relay_pin = (relay_number - 1) % 8                          #identify the I2C module pinout number
        relay_pin += 1                                              #correcting with +1, since 0-7 maps with 1-8
        self.module[module_number].turn_on(relay_pin)


    def turn_off(self,channel):                                     #turn off specific relay which user will enter
        module_number = (relay_number - 1) // 8
        relay_pin = (relay_number - 1) % 8                          #identify the I2C module pinout number
        relay_pin += 1                                              #correcting with +1, since 0-7 maps with 1-8
        self.module[module_number].turn_off(relay_pin)              
        

if __name__ == "__main__":                                  #to check if the script run directly or imported as a module
    obj = MultiRelayModule()                                #class is created and assigned to the variable "obj"
    while 1:                                                #infinite loop as main program
        menu = int(input("=========== MENU ===========\n1) add relay module\n2) control relay\n3) Exit\nEnter your option: "))
        if menu == 1:                                       #option 1 to add devices in the "module" array
            addr = input("\nEnter I2C address of the module: ")
            obj.add_module(addr)
        elif menu == 2:                                     #option to control (On/Off) the relays
            if len(obj.module) == 0:                        #if no module is selected before selection option 2
                print("\n[ warning ] module not added\n")   #module not added error
                continue
            _start = 1
            print(f"available relays 1 -> {len(obj.module) * 8}")   #if everything okay, the program asks for the relay number to control
            relay_number = int(input("\nEnter relay number: "))     #if relay number is not inline
            if  not 1 <= relay_number <= len(obj.module) * 8:
                print(f"[ error ] relay number should be between 1 - {len(obj.module) * 8}")
            module_number = (relay_number - 1) // 8
            print(module_number)
            # print(relay_number," : ",module_number," : ",relay_pin)   #used for debugging
            if not module_number <= len(obj.module):                #if module number is beyond actual number
                print("[ error ] invalid relay number")
                continue
            action = int(input("1) Turn ON\n2) Turn OFF\n3) Menu\nEnter your option: "))    #catch the user input
            if action == 1:                                                                 #turn the relay ON
                obj.turn_on(relay_number)
            elif action == 2:                                                               #turn the relay OFF
                obj.turn_off(relay_number)
        else:
            exit(0)

