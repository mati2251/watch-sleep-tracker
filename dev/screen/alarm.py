import datetime
from .time import TimeScreen
import adafruit_ssd1306

class AlarmScreen(TimeScreen):
    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C, time: datetime.time = datetime.time(0, 0, 0), enable: bool = False):
        super().__init__(display)
        self.time = time
        self.enable = enable

    def iteration(self):
        enableLabel = "off"
        if self.enable == True:
            enableLabel = "on"
        self.display.text(enableLabel, 112, 0, 1)
        super().iteration()
