from pathlib import Path

import pygame


class AssetManager:

    def __init__(self, sprites_dir: Path, sounds_dir: Path):

        # pasta onde ficam os sprites/imagens
        self.sprites_dir = sprites_dir

        # pasta onde ficam os sons
        self.sounds_dir = sounds_dir

        # dicionário para guardar imagens carregadas
        self._images: dict[str, pygame.Surface] = {}

        # dicionário para guardar sons carregados
        self._sounds: dict[str, pygame.mixer.Sound] = {}

    # carrega uma imagem
    def load_image(
        self,
        key: str,
        filename: str,
        scale: tuple[int, int] | None = None
    ) -> pygame.Surface:

        # monta caminho da imagem
        caminho = self.sprites_dir / filename

        # carrega imagem com transparência
        image = pygame.image.load(str(caminho)).convert_alpha()

        # redimensiona caso tenha scale
        if scale:
            image = pygame.transform.scale(image, scale)

        # salva imagem no dicionário
        self._images[key] = image

        return image

    # pega imagem já carregada
    def get_image(self, key: str) -> pygame.Surface:

        return self._images[key]

    # carrega um som
    def load_sound(
        self,
        key: str,
        filename: str,
        volume: float = 1.0
    ) -> pygame.mixer.Sound:

        # monta caminho do som
        caminho = self.sounds_dir / filename

        # carrega som
        sound = pygame.mixer.Sound(str(caminho))

        # ajusta volume
        sound.set_volume(volume)

        # salva no dicionário
        self._sounds[key] = sound

        return sound

    # pega som já carregado
    def get_sound(self, key: str) -> pygame.mixer.Sound:

        return self._sounds[key]
