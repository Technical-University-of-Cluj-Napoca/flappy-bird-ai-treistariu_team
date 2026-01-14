# src/ui/ui_manager.py
from core.game_state import Screen

class UIManager:

    def __init__(self, game_state):
        self.game_state = game_state
        self.current_screen = None
        self.screens = {}

    def register_screen(self, screen_type, screen_instance):
        self.screens[screen_type] = screen_instance

    def change_screen(self, new_screen_type):
        if self.current_screen:
            self.current_screen.on_exit()

        self.current_screen = self.screens.get(new_screen_type)

        if self.current_screen:
            self.current_screen.on_enter()
            self.game_state.current_screen = new_screen_type

    def handle_event(self, event):
        if self.current_screen:
            self.current_screen.handle_event(event)

    def update(self, dt):
        if self.game_state.next_screen:
            self.change_screen(self.game_state.next_screen)
            self.game_state.next_screen = None

        if self.current_screen:
            self.current_screen.update(dt)


    def draw(self, surface):
        if self.current_screen:
            self.current_screen.draw(surface)
