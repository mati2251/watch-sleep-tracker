import datetime as dt
from .time import TimeScreen
import adafruit_ssd1306


class CountdownScreen(TimeScreen):
    start_time: dt.time = None
    countdown_time: dt.time
    reset_countdown_time: dt.time

    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C,
                 countdown_time: dt.time = dt.time(0, 20, 0)):
        super().__init__(display)
        self.countdown_time = dt.datetime.combine(dt.datetime.today(), countdown_time).time()
        self.reset_countdown_time = self.countdown_time

    def iteration(self):
        if self.start_time is not None:
            self.time = (dt.datetime.combine(dt.datetime.today(), self.countdown_time) + (
                        dt.datetime.combine(dt.date.today(), self.start_time) - dt.datetime.now())).time()
        else:
            self.time = self.countdown_time
        super().iteration()

    def start(self):
        self.start_time = dt.datetime.now().time()

    def stop(self):
        self.countdown_time = self.time
        self.start_time = None

    def reset(self):
        self.stop()
        self.countdown_time = self.reset_countdown_time
        self.time = self.countdown_time

    def start_stop(self):
        if self.start_time is None:
            self.start()
        else:
            self.stop()
