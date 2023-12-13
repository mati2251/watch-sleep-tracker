import screen as scr
from .statei import State
import datetime as dt


class AlarmState(State):
    screen: scr.Screen

    def __init__(self, time_screen, controller):
        super().__init__(controller)
        self.time_screen = time_screen
        time_screen.time = dt.datetime.combine(dt.datetime.today(), controller.config.alarm_time)
        self.screen = scr.AlarmScreen(time_screen)

    def iteration(self):
        self.screen.iteration()
        pass

    def left_button(self):
        from .watch import WatchState
        self.controller.change_state(WatchState(self.time_screen, self.controller))

    def right_button(self):
        pass

    def right_button_held(self):
        pass

    def left_button_held(self):
        from .edit_alarm import EditAlarmState
        self.controller.change_state(EditAlarmState(self.time_screen, self.controller))
