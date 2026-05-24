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

    # desenha espada na tela
    def draw(self, surface: pygame.Surface):

        # só desenha se estiver ativa
        if self.active:

            pygame.draw.polygon(
                surface,
                (255, 215, 0),
                [

                    # topo
                    (self.rect.centerx, self.rect.top),

                    # direita
                    (self.rect.right, self.rect.centery),

                    # baixo
                    (self.rect.centerx, self.rect.bottom),

                    # esquerda
                    (self.rect.left, self.rect.centery)

                ]
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

    # desenha escudo na tela
    def draw(self, surface: pygame.Surface):

        # só desenha se estiver ativo
        if self.active:

            pygame.draw.circle(

                # superfície
                surface,

                # cor
                (100, 149, 237),

                # centro do círculo
                self.rect.center,

                # raio
                15,

                # espessura da borda
                2
            )