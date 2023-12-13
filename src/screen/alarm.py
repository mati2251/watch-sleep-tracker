from screen import Screen
import datetime


class AlarmScreen(Screen):
    def __init__(self, screen):
        self.screen = screen
        self.screen.time = datetime.datetime.combine(datetime.datetime.today(), datetime.time(8, 0, 0))

    def iteration(self):
            self.screen.iteration()
