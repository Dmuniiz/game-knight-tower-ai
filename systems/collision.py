import pygame

def criar_paredes():

    paredes = []

    # parede 1
    paredes.append(pygame.Rect(200, 100, 50, 300))

    # parede 2
    paredes.append(pygame.Rect(400, 0, 50, 250))

    return paredes
