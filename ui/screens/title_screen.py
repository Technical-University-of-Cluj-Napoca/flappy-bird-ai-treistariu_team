# ui/screens/title_screen.py
import pygame
from ui.screens.base_screen import BaseScreen
from core.game_state import Screen, GameMode
from ui.components.score_popup import ScorePopup

class TitleScreen(BaseScreen):

    def __init__(self, game_state):
        super().__init__(game_state)
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 24)

        self.manual_rect = pygame.Rect(200, 300, 200, 50)
        self.auto_rect = pygame.Rect(200, 370, 200, 50)
        self.score_rect = pygame.Rect(200, 440, 200, 50)

        self.score_popup = ScorePopup(game_state)

    def handle_event(self, event):
        if self.game_state.show_score_popup:
            self.score_popup.handle_event(event)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.manual_rect.collidepoint(event.pos):
                self.game_state.game_mode = GameMode.MANUAL
                self.game_state.next_screen = Screen.SINGER_SELECT

            elif self.auto_rect.collidepoint(event.pos):
                self.game_state.game_mode = GameMode.AUTO
                self.game_state.next_screen = Screen.SINGER_SELECT
                
            elif self.score_rect.collidepoint(event.pos):
                self.game_state.show_score_popup = True


    def update(self, dt):   
        pass

    def draw(self, surface):
        surface.fill((135, 206, 235))  # sky blue

        title = self.font.render("Flappy Bird", True, (255, 255, 255))
        surface.blit(title, (180, 100))

        copyright_text = self.small_font.render(
            "© 2025 YourName", True, (0, 0, 0)
        )
        surface.blit(copyright_text, (10, 460))

        pygame.draw.rect(surface, (0, 200, 0), self.manual_rect)
        pygame.draw.rect(surface, (0, 200, 0), self.auto_rect)
        pygame.draw.rect(surface, (0, 200, 0), self.score_rect)

        surface.blit(
            self.small_font.render("Manual Mode", True, (0, 0, 0)),
            (240, 315)
        )
        surface.blit(
            self.small_font.render("Autonomous Mode", True, (0, 0, 0)),
            (215, 385)
        )
        surface.blit(
            self.small_font.render("Highest Score", True, (0, 0, 0)),
            (225, 455)
        )
        if self.game_state.show_score_popup:
            self.score_popup.draw(surface)

