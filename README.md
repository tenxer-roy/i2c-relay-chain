# i2c-relay-chain
Managing upto 64 different relay channels using PCF8574 I2c Expander and Raspberry Pi 4

### Directory structure:
* i2ctest.py - I2C-Pi communication demo.<br>
* **Relay_Test_F.py** -  OOPS version of main code.<br>
* Relay_Trigger.py -The first iteration of main code.<br>
* Relay_Trigger.py.bak - Backup file, previous iteration.<br><br>

### Workflow:
1 i2c device can manage upto 8 relay pins. This code takes information like number of I2c Devices, their addresses etc. from the user. All the device addresses and Initial values are stored in respective arrays D[] and V[]. Based on the relay control instruction, this code sends appropriate signal to the desired Relay via the I2C IO expander board.<br><br>
The Relay board is **Low Level Trigger** type, which means when we send `0` the relay will be ON.<br> To turn ON a pin `&= ~(1<<pin_no)` is used and to turn OFF a pin `|= (1<<pin_no)` is used. Everytime user sends a new command, the previous state of the I2C pins are updated with "AND" or "OR" operations.

![Board Connection](../main/Images/16i2crelay.drawio.png)
