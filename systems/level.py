import pygame

from core.settings import TILE_SIZE
from entities.enemy import Enemy

MAPS = [
    [
        "1111111111111111",
        "1P0000C000000C01",
        "1001110111111101",
        "10C0010000000001",
        "1011011111110101",
        "1001000C00010001",
        "1011110111011101",
        "1000C001C00000C1",
        "1110000011000001",
        "11000C00000010ID",
        "1111111111111111",
    ],
    [
        "1111111111111111",
        "1P000001000000C1",
        "1011101011110101",
        "10C0101000010101",
        "1010101111010101",
        "1010100001010101",
        "1010111101010101",
        "100000C0010000C1",
        "1011110111111101",
        "1I000000000000D1",
        "1111111111111111",
    ],
    [
        "1111111111111111",
        "1P000000100000C1",
        "1011111101011101",
        "1000000101000101",
        "1111100101110101",
        "1C00100100010101",
        "1010111011100101",
        "1010000010000C01",
        "1010111110111101",
        "1I000000000000D1",
        "1111111111111111",
    ],
    [
        "1111111111111111",
        "1P000001000000C1",
        "1011101010111101",
        "10C0101010000101",
        "1010101111010101",
        "1010100001010101",
        "1010111101010101",
        "1C000000010000C1",
        "1011110111111101",
        "1II00000000000D1",
        "1111111111111111",
    ],
    [
        "1111111111111111",
        "1P0000C0100000C1",
        "1011110101111101",
        "1000010101000001",
        "1111010101011111",
        "1C000010100000C1",
        "1011111101111101",
        "1000000000000001",
        "1011111111111101",
        "1III0000000000D1",
        "1111111111111111",
    ],
]


def criar_mapa(stage: int = 1, ai_level: float = 0.0):
    mapa = MAPS[(stage - 1) % len(MAPS)]

    paredes = []
    chaves = []
    inimigos = []
    player_posicao = None
    porta = None

    speed_bonus = min(2.0, ai_level * 0.25 + (stage - 1) * 0.2)

    for linha_numero, linha in enumerate(mapa):
        for coluna_numero, bloco in enumerate(linha):
            x = coluna_numero * TILE_SIZE
            y = linha_numero * TILE_SIZE

            if bloco == "1":
                paredes.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif bloco == "P":
                player_posicao = (x, y)
            elif bloco == "C":
                chaves.append(pygame.Rect(x + 10, y + 10, 30, 30))
            elif bloco == "D":
                porta = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            elif bloco == "I":
                inimigos.append(Enemy(x, y, speed_bonus=speed_bonus))

    return paredes, player_posicao, chaves, porta, inimigos