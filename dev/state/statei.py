from abc import ABC, abstractmethod


class State(ABC):

    def __init__(self, controller):
        self.controller = controller

    @abstractmethod
    def iteration(self):
        pass

    @abstractmethod
    def left_button(self):
        pass

    @abstractmethod
    def right_button(self):
        pass

    @abstractmethod
    def right_button_held(self):
        pass

    @abstractmethod
    def left_button_held(self):
        pass
