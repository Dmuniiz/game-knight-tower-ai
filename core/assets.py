from pathlib import Path

import pygame


class AssetManager:
    def __init__(self, sprites_dir: Path, sounds_dir: Path):
        self.sprites_dir = sprites_dir
        self.sounds_dir = sounds_dir
        self._images: dict[str, pygame.Surface] = {}
        self._sounds: dict[str, pygame.mixer.Sound] = {}

    def load_image(self, key: str, filename: str, scale: tuple[int, int] | None = None) -> pygame.Surface:
        image = pygame.image.load(str(self.sprites_dir / filename)).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        self._images[key] = image
        return image

    def get_image(self, key: str) -> pygame.Surface:
        return self._images[key]

    def load_sound(self, key: str, filename: str, volume: float = 1.0) -> pygame.mixer.Sound:
        sound = pygame.mixer.Sound(str(self.sounds_dir / filename))
        sound.set_volume(volume)
        self._sounds[key] = sound
        return sound

    def get_sound(self, key: str) -> pygame.mixer.Sound:
        return self._sounds[key]
