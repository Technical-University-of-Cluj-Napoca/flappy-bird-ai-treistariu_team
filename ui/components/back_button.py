import pygame

class BackButton:
    def __init__(self, x=20, y=20, width=80, height=35):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 24)

    def handle_event(self, event, callback):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                callback()

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect, border_radius=6)
        text = self.font.render("Back", True, (0, 0, 0))
        surface.blit(
            text,
            (
                self.rect.centerx - text.get_width() // 2,
                self.rect.centery - text.get_height() // 2
            )
        )
