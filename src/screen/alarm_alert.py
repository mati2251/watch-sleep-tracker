from screen import Screen
import datetime
import adafruit_ssd1306


class AlarmAlertScreen(Screen):
    blink_time_iterator = 0
    is_flash = True

    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C):
        self.display = display

    def iteration(self):
        self.display.fill_rect(17, 9, 64, 16, 0)
        self.blink_time_iterator += 1
        if self.blink_time_iterator >= 4:
            self.blink_time_iterator = 0
            self.is_flash = not self.is_flash
        if self.is_flash:
            self.display.fill(0)
            self.display.text("ALARM", 35, 9, 1, size=2)
            self.display.show()
        else:
            self.display.fill(1)
            self.display.text("ALARM", 35, 9, 0, size=2)
            self.display.show()
