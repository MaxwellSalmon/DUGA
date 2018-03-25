import SETTINGS
import TEXT
import pygame

class hud:

    def __init__(self, sprite):
        self.health = SETTINGS.player_health
        self.armor = SETTINGS.player_armor
        self.ammo = 0

        self.sprite = pygame.image.load(sprite).convert()
        self.sprite = pygame.transform.scale(self.sprite, (SETTINGS.canvas_actual_width, SETTINGS.window_height-SETTINGS.canvas_target_height))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (0, SETTINGS.canvas_target_height)

        self.text = [TEXT.Text(int(self.rect.width/35), self.rect.y + int(self.rect.height/2.5), 'PLAYER ARMOR', SETTINGS.DARKGRAY, 'DUGAFONT.ttf', 35),
                     TEXT.Text(int(self.rect.width/3.4), self.rect.y + int(self.rect.height/2.5), 'PLAYER HEALTH', SETTINGS.DARKGRAY, 'DUGAFONT.ttf', 35),
                     TEXT.Text(int(self.rect.width/1.8), self.rect.y + int(self.rect.height/2.5), 'AMMUNITION', SETTINGS.DARKGRAY, 'DUGAFONT.ttf', 35)]
        
    def render(self, canvas):
        
        canvas.blit(self.sprite, self.rect)
        self.text[0].update_string('%s' % SETTINGS.player_armor)
        self.text[1].update_string('%s' % SETTINGS.player_health)
        if SETTINGS.current_gun and SETTINGS.current_gun.ammo_type:
            self.text[2].update_string('%s / %s' % (SETTINGS.current_gun.current_mag, SETTINGS.held_ammo[SETTINGS.current_gun.ammo_type]))
        else:
            self.text[2].update_string('-- / --')
        for string in self.text:
            string.draw(canvas)
