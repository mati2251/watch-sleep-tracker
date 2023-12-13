from screen import Screen
import datetime


class EditScreen(Screen):
    blink_time_iterator = 0
    is_flash = False

    def __init__(self, screen):
        self.screen = screen
        self.display = screen.display

    def iteration(self):
        self.display.fill_rect(17, 9, 64, 16, 0)
        self.blink_time_iterator += 1
        if self.blink_time_iterator >= 8:
            self.blink_time_iterator = 0
            self.is_flash = not self.is_flash
        if self.is_flash:
            self.screen.iteration()
        else:
            self.display.fill(0)
            self.display.show()
            self.blink_time_iterator += 2
        pass

    def add_minute(self):
        self.screen.time += datetime.timedelta(minutes=1)
        self.time = self.screen.time

    def subtract_minute(self):
        self.screen.time -= datetime.timedelta(minutes=1)
        self.time = self.screen.time

