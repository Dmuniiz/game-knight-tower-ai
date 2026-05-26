import pygame

from core.settings import TILE_SIZE
from entities.enemy import Enemy, WanderEnemy, HunterEnemy
from entities.items import Sword, Shield


#Cria os mapas utilizando matrizzes
#Cada caracter representa um tipo de bloco ou entidade:
# "1" = parede  
# "P" = posição inicial do player
# "C" = chave
# "D" = porta de saída
# "I" = inimigo
MAPS = [
    
    [
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
        "10001000000010000001",
        "1P00S000000000W0000D0",   
        "100000E0010000001001",
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
        "11111111111111111111",
    ],
    [
        "11111111111111111111",
        "1P000001I00W000C00001",
        "10111010101111010101",
        "10C0101010000101010C1",
        "1010101111010101I101",
        "1010100S010101010101",
        "10101111010101010101",
        "1C00000001010000C001",
        "10111101111111010101",
        "10000000001000W00001",
        "10000101000000100001",
        "10111001111101010101",
        "1S00001000C000000I01",
        "10111110111110101101",
        "1II0000000000000000D1",
        "11111111111111111111",
    ],
]


def criar_mapa(stage: int = 1, ai_level: float = 0.0):
        
        #seleciona o mapa pelo seu número
        mapa = MAPS[(stage - 1) % len(MAPS)]

        paredes = []
        chaves = []
        inimigos = []
        espadas = []
        escudos = []
        player_posicao = None
        porta = None

        #aumenta a velocidade dos inimigos
        speed_bonus = min(1.0, ai_level * 0.10 + (stage - 1) * 0.08)   

        for linha_numero, linha in enumerate(mapa):
            for coluna_numero, bloco in enumerate(linha):
                x = coluna_numero * TILE_SIZE
                y = linha_numero * TILE_SIZE
                
                #define o tipo de bloco ou entidade com base no caracter do mapa

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

                elif bloco == "S":
                    espadas.append(Sword(x, y))

                elif bloco == "E":
                    escudos.append(Shield(x, y))

                elif bloco == "W":
                    inimigos.append(WanderEnemy(x, y, speed_bonus=speed_bonus))

                elif bloco == "H":
                    inimigos.append(HunterEnemy(x, y, speed_bonus=speed_bonus))

        return paredes, player_posicao, chaves, porta, inimigos, espadas, escudos