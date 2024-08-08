from guizero import App, Text, TextBox, PushButton, Slider
import urllib.request
from urllib.parse import quote
from smbus import SMBus #import SMBus module of I2C
from time import sleep          #import
import requests
'''
Author: Derek Huang
Lab 14: Project
ELEC5650-01A
08/07/2024
'''

# ADXL345 registers/addresses
PWR_ADDR = 0x1D
GND_ADDR = 0x53
DATA_FORMAT = 0x31
BW_RATE = 0x2C
POWER_CTL = 0x2D
    
bus = SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards

stop = False # Stop ADXL345

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
        
        return x, y, z
def cbButn_StartMPU6050():
    data = []
    device_gnd = ADXL345(GND_ADDR)
    sleep(0.1)
    device_pwr = ADXL345(PWR_ADDR)
    sleep(0.1)
    while True:
        data.append(device_gnd.getAxes())
        sleep(0.1)
        data.append(device_pwr.getAxes())
        urlFull = urlBase + "?AccelX=" + quote(str(data[0])) + "&AccelY=" + quote(str(data[1])) + "&AccelZ=" + quote(str(data[2])) + "&GyroX=" + quote(str(data[3])) + "&GyroY=" + quote(str(data[4])) + "&GyroZ=" + quote(str(data[5]))
        print(urlFull)
        webResponse = requests.get(urlFull)
        if webResponse.status_code == 200:
            txtTime.value = "Data Storing..."
        else:
            txtTime.value = "Issue with Storing Data!"
        app.update()
        sleep(initDelay)
        if stop:
            break
        
def cbButn_StopMPU6050():
    global stop
    stop = True
    txtTime.value = "Stopping MPU6050 Data Collection..."
    app.update()
    sleep(1)
    app.destroy()

def cbSldr_DelayTime(slider_value):
    global initDelay
    initDelay = slider_value
    font_size.value = f"Delay Time: {slider_value}"

if __name__ == '__main__':
    global urlBase
    global initDelay
    urlBase = "https://script.google.com/macros/s/AKfycbyZuUS5ln63BaxUhiVuu9_YmAhROL_30Y0pRwJfRwq43MD3-3x-syCX0weY3uGMd_tJ/exec"
    initDelay = 1
    app = App(title="MPU6050 Monitoring GUI")
    txtTime = Text(app, text="Please Select the Time Interval To Store Data (seconds):", size=10, font="Times New Roman", color="red")
    delay_size = Slider(app, command=cbSldr_DelayTime, start=1, end=30)
    font_size = Text(app, text=f"Delay Time: {initDelay}")
    store_start = PushButton(app, command=cbButn_StartMPU6050, text="Start MPU6050 Data Collection")
    store_stop = PushButton(app, command=cbButn_StopMPU6050, text="Stop MPU6050 Data Collection")
    app.display()
            
