class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize game settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (45, 45, 45)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 6
        self.bullet_height = 12
        self.bullet_color = (223, 30, 60)

        # Alien settings
        self.fleet_drop_speed = 10

        # Speed multiplier
        self.speedup_scale = 1.2
        self.score_scale = 1.2
        

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # Set score for aliens
        self.alien_points = 50
        
        # fleet_direction of 1 = right; -1 = left
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

