import pygame
from pygame.sprite import Sprite
import pygame
import random
import os.path


class Alien(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        self.image = pygame.image.load(
            os.path.join(os.path.dirname(__name__), "images", "Alien.png")
        ).convert_alpha()
        self.image.set_alpha(random.randint(1, 255))  # Make aliens randomly transparent
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if an alien hits the edge of the screen"""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True

    def create_fleet(self):
        alien = Alien(self.game)
        alien_width, alien_height = alien.rect.size  # size = tuple(int x, int y)
        ship_height = self.game.ship.rect.height

        # Calculate how many aliens fit in a row including empty space
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = available_space_x // (2 * alien_width)

        # Calculate how many rows of aliens fit including empty space
        available_space_y = self.settings.screen_height - 3 * alien_height - ship_height
        number_of_aliens_y = available_space_y // (2 * alien_height)

        # Create full fleet
        for row in range(number_of_aliens_y):
            for alien_number in range(number_of_aliens_x):
                self.create_alien(alien_number, row)

    def create_alien(self, alien_number, row):
        alien = Alien(self.game)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row
        self.game.aliens.add(alien)

    def check_fleet_edges(self):
        for alien in self.game.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Drop the fleet and change direction"""
        for alien in self.game.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_aliens_bottom(self):
        for alien in self.game.aliens:
            if alien.rect.bottom >= self.screen_rect.bottom:
                self.game.ship.ship_hit()
                break

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
