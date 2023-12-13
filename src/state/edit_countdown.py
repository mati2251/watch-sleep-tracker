import screen as scr
from .edit import EditState


class EditCountdownState(EditState):

    def left_button_held(self):
        self.controller.config.countdown_time = self.screen.time.time()
        from .countdown import CountdownState
        self.controller.change_state(CountdownState(self.time_screen, self.controller))
