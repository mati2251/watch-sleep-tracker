import screen as scr
from .statei import State
import datetime as dt


class AlarmState(State):
    screen: scr.Screen

    def __init__(self, controller):
        super().__init__(controller)
        self.screen = scr.AlarmScreen(controller.display, controller.config.alarm_time)

    def iteration(self):
        self.screen.iteration()
        pass

    def left_button(self):
        from .watch import WatchState
        self.controller.change_state(WatchState(self.controller))

    def right_button(self):
        pass

    def right_button_held(self):
        pass

    def left_button_held(self):
        from .edit_alarm import EditAlarmState
        self.controller.change_state(EditAlarmState(self.controller))
