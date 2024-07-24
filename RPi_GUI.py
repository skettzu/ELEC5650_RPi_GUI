from guizero import App, Text, TextBox, PushButton, Slider
import urllib.request
'''
Author: Derek Huang
Lab 12: RPi GUI
ELEC5650-01A
07/26/2024
'''

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
            
