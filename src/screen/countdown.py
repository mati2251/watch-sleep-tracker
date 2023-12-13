import datetime as dt

from screen import Screen


class CountdownScreen(Screen):
    start_time: dt.datetime = None
    countdown_time: dt.datetime

    def __init__(self, screen: Screen, countdown_time: dt.time = dt.time(0, 20, 0)):
        self.screen = screen
        self.display = screen.display
        self.countdown_time = dt.datetime.combine(dt.datetime.today(), countdown_time)

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

    def reset(self):
        self.stop()
        self.countdown_time = dt.datetime.combine(dt.datetime.today(), dt.time(0, 20, 0))
        self.screen.time = self.countdown_time

    def start_stop(self):
        if self.start_time is None:
            self.start()
        else:
            self.stop()
