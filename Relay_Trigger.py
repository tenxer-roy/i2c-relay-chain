import smbus
import time

bus = smbus.SMBus(1)

max_device = int(input("Enter the number of I2C devices: "))
#max_device = d
D = []
V = []
for i in range(max_device):
    s = input("Enter the address for device no. {}: ".format(i + 1))
    v = 0xFF
    D.append(s)
    V.append(v)
    bus.write_byte(int(D[i], 16), V[i])

print("Addresses:", D)
print("Values:", V)

while True:
    try:
        command = input("Enter Relay command (format: RxxN or RxxF): ")
        print(command)

        if len(command) < 3:
            print("Wrong instruction! Please review the command format.")
        else:
            fst_ltr = command[0]
            rly_num = command[1:-1]
            lst_ltr = command[-1]

            if not (fst_ltr.lower() == "r" and (lst_ltr.lower() in ["n", "f"])):
                print("Wrong instruction! Please review the command format.")
            else:
                rly_num = int(rly_num)
                
                if rly_num==0:
                    print("Failed! Relay number out of range.")
                    continue

                module_num = rly_num // 8
                pin_num = rly_num % 8
                if pin_num == 0:
                    module_num-=1
                    pin_num = 8
                

                if module_num >= max_device:
                    print("Failed! Relay number out of range.")
                else:
                    print("module_num:", (module_num+1))
                    print("pin_num:", pin_num)

                    if lst_ltr.lower() == "n":
                        print("old", bin(V[module_num]))
                        V[module_num] &= ~(1 << (pin_num - 1))
                        print("new", bin(V[module_num]))
                        bus.write_byte(int(D[module_num], 16), V[module_num])

                    if lst_ltr.lower() == "f":
                        print("old", bin(V[module_num]))
                        V[module_num] |= (1 << (pin_num - 1))
                        a = 0b11111111
                        print("new", bin(V[module_num]))
                        bus.write_byte(int(D[module_num], 16), V[module_num])

    except KeyboardInterrupt:
        for i in range(max_device):
            bus.write_byte(int(D[i], 16), 0xFF)
            time.sleep(0.3)
        print("\nInterrupted")
        break