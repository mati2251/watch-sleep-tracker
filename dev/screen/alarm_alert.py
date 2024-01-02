import time

from screen import Screen
import adafruit_ssd1306
from gpiozero import TonalBuzzer


class AlertScreen(Screen):
    blink_time_iterator = 0
    is_flash = True
    next_tone = 0
    tones = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'E#4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'G#4', 'G4', 'F#4', 'F4', 'E#4',
             'E4', 'D#4', 'D4', 'C#4']

    def __init__(self, display: adafruit_ssd1306.SSD1306_I2C, buzzer: TonalBuzzer):
        self.display = display
        self.buzzer = buzzer

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
        self.buzzer.play(self.tones[self.next_tone % len(self.tones)])
        self.next_tone += 1

    def clear(self):
        self.buzzer.stop()

    def stop(self):
        time.sleep(0.2)
        self.buzzer.stop()
        self.display.fill(0)
        self.display.show()
