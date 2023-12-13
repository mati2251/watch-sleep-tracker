from screen import Screen
import datetime
from .time import TimeScreen
import adafruit_ssd1306

class AlarmScreen(TimeScreen):
    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C, time: datetime.time = datetime.time(0, 0, 0)):
        super().__init__(display)
        self.time = time

    def iteration(self):
        super().iteration()
