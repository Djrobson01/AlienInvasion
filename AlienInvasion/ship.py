import pygame

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('Python Projects/AlienInvasion/images/fighter.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Will allow speed to be decimal values
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """Center the ship on the bottom of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.screen_rect.height - self.rect.height
        self.y = self.rect.y
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position based on movement flags"""
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_up and self.rect.top > (self.screen_rect.height / 2):
            self.y -= self.settings.ship_speed
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Updates ship obj rect location
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        # Draw the ship to the screen
        self.screen.blit(self.image, self.rect)