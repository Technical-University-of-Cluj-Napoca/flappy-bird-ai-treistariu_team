# ui/screens/game_screen.py
import pygame
from ui.screens.base_screen import BaseScreen
from core.game_state import Screen, GameMode
from core.singer_config import SINGER_CONFIG
from core.game_engine import GameEngine
from core.autonomous import AutonomousController


class GameScreen(BaseScreen):
    WINDOW_W, WINDOW_H = 600, 500

    def __init__(self, game_state, audio_manager):
        super().__init__(game_state)
        self.audio_manager = audio_manager

        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 22)

        self.background_image = None
        self.bird_image = None
        self.pipe_image = None

        # Engine + AI controller
        self.engine = GameEngine(population_size=20)
        self.auto_controller = AutonomousController(population_size=20)

        self.flap_requested = False

    def on_enter(self):
        # Music + assets
        self.audio_manager.play_singer_music(self.game_state.selected_singer)
        cfg = SINGER_CONFIG[self.game_state.selected_singer]

        self.game_state.reset_run()

        self.background_image = pygame.image.load(cfg["background"]).convert()
        self.background_image = pygame.transform.smoothscale(
            self.background_image, (self.WINDOW_W, self.WINDOW_H)
        )

        self.pipe_image = pygame.image.load(cfg["pipe"]).convert_alpha()

        self.bird_image = pygame.image.load(cfg["bird"]).convert_alpha()
        self.bird_image = pygame.transform.smoothscale(self.bird_image, (40, 40))

        # Reset depending on mode
        if self.game_state.game_mode == GameMode.MANUAL:
            self.engine.reset_manual()
        else:
            self.auto_controller.reset()
            self.auto_controller.start_generation()
            self.engine.reset_population(self.auto_controller.population)

        self.flap_requested = False

    def handle_event(self, event):
        if self.game_state.game_mode == GameMode.MANUAL:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.flap_requested = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.flap_requested = True

    def update(self, dt):
        if self.game_state.game_mode == GameMode.MANUAL:
            self.engine.update(dt, self.flap_requested)
            self.flap_requested = False

            self.game_state.score = int(self.engine.score)

            if not self.engine.alive:
                self.game_state.apply_game_over()
                self.game_state.next_screen = Screen.GAME_OVER

        else:
            # AUTO mode: no user input
            self.engine.update_auto(dt, self.auto_controller)

            # display score as best fitness/pipes passed
            self.game_state.score = int(self.auto_controller.best_fitness)
            self.game_state.best_auto = max(self.game_state.best_auto, self.game_state.score)

    def draw(self, surface):
        if self.background_image:
            surface.blit(self.background_image, (0, 0))

        # Pipes
        if self.pipe_image:
            for pair in self.engine.pipes:
                top_pipe = pair["top"]
                bottom_pipe = pair["bottom"]

                top_img = pygame.transform.smoothscale(self.pipe_image, (top_pipe.width, top_pipe.height))
                top_img = pygame.transform.flip(top_img, False, True)
                surface.blit(top_img, top_pipe)

                bottom_img = pygame.transform.smoothscale(self.pipe_image, (bottom_pipe.width, bottom_pipe.height))
                surface.blit(bottom_img, bottom_pipe)

        # Birds
        if self.bird_image:
            if self.game_state.game_mode == GameMode.MANUAL:
                surface.blit(self.bird_image, self.engine.bird_rect)
            else:
                for rect in self.engine.get_alive_bird_rects():
                    surface.blit(self.bird_image, rect)

        # Score
        score_text = self.font.render(str(int(self.game_state.score)), True, (255, 255, 255))
        surface.blit(score_text, (290, 30))

        # AUTO HUD
        if self.game_state.game_mode == GameMode.AUTO:
            status = self.auto_controller.population_status()
            hud = f"Gen {status['generation']}  Alive {status['alive']}/{status['total']}  Best {int(status['best_fitness'])}"
            hud_text = self.small_font.render(hud, True, (255, 255, 255))
            surface.blit(hud_text, (10, 10))
