import SETTINGS
import TEXT
import pygame
import os

class hud:

    def __init__(self):
        self.health = SETTINGS.player_health
        self.armor = SETTINGS.player_armor
        self.ammo = 0

        self.sprite = pygame.image.load(os.path.join('graphics', 'hud.png')).convert()
        self.sprite = pygame.transform.scale(self.sprite, (SETTINGS.canvas_actual_width, SETTINGS.window_height-SETTINGS.canvas_target_height))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (0, SETTINGS.canvas_target_height)

        self.text = [TEXT.Text(int(self.rect.width/35), self.rect.y + int(self.rect.height/2.5), 'PLAYER ARMOR', SETTINGS.DARKGRAY, 'DUGAFONT.ttf', 35),
                     TEXT.Text(int(self.rect.width/3.4), self.rect.y + int(self.rect.height/2.5), 'PLAYER HEALTH', SETTINGS.DARKGRAY, 'DUGAFONT.ttf', 35),
                     TEXT.Text(int(self.rect.width/1.8), self.rect.y + int(self.rect.height/2.5), 'AMMUNITION', SETTINGS.DARKGRAY, 'DUGAFONT.ttf', 35)]

        self.arrow_spritesheet = pygame.image.load(os.path.join('graphics', 'arrows.png')).convert_alpha()


        self.arrow = self.arrow_spritesheet.subsurface(0,0,17,17).convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (50,50))
        self.original_arrow = self.arrow
        self.arrow_rect = self.arrow.get_rect()
        self.arrow_rect.center = (self.rect.topright[0] - 46, self.rect.topright[1] + 66)
        self.arrow_center = (self.arrow_rect.centerx - self.arrow_rect.width / 2,
                             self.arrow_rect.centery - self.arrow_rect.height / 2)

        self.arrow2 = self.arrow_spritesheet.subsurface(0,17,17,17).convert_alpha()
        self.arrow2 = pygame.transform.scale(self.arrow2, (50,50))
        self.original_arrow2 = self.arrow2
        self.arrow3 = self.arrow_spritesheet.subsurface(0,34,17,17).convert_alpha()
        self.arrow3 = pygame.transform.scale(self.arrow3, (50,50))
        self.original_arrow3 = self.arrow3

        
    def render(self, canvas):
        
        canvas.blit(self.sprite, self.rect)
        self.text[0].update_string('%s / 100' % SETTINGS.player_armor)
        self.text[1].update_string('%s / 100' % SETTINGS.player_health)
        if SETTINGS.current_gun and SETTINGS.current_gun.ammo_type:
            self.text[2].update_string('%s / %s' % (SETTINGS.current_gun.current_mag, SETTINGS.held_ammo[SETTINGS.current_gun.ammo_type]))
        else:
            self.text[2].update_string('-- / --')
        for string in self.text:
            string.draw(canvas)

  
        self.arrow = pygame.transform.rotate(self.original_arrow, SETTINGS.end_angle)
        self.arrow_rect.topleft = (self.arrow_center[0] - self.arrow.get_rect().width /2,
                                   self.arrow_center[1] - self.arrow.get_rect().height /2)
        canvas.blit(self.arrow, self.arrow_rect)

        #test
        self.arrow2 = pygame.transform.rotate(self.original_arrow2, SETTINGS.end_angle)
        self.arrow3 = pygame.transform.rotate(self.original_arrow3, SETTINGS.end_angle)

        canvas.blit(self.arrow2, (self.arrow_rect[0], self.arrow_rect[1] - 4))
        canvas.blit(self.arrow3, (self.arrow_rect[0], self.arrow_rect[1] - 8))




        
