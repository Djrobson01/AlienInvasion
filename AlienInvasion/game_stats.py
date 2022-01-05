import json

class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        try:
            # Loads highest score recorded from a file
            with open("high_score.json") as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1