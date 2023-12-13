from screen import Screen
import datetime as dt
from .time import TimeScreen
import adafruit_ssd1306


class EditScreen(TimeScreen):
    blink_time_iterator = 0
    is_flash = False

    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C, time: dt.time):
        super().__init__(display)
        self.time = time

    def iteration(self):
        self.display.fill_rect(17, 9, 64, 16, 0)
        self.blink_time_iterator += 1
        if self.blink_time_iterator >= 8:
            self.blink_time_iterator = 0
            self.is_flash = not self.is_flash
        if self.is_flash:
            super().iteration()
        else:
            self.display.fill(0)
            self.display.show()
            self.blink_time_iterator += 2
        pass

    def add_minute(self):
        self.time = (dt.datetime.combine(dt.datetime.today(), self.time) + dt.timedelta(minutes=1)).time()

    def subtract_minute(self):
        self.time = (dt.datetime.combine(dt.datetime.today(), self.time) - dt.timedelta(minutes=1)).time()
