from guizero import App, Text, TextBox, PushButton, Slider
import urllib.request
from smbus2 import SMBus					#import SMBus module of I2C
from time import sleep          #import
'''
Author: Derek Huang
Lab 14: Project
ELEC5650-01A
08/07/2024
'''

class MPU6050():
    #some MPU6050 Registers and their Address
    PWR_MGMT_1   = 0x6B
    SMPLRT_DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    INT_ENABLE   = 0x38
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    GYRO_XOUT_H  = 0x43
    GYRO_YOUT_H  = 0x45
    GYRO_ZOUT_H  = 0x47

    bus = SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
    Device_Address = 0x68   # MPU6050 device address

    def MPU_Init():
        #write to sample rate register
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
        
        #Write to power management register
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
        
        #Write to Configuration register
        bus.write_byte_data(Device_Address, CONFIG, 0)
        
        #Write to Gyro configuration register
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
        
        #Write to interrupt enable register
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    def read_raw_data(addr):
        #Accelero and Gyro value are 16-bit
            high = bus.read_byte_data(Device_Address, addr)
            low = bus.read_byte_data(Device_Address, addr+1)
        
            #concatenate higher and lower value
            value = ((high << 8) | low)
            
            #to get signed value from mpu6050
            if(value > 32768):
                    value = value - 65536
            return value

    def read_all_data(delay):
        #Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
        
        #Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
        
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0

        print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
        sleep(delay)
        data = [Ax, Ay, Az, Gx, Gy, Gz]
        return data

def cbButn_StartMPU6050():
    device = MPU6050()
    device.MPU_Init()
    sleep(0.1)
    while True:
        data = device.read_all_data_and_store(initDelay)
        urlFull = urlBase + "?AccelX=" + str(data[0]) + "&AccelY=" + str(data[1]) + "&AccelZ=" + str(data[2]) + "&GyroX=" + str(data[3]) + "&GyroY=" + str(data[4]) + "&GyroZ=" + str(data[5])
        webResponse = urllib.request.urlopen(urlFull)
        txtTime.value = str(webResponse)
        #print(urlFull)


def cbSldr_DelayTime(slider_value):
    global initDelay
    initDelay = slider_value
    font_size.value = f"Font Size: {slider_value}"

if __name__ == '__main__':
    global urlBase
    global initDelay
    urlBase = "https://script.google.com/macros/library/d/1KI1AVEBQtapiRhgVJYCyFibObwJprqf69-3bvyEVtjeJCPmsqR3xKl7y/2"
    initDelay = 1
    app = App(title="MPU6050 Monitoring GUI")
    txtTime = Text(app, text="Please Select the Time Interval To Store Data (seconds):", size=10, font="Times New Roman", color="red")
    delay_size = Slider(app, command=cbSldr_DelayTime, start=1, end=30)
    font_size = Text(app, text=f"Delay Time: {initDelay}")
    store_size = PushButton(app, command=cbButn_StartMPU6050, text="Start MPU6050 Data Collection")
    app.display()
            
