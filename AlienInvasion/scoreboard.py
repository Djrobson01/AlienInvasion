import pygame.font

class Scoreboard:
    """A class to report scoring information"""
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (225, 220, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial scoring image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = "Lvl: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
            self.text_color, self.settings.bg_color)

        # Position in top right
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.screen_rect.top
        self.level_rect.right = self.screen_rect.right - 30

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, 
            self.text_color, self.settings.bg_color)

        # Center it at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.settings.bg_color)
        
        # Display score at the bottom right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - self.score_rect.width
        self.score_rect.bottom = self.screen_rect.bottom

    def check_high_score(self):
        """Check to see if there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw scores to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    