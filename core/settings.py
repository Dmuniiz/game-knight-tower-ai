from pathlib import Path


# largura da janela
WIDTH = 1000

# altura da janela
HEIGHT = 860

# frames por segundo
FPS = 60

# tamanho de cada bloco do mapa
TILE_SIZE = 50


# altura da área jogável
MAP_HEIGHT = 800

# posição Y da HUD
HUD_Y = MAP_HEIGHT

# altura da HUD
HUD_HEIGHT = HEIGHT - MAP_HEIGHT


# pasta raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent

# pasta principal de assets
ASSETS_DIR = ROOT_DIR / "assets"

# pasta de sprites
SPRITES_DIR = ASSETS_DIR / "sprites"

# pasta de sons
SOUNDS_DIR = ASSETS_DIR / "sounds"


# nome da janela
WINDOW_TITLE = "Torre do Cavaleiro"