import pygame
from pygame.sprite import Sprite

class Lives(Sprite):
    """Creates life sprites for Alien Invasion"""
    
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load image
        self.image = pygame.image.load('AlienInvasion/images/fighter.bmp')
        self.rect = self.image.get_rect()

        # Place image at the bottom left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

