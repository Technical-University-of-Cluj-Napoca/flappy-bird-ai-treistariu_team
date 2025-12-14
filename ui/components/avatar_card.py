import pygame

class AvatarCard:

    def __init__(self, rect, singer, label, image_path):
        self.rect = rect
        self.singer = singer
        self.label = label

        self.font = pygame.font.SysFont(None, 24)

        # Load and scale image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(
            self.image,
            (rect.width - 20, rect.height - 50)
        )

    def draw(self, surface, selected=False):
        # Card background
        color = (0, 200, 0) if selected else (200, 200, 200)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        # Draw image
        surface.blit(
            self.image,
            (self.rect.x + 10, self.rect.y + 10)
        )

        # Draw label
        text = self.font.render(self.label, True, (0, 0, 0))
        surface.blit(
            text,
            (
                self.rect.centerx - text.get_width() // 2,
                self.rect.bottom - 30
            )
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
