import screen as scr
from .statei import State


class EditState(State):
    screen: scr.EditScreen
    current_type = 1
    types = ['seconds', 'minutes', 'hours']

    def iteration(self):
        self.screen.clear()
        self.screen.iteration(self.current_type)

    def left_button(self):
        self.screen.add(self.types[self.current_type])

    def right_button(self):
        self.screen.subtract(self.types[self.current_type])

    def left_button_held(self):
        pass

    def right_button_held(self):
        self.current_type += 1
        if self.current_type >= len(self.types):
            self.current_type = 0
