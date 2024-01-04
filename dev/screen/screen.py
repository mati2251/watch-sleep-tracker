import datetime
from abc import ABC, abstractmethod
import adafruit_ssd1306


class Screen(ABC):
    display: adafruit_ssd1306.SSD1306_I2C
    time: datetime.time

    @abstractmethod
    def iteration(self):
        pass

    @abstractmethod
    def clear(self):
        pass 
