import pygame

from core.settings import HEIGHT, HUD_HEIGHT, HUD_Y, WIDTH

OURO = (180, 140, 60)
OURO_ESC = (100, 75, 25)
OURO_BRIL = (220, 185, 90)
PERGAMINHO = (240, 230, 210)


class Hud:
    def __init__(self, key_icon: pygame.Surface):
        self.key_icon = pygame.transform.scale(key_icon, (28, 28))
        self.font_large = self._load_font(19, bold=True)
        self.font_small = self._load_font(17)
        self.bg = self._build_bg()

    def _load_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        for name in ["Palatino Linotype", "Book Antiqua", "Garamond", "Times New Roman"]:
            font = pygame.font.SysFont(name, size, bold=bold)
            if font:
                return font
        return pygame.font.SysFont(None, size, bold=bold)

    def _build_bg(self) -> pygame.Surface:
        surface = pygame.Surface((WIDTH, HUD_HEIGHT))
        surface.fill((0, 0, 0))
        pygame.draw.line(surface, OURO_ESC, (0, 0), (WIDTH, 0), 1)
        pygame.draw.line(surface, OURO, (0, 2), (WIDTH, 2), 1)
        pygame.draw.line(surface, OURO_BRIL, (0, 3), (WIDTH, 3), 2)
        pygame.draw.line(surface, OURO, (0, 5), (WIDTH, 5), 1)
        pygame.draw.line(surface, OURO_ESC, (0, 6), (WIDTH, 6), 1)

        center_x = WIDTH // 2
        pygame.draw.line(surface, OURO_ESC, (center_x - 1, 10), (center_x - 1, HUD_HEIGHT - 6), 1)
        pygame.draw.line(surface, OURO, (center_x, 8), (center_x, HUD_HEIGHT - 5), 1)
        pygame.draw.line(surface, OURO_ESC, (center_x + 1, 10), (center_x + 1, HUD_HEIGHT - 6), 1)

        middle = HUD_HEIGHT // 2
        diamond = [(center_x, 5), (center_x + 6, middle), (center_x, HUD_HEIGHT - 6), (center_x - 6, middle)]
        pygame.draw.polygon(surface, OURO, diamond)
        pygame.draw.polygon(surface, OURO_BRIL, diamond, 1)

        for x in [6, WIDTH - 12]:
            pygame.draw.rect(surface, OURO, (x, 10, 6, 6))
            pygame.draw.rect(surface, OURO_BRIL, (x, 10, 6, 6), 1)

        return surface

    def draw(self, surface: pygame.Surface, collected_keys: int, total_keys: int, stage: int) -> None:
        surface.blit(self.bg, (0, HUD_Y))

        center_x = WIDTH // 2
        center_y = HUD_Y + HUD_HEIGHT // 2

        left = center_x // 2
        stage_label = self.font_small.render("✦  FASE  ✦", True, OURO)
        stage_value = self.font_large.render(str(stage), True, OURO_BRIL)
        surface.blit(stage_label, (left - stage_label.get_width() // 2, HUD_Y + 9))
        surface.blit(stage_value, (left - stage_value.get_width() // 2, HUD_Y + 24))

        right = center_x + center_x // 2
        keys_label = self.font_small.render("CHAVES", True, OURO)
        keys_value = self.font_large.render(f"{collected_keys} / {total_keys}", True, PERGAMINHO)
        surface.blit(keys_label, (right - keys_label.get_width() // 2, HUD_Y + 9))

        block_w = self.key_icon.get_width() + 6 + keys_value.get_width()
        icon_x = right - block_w // 2
        icon_y = center_y - self.key_icon.get_height() // 2 + 4
        surface.blit(self.key_icon, (icon_x, icon_y))
        surface.blit(keys_value, (icon_x + self.key_icon.get_width() + 6, center_y - keys_value.get_height() // 2 + 4))