from pathlib import Path

WIDTH = 1000
HEIGHT = 860
FPS = 60
TILE_SIZE = 50

MAP_HEIGHT = 800
HUD_Y = MAP_HEIGHT
HUD_HEIGHT = HEIGHT - MAP_HEIGHT

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
SPRITES_DIR = ASSETS_DIR / "sprites"
SOUNDS_DIR = ASSETS_DIR / "sounds"

WINDOW_TITLE = "Torre do Cavaleiro"
