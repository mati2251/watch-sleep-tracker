import screen as scr
from .statei import State


class AlertState(State):
    screen: scr.AlertScreen

    def __init__(self, controller):
        super().__init__(controller)
        self.screen = scr.AlertScreen(self.controller.display, self.controller.buzzer)

    def iteration(self):
        self.screen.clear()
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
