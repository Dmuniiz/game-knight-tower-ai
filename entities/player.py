import pygame

# escala dos sprites
ESCALA = 0.30

# configurações das spritesheets
SHEETS = {

    # animação andando para frente
    "frente": {
        "path": "assets/sprites/cavaleiro_frente_walk.png",
        "frames": 3,
        "frame_w": 108,
        "frame_h": 175
    },

    # animação andando para trás
    "costas": {
        "path": "assets/sprites/cavaleiro_costas_walk.png",
        "frames": 3,
        "frame_w": 108,
        "frame_h": 175
    },

    # animação lateral
    "lado": {
        "path": "assets/sprites/cavaleiro_lado_walk.png",
        "frames": 5,
        "frame_w": 118,
        "frame_h": 170
    },
}


class Player:

    def __init__(self, x, y):

        # hitbox do player
        self.rect = pygame.Rect(
            x + 6,
            y + 6,
            28,
            28
        )

        # velocidade atual
        self.velocidade = 4

        # ── animações de movimento ─────────────────────────────

        # dicionário com os frames carregados
        self._frames = {}

        # percorre cada spritesheet
        for nome, cfg in SHEETS.items():

            # carrega imagem
            sheet = pygame.image.load(
                cfg["path"]
            ).convert_alpha()

            frames = []

            # corta os frames da spritesheet
            for i in range(cfg["frames"]):

                frame = sheet.subsurface(

                    pygame.Rect(
                        i * cfg["frame_w"],
                        0,
                        cfg["frame_w"],
                        cfg["frame_h"]
                    )

                ).copy()

                # redimensiona sprite
                frame = pygame.transform.scale(
                    frame,
                    (
                        int(cfg["frame_w"] * ESCALA),
                        int(cfg["frame_h"] * ESCALA)
                    )
                )

                frames.append(frame)

            # salva lista de frames
            self._frames[nome] = frames

        # ── sprite parado ──────────────────────────────────────

        idle_raw = pygame.image.load(
            "assets/sprites/idle.png"
        ).convert_alpha()

        self._idle_frame = pygame.transform.scale(
            idle_raw,
            (
                int(111 * ESCALA),
                int(175 * ESCALA)
            )
        )

        # ── animação ───────────────────────────────────────────

        self._direcao = "frente"
        self._virado = False

        # frame atual da animação
        self._anim_index = 0.0

        # velocidade da animação
        self._anim_vel = 0.13

        # define se está andando
        self._movendo = False

        # ── efeitos ────────────────────────────────────────────

        # velocidade base
        self.base_speed = 4

        # tempo do boost de velocidade
        self.speed_boost_until = 0

        # tempo da invencibilidade
        self.invincible_until = 0

        # ── itens ──────────────────────────────────────────────

        # espada equipada
        self.has_sword = False

        # durabilidade do escudo
        # 0 = sem escudo
        # 1 = com escudo
        self.shield_durability = 0

        #cooldown da espada
        self.sword_ready_until = 0


    # movimentação do player
    def mover(self, teclas, paredes):

        # aplica boost de velocidade temporário
        self.velocidade = self.base_speed + (
            1 if pygame.time.get_ticks() < self.speed_boost_until else 0
        )

        # salva posição anterior
        posicao_antiga = self.rect.copy()

        # começa parado
        self._movendo = False

        # movimento para cima
        if teclas[pygame.K_w]:

            self.rect.y -= self.velocidade

            self._direcao = "costas"
            self._movendo = True

        # movimento para baixo
        if teclas[pygame.K_s]:

            self.rect.y += self.velocidade

            self._direcao = "frente"
            self._movendo = True

        # movimento esquerda
        if teclas[pygame.K_a]:

            self.rect.x -= self.velocidade

            self._direcao = "lado"
            self._virado = True
            self._movendo = True

        # movimento direita
        if teclas[pygame.K_d]:

            self.rect.x += self.velocidade

            self._direcao = "lado"
            self._virado = False
            self._movendo = True

        # colisão com paredes
        for parede in paredes:

            if self.rect.colliderect(parede):

                # volta para posição anterior
                self.rect = posicao_antiga

        # atualiza animação
        if self._movendo:

            # quantidade de frames
            n = SHEETS[self._direcao]["frames"]

            # avança animação
            self._anim_index = (
                self._anim_index + self._anim_vel
            ) % n

        else:

            # volta pro primeiro frame
            self._anim_index = 0.0

    # desenha player
    def desenhar(self, tela):

        # escolhe frame
        if self._movendo:

            frame = self._frames[
                self._direcao
            ][int(self._anim_index)]

        else:

            frame = self._idle_frame

        # vira sprite horizontalmente
        if self._virado:

            frame = pygame.transform.flip(
                frame,
                True,
                False
            )

        # centraliza sprite na hitbox
        sprite_rect = frame.get_rect(
            center=self.rect.center
        )

        # efeito visual de invencibilidade
        if pygame.time.get_ticks() < self.invincible_until:

            pygame.draw.circle(
                tela,
                (255, 255, 255),
                self.rect.center,
                self.rect.width // 2 + 4,
                2
            )

        # aura da espada
        if self.has_sword:

            pygame.draw.circle(
                tela,
                (255, 215, 0),
                self.rect.center,
                self.rect.width // 2 + 7,
                2
            )

        # aura do escudo
        if self.shield_durability > 0:

            pygame.draw.circle(
                tela,
                (100, 149, 237),
                self.rect.center,
                self.rect.width // 2 + 11,
                2
            )
        # desenha sprite
        tela.blit(frame, sprite_rect)

        # DEBUG:
        # mostra hitbox do player
        # pygame.draw.rect(tela, (255, 0, 0), self.rect, 1)