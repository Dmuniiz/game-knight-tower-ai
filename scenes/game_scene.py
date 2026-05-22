import random

import pygame

from core.assets import AssetManager
from core.settings import HEIGHT, TILE_SIZE, WIDTH
from entities.player import Player
from systems.level import criar_mapa
from ui.hud import Hud


class GameScene:
    def __init__(self, assets: AssetManager):
        self.assets = assets
        self.tile_size = TILE_SIZE
        self.stage = 1

        self.dungeon = self.assets.load_image("dungeon", "Dungeon_Tileset.png")
        self.key_sprite = self.assets.load_image("key", "keys.png", scale=(TILE_SIZE, TILE_SIZE))

        self.sound_key = self.assets.load_sound("key", "mixkit-fairy-arcade-sparkle-866.wav", volume=0.5)
        self.sound_door = self.assets.load_sound("door", "mixkit-prison-metal-door-close-201.wav", volume=0.4)

        self.hud = Hud(self.key_sprite)
        self._build_tile_set()
        self._build_static_layers()
        self.reset_level_state()

    def _get_tile(self, col: int, row: int, tw: int = 16, th: int = 16) -> pygame.Surface:
        surface = pygame.Surface((tw, th), pygame.SRCALPHA)
        surface.blit(self.dungeon, (0, 0), (col * tw, row * th, tw, th))
        return pygame.transform.scale(surface, (self.tile_size, self.tile_size))

    def _build_tile_set(self):
        self.floor_tiles = [self._get_tile(c, r) for r in (1, 2, 3) for c in (1, 2, 3)]
        self.wall_tiles = {
            "canto_sup_esq": self._get_tile(0, 0),
            "canto_sup_dir": self._get_tile(5, 5),
            "canto_inf_esq": self._get_tile(0, 4),
            "canto_inf_dir": self._get_tile(5, 4),
            "topo": self._get_tile(1, 0),
            "base": self._get_tile(1, 4),
            "lat_esq": self._get_tile(0, 1),
            "lat_dir": self._get_tile(5, 1),
            "interior": self._get_tile(4, 9),
            "isolado": self._get_tile(3, 0),
            "ponta_cima": self._get_tile(0, 3),
            "ponta_baixo": self._get_tile(5, 1),
            "ponta_esq": self._get_tile(4, 0),
            "ponta_dir": self._get_tile(2, 0),
        }
        self.door_closed = self._get_tile(7, 5)
        self.door_open = self._get_tile(7, 6)
        self.decorations = {
            self._get_tile(4, 3): [(1, 1), (18, 1), (1, 12), (18, 12)],
            self._get_tile(9, 5): [(2, 1), (17, 1), (2, 12), (17, 12)],
            self._get_tile(7, 7): [(5, 4), (10, 7), (14, 3)],
            self._get_tile(8, 6): [(7, 9), (13, 10)],
        }

    def _build_static_layers(self):
        random.seed(99)
        self.floor_surface = pygame.Surface((WIDTH, HEIGHT))
        for ry in range(HEIGHT // self.tile_size + 1):
            for rx in range(WIDTH // self.tile_size + 1):
                self.floor_surface.blit(random.choice(self.floor_tiles), (rx * self.tile_size, ry * self.tile_size))

        self.deco_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for sprite, positions in self.decorations.items():
            for gx, gy in positions:
                self.deco_surface.blit(sprite, (gx * self.tile_size, gy * self.tile_size))

    def reset_level_state(self):
        self.collected_keys = 0
        self.door_is_open = False
        self.walls, player_position, self.keys, self.door, self.enemies = criar_mapa()
        self.player = Player(player_position[0], player_position[1])
        self.total_keys = len(self.keys)
        wall_positions = {(wall.x // self.tile_size, wall.y // self.tile_size) for wall in self.walls}
        self.wall_sprites = [(wall, self._choose_wall_tile(wall_positions, wall.x // self.tile_size, wall.y // self.tile_size)) for wall in self.walls]

    def _choose_wall_tile(self, wall_positions: set[tuple[int, int]], gx: int, gy: int) -> pygame.Surface:
        c = (gx, gy - 1) in wall_positions
        b = (gx, gy + 1) in wall_positions
        e = (gx - 1, gy) in wall_positions
        d = (gx + 1, gy) in wall_positions
        t = self.wall_tiles
        if not c and not b and not e and not d: return t["isolado"]
        if c and not b and not e and not d: return t["ponta_cima"]
        if not c and b and not e and not d: return t["ponta_baixo"]
        if not c and not b and e and not d: return t["ponta_esq"]
        if not c and not b and not e and d: return t["ponta_dir"]
        if not c and not e and b and d: return t["canto_sup_esq"]
        if not c and not d and b and e: return t["canto_sup_dir"]
        if not b and not e and c and d: return t["canto_inf_esq"]
        if not b and not d and c and e: return t["canto_inf_dir"]
        if not c and not b and e and d: return t["topo"]
        if c and b and not e and not d: return t["lat_esq"]
        if c and b and e and not d: return t["lat_dir"]
        if c and b and d and not e: return t["lat_esq"]
        if c and e and d and not b: return t["base"]
        if b and e and d and not c: return t["topo"]
        if not c and b: return t["topo"]
        if c and not b: return t["base"]
        if not e and d: return t["lat_esq"]
        if e and not d: return t["lat_dir"]
        return t["interior"]

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.mover(keys, self.walls)

        for enemy in self.enemies:
            enemy.mover(self.player, self.walls)

        for key in self.keys[:]:
            if self.player.rect.colliderect(key):
                self.keys.remove(key)
                self.collected_keys += 1
                self.sound_key.play()
                if len(self.keys) == 0 and not self.door_is_open:
                    self.door_is_open = True
                    self.sound_door.play()

        if self.door_is_open and self.player.rect.colliderect(self.door):
            self.stage += 1
            self.reset_level_state()

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.reset_level_state()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.floor_surface, (0, 0))
        screen.blit(self.deco_surface, (0, 0))

        for wall, sprite in self.wall_sprites:
            screen.blit(sprite, (wall.x, wall.y))

        door_sprite = self.door_open if self.door_is_open else self.door_closed
        screen.blit(door_sprite, (self.door.x, self.door.y))

        for key in self.keys:
            screen.blit(self.key_sprite, (key.x - 10, key.y - 10))

        self.player.desenhar(screen)
        for enemy in self.enemies:
            enemy.desenhar(screen)

        self.hud.draw(screen, self.collected_keys, self.total_keys, self.stage)
