import datetime as dt

from screen import Screen


class StopwatchScreen(Screen):
    start_time: dt.datetime = None
    countdown_time: dt.datetime = dt.datetime.combine(dt.datetime.today(), dt.time(0, 20, 0))

    def __init__(self, screen: Screen):
        self.screen = screen

    def iteration(self):
        if self.start_time is not None:
            self.screen.time = self.countdown_time + (self.start_time - dt.datetime.now())
        else:
            self.screen.time = self.countdown_time
        self.screen.iteration()

    def start(self):
        self.start_time = dt.datetime.now()

    def stop(self):
        self.countdown_time = self.screen.time
        self.start_time = None
