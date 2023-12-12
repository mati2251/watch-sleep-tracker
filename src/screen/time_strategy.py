from screen import ScreenStrategy
import adafruit_ssd1306
import math
import adafruit_framebuf
import threading
import time
import datetime


class TimeScreen(ScreenStrategy):
    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C):
        self.display = display
        self.display.rotate(180)
        self.thread = threading.Thread(target=self.start_thread)
        self.stop = False

    def start(self):
        self.stop = False
        self.thread.start()

        self.thread.join()

    def start_thread(self):
        while True:
            self.display.fill(0)
            date = datetime.datetime.now()
            self.display.text(date.strftime("%H:%M:%S"), int(self.display.width / 2) - 47,
                              int(self.display.height / 2) - 7, 1, size=2)
            time.sleep(1/60)
            if self.stop:
                break
            self.display.show()

    def stop(self):
        self.stop = True
