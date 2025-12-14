# ui/screens/tutorial_screen.py
import pygame
from ui.screens.base_screen import BaseScreen
from core.game_state import Screen, GameMode


class TutorialScreen(BaseScreen):

    def __init__(self, game_state):
        super().__init__(game_state)

        self.title_font = pygame.font.SysFont(None, 40)
        self.text_font = pygame.font.SysFont(None, 26)
        self.button_font = pygame.font.SysFont(None, 30)

        self.start_rect = pygame.Rect(200, 380, 200, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_rect.collidepoint(event.pos):
                # reset score and go to game
                self.game_state.reset_run()
                self.game_state.next_screen = Screen.PLAYING

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((150, 200, 255))

        # Title
        title = self.title_font.render("How to Play", True, (0, 0, 0))
        surface.blit(title, (210, 80))

        # Mode-dependent tutorial text
        if self.game_state.game_mode == GameMode.MANUAL:
            lines = [
                "Manual Mode",
                "",
                "Click the mouse or press SPACE",
                "to flap the bird.",
                "Avoid the pipes and the ground.",
                "",
                "Each pipe passed gives +1 point."
            ]
        else:
            lines = [
                "Autonomous Mode",
                "",
                "Watch birds learn how to fly.",
                "They evolve using genetic algorithms.",
                "Only the strongest survive.",
                "",
                "Sit back and observe."
            ]

        y = 150
        for line in lines:
            text = self.text_font.render(line, True, (0, 0, 0))
            surface.blit(text, (160, y))
            y += 30

        # Start button
        pygame.draw.rect(surface, (0, 180, 0), self.start_rect)
        start_text = self.button_font.render("Start", True, (0, 0, 0))
        surface.blit(start_text, (260, 392))
