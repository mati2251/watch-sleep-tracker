import screen as scr
from .statei import State


class EditState(State):
    screen: scr.Screen

    def iteration(self):
        self.screen.iteration()

    def left_button(self):
        self.screen.add_minute()

    def right_button(self):
        self.screen.subtract_minute()

    def left_button_held(self):
        pass

    def right_button_held(self):
        pass

