from pathlib import Path

WIDTH = 800
HEIGHT = 600
FPS = 60
TILE_SIZE = 50

MAP_HEIGHT = 540
HUD_Y = MAP_HEIGHT
HUD_HEIGHT = HEIGHT - MAP_HEIGHT

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
SPRITES_DIR = ASSETS_DIR / "sprites"
SOUNDS_DIR = ASSETS_DIR / "sounds"

WINDOW_TITLE = "Torre do Cavaleiro"
