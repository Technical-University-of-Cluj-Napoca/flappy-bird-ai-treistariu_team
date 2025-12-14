import pygame
from ui.screens.base_screen import BaseScreen
from core.game_state import Screen, Singer
from ui.components.avatar_card import AvatarCard
from core.singer_config import SINGER_CONFIG
from ui.components.back_button import BackButton


class SingerSelectScreen(BaseScreen):

    def __init__(self, game_state):
        super().__init__(game_state)

        self.title_font = pygame.font.SysFont(None, 42)
        self.back_button = BackButton()

        self.cards = [
            AvatarCard(
                pygame.Rect(60, 180, 150, 180),
                Singer.TR,
                "Trestariu",
                SINGER_CONFIG[Singer.TR]["bird"]
            ),
            AvatarCard(
                pygame.Rect(225, 180, 150, 180),
                Singer.DB,
                "Dan Balan",
                SINGER_CONFIG[Singer.DB]["bird"]
            ),
            AvatarCard(
                pygame.Rect(390, 180, 150, 180),
                Singer.CR,
                "Cristi din Banat",
                SINGER_CONFIG[Singer.CR]["bird"]
            ),
        ]


        self.continue_rect = pygame.Rect(200, 380, 200, 50)

    def handle_event(self, event):
        self.back_button.handle_event(
            event,
            lambda: setattr(self.game_state, "next_screen", Screen.TITLE)
        )

        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in self.cards:
                if card.is_clicked(event.pos):
                    self.game_state.selected_singer = card.singer

            if self.continue_rect.collidepoint(event.pos):
                self.game_state.next_screen = Screen.TUTORIAL

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((120, 180, 240))
        self.back_button.draw(surface)


        title = self.title_font.render("Choose Your Singer", True, (0, 0, 0))
        surface.blit(title, (170, 80))

        for card in self.cards:
            card.draw(
                surface,
                selected=(card.singer == self.game_state.selected_singer)
            )

        pygame.draw.rect(surface, (0, 180, 0), self.continue_rect)
        txt = pygame.font.SysFont(None, 30).render("Continue", True, (0, 0, 0))
        surface.blit(txt, (260, 392))
