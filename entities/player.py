import pygame

ESCALA = 0.30

SHEETS = {
    "frente": {"path": "assets/sprites/cavaleiro_frente_walk.png", "frames": 3, "frame_w": 108, "frame_h": 175},
    "costas": {"path": "assets/sprites/cavaleiro_costas_walk.png", "frames": 3, "frame_w": 108, "frame_h": 175},
    "lado":   {"path": "assets/sprites/cavaleiro_lado_walk.png",   "frames": 5, "frame_w": 118, "frame_h": 170},
}


class Player:

    def __init__(self, x, y):

        self.rect       = pygame.Rect(x, y, 40, 40)
        self.velocidade = 4

        # ── Walk (RGBA transparente) ───────────────────────────────
        self._frames = {}
        for nome, cfg in SHEETS.items():
            sheet = pygame.image.load(cfg["path"]).convert_alpha()
            frames = []
            for i in range(cfg["frames"]):
                frame = sheet.subsurface(pygame.Rect(i * cfg["frame_w"], 0, cfg["frame_w"], cfg["frame_h"])).copy()
                frame = pygame.transform.scale(frame, (int(cfg["frame_w"] * ESCALA), int(cfg["frame_h"] * ESCALA)))
                frames.append(frame)
            self._frames[nome] = frames

        # ── Idle (já com alpha limpo) ──────────────────────────────
        idle_raw = pygame.image.load("assets/sprites/idle.png").convert_alpha()
        self._idle_frame = pygame.transform.scale(idle_raw, (int(111 * ESCALA), int(175 * ESCALA)))

        self._direcao    = "frente"
        self._virado     = False
        self._anim_index = 0.0
        self._anim_vel   = 0.13
        self._movendo    = False

    # ─────────────────────────────────────────────────────────────
    def mover(self, teclas, paredes):

        posicao_antiga = self.rect.copy()
        self._movendo  = False

        if teclas[pygame.K_w]:
            self.rect.y  -= self.velocidade
            self._direcao = "costas"
            self._movendo = True

        if teclas[pygame.K_s]:
            self.rect.y  += self.velocidade
            self._direcao = "frente"
            self._movendo = True

        if teclas[pygame.K_a]:
            self.rect.x  -= self.velocidade
            self._direcao = "lado"
            self._virado  = True
            self._movendo = True

        if teclas[pygame.K_d]:
            self.rect.x  += self.velocidade
            self._direcao = "lado"
            self._virado  = False
            self._movendo = True

        for parede in paredes:
            if self.rect.colliderect(parede):
                self.rect = posicao_antiga

        if self._movendo:
            n = SHEETS[self._direcao]["frames"]
            self._anim_index = (self._anim_index + self._anim_vel) % n
        else:
            self._anim_index = 0.0

    # ─────────────────────────────────────────────────────────────
    def desenhar(self, tela):

        if self._movendo:
            frame = self._frames[self._direcao][int(self._anim_index)]
        else:
            frame = self._idle_frame

        if self._virado:
            frame = pygame.transform.flip(frame, True, False)

        sprite_rect = frame.get_rect(center=self.rect.center)
        tela.blit(frame, sprite_rect)

        # DEBUG – descomente para ver hitbox:
        # pygame.draw.rect(tela, (255, 0, 0), self.rect, 1)