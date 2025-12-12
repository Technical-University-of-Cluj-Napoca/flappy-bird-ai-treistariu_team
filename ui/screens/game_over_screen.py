# ui/screens/game_over_screen.py
import pygame
from ui.screens.base_screen import BaseScreen
from core.game_state import Screen, GameMode


class GameOverScreen(BaseScreen):

    def __init__(self, game_state, audio_manager):
        super().__init__(game_state)
        self.audio_manager = audio_manager


        self.title_font = pygame.font.SysFont(None, 48)
        self.text_font = pygame.font.SysFont(None, 28)
        self.button_font = pygame.font.SysFont(None, 30)

        self.menu_rect = pygame.Rect(200, 450, 200, 50)

        self.replay_rect = pygame.Rect(200, 320, 200, 50)
        self.share_rect = pygame.Rect(200, 390, 200, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.replay_rect.collidepoint(event.pos):
                # restart same mode
                self.game_state.reset_run()
                self.game_state.next_screen = Screen.PLAYING

            elif self.share_rect.collidepoint(event.pos):
                print("Share button clicked (optional feature)")
            elif self.menu_rect.collidepoint(event.pos):
                self.game_state.next_screen = Screen.TITLE


    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((200, 200, 200))

        # Title
        title = self.title_font.render("Game Over", True, (0, 0, 0))
        surface.blit(title, (200, 80))

        # Current score
        score_text = self.text_font.render(
            f"Score: {int(self.game_state.score)}", True, (0, 0, 0)
        )
        surface.blit(score_text, (230, 160))

        # Best score (mode dependent)
        if self.game_state.game_mode == GameMode.MANUAL:
            best = self.game_state.best_manual
        else:
            best = self.game_state.best_auto

        best_text = self.text_font.render(
            f"Best: {best}", True, (0, 0, 0)
        )
        surface.blit(best_text, (240, 200))

        # Replay button
        pygame.draw.rect(surface, (0, 180, 0), self.replay_rect)
        replay_text = self.button_font.render("Replay", True, (0, 0, 0))
        surface.blit(replay_text, (260, 335))

        # Share button (dummy)
        pygame.draw.rect(surface, (0, 150, 200), self.share_rect)
        share_text = self.button_font.render("Share", True, (0, 0, 0))
        surface.blit(share_text, (270, 405))

        pygame.draw.rect(surface, (180, 180, 180), self.menu_rect)
        menu_text = self.button_font.render("Main Menu", True, (0, 0, 0))
        surface.blit(menu_text, (240, 465))

def on_enter(self):
    self.audio_manager.stop_music()
