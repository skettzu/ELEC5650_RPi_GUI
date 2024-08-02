from guizero import App, Text, TextBox, PushButton, Slider
import urllib.request
from smbus2 import SMBus					#import SMBus module of I2C
from time import sleep          #import
'''
Author: Derek Huang
Lab 12: RPi GUI
ELEC5650-01A
07/26/2024
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

    def read_all_data():
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
        sleep(1)

def cbButn_StoreSheets():
    urlFull = urlBase + "?sliderValue=" + str(txtTale.size)
    webResponse = urllib.request.urlopen(urlFull)
    print(webResponse.getcode())
    print(urlFull)

def cbButn_AddWord():
    txtTale.value += " " + user_story.value
    user_story.clear()

def cbSldr_FontSize(slider_value):
    txtTale.size = slider_value
    font_size.value = f"Font Size: {slider_value}"

if __name__ == '__main__':
    global urlBase
    global initFontSize
    urlBase = "https://script.google.com/macros/s/AKfycbzdwHxxaimndNQsxXqQsCE1GtKEHzXQSdu2-4Hm3FXoNLoyOwyi641TzXc2iv_wYi9s/exec"
    initFontSize = 12
    app = App(title="Tales of Old by Derek")
    txtTale = Text(app, text="Once upon a time", size=initFontSize, font="Times New Roman", color="red")
    user_story = TextBox(app, width=30)
    add_story = PushButton(app, command=cbButn_AddWord, text="Add to Story")
    text_size = Slider(app, command=cbSldr_FontSize, start=4, end=40)
    font_size = Text(app, text=f"Font Size: {initFontSize}")
    store_size = PushButton(app, command=cbButn_StoreSheets, text="Store to Google Sheets")
    app.display()
            
