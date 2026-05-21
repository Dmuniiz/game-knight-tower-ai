import pygame
import sys
import os


class Menu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.active = True

        # ── Assets paths ──────────────────────────────────────────────
        base_dir   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_dir = os.path.join(base_dir, "assets", "main screen")

        # Background
        bg_path = os.path.join(assets_dir, "backgroundmainscreen.jpg")
        raw_bg  = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(raw_bg, (self.width, self.height))

        # Music
        self.music_path = os.path.join(base_dir, "assets", "sounds", "mainscreen.mp3")

        # Fonts
        self.font_prompt = pygame.font.SysFont("palatino linotype", 38, bold=True)

        # Animações
        self._blink_timer   = 0
        self._blink_visible = True
        self.BLINK_INTERVAL = 700  # ms

        self._time = 0  # contador geral para efeitos

    # ─────────────────────────────────────────────────────────────────
    def start_music(self):
        if not pygame.mixer.get_init():
            return
        if pygame.mixer.music.get_busy():
            return
        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"[Menu] Could not load music: {e}")

    def stop_music(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    # ─────────────────────────────────────────────────────────────────
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.stop_music()
            self.active = False
            return True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        return False

    # ─────────────────────────────────────────────────────────────────
    def update(self, dt: int):
        self._time += dt
        self._blink_timer += dt
        if self._blink_timer >= self.BLINK_INTERVAL:
            self._blink_timer  -= self.BLINK_INTERVAL
            self._blink_visible = not self._blink_visible

    # ─────────────────────────────────────────────────────────────────
    def _draw_outlined(self, font, text, color, outline_color, center, outline_size=3):
        cx, cy = center
        outline_surf = font.render(text, True, outline_color)
        offsets = [(-outline_size, 0), (outline_size, 0), (0, -outline_size), (0, outline_size),
                   (-outline_size, -outline_size), (outline_size, -outline_size),
                   (-outline_size, outline_size), (outline_size, outline_size)]
        for ox, oy in offsets:
            r = outline_surf.get_rect(center=(cx + ox, cy + oy))
            self.screen.blit(outline_surf, r)
        main_surf = font.render(text, True, color)
        main_rect = main_surf.get_rect(center=(cx, cy))
        self.screen.blit(main_surf, main_rect)

    def _draw_divider(self, cy, color=(200, 170, 50), alpha=180):
        """Linha decorativa horizontal com fade nas bordas."""
        margin = self.width // 6
        surf = pygame.Surface((self.width - margin * 2, 2), pygame.SRCALPHA)
        w = surf.get_width()
        for x in range(w):
            # fade nas pontas
            t = x / w
            fade = int(255 * (1 - abs(t - 0.5) * 2))
            surf.set_at((x, 0), (*color, min(fade, alpha)))
            surf.set_at((x, 1), (*color, min(fade // 2, alpha)))
        self.screen.blit(surf, (margin, cy))

    # ─────────────────────────────────────────────────────────────────
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        cx = self.width  // 2
        

        # ── Faixa escura na parte inferior para o prompt ───────────
        footer_h = 90
        footer = pygame.Surface((self.width, footer_h), pygame.SRCALPHA)
        footer.fill((0, 0, 0, 130))
        self.screen.blit(footer, (0, self.height - footer_h))

        # ── Linha decorativa acima do prompt ──────────────────────
        self._draw_divider(self.height - footer_h + 4)

        # ── PRESS ENTER TO START piscando ──────────────────────────
        if self._blink_visible:
            self._draw_outlined(
                self.font_prompt,
                "* PRESS ENTER TO START *",
                (255, 220, 80),
                (60, 30, 0),
                (cx, self.height - footer_h // 2),
                outline_size=3
            )

    # ─────────────────────────────────────────────────────────────────
    def run(self) -> None:
        self.start_music()
        clock = pygame.time.Clock()
        while self.active:
            dt = clock.tick(60)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()
            pygame.display.flip()