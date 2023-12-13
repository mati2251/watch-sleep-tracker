from screen import Screen
import adafruit_ssd1306
import time
import datetime

class TimeScreen(Screen):
    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C):
        self.display = display
        self.time = datetime.datetime.now()

    def iteration(self):
        self.display.fill_rect(17, 9, 64, 16, 0)
        self.display.fill(0)
        self.display.text(self.time.strftime("%H:%M:%S"), 17, 9, 1, size=2)
        self.display.show()

