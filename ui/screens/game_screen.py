# ui/screens/game_screen.py
import pygame
from ui.screens.base_screen import BaseScreen
from core.game_state import Screen, GameMode
from core.singer_config import SINGER_CONFIG
from core.game_engine import GameEngine


class GameScreen(BaseScreen):
    WINDOW_W, WINDOW_H = 600, 500

    def __init__(self, game_state, audio_manager):
        super().__init__(game_state)
        self.audio_manager = audio_manager

        self.font = pygame.font.SysFont(None, 36)

        self.background_image = None
        self.bird_image = None
        self.pipe_image = None

        # Member 1 engine
        self.engine = GameEngine()

        # Manual input flag
        self.flap_requested = False

    def on_enter(self):
        # Start music
        self.audio_manager.play_singer_music(self.game_state.selected_singer)
        cfg = SINGER_CONFIG[self.game_state.selected_singer]

        # Reset run state + engine
        self.game_state.reset_run()
        self.engine.reset()

        # Background
        self.background_image = pygame.image.load(cfg["background"]).convert()
        self.background_image = pygame.transform.smoothscale(
            self.background_image, (self.WINDOW_W, self.WINDOW_H)
        )

        # Bird
        self.bird_image = pygame.image.load(cfg["bird"]).convert_alpha()
        self.bird_image = pygame.transform.smoothscale(
            self.bird_image,
            (self.engine.bird_rect.width, self.engine.bird_rect.height),
        )

        # Pipes
        self.pipe_image = pygame.image.load(cfg["pipe"]).convert_alpha()

        # Reset input
        self.flap_requested = False

    def handle_event(self, event):
        if self.game_state.game_mode == GameMode.MANUAL:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.flap_requested = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.flap_requested = True

    def update(self, dt):
        self.engine.update(dt, self.flap_requested)
        self.flap_requested = False

        # Sync score into shared game_state (used by UI screens)
        self.game_state.score = self.engine.score

        # Death -> game over screen
        if not self.engine.alive:
            self.game_state.apply_game_over()
            self.game_state.next_screen = Screen.GAME_OVER

    def draw(self, surface):
        # Background
        if self.background_image:
            surface.blit(self.background_image, (0, 0))

        # Pipes
        if self.pipe_image:
            for pair in self.engine.pipes:
                top_pipe = pair["top"]
                bottom_pipe = pair["bottom"]

                # Top pipe (flip vertically)
                top_img = pygame.transform.smoothscale(
                    self.pipe_image, (top_pipe.width, top_pipe.height)
                )
                top_img = pygame.transform.flip(top_img, False, True)
                surface.blit(top_img, top_pipe)

                # Bottom pipe
                bottom_img = pygame.transform.smoothscale(
                    self.pipe_image, (bottom_pipe.width, bottom_pipe.height)
                )
                surface.blit(bottom_img, bottom_pipe)

        # Bird
        if self.bird_image:
            surface.blit(self.bird_image, self.engine.bird_rect)

        # Score
        score_text = self.font.render(str(int(self.game_state.score)), True, (255, 255, 255))
        surface.blit(score_text, (290, 30))
