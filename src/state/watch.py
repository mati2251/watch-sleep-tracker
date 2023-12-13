import screen as scr
from .statei import State


class WatchState(State):
    screen: scr.Screen

    def __init__(self, time_screen, controller):
        super().__init__(controller)
        self.time_screen = time_screen
        self.screen = scr.WatchScreen(time_screen)

    def iteration(self):
        self.screen.iteration()
        pass

    def left_button(self):
        from .countdown import CountdownState
        self.controller.change_state(CountdownState(self.time_screen, self.controller))

    def right_button(self):
        pass

    def right_button_held(self):
        pass

    def left_button_held(self):
        pass
