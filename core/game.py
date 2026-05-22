import sys

import pygame

from core.assets import AssetManager
from core.settings import FPS, SOUNDS_DIR, SPRITES_DIR, WIDTH, HEIGHT, WINDOW_TITLE
from scenes.game_scene import GameScene
from ui.menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.assets = AssetManager(SPRITES_DIR, SOUNDS_DIR)
        self.scene = GameScene(self.assets)

    def run(self):
        menu = Menu(self.screen)
        menu.run()

        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.scene.update()
            self.scene.draw(self.screen)
            pygame.display.update()
