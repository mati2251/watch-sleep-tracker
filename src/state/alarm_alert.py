import time

import screen as scr
from .statei import State


class AlarmAlertState(State):
    screen: scr.Screen

    def __init__(self, controller):
        super().__init__(controller)
        self.screen = scr.AlarmAlertScreen(self.controller.display, self.controller.buzzer)

    def iteration(self):
        self.screen.iteration()

    def left_button(self):
        self.comeback()

    def right_button(self):
        self.comeback()

    def left_button_held(self):
        self.comeback()

    def right_button_held(self):
        self.comeback()

    def comeback(self):
        from .watch import WatchState
        self.controller.change_state(WatchState(self.controller))
        self.screen.stop()
