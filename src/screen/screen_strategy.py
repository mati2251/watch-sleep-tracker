from abc import ABC, abstractmethod

class ScreenStrategy(ABC):
    @abstractmethod
    def display(self):
        pass
