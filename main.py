import pygame
import sys

from core.game_state import GameState, Screen
from ui.ui_manager import UIManager
from ui.audio_manager import AudioManager

from ui.screens.title_screen import TitleScreen
from ui.screens.singer_select_screen import SingerSelectScreen
from ui.screens.tutorial_screen import TutorialScreen
from ui.screens.game_screen import GameScreen
from ui.screens.game_over_screen import GameOverScreen


def main():
    pygame.init()

    WIDTH, HEIGHT = 600, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird UI Test")

    clock = pygame.time.Clock()

    # ✅ Create state first
    game_state = GameState()

    # ✅ Create audio manager BEFORE screens that need it
    audio_manager = AudioManager()

    # ✅ Create UI manager
    ui_manager = UIManager(game_state)

    # ✅ Create screens
    title_screen = TitleScreen(game_state)
    singer_select_screen = SingerSelectScreen(game_state)
    tutorial_screen = TutorialScreen(game_state)
    game_screen = GameScreen(game_state, audio_manager)          # ✅ now works
    game_over_screen = GameOverScreen(game_state, audio_manager) # ✅ now works

    # ✅ Register screens
    ui_manager.register_screen(Screen.TITLE, title_screen)
    ui_manager.register_screen(Screen.SINGER_SELECT, singer_select_screen)
    ui_manager.register_screen(Screen.TUTORIAL, tutorial_screen)
    ui_manager.register_screen(Screen.PLAYING, game_screen)
    ui_manager.register_screen(Screen.GAME_OVER, game_over_screen)

    ui_manager.change_screen(Screen.TITLE)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui_manager.handle_event(event)

        ui_manager.update(dt)
        ui_manager.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
