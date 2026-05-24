import os
import sys

import pygame


class Menu:

    def __init__(self, screen: pygame.Surface):

        # tela principal
        self.screen = screen

        # tamanho da janela
        self.width, self.height = screen.get_size()

        # controla se o menu ainda está aberto
        self.active = True

        # =====================================================
        # CAMINHOS DOS ARQUIVOS
        # =====================================================

        # pasta principal do projeto
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # pasta da tela inicial
        assets_dir = os.path.join(
            base_dir,
            "assets",
            "main screen"
        )

        # =====================================================
        # BACKGROUND
        # =====================================================

        bg_path = os.path.join(
            assets_dir,
            "backgroundmainscreen.jpg"
        )

        # carrega imagem
        raw_bg = pygame.image.load(bg_path).convert()

        # ajusta para tamanho da tela
        self.background = pygame.transform.scale(
            raw_bg,
            (self.width, self.height)
        )

        # =====================================================
        # MÚSICA
        # =====================================================

        self.music_path = os.path.join(
            base_dir,
            "assets",
            "sounds",
            "mainscreen.mp3"
        )

        # =====================================================
        # FONTES
        # =====================================================

        self.font_prompt = pygame.font.SysFont(
            "palatino linotype",
            38,
            bold=True
        )

        # =====================================================
        # ANIMAÇÕES
        # =====================================================

        # controla efeito piscando
        self._blink_timer = 0
        self._blink_visible = True

        # tempo do pisca em milissegundos
        self.BLINK_INTERVAL = 700

        # contador geral
        self._time = 0

    # =========================================================
    # TOCA MÚSICA
    # =========================================================
    def start_music(self):

        # verifica se mixer foi iniciado
        if not pygame.mixer.get_init():
            return

        # evita tocar música duplicada
        if pygame.mixer.music.get_busy():
            return

        try:

            pygame.mixer.music.load(self.music_path)

            pygame.mixer.music.set_volume(0.6)

            # -1 = loop infinito
            pygame.mixer.music.play(-1)

        except pygame.error as erro:

            print(
                f"[Menu] Erro ao carregar música: {erro}"
            )

    # =========================================================
    # PARA MÚSICA
    # =========================================================
    def stop_music(self):

        if pygame.mixer.get_init():

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

    # =========================================================
    # EVENTOS
    # =========================================================
    def handle_event(self, event: pygame.event.Event):

        # ENTER inicia o jogo
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_RETURN
        ):

            self.stop_music()

            self.active = False

            return True

        # fechar janela
        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        return False

    # =========================================================
    # UPDATE
    # =========================================================
    def update(self, dt: int):

        # tempo total
        self._time += dt

        # timer do pisca
        self._blink_timer += dt

        # alterna visibilidade
        if self._blink_timer >= self.BLINK_INTERVAL:

            self._blink_timer -= self.BLINK_INTERVAL

            self._blink_visible = (
                not self._blink_visible
            )

    # =========================================================
    # TEXTO COM CONTORNO
    # =========================================================
    def _draw_outlined(
        self,
        font,
        text,
        color,
        outline_color,
        center,
        outline_size=3
    ):

        cx, cy = center

        # texto da borda
        outline_surf = font.render(
            text,
            True,
            outline_color
        )

        # posições da sombra
        offsets = [

            (-outline_size, 0),
            (outline_size, 0),
            (0, -outline_size),
            (0, outline_size),

            (-outline_size, -outline_size),
            (outline_size, -outline_size),

            (-outline_size, outline_size),
            (outline_size, outline_size)

        ]

        # desenha borda
        for ox, oy in offsets:

            rect = outline_surf.get_rect(
                center=(cx + ox, cy + oy)
            )

            self.screen.blit(
                outline_surf,
                rect
            )

        # texto principal
        main_surf = font.render(
            text,
            True,
            color
        )

        main_rect = main_surf.get_rect(
            center=(cx, cy)
        )

        self.screen.blit(
            main_surf,
            main_rect
        )

    # =========================================================
    # LINHA DECORATIVA
    # =========================================================
    def _draw_divider(
        self,
        cy,
        color=(200, 170, 50),
        alpha=180
    ):

        # margem lateral
        margin = self.width // 6

        # superfície transparente
        surf = pygame.Surface(
            (self.width - margin * 2, 2),
            pygame.SRCALPHA
        )

        w = surf.get_width()

        # cria fade nas pontas
        for x in range(w):

            t = x / w

            fade = int(
                255 * (1 - abs(t - 0.5) * 2)
            )

            surf.set_at(
                (x, 0),
                (*color, min(fade, alpha))
            )

            surf.set_at(
                (x, 1),
                (*color, min(fade // 2, alpha))
            )

        # desenha linha
        self.screen.blit(
            surf,
            (margin, cy)
        )

    # =========================================================
    # DESENHA MENU
    # =========================================================
    def draw(self):

        # fundo
        self.screen.blit(
            self.background,
            (0, 0)
        )

        # centro horizontal
        cx = self.width // 2

        # =====================================================
        # BARRA ESCURA INFERIOR
        # =====================================================

        footer_h = 90

        footer = pygame.Surface(
            (self.width, footer_h),
            pygame.SRCALPHA
        )

        footer.fill((0, 0, 0, 130))

        self.screen.blit(
            footer,
            (0, self.height - footer_h)
        )

        # =====================================================
        # LINHA DECORATIVA
        # =====================================================

        self._draw_divider(
            self.height - footer_h + 4
        )

        # =====================================================
        # TEXTO "PRESS ENTER"
        # =====================================================

        if self._blink_visible:

            self._draw_outlined(

                self.font_prompt,

                "* PRESS ENTER TO START *",

                (255, 220, 80),

                (60, 30, 0),

                (
                    cx,
                    self.height - footer_h // 2
                ),

                outline_size=3
            )

    # =========================================================
    # LOOP DO MENU
    # =========================================================
    def run(self):

        self.start_music()

        clock = pygame.time.Clock()

        while self.active:

            # delta time
            dt = clock.tick(60)

            # eventos
            for event in pygame.event.get():

                self.handle_event(event)

            # atualiza
            self.update(dt)

            # desenha
            self.draw()

            # atualiza tela
            pygame.display.flip()