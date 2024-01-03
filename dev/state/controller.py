import time
from .statei import State
from board import SCL, SDA
import adafruit_ssd1306
import busio
from gpiozero import Button, TonalBuzzer
from dataclasses import dataclass
import threading
import datetime
from heartrate import HeartRateMonitor 
import asyncio
@dataclass
class Config:
    alarm_time: datetime.time
    alarm_enabled: bool
    countdown_time: datetime.time


class Controller:
    left_held = False
    right_held = False
    config = Config(datetime.time(7, 00, 00), True, datetime.time(0, 20))

    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        display.rotate(180)
        self.display = display
        self.buzzer = TonalBuzzer(12)
        from .watch import WatchState
        self.state = WatchState(self)
        self.left_button = Button(17)
        self.right_button = Button(4)
        self.left_button.when_released = self.left_button_released
        self.right_button.when_released = self.right_button_released
        self.left_button.when_held = self.left_button_held
        self.right_button.when_held = self.right_button_held

    def change_state(self, state: State):
        self.state = state

    def loop(self):
        threading.Thread(target=self.alarm_thread).start()
        threading.Thread(target=self.hr_thread).start()
        while True:
            self.state.iteration()
            time.sleep(1 / 10)

    def left_button_released(self):
        if self.left_held:
            self.left_held = False
            return
        self.state.left_button()

    def left_button_held(self, _):
        self.left_held = True
        self.state.left_button_held()

    def right_button_released(self):
        if self.right_held:
            self.right_held = False
            return
        self.state.right_button()

    def right_button_held(self, _):
        self.right_held = True
        self.state.right_button_held()

    def alarm_thread(self):
        while True:
            if self.config.alarm_enabled:
                to_next_alarm = abs(datetime.datetime.now() - datetime.datetime.combine(datetime.datetime.today(),
                                                                                    self.config.alarm_time))
                if to_next_alarm <= datetime.timedelta(seconds=1):
                    from .alarm_alert import AlertState
                    self.state = AlertState(self)
            time.sleep(1)

    def hr_thread(self):
        monitor = HeartRateMonitor("B2:EF:04:D1:37:B4", "00002a37-0000-1000-8000-00805f9b34fb")
        asyncio.run(monitor.start_monitoring())
