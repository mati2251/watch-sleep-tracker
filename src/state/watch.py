import screen as scr
from .statei import State


class WatchState(State):
    screen: scr.Screen

    def __init__(self, controller):
        super().__init__(controller)
        self.screen = scr.WatchScreen(controller.display)

    def iteration(self):
        self.screen.clear()
        self.screen.iteration()
        pass

    def left_button(self):
        from .countdown import CountdownState
        self.controller.change_state(CountdownState(self.controller))

    def right_button(self):
        pass

    def right_button_held(self):
        pass

    def left_button_held(self):
        pass
