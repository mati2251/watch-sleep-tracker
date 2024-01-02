import screen as scr
from .edit import EditState


class EditCountdownState(EditState):

    def __init__(self, controller):
        super().__init__(controller)
        self.screen = scr.EditScreen(self.controller.display, self.controller.config.countdown_time)

    def left_button_held(self):
        self.controller.config.countdown_time = self.screen.time
        from .countdown import CountdownState
        self.controller.change_state(CountdownState(self.controller))
