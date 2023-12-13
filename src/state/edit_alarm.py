import screen as scr
from .edit import EditState


class EditAlarmState(EditState):

    def left_button_held(self):
        self.controller.config.alarm_time = self.screen.time.time()
        from .alarm import AlarmState
        self.controller.change_state(AlarmState(self.time_screen, self.controller))
