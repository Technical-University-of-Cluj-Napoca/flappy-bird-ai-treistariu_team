# src/ui/screens/base_screen.py
from abc import ABC, abstractmethod

class BaseScreen(ABC):

    def __init__(self, game_state):
        self.game_state = game_state

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def on_enter(self):
        """Called when this screen becomes active"""
        pass

    def on_exit(self):
        """Called when this screen is removed"""
        pass
