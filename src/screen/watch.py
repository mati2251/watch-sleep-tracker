from screen import Screen
import datetime
from .time import TimeScreen
import adafruit_ssd1306


class WatchScreen(TimeScreen):
    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C):
        super().__init__(display)

    def iteration(self):
        self.time = datetime.datetime.now().time()
        super().iteration()
