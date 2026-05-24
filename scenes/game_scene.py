import random

import pygame

from core.assets import AssetManager
from core.settings import HEIGHT, TILE_SIZE, WIDTH
from entities.player import Player
from entities.items import Sword, Shield
from systems.level import criar_mapa, MAPS
from ui.hud import Hud


class GameScene:

    def __init__(self, assets: AssetManager):

        # gerenciador de assets
        self.assets = assets

        # tamanho dos blocos do mapa
        self.tile_size = TILE_SIZE

        # fase atual
        self.stage = 1

        # quantidade máxima de fases
        self.max_stage = len(MAPS)

        # nível de aprendizado da IA
        self.ai_learning = 0.0

        # memória do movimento do player
        self.player_move_memory = [0, 0]

        # ── carregar imagens ─────────────────────────────────

        self.dungeon = self.assets.load_image(
            "dungeon",
            "Dungeon_Tileset.png"
        )

        self.key_sprite = self.assets.load_image(
            "key",
            "keys.png",
            scale=(TILE_SIZE, TILE_SIZE)
        )

        # ── carregar sons ────────────────────────────────────

        self.sound_key = self.assets.load_sound(
            "key",
            "mixkit-fairy-arcade-sparkle-866.wav",
            volume=0.5
        )

        self.sound_door = self.assets.load_sound(
            "door",
            "mixkit-prison-metal-door-close-201.wav",
            volume=0.4
        )

        # HUD do jogo
        self.hud = Hud(self.key_sprite)

        # cria tiles
        self._build_tile_set()

        # cria chão e decoração
        self._build_static_layers()

        # inicia fase
        self.reset_level_state()

    # pega tile da spritesheet
    def _get_tile(
        self,
        col: int,
        row: int,
        tw: int = 16,
        th: int = 16
    ) -> pygame.Surface:

        surface = pygame.Surface(
            (tw, th),
            pygame.SRCALPHA
        )

        # corta tile da spritesheet
        surface.blit(
            self.dungeon,
            (0, 0),
            (col * tw, row * th, tw, th)
        )

        # aumenta tamanho
        return pygame.transform.scale(
            surface,
            (self.tile_size, self.tile_size)
        )

    # cria tiles do jogo
    def _build_tile_set(self):

        # tiles aleatórios do chão
        self.floor_tiles = [

            self._get_tile(c, r)

            for r in (1, 2, 3)
            for c in (1, 2, 3)

        ]

        # tiles das paredes
        self.wall_tiles = {

            "canto_sup_esq": self._get_tile(0, 0),
            "canto_sup_dir": self._get_tile(5, 5),

            "canto_inf_esq": self._get_tile(0, 4),
            "canto_inf_dir": self._get_tile(5, 4),

            "topo": self._get_tile(1, 0),
            "base": self._get_tile(1, 4),

            "lat_esq": self._get_tile(0, 1),
            "lat_dir": self._get_tile(5, 1),

            "interior": self._get_tile(1, 0),

            "isolado": self._get_tile(3, 0),

            "ponta_cima": self._get_tile(0, 3),
            "ponta_baixo": self._get_tile(5, 1),

            "ponta_esq": self._get_tile(4, 0),
            "ponta_dir": self._get_tile(2, 0),

        }

        # nomes alternativos
        self.wall_tiles.setdefault(
            "lado_esq",
            self.wall_tiles["lat_esq"]
        )

        self.wall_tiles.setdefault(
            "lado_dir",
            self.wall_tiles["lat_dir"]
        )

        # porta fechada
        self.door_closed = self._get_tile(7, 5)

        # porta aberta
        self.door_open = self._get_tile(7, 6)

        # decoração do mapa
        self.decorations = {

            self._get_tile(4, 3): [
                (1, 1),
                (18, 1),
                (1, 12),
                (18, 12)
            ],

            self._get_tile(9, 5): [
                (2, 1),
                (17, 1),
                (2, 12),
                (17, 12)
            ],

            self._get_tile(7, 7): [
                (5, 4),
                (10, 7),
                (14, 3)
            ],

            self._get_tile(8, 6): [
                (7, 9),
                (13, 10)
            ],
        }

    # cria fundo fixo
    def _build_static_layers(self):

        # deixa aleatório consistente
        random.seed(99)

        # superfície do chão
        self.floor_surface = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        # desenha chão
        for ry in range(HEIGHT // self.tile_size + 1):

            for rx in range(WIDTH // self.tile_size + 1):

                self.floor_surface.blit(

                    random.choice(self.floor_tiles),

                    (
                        rx * self.tile_size,
                        ry * self.tile_size
                    )

                )

        # superfície de decoração
        self.deco_surface = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        # desenha decoração
        for sprite, positions in self.decorations.items():

            for gx, gy in positions:

                self.deco_surface.blit(
                    sprite,
                    (
                        gx * self.tile_size,
                        gy * self.tile_size
                    )
                )

    # reinicia estado da fase
    def reset_level_state(self):

        # chaves coletadas
        self.collected_keys = 0

        # porta começa fechada
        self.door_is_open = False

        # cria mapa
        (
            self.walls,
            player_position,
            self.keys,
            self.door,
            self.enemies,
            self.swords,
            self.shields

        ) = criar_mapa(

            stage=self.stage,
            ai_level=self.ai_learning

        )

        # cria player
        self.player = Player(
            player_position[0],
            player_position[1]
        )

        # total de chaves
        self.total_keys = len(self.keys)

        # se não tiver chave, abre porta
        if self.total_keys == 0:
            self.door_is_open = True

        # posições das paredes
        wall_positions = {

            (
                wall.x // self.tile_size,
                wall.y // self.tile_size
            )

            for wall in self.walls

        }

        # sprites das paredes
        self.wall_sprites = [

            (
                wall,

                self._choose_wall_tile(
                    wall_positions,
                    wall.x // self.tile_size,
                    wall.y // self.tile_size
                )
            )

            for wall in self.walls

        ]

    # pega tile da parede
    def _tile(self, key: str) -> pygame.Surface:

        return self.wall_tiles.get(
            key,
            self.wall_tiles["interior"]
        )

    # escolhe sprite correto da parede
    def _choose_wall_tile(
        self,
        wall_positions: set[tuple[int, int]],
        gx: int,
        gy: int

    ) -> pygame.Surface:

        # verifica vizinhos
        c = (gx, gy - 1) in wall_positions
        b = (gx, gy + 1) in wall_positions
        e = (gx - 1, gy) in wall_positions
        d = (gx + 1, gy) in wall_positions

        t = self.wall_tiles

        if not c and not b and not e and not d:
            return t["isolado"]

        if c and not b and not e and not d:
            return t["ponta_cima"]

        if not c and b and not e and not d:
            return t["ponta_baixo"]

        if not c and not b and e and not d:
            return t["ponta_esq"]

        if not c and not b and not e and d:
            return t["ponta_dir"]

        if not c and not e and b and d:
            return t["canto_sup_esq"]

        if not c and not d and b and e:
            return t["canto_sup_dir"]

        if not b and not e and c and d:
            return t["canto_inf_esq"]

        if not b and not d and c and e:
            return t["canto_inf_dir"]

        if not c and not b and e and d:
            return t["topo"]

        if c and b and not e and not d:
            return t["lat_esq"]

        if c and b and e and not d:
            return t["lat_dir"]

        if c and b and d and not e:
            return t["lat_esq"]

        if c and e and d and not b:
            return t["base"]

        if b and e and d and not c:
            return t["topo"]

        if not c and b:
            return t["topo"]

        if c and not b:
            return t["base"]

        if not e and d:
            return t["lat_esq"]

        if e and not d:
            return t["lat_dir"]

        return t["interior"]

    # atualiza lógica do jogo
    def update(self):

        # teclas pressionadas
        keys = pygame.key.get_pressed()

        # direção do player
        axis_x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        axis_y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        # memória de movimento da IA
        self.player_move_memory[0] = (
            self.player_move_memory[0] * 0.9 + axis_x
        )

        self.player_move_memory[1] = (
            self.player_move_memory[1] * 0.9 + axis_y
        )

        # move player
        self.player.mover(
            keys,
            self.walls
        )

        # tendência do movimento
        learned_bias = (
            self.player_move_memory[0],
            self.player_move_memory[1]
        )

        # move inimigos
        for enemy in self.enemies:

            enemy.mover(

                self.player,
                self.walls,
                MAPS[self.stage - 1],
                learned_bias=learned_bias

            )

        # ── coletar chaves ───────────────────────────────

        for key in self.keys[:]:

            if self.player.rect.colliderect(key):

                self.keys.remove(key)

                self.collected_keys += 1

                self.sound_key.play()

                # abre porta
                if len(self.keys) == 0 and not self.door_is_open:

                    self.door_is_open = True

                    self.sound_door.play()

        # ── coletar espada ───────────────────────────────

        for sword in self.swords[:]:

            if self.player.rect.colliderect(sword.rect):

                self.player.has_sword = True

                self.swords.remove(sword)

                self.sound_key.play()

        # ── coletar escudo ───────────────────────────────

        for shield in self.shields[:]:

            if self.player.rect.colliderect(shield.rect):

                self.player.shield_durability = 1

                self.shields.remove(shield)

                self.sound_key.play()

        # ── próxima fase ─────────────────────────────────

        if (
            self.door_is_open
            and
            self.player.rect.colliderect(self.door)
        ):

            # IA aprende
            self.ai_learning += 0.35

            # próxima fase
            self.stage = (

                1

                if self.stage >= self.max_stage

                else self.stage + 1

            )

            self.reset_level_state()

        # ── colisão com inimigos ─────────────────────────

        now = pygame.time.get_ticks()

        for enemy in self.enemies[:]:

            if self.player.rect.colliderect(enemy.rect):

                # player invencível
                if now < self.player.invincible_until:
                    continue

                # mata inimigo
                if self.player.has_sword:

                    self.enemies.remove(enemy)

                    self.player.has_sword = False

                    self.sound_key.play()

                # escudo absorve dano
                elif self.player.shield_durability > 0:

                    self.player.shield_durability = 0

                    self.player.invincible_until = now + 1000

                    self.player.speed_boost_until = now + 1000

                    self.sound_key.play()

                # player morre
                else:

                    self.ai_learning += 0.15

                    self.reset_level_state()

    # desenha tudo na tela
    def draw(self, screen: pygame.Surface):

        # chão
        screen.blit(
            self.floor_surface,
            (0, 0)
        )

        # decoração
        screen.blit(
            self.deco_surface,
            (0, 0)
        )

        # paredes
        for wall, sprite in self.wall_sprites:

            screen.blit(
                sprite,
                (wall.x, wall.y)
            )

        # sprite da porta
        door_sprite = (

            self.door_open

            if self.door_is_open

            else self.door_closed

        )

        # desenha porta
        screen.blit(
            door_sprite,
            (self.door.x, self.door.y)
        )

        # desenha chaves
        for key in self.keys:

            screen.blit(
                self.key_sprite,
                (key.x - 10, key.y - 10)
            )

        # ── desenha itens ────────────────────────────────

        for sword in self.swords:
            sword.draw(screen)

        for shield in self.shields:
            shield.draw(screen)

        # player
        self.player.desenhar(screen)

        # inimigos
        for enemy in self.enemies:
            enemy.desenhar(screen)

        # HUD
        self.hud.draw(
            screen,
            self.collected_keys,
            self.total_keys,
            self.stage
        )