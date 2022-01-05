import sys
import json
from time import sleep

import pygame
from pygame import mouse
from pygame import KEYDOWN
from pygame.constants import MOUSEBUTTONDOWN

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from lives import Lives
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behaviors"""

    def __init__(self):
        # Initializes necessary tools for pygame to work
        pygame.init()

        # Creates settings object to maintain all settings
        self.settings = Settings()

        # Sets window screen size
        #self.screen = pygame.display.set_mode((1200, 800))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        # Gives window a name
        pygame.display.set_caption("Alien Invasion")

        # Create instances to keep stats and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Creates Ship object as ship and passes this objects as ai_game
        # @see def __init__() in ship.py
        self.ship = Ship(self)

        # Group of lives
        self.lives = pygame.sprite.Group()
        # Group of bullet sprites
        self.bullets = pygame.sprite.Group()
        # Group of alien sprites
        self.aliens = pygame.sprite.Group()

        self._set_lives()
        self._create_fleet()
        
        # Creates play button
        self.play_button = Button(self, "Play!")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Helper to check for mouse and keyboard events
            self._check_events()
        
            if self.stats.game_active:
                # Updates the ship's position
                self.ship.update()
                # Updates bullets
                self._update_bullets()
                # Updates aliens
                self._update_aliens()

            # Helper to update screen changes put all other updates before this one
            # Independent of whether or not the game is active
            self._update_screen()

    def _check_events(self):
        """Responds to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Saves the current high score to a file
                filename = "high_score.json"
                with open(filename, 'w') as f:
                    json.dump(self.stats.high_score, f)
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
               mouse_pos = pygame.mouse.get_pos()
               self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play!"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            # Initialize dynamic settings
            self.settings.initialize_dynamic_settings()

            # Reset stats and prep score and level
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.stats.game_active = True
    
            # Hide mouse
            pygame.mouse.set_visible(False)

            # Delete remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
    
            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_RETURN:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            # Pauses for 5 seconds
            sleep(5.0)
        elif event.key == pygame.K_ESCAPE:
            # Saves current high score to a file before exiting
            filename = "high_score.json"
            with open(filename, 'w') as f:
                json.dump(self.stats.high_score, f)
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _update_bullets(self):
        """Update bullet position and get rid of old bullets"""
        # Update ship's bullets
        self.bullets.update()

        # Delete unseen bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _create_life(self, life_number):
        """Creates life image and determines x and y coordinates"""
        life = Lives(self)
        life_width, life_height = life.rect.size

        life = Lives(self)
        life.rect.x = life_width * life_number
        life.rect.y = self.settings.screen_height - life_height

        # Adds to sprite group
        self.lives.add(life)

    def _set_lives(self):
        for life_number in range(self.settings.ship_limit):
            self._create_life(life_number)
            
    def _remove_life(self):
        """Remove a life when the ship gets hit or aliens hit the ground"""
        self.lives.empty()

        for lives_remaining in range(self.stats.ships_left):
            self._create_life(lives_remaining)
    
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        # Ensures that aliens that are hit at the same time are still counted towards score
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Make new level and increase difficulty when fleet is destroyed
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.settings.increase_speed()
            self.bullets.empty()
            self._create_fleet()

            # Increase level 
            self.stats.level += 1
            self.sb.prep_level()

            # Bonus points for destroying fleet
            self.stats.score += 500
        
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        new_bullet = Bullet(self)

        # Adds new bullet to sprite group if there are no more than 5 bullets on screen
        if(len(self.bullets) < 5):
            self.bullets.add(new_bullet)
    
    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Make an alien
        alien = Alien(self)

        # Determine how many aliens go in a row
        # Note: alien.rect.size returns a tuple of width and height
        alien_width, alien_height = alien.rect.size

        space_available_x = self.settings.screen_width - (2 * alien_width) - 15
        num_aliens_x = space_available_x // ((2 * alien_width) + 15)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        space_available_y = (self.settings.screen_height - 
            (3 * alien_height) - ship_height)
        num_rows = space_available_y // (2 * alien_height)

        # Create full fleet of aliens
        for row_number in range(num_rows):
            for alien_number in range(num_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        # Make an alien
        alien = Alien(self)
        # Determine how many aliens go in a row
        alien_width, alien_height = alien.rect.size
        
        # Create an alien and place it in the row
        alien = Alien(self)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien.rect.height + 2 * alien_height * row_number) - (self.screen.get_height() // 4)
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Updates the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Responds appropriately if an alien reaches the bottom"""
        screen_rect = self.screen.get_rect()

        # Checks through alien sprite group to see if one has reached the bootom
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat it as a ship hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit"""
        if self.stats.ships_left > 0:
            # Decrement ships left and remove a life
            self.stats.ships_left -= 1
            self._remove_life()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause for 1.5 seconds
            sleep(1.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        # Redraw the screen during each pass through the loop
        # Fills display window with specified color
        self.screen.fill(self.settings.bg_color)
        
        # Draws ship to screen
        self.ship.blitme()

        # Draw bullets to screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draws lives onto the screen
        self.lives.draw(self.screen)

        # Draw aliens to screen using sprite group draw
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draws button to the screen
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()