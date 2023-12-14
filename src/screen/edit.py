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

    def iteration(self, to: int = 1):
        self.blink_time_iterator += 1
        if self.blink_time_iterator >= 8:
            self.blink_time_iterator = 0
            self.is_flash = not self.is_flash
        if self.is_flash:
            super().iteration()
        else:
            self.display.fill_rect(89 - (36 * to), 9, 22, 16, 0)
            self.display.show()
            self.blink_time_iterator += 2
        pass

    def add(self, to: str):
        self.time = (dt.datetime.combine(dt.datetime.today(), self.time) + dt.timedelta(**{to: 1})).time()

    def subtract(self, to: str):
        self.time = (dt.datetime.combine(dt.datetime.today(), self.time) - dt.timedelta(**{to: 1})).time()
