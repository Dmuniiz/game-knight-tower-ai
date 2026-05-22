import pygame

FRAME_W_IDLE = 96
FRAME_W_WALK = 96
FRAMES_IDLE = 6
FRAMES_WALK = 8
FRAME_H = 96
BG_THRESH = 20
ESCALA = 3


def _remove_bg(surface: pygame.Surface) -> pygame.Surface:
    out = surface.convert_alpha()
    w, h = out.get_size()
    for x in range(w):
        for y in range(h):
            r, g, b, _ = out.get_at((x, y))
            if r < BG_THRESH and g < BG_THRESH and b < BG_THRESH:
                out.set_at((x, y), (0, 0, 0, 0))
    return out


def _load_frames(path, frame_w, n_frames, escala):
    sheet = pygame.image.load(path).convert()
    frames = []
    for i in range(n_frames):
        raw = sheet.subsurface(pygame.Rect(i * frame_w, 0, frame_w, FRAME_H)).copy()
        frame = _remove_bg(raw)
        frame = pygame.transform.scale(frame, (int(frame_w * escala), int(FRAME_H * escala)))
        frames.append(frame)
    return frames


class Enemy:
    def __init__(self, x, y, speed_bonus: float = 0.0):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.velocidade = 2.0 + speed_bonus

        base = "assets/sprites/monster"
        self._frames_idle = _load_frames(f"{base}/Monster_Slime_Idle-Sheet.png", FRAME_W_IDLE, FRAMES_IDLE, ESCALA)
        self._frames_walk = _load_frames(f"{base}/Monster_Slime_Walk-Sheet.png", FRAME_W_WALK, FRAMES_WALK, ESCALA)

        self._anim_index = 0.0
        self._anim_vel = 0.12
        self._movendo = False
        self._virado = False

    def _axis_move(self, dx: float, dy: float, paredes):
        if dx != 0:
            self.rect.x += int(dx)
            for parede in paredes:
                if self.rect.colliderect(parede):
                    if dx > 0:
                        self.rect.right = parede.left
                    else:
                        self.rect.left = parede.right
        if dy != 0:
            self.rect.y += int(dy)
            for parede in paredes:
                if self.rect.colliderect(parede):
                    if dy > 0:
                        self.rect.bottom = parede.top
                    else:
                        self.rect.top = parede.bottom

    def mover(self, player, paredes, learned_bias: tuple[float, float] = (0.0, 0.0)):
        target_dx = player.rect.centerx - self.rect.centerx
        target_dy = player.rect.centery - self.rect.centery

        bias_x, bias_y = learned_bias
        move_x = self.velocidade if target_dx > 0 else -self.velocidade if target_dx < 0 else 0
        move_y = self.velocidade if target_dy > 0 else -self.velocidade if target_dy < 0 else 0

        if abs(target_dx) > abs(target_dy):
            move_y += bias_y * 0.4
        else:
            move_x += bias_x * 0.4

        self._virado = move_x < 0
        self._movendo = move_x != 0 or move_y != 0

        self._axis_move(move_x, 0, paredes)
        self._axis_move(0, move_y, paredes)

        frames_count = len(self._frames_walk if self._movendo else self._frames_idle)
        self._anim_index = (self._anim_index + self._anim_vel) % frames_count

    def desenhar(self, tela):
        frames = self._frames_walk if self._movendo else self._frames_idle
        frame = frames[int(self._anim_index)]
        if self._virado:
            frame = pygame.transform.flip(frame, True, False)
        tela.blit(frame, frame.get_rect(center=self.rect.center))