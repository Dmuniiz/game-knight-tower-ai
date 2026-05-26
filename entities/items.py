import pygame


class Sword:

    def __init__(self, x: float, y: float):

        # hitbox da espada
        self.rect = pygame.Rect(
            x + 10,
            y + 10,
            30,
            30
        )

        # define se a espada ainda existe
        self.active = True

        #carrega sprite da espada
        self.sprite = pygame.image.load(
            "assets\sprites\Itens\Espada.png"
        ).convert_alpha()

        #tamanho do sprite
        self.sprite = pygame.transform.scale(
            self.sprite,
            (60, 60)
        )

    # desenha espada na tela
    def draw(self, surface: pygame.Surface):

        # só desenha se estiver ativa
        if self.active:

            surface.blit(
                self.sprite,
                self.sprite.get_rect(center=self.rect.center)
            )



class Shield:

    def __init__(self, x: float, y: float):

        # hitbox do escudo
        self.rect = pygame.Rect(
            x + 10,
            y + 10,
            30,
            30
        )

        # define se o escudo ainda existe
        self.active = True

        #carrega sprite do escudo
        self.sprite = pygame.image.load(
            "assets/sprites/itens/Escudo.png"
        ).convert_alpha()

        #converte pixel preto em transparente
        self.sprite.set_colorkey((0, 0, 0))

        #tamanho do sprite
        self.sprite = pygame.transform.scale(
            self.sprite,
            (50, 50)
        )

    # desenha escudo na tela
    def draw(self, surface: pygame.Surface):

        if self.active:

            surface.blit(
                self.sprite,
                self.sprite.get_rect(center=self.rect.center)
            )