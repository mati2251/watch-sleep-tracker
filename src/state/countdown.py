import screen as scr
from .statei import State
import RPi.GPIO as GPIO
import time


class CountdownState(State):
    screen: scr.Screen

    def __init__(self, time_screen, controller):
        super().__init__(controller)
        self.time_screen = time_screen
        self.screen = scr.CountdownScreen(time_screen, self.controller.config.countdown_time)

    def iteration(self):
        self.screen.iteration()

    def left_button(self):
        from .alarm import AlarmState
        self.controller.change_state(AlarmState(self.time_screen, self.controller))

    def right_button(self):
        self.screen.start_stop()

    def right_button_held(self):
        self.screen.reset()

    def left_button_held(self):
        from .edit_countdown import EditCountdownState
        self.controller.change_state(EditCountdownState(self.time_screen, self.controller))