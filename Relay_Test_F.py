import smbus
import time

class RelayController:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.D = []
        self.V = []

    def initialize(self, num_devices):
        self.D = []
        self.V = []
        for i in range(num_devices):
            address = input(f"Enter the address for device no. {i + 1}: ")
            self.D.append(address)
            self.V.append(0xFF)
            self.bus.write_byte(int(self.D[i], 16), self.V[i])

    def process_command(self, command):
        if len(command) < 3:
            print("Wrong instruction! Please review the command format.")
            return

        fst_ltr = command[0]
        rly_num = command[1:-1]
        lst_ltr = command[-1]

        if not (fst_ltr.lower() == "r" and (lst_ltr.lower() in ["n", "f"])):
            print("Wrong instruction! Please review the command format.")
            return
        
        if(rly_num.isnumeric()==False):
            print("Failed! Relay number out of range.")
            return

        rly_num = int(rly_num)
        if (rly_num == 0):
            print("Failed! Relay number out of range.")
            return

        module_num = (rly_num - 1) // 8
        pin_num = (rly_num - 1) % 8

        if module_num >= len(self.D):
            print("Failed! Relay number out of range.")
            return

        print("module_num:", module_num + 1)
        print("pin_num:", pin_num + 1)

        if lst_ltr.lower() == "n":
            print("old", bin(self.V[module_num]))
            self.V[module_num] &= ~(1 << pin_num)
            print("new", bin(self.V[module_num]))
            self.bus.write_byte(int(self.D[module_num], 16), self.V[module_num])

        if lst_ltr.lower() == "f":
            print("old", bin(self.V[module_num]))
            self.V[module_num] |= (1 << pin_num)
            print("new", bin(self.V[module_num]))
            self.bus.write_byte(int(self.D[module_num], 16), self.V[module_num])

    def cleanup(self):
        for i in range(len(self.D)):
            self.bus.write_byte(int(self.D[i], 16), 0xFF)
            time.sleep(0.3)

if __name__ == "__main__":
    controller = RelayController()
    num_devices = int(input("Enter the number of I2C devices: "))
    controller.initialize(num_devices)

    try:
        while True:
            command = input("Enter Relay command (format: RxxN or RxxF): ")
            print(command)
            controller.process_command(command)

    except KeyboardInterrupt:
        controller.cleanup()
        print("\nInterrupted")