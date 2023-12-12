from abc import ABC, abstractmethod

class ScreenStrategy(ABC):
    @abstractmethod
    def start(self):
        pass
