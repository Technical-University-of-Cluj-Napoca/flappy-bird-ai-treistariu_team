# ui/screens/game_screen.py
import pygame
from ui.screens.base_screen import BaseScreen
from core.game_state import Screen, GameMode
from core.singer_config import SINGER_CONFIG


class GameScreen(BaseScreen):

    def __init__(self, game_state, audio_manager):
        super().__init__(game_state)
        self.audio_manager = audio_manager

        self.font = pygame.font.SysFont(None, 36)

        self.bird_image = None
        self.bird_rect = pygame.Rect(120, 220, 40, 40)


        self.pipe_image = None

        self.pipes = [
            pygame.Rect(350, 0, 60, 160),
            pygame.Rect(350, 300, 60, 200)
        ]

        self.background_image = None



    def handle_event(self, event):
        # Manual mode input (UI responsibility)
        if self.game_state.game_mode == GameMode.MANUAL:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Flap (manual mode)")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("Flap (manual mode)")

    def update(self, dt):
        # TEMP: simulate score increasing
        self.game_state.score += dt

        # TEMP: simulate game over after score reaches 10
        if int(self.game_state.score) >= 10:
            self.game_state.apply_game_over()
            self.game_state.next_screen = Screen.GAME_OVER

    def draw(self, surface):
        # Background
        surface.blit(self.background_image, (0, 0))


        # Pipes
        for i, pipe in enumerate(self.pipes):
            img = pygame.transform.smoothscale(
                self.pipe_image,
                (pipe.width, pipe.height)
            )

            if pipe.y == 0:  # top pipe
                img = pygame.transform.flip(img, False, True)

            surface.blit(img, pipe)



        # Bird
        surface.blit(self.bird_image, self.bird_rect)

        # Score
        score_text = self.font.render(
            str(int(self.game_state.score)), True, (255, 255, 255)
        )
        surface.blit(score_text, (290, 30))
    
    def on_enter(self):
        self.audio_manager.play_singer_music(
            self.game_state.selected_singer
        )
        cfg = SINGER_CONFIG[self.game_state.selected_singer]

        # Load background
        self.background_image = pygame.image.load(cfg["background"]).convert()
        self.background_image = pygame.transform.smoothscale(
            self.background_image,
            (600, 500)  # window size
        )

        # Load bird
        self.bird_image = pygame.image.load(cfg["bird"]).convert_alpha()
        self.bird_image = pygame.transform.smoothscale(
            self.bird_image,
            (self.bird_rect.width, self.bird_rect.height)
        )

        # Load pipe image
        self.pipe_image = pygame.image.load(cfg["pipe"]).convert_alpha()

