import screen as scr
from .statei import State


class AlarmState(State):
    screen: scr.AlarmScreen

    def __init__(self, controller):
        super().__init__(controller)
        self.screen = scr.AlarmScreen(controller.display, controller.config.alarm_time, controller.config.alarm_enabled)

    def iteration(self):
        self.screen.clear()
        self.screen.iteration()
        pass

    def left_button(self):
        from .watch import WatchState
        self.controller.change_state(WatchState(self.controller))

    def right_button(self):
        self.controller.config.alarm_enabled = not self.controller.config.alarm_enabled
        self.screen.enable = self.controller.config.alarm_enabled
        pass

    def right_button_held(self):
        pass

    def left_button_held(self):
        from .edit_alarm import EditAlarmState
        self.controller.change_state(EditAlarmState(self.controller))
