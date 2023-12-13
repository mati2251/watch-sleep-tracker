import screen as scr
from .statei import State
import RPi.GPIO as GPIO
import time


class StopWatchState(State):
    screen: scr.Screen

    def __init__(self, time_screen, controller):
        super().__init__(controller)
        self.time_screen = time_screen
        self.screen = scr.StopwatchScreen(time_screen)

    def iteration(self):
        self.screen.iteration()
        pass

    def left_button(self):
        from .alarm import AlarmState
        self.controller.change_state(AlarmState(self.time_screen, self.controller))

    def right_button(self):
        self.screen.start_stop()

    def right_button_held(self):
        self.screen.reset()

    def left_button_held(self):
        pass
