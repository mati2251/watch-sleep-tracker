from screen import Screen
import adafruit_ssd1306
import datetime


class TimeScreen(Screen):
    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C):
        self.display = display
        self.time = datetime.datetime.now().time()

    def iteration(self):
        self.display.text(self.time.strftime("%H:%M:%S"), 17, 9, 1, size=2)
        self.display.show()

    def clear(self):
        self.display.fill_rect(17, 0, 111, 25, 0)
