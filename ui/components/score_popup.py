import pygame


class ScorePopup:

    def __init__(self, game_state):
        self.game_state = game_state

        self.rect = pygame.Rect(150, 150, 300, 200)
        self.close_rect = pygame.Rect(410, 160, 30, 30)

        self.font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 32)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_rect.collidepoint(event.pos):
                self.game_state.show_score_popup = False

    def draw(self, surface):
        # dark overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        # popup box
        pygame.draw.rect(surface, (240, 240, 240), self.rect, border_radius=10)

        # close button
        pygame.draw.rect(surface, (200, 50, 50), self.close_rect)
        surface.blit(
            self.font.render("X", True, (255, 255, 255)),
            (418, 165)
        )

        # title
        title = self.title_font.render("Highest Scores", True, (0, 0, 0))
        surface.blit(title, (220, 165))

        # scores
        manual = self.font.render(
            f"Manual Mode: {self.game_state.best_manual}", True, (0, 0, 0)
        )
        auto = self.font.render(
            f"Autonomous Mode: {self.game_state.best_auto}", True, (0, 0, 0)
        )

        surface.blit(manual, (200, 220))
        surface.blit(auto, (200, 260))
