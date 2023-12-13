from screen import Screen
import datetime


class WatchScreen(Screen):
    def __init__(self, screen):
        self.screen = screen

    def iteration(self):
        self.screen.time = datetime.datetime.now()
        self.screen.iteration()
