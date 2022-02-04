from pygame.sprite import Sprite
import pygame


class Explosion(Sprite):
    def __init__(self, game):
        super().__init__()
        self.explosion_anim = {}
        self.explosion_anim["alien"] = []
        self.explosion_anim["ship"] = []
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # ms
        self.game = game

        for i in range(9):
            filename = f"regularExplosion0{i}.png"
            img = pygame.image.load(
                "images/explosion_animation/" + filename
            ).convert_alpha()

            # alien explosion
            img_alien = pygame.transform.scale(img, (60, 58))
            self.explosion_anim["alien"].append(img_alien)

            # ship explosion
            img_ship = pygame.transform.scale(img, (120, 116))
            self.explosion_anim["ship"].append(img_ship)

    def set_explosion_center_and_object(self, center, obj):
        self.obj = obj
        self.image = self.explosion_anim[self.obj][0]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:  # if 50ms has passed
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.obj]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.obj][self.frame]
                self.rect.center = center