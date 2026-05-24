import sys

import pygame

from core.assets import AssetManager
from core.settings import (
    FPS,
    SOUNDS_DIR,
    SPRITES_DIR,
    WIDTH,
    HEIGHT,
    WINDOW_TITLE
)

from scenes.game_scene import GameScene
from ui.menu import Menu


class Game:

    def __init__(self):

        # inicia pygame
        pygame.init()

        # inicia sistema de áudio
        pygame.mixer.init()

        # cria janela do jogo
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # define título da janela
        pygame.display.set_caption(WINDOW_TITLE)

        # controla FPS
        self.clock = pygame.time.Clock()

        # gerenciador de assets
        self.assets = AssetManager(
            SPRITES_DIR,
            SOUNDS_DIR
        )

        # cria cena principal do jogo
        self.scene = GameScene(self.assets)

    # loop principal do jogo
    def run(self):

        # cria menu inicial
        menu = Menu(self.screen)

        # executa menu
        menu.run()

        # loop infinito do jogo
        while True:

            # limita FPS
            self.clock.tick(FPS)

            # verifica eventos
            for event in pygame.event.get():

                # fechar janela
                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

            # atualiza lógica do jogo
            self.scene.update()

            # desenha tudo na tela
            self.scene.draw(self.screen)

            # atualiza tela
            pygame.display.update()
