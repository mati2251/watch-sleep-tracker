import screen
import time
from .statei import State
from board import SCL, SDA
import adafruit_ssd1306
import busio
from gpiozero import Button


class Controller:
    left_held = False
    right_held = False

    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        display.rotate(180)
        from .watch import WatchState
        self.state = WatchState(screen.TimeScreen(display), self)
        self.left_button = Button(4)
        self.right_button = Button(17)
        self.left_button.when_released = self.left_button_released
        self.right_button.when_released = self.right_button_released
        self.left_button.when_held = self.left_button_held
        self.right_button.when_held = self.right_button_held

    def change_state(self, state: State):
        self.state = state

    def loop(self):
        while True:
            self.state.iteration()
            time.sleep(1 / 60)

    def left_button_released(self):
        if self.left_held:
            self.left_held = False
            return
        self.state.left_button()

    def left_button_held(self, time):
        self.left_held = True
        self.state.left_button_held()

    def right_button_released(self):
        if self.right_held:
            self.right_held = False
            return
        self.state.right_button()

    def right_button_held(self, time):
        self.right_held = True
        self.state.right_button_held()
