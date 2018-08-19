import SETTINGS
import SPRITES
import SOUND
import pygame
import os


class Item:

    def __init__(self, pos, sprite, item_type, effect):
        '''Item that can be picked up by the player\npos -> tile pos | sprite -> texture path | item_type -> health, armor, *ammo*, gun\neffect -> relative'''
        self.pos = (pos[0] * SETTINGS.tile_size, pos[1] * SETTINGS.tile_size)
        self.map_pos = pos
        self.item_type = item_type
        self.rect = pygame.Rect(self.pos[0], self.pos[1], int(SETTINGS.tile_size), int(SETTINGS.tile_size))
        self.rect.center = (self.pos[0] + SETTINGS.tile_size/2, self.pos[1] + SETTINGS.tile_size/2)
        self.sprite = SPRITES.Sprite(pygame.image.load(sprite), hash(item_type), self.rect.center, 'sprite')
        self.effect = effect
        self.sound = pygame.mixer.Sound(os.path.join('sounds', 'other', 'blub.ogg'))
        
    def update(self):
        remove = False
        if self.rect:
            if SETTINGS.player_rect.colliderect(self.rect):
                if self.item_type == 'health':
                    if SETTINGS.player_health < 100:
                        SETTINGS.player_health += self.effect
                        if SETTINGS.player_health > 100:
                            SETTINGS.player_health = 100
                        SETTINGS.player_states['heal'] = True
                        remove = True
                    
                elif self.item_type == 'armor':
                    if SETTINGS.player_armor < 100:
                        SETTINGS.player_armor += self.effect
                        if SETTINGS.player_armor > 100:
                            SETTINGS.player_armor = 100
                        SETTINGS.player_states['armor'] = True
                        remove = True

                elif self.item_type == 'bullet' or self.item_type == 'shell' or self.item_type == 'ferromag':
                    if SETTINGS.held_ammo[self.item_type] < SETTINGS.max_ammo[self.item_type]:
                        SETTINGS.held_ammo[self.item_type] += self.effect
                        if SETTINGS.held_ammo[self.item_type] > SETTINGS.max_ammo[self.item_type]:
                            SETTINGS.held_ammo[self.item_type] = SETTINGS.max_ammo[self.item_type]
                        #Same effect as armor
                        SETTINGS.player_states['armor'] = True
                        remove = True

                elif self.item_type == 'primary':
                    if not SETTINGS.inventory['primary']:
                        SETTINGS.inventory['primary'] = self.effect
                        SETTINGS.next_gun = self.effect
                        SETTINGS.player_states['armor'] = True
                        remove = True
                    else:
                        SETTINGS.ground_weapon = self.effect

                elif self.item_type == 'secondary':
                    if not SETTINGS.inventory['secondary']:
                        SETTINGS.inventory['secondary'] = self.effect
                        SETTINGS.next_gun = self.effect
                        SETTINGS.player_states['armor'] = True
                        remove = True
                    else:
                        SETTINGS.ground_weapon = self.effect

                elif self.item_type == 'melee':
                    if not SETTINGS.inventory['melee']:
                        SETTINGS.inventory['melee'] = self.effect
                        SETTINGS.next_gun = self.effect
                        SETTINGS.player_states['armor'] = True
                        remove = True
                    else:
                        SETTINGS.ground_weapon = self.effect
                            
                #Remove sprite and rect
                if self.sprite in SETTINGS.all_sprites and remove:
                    SOUND.play_sound(self.sound, 0)
                    SETTINGS.all_sprites.remove(self.sprite)
                    self.rect = None
                
