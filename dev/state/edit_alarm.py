import screen as scr
from .edit import EditState


class EditAlarmState(EditState):

    def __init__(self, controller):
        super().__init__(controller)
        self.screen = scr.EditScreen(self.controller.display, self.controller.config.alarm_time)

    def left_button_held(self):
        self.controller.config.alarm_time = self.screen.time
        from .alarm import AlarmState
        self.controller.change_state(AlarmState(self.controller))
