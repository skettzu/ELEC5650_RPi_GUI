import smbus
import time
from time import sleep
import sys

bus = smbus.SMBus(1)
PWR_ADDR = 0x1D
GND_ADDR = 0x53
DATA_FORMAT = 0x31
BW_RATE = 0x2C
POWER_CTL = 0x2D
class ADXL345():
    def __init__(self, slave):
        self.slave_address = slave # ADXL345 device address when GND
        bus.write_byte_data(self.slave_address, BW_RATE, 0x0B) # configures data output rate to 200 bps
        value = bus.read_byte_data(0x53, DATA_FORMAT) # read current status of 0x31 register [data format]
        value &= ~0x0F # mask register value
        value |= 0x0B  # Full res, right justified bit, 10-bit +/- 2g
        bus.write_byte_data(0x53, DATA_FORMAT, value)
        bus.write_byte_data(0x53, POWER_CTL, 0x08) # Operated in measurement mode
    def getAxes(self):
        bytes = bus.read_i2c_block_data(0x53, 0x32, 6) # read status of axes registers 2 bits each for x,y,z

        # store and format accel output
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)

        self.accely = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)

        self.accelz = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)

        # convert to SI units
        x = x * 0.004 
        y = y * 0.004
        z = z * 0.004

        x = x * 9.80665
        y = y * 9.80665
        z = z * 9.80665

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        print("   x = %.3f ms2" %x)
        print("   y = %.3f ms2" %y)
        print("   z = %.3f ms2" %z)
        print("\n\n")
        
        self.accelx = x
        self.accely = y
        self.accelz = z
    
if __name__ == "__main__":
    try:
        device = ADXL345(GND_ADDR)
        while True: 
            device.getAxes()
            time.sleep(2)
    except KeyboardInterrupt:
        sys.exit()
