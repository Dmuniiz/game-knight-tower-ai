import pygame

# ── Spritesheet config ─────────────────────────────────────────────
FRAME_W_IDLE = 96
FRAME_W_WALK = 96
FRAMES_IDLE  = 6
FRAMES_WALK  = 8
FRAME_H      = 96
SPRITE_Y0    = 0      # linha única, começa no topo
BG_THRESH    = 20
ESCALA       = 3


def _remove_bg(surface: pygame.Surface) -> pygame.Surface:
    out = surface.convert_alpha()
    w, h = out.get_size()
    for x in range(w):
        for y in range(h):
            r, g, b, a = out.get_at((x, y))
            if r < BG_THRESH and g < BG_THRESH and b < BG_THRESH:
                out.set_at((x, y), (0, 0, 0, 0))
    return out


def _load_frames(path, frame_w, n_frames, escala):
    sheet = pygame.image.load(path).convert()
    frames = []
    for i in range(n_frames):
        raw   = sheet.subsurface(pygame.Rect(i * frame_w, 0, frame_w, FRAME_H)).copy()
        frame = _remove_bg(raw)
        frame = pygame.transform.scale(frame, (int(frame_w * escala), int(FRAME_H * escala)))
        frames.append(frame)
    return frames


class Enemy:

    def __init__(self, x, y):

        self.rect       = pygame.Rect(x, y, 40, 40)
        self.velocidade = 2

        self.direcao_x = 0
        self.direcao_y = 0

        # ── Sprites ───────────────────────────────────────────────
        base = "assets/sprites/monster"
        self._frames_idle = _load_frames(f"{base}/Monster_Slime_Idle-Sheet.png", FRAME_W_IDLE, FRAMES_IDLE, ESCALA)
        self._frames_walk = _load_frames(f"{base}/Monster_Slime_Walk-Sheet.png", FRAME_W_WALK, FRAMES_WALK, ESCALA)

        self._anim_index = 0.0
        self._anim_vel   = 0.12
        self._movendo    = False
        self._virado     = False   # True = indo para a esquerda

    # ─────────────────────────────────────────────────────────────
    def mover(self, player, paredes):

        movimento_x = 0
        movimento_y = 0

        # seguir player
        if player.rect.x > self.rect.x:
            movimento_x = self.velocidade
            self._virado = False

        elif player.rect.x < self.rect.x:
            movimento_x = -self.velocidade
            self._virado = True

        if player.rect.y > self.rect.y:
            movimento_y = self.velocidade

        elif player.rect.y < self.rect.y:
            movimento_y = -self.velocidade

        self._movendo = (movimento_x != 0 or movimento_y != 0)

        # MOVIMENTO X
        self.rect.x += movimento_x
        bateu_x = False
        for parede in paredes:
            if self.rect.colliderect(parede):
                self.rect.x -= movimento_x
                bateu_x = True
                break

        if bateu_x:
            if player.rect.y > self.rect.y:
                self.rect.y += self.velocidade
            elif player.rect.y < self.rect.y:
                self.rect.y -= self.velocidade

        # MOVIMENTO Y
        self.rect.y += movimento_y
        bateu_y = False
        for parede in paredes:
            if self.rect.colliderect(parede):
                self.rect.y -= movimento_y
                bateu_y = True
                break

        if bateu_y:
            if player.rect.x > self.rect.x:
                self.rect.x += self.velocidade
            elif player.rect.x < self.rect.x:
                self.rect.x -= self.velocidade

        # animação
        if self._movendo:
            frames_count = len(self._frames_walk)
            self._anim_index = (self._anim_index + self._anim_vel) % frames_count
        else:
            frames_count = len(self._frames_idle)
            self._anim_index = (self._anim_index + self._anim_vel) % frames_count

    # ─────────────────────────────────────────────────────────────
    def desenhar(self, tela):

        frames = self._frames_walk if self._movendo else self._frames_idle
        frame  = frames[int(self._anim_index)]

        if self._virado:
            frame = pygame.transform.flip(frame, True, False)

        sprite_rect = frame.get_rect(center=self.rect.center)
        tela.blit(frame, sprite_rect)

        # DEBUG – descomente para ver hitbox:
        # pygame.draw.rect(tela, (255, 0, 0), self.rect, 1)