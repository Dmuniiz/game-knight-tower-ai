import pygame
from settings import TAMANHO_BLOCO
from entities.enemy import Enemy

# mapa da fase
mapa = [

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
    "1111111111111111"

]

def criar_mapa():

    paredes = []
    chaves = []
    inimigos = []
    player_posicao = None
    porta = None

    # percorre linhas
    for linha_numero, linha in enumerate(mapa):

        # percorre colunas
        for coluna_numero, bloco in enumerate(linha):

            x = coluna_numero * TAMANHO_BLOCO
            y = linha_numero * TAMANHO_BLOCO

            # se for parede
            if bloco == "1":

                parede = pygame.Rect(

                    x,
                    y,
                    TAMANHO_BLOCO,
                    TAMANHO_BLOCO
                )

                paredes.append(parede)

            # player
            elif bloco == "P":

                player_posicao = (x,y)

            elif bloco == "C":

                chave = pygame.Rect(
                    x + 10,
                    y + 10,
                    30,
                    30
                )

                chaves.append(chave)

            elif bloco == "D":

                porta = pygame.Rect (
                    x,
                    y,
                    TAMANHO_BLOCO,
                    TAMANHO_BLOCO
                )
                
            #inimigo
            elif bloco == "I":
                
                inimigo = Enemy(x, y)

                inimigos.append(inimigo)
                

    print(porta)


    return paredes, player_posicao, chaves, porta, inimigos