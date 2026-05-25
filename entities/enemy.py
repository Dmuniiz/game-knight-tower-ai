import pygame
import random
from systems.ai import buscar_caminho, pixel_para_grid
from core.settings import TILE_SIZE


# largura dos frames da animação idle
FRAME_W_IDLE = 96

# largura dos frames da animação andando
FRAME_W_WALK = 96

# quantidade de frames idle
FRAMES_IDLE = 6

# quantidade de frames andando
FRAMES_WALK = 8

# altura dos frames
FRAME_H = 96

# limite para remover fundo preto
BG_THRESH = 20

# escala do sprite
ESCALA = 3


# remove fundo preto da imagem
def _remove_bg(surface: pygame.Surface) -> pygame.Surface:

    # converte imagem para suportar transparência
    out = surface.convert_alpha()

    # pega largura e altura
    w, h = out.get_size()

    # percorre pixels da imagem
    for x in range(w):
        for y in range(h):

            r, g, b, _ = out.get_at((x, y))

            # se pixel for quase preto
            if (
                r < BG_THRESH
                and g < BG_THRESH
                and b < BG_THRESH
            ):

                # deixa transparente
                out.set_at((x, y), (0, 0, 0, 0))

    return out


# carrega spritesheet e separa frames
def _load_frames(path, frame_w, n_frames, escala):

    # carrega spritesheet
    sheet = pygame.image.load(path).convert()

    frames = []

    # percorre quantidade de frames
    for i in range(n_frames):

        # corta frame da spritesheet
        raw = sheet.subsurface(
            pygame.Rect(
                i * frame_w,
                0,
                frame_w,
                FRAME_H
            )
        ).copy()

        # remove fundo
        frame = _remove_bg(raw)

        # aumenta escala
        frame = pygame.transform.scale(
            frame,
            (
                int(frame_w * escala),
                int(FRAME_H * escala)
            )
        )

        # adiciona frame na lista
        frames.append(frame)

    return frames

    
class Enemy:

    def __init__(self, x, y, speed_bonus: float = 0.0):

        # hitbox do inimigo
        self.rect = pygame.Rect(x, y, 40, 40)

        # velocidade base
        self.velocidade = 2.5 + speed_bonus

        # pasta dos sprites
        base = "assets/sprites/monster"

        # animação parado
        self._frames_idle = _load_frames(
            f"{base}/Monster_Slime_Idle-Sheet.png",
            FRAME_W_IDLE,
            FRAMES_IDLE,
            ESCALA
        )

        # animação andando
        self._frames_walk = _load_frames(
            f"{base}/Monster_Slime_Walk-Sheet.png",
            FRAME_W_WALK,
            FRAMES_WALK,
            ESCALA
        )

        # controle de animação
        self._anim_index = 0.0
        self._anim_vel = 0.12

        # estado atual
        self._movendo = False
        self._virado = False

        #morte
        self.morrendo = False
        self.morte_ate = 0

    # movimentação com colisão
    def _axis_move(self, dx: float, dy: float, paredes):

        # movimento horizontal
        if dx != 0:

            self.rect.x += int(dx)

            # verifica colisão com paredes
            for parede in paredes:

                if self.rect.colliderect(parede):

                    # colisão indo para direita
                    if dx > 0:
                        self.rect.right = parede.left

                    # colisão indo para esquerda
                    else:
                        self.rect.left = parede.right

        # movimento vertical
        if dy != 0:

            self.rect.y += int(dy)

            # verifica colisão
            for parede in paredes:

                if self.rect.colliderect(parede):

                    # colisão descendo
                    if dy > 0:
                        self.rect.bottom = parede.top

                    # colisão subindo
                    else:
                        self.rect.top = parede.bottom

    # movimenta inimigo até o player
    def mover(
        self,
        player,
        paredes,
        mapa,
        learned_bias=(0.0, 0.0)
    ):
        if self.morrendo:
            return

        # posição do inimigo no grid
        inicio = pixel_para_grid(
            self.rect.centerx,
            self.rect.centery,
            TILE_SIZE
        )

        # posição do player no grid
        fim = pixel_para_grid(
            player.rect.centerx,
            player.rect.centery,
            TILE_SIZE
        )

        # calcula caminho até player
        caminho = buscar_caminho(
            inicio,
            fim,
            mapa
        )

        # começa parado
        self._movendo = False

        # se existir caminho
        if caminho:

            # próximo bloco do caminho
            proximo = caminho[0]

            # transforma grid em pixel
            alvo_x = proximo[0] * TILE_SIZE
            alvo_y = proximo[1] * TILE_SIZE

            move_x = 0
            move_y = 0

            # movimento horizontal
            if self.rect.x < alvo_x:
                move_x = self.velocidade

            elif self.rect.x > alvo_x:
                move_x = -self.velocidade

            # movimento vertical
            if self.rect.y < alvo_y:
                move_y = self.velocidade

            elif self.rect.y > alvo_y:
                move_y = -self.velocidade

            # vira sprite
            self._virado = move_x < 0

            # define se está andando
            self._movendo = (
                move_x != 0
                or move_y != 0
            )

            # aplica movimento
            self._axis_move(move_x, 0, paredes)
            self._axis_move(0, move_y, paredes)

        # escolhe quantidade de frames
        frames_count = len(
            self._frames_walk
            if self._movendo
            else self._frames_idle
        )

        # atualiza animação
        self._anim_index = (
            self._anim_index + self._anim_vel
        ) % frames_count

    # desenha inimigo
    def desenhar(self, tela):

        # escolhe animação
        frames = (
            self._frames_walk
            if self._movendo
            else self._frames_idle
        )

        # frame atual
        frame = frames[int(self._anim_index)]

        # vira sprite horizontalmente
        if self._virado:
            frame = pygame.transform.flip(
                frame,
                True,
                False
            )

        
        # se estiver morrendo, fica vermelho
        if self.morrendo:
            frame = frame.copy()
            frame.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_MULT)
        # desenha frame na tela
        tela.blit(
            frame,
            frame.get_rect(center=self.rect.center)
        )

# inimigo que anda aleatoriamente
class WanderEnemy(Enemy):

    def __init__(self, x, y, speed_bonus=0.0):

        # herda Enemy
        super().__init__(x, y, speed_bonus)

        # velocidade
        self.velocidade = 1.8

        # direção atual
        self.direcao = [1, 0]

        # timer de troca
        self.tempo_troca = 0

    def mover(self, player, paredes, mapa, learned_bias=(0.0, 0.0)):

        if self.morrendo:
            return

        agora = pygame.time.get_ticks()

        # troca direção a cada 1 segundo
        if agora > self.tempo_troca:

            self.tempo_troca = agora + 1000

            self.direcao = random.choice([

                [1, 0],
                [-1, 0],
                [0, 1],
                [0, -1]

            ])

        self._movendo = True

        # vira sprite
        self._virado = self.direcao[0] < 0

        # move
        self._axis_move(
            self.direcao[0] * self.velocidade,
            0,
            paredes
        )

        self._axis_move(
            0,
            self.direcao[1] * self.velocidade,
            paredes
        )

        # animação
        frames_count = len(self._frames_walk)

        self._anim_index = (
            self._anim_index + self._anim_vel
        ) % frames_count


# inimigo que só persegue se ver player
class HunterEnemy(Enemy):

    def __init__(self, x, y, speed_bonus=0.0):

        super().__init__(x, y, speed_bonus)

        # mais rápido
        self.velocidade = 4

        # distância de visão
        self.visao = 7

        #tempo para esquecer o player 
        self.tempo_memoria = 2500

        #ultima vez que viu o player 
        self.ultima_visao = 0

    # verifica se player está perto
    # verifica se player está perto e sem parede no caminho
    def pode_ver_player(self, player, mapa):

        enemy_grid = pixel_para_grid(
            self.rect.centerx,
            self.rect.centery,
            TILE_SIZE
        )

        player_grid = pixel_para_grid(
            player.rect.centerx,
            player.rect.centery,
            TILE_SIZE
        )

        ex, ey = enemy_grid
        px, py = player_grid

        distancia = abs(ex - px) + abs(ey - py)

        # longe demais
        if distancia > self.visao:
            return False

        # só enxerga em linha reta
        if ex != px and ey != py:
            return False

        # mesma coluna
        if ex == px:
            inicio = min(ey, py) + 1
            fim = max(ey, py)

            for y in range(inicio, fim):
                if mapa[y][ex] == "1":
                    return False

        # mesma linha
        if ey == py:
            inicio = min(ex, px) + 1
            fim = max(ex, px)

            for x in range(inicio, fim):
                if mapa[ey][x] == "1":
                    return False

        return True

    def mover(self, player, paredes, mapa, learned_bias=(0.0, 0.0)):

        if self.morrendo:
            return

        agora = pygame.time.get_ticks()

        # se estiver vendo o player agora, atualiza memória
        if self.pode_ver_player(player, mapa):
            self.ultima_visao = agora

        # continua perseguindo por um tempo depois de perder visão
        ainda_lembra = agora - self.ultima_visao <= self.tempo_memoria

        if ainda_lembra:

            super().mover(
                player,
                paredes,
                mapa,
                learned_bias
            )

        else:

            # para quando esquece o player
            self._movendo = False

            frames_count = len(self._frames_idle)

            self._anim_index = (
                self._anim_index + self._anim_vel
            ) % frames_count