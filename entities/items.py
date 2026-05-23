import pygame


class Sword:
    """Espada: mata um inimigo ao encostar, depois quebra."""
    
    def __init__(self, x: float, y: float):
        self.rect = pygame.Rect(x + 10, y + 10, 30, 30)
        self.active = True
        
    def draw(self, surface: pygame.Surface):
        """Desenha a espada como um retângulo dourado."""
        if self.active:
            pygame.draw.polygon(surface, (255, 215, 0), [
                (self.rect.centerx, self.rect.top),
                (self.rect.right, self.rect.centery),
                (self.rect.centerx, self.rect.bottom),
                (self.rect.left, self.rect.centery)
            ])


class Shield:
    """Escudo: absorve um hit do inimigo."""
    
    def __init__(self, x: float, y: float):
        self.rect = pygame.Rect(x + 10, y + 10, 30, 30)
        self.active = True
        
    def draw(self, surface: pygame.Surface):
        """Desenha o escudo como um círculo azul."""
        if self.active:
            pygame.draw.circle(surface, (100, 149, 237), self.rect.center, 15, 2)
