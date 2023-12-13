from screen import Screen
import datetime


class AlarmScreen(Screen):
    def __init__(self, screen):
        self.screen = screen
        self.screen.time = self.screen.time
        print(self.screen.time)
        self.display = screen.display

    def iteration(self):
            self.screen.iteration()
