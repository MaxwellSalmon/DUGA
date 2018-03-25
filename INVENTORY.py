#This class / script is not a part of the engine itself. This means it will not
#Be as easy to modify as the other parts. (As if they were easy)
import SETTINGS
import TEXT
import ITEMS
import pygame
import os

class inventory:
    
    #ammo_dict is dict with the max amout of each type of ammo.
    def __init__(self, ammo_dict):
        self.bg = pygame.image.load(os.path.join('graphics', 'inventory.png')).convert_alpha()
        self.rect = self.bg.get_rect()
        self.rect.center = (int(SETTINGS.canvas_actual_width/2), int(SETTINGS.canvas_target_height/2))
        
        self.held_ammo = {}
        for x in ammo_dict:
            self.held_ammo[x] = 0

        SETTINGS.held_ammo = self.held_ammo
        SETTINGS.max_ammo = ammo_dict

        #Menu
        self.menu = pygame.Surface((150, 200)).convert()
        self.menu_rect = self.menu.get_rect()
        self.menudraw = False
        self.selected = None

        self.submenus = []
        self.submenu_rects = []

        for i in range(0, 9):
            if i == 0 or i == 8:
                self.submenus.append(self.menu.subsurface(0, 0, 150, 30).convert())
                self.submenu_rects.append(self.submenus[i].get_rect())
            else:
                self.submenus.append(self.menu.subsurface(0, 0, 150, 20).convert())
                self.submenu_rects.append(self.submenus[i].get_rect())
            
            if i % 2 == 0:
                self.submenus[i].fill((65,65,65))
            else:
                self.submenus[i].fill((55,55,55))
        
        #Close button
        self.closebtn = pygame.Surface((176, 64)).convert_alpha()
        self.closebtn_rect = self.closebtn.get_rect()
        self.closebtn_rect.topleft = (self.rect.x + 353, self.rect.y + 353)
        self.closebtn.fill((100,100,100,100))

        #Primary weapon
        self.primaryslot = pygame.Surface((272, 80)).convert_alpha()
        self.primaryslot_rect = self.primaryslot.get_rect()
        self.primaryslot_rect.topleft = (self.rect.x + 33, self.rect.y + 33)
        self.primaryslot.fill((100,100,100,100))

        #Secondary weapon
        self.secondslot = pygame.Surface((176, 81)).convert_alpha()
        self.secondslot_rect = self.secondslot.get_rect()
        self.secondslot_rect.topleft = (self.rect.x + 33, self.rect.y + 129)
        self.secondslot.fill((100,100,100,100))

        #Melee weapon
        self.meleeslot = pygame.Surface((176, 81)).convert_alpha()
        self.meleeslot_rect = self.meleeslot.get_rect()
        self.meleeslot_rect.topleft = (self.rect.x + 33, self.rect.y + 225)
        self.meleeslot.fill((100,100,100,100))

        #Stuff
        self.mousepos = pygame.mouse.get_pos()
        self.timer = 0
        self.closing = False
        self.text = [TEXT.Text(0, 0, 'NAME', SETTINGS.WHITE, 'DUGAFONT.ttf', 18),
                     TEXT.Text(0, 0, 'DAMAGE: --', SETTINGS.LIGHTGRAY, 'DUGAFONT.ttf', 15),
                     TEXT.Text(0, 0, 'SPREAD: --', SETTINGS.LIGHTGRAY, 'DUGAFONT.ttf', 15),
                     TEXT.Text(0, 0, 'ACCURACY: --', SETTINGS.LIGHTGRAY, 'DUGAFONT.ttf', 15),
                     TEXT.Text(0, 0, 'RANGE: --', SETTINGS.LIGHTGRAY, 'DUGAFONT.ttf', 15),
                     TEXT.Text(0, 0, 'MAGAZINE SIZE: --', SETTINGS.LIGHTGRAY, 'DUGAFONT.ttf', 15),
                     TEXT.Text(0, 0, 'RELOAD TIME: --', SETTINGS.LIGHTGRAY, 'DUGAFONT.ttf', 15),
                     TEXT.Text(0, 0, 'AMMO TYPE: --', SETTINGS.LIGHTGRAY, 'DUGAFONT.ttf', 15),
                     TEXT.Text(0, 0, 'DROP', SETTINGS.WHITE, 'DUGAFONT.ttf', 18)]

    def draw(self, canvas):
        canvas.blit(self.bg, self.rect)
        self.timer += SETTINGS.dt

        #Draw items
        if SETTINGS.inventory['primary']:
            canvas.blit(SETTINGS.inventory['primary'].subitemtexture, (self.primaryslot_rect.x, self.primaryslot_rect.y + 5))
        if SETTINGS.inventory['secondary']:
            canvas.blit(SETTINGS.inventory['secondary'].subitemtexture, (self.secondslot_rect.x - self.secondslot_rect.width/4, self.secondslot_rect.y))
        if SETTINGS.inventory['melee']:
            canvas.blit(SETTINGS.inventory['melee'].subitemtexture, (self.meleeslot_rect.x - self.secondslot_rect.width/4, self.meleeslot_rect.y))

       #Mouse on close button
        if self.closebtn_rect.collidepoint(pygame.mouse.get_pos()):
            canvas.blit(self.closebtn, self.closebtn_rect)
            if pygame.mouse.get_pressed()[0]:
                self.timer = 0
                self.closing = True
                
        #Mouse on primary
        elif self.primaryslot_rect.collidepoint(pygame.mouse.get_pos()) and (not self.menudraw or self.selected == 'primary'):
            canvas.blit(self.primaryslot, self.primaryslot_rect)
            self.selected = 'primary'
            if pygame.mouse.get_pressed()[0] and SETTINGS.inventory['primary']:
                self.menudraw = True
                self.mousepos = pygame.mouse.get_pos()
                
        #Mouse on secondary
        elif self.secondslot_rect.collidepoint(pygame.mouse.get_pos()) and (not self.menudraw or self.selected == 'secondary'):
            canvas.blit(self.secondslot, self.secondslot_rect)
            self.selected = 'secondary'
            if pygame.mouse.get_pressed()[0] and SETTINGS.inventory['secondary']:
                self.menudraw = True
                self.mousepos = pygame.mouse.get_pos()
            
        #Mouse on melee
        elif self.meleeslot_rect.collidepoint(pygame.mouse.get_pos()) and (not self.menudraw or self.selected == 'melee'):
            canvas.blit(self.meleeslot, self.meleeslot_rect)
            self.selected = 'melee'
            if pygame.mouse.get_pressed()[0] and SETTINGS.inventory['melee']:
                self.menudraw = True
                self.mousepos = pygame.mouse.get_pos()

        #Mouse on menu
        elif self.menu_rect.collidepoint(pygame.mouse.get_pos()) and self.menudraw:
            self.menudraw = True
            
        else:
            self.menudraw = False
            self.selected = None

        if self.menudraw and SETTINGS.inventory[self.selected]:
            self.draw_menu(canvas)

        #Close menu without shooting
        if self.closing and self.timer >= 0.2:
            SETTINGS.player_states['invopen'] = False
            self.closing = False
            self.timer = 0

    def draw_menu(self, canvas):
        self.menu_rect.topleft = self.mousepos

        #Draw menu
        i = 0
        for menu in self.submenus:
            if i == 0:
                self.submenu_rects[i].topleft = (self.mousepos[0], self.mousepos[1])
            else:
                self.submenu_rects[i].topleft = (self.mousepos[0], self.mousepos[1]+i*20+10)
            canvas.blit(menu, self.submenu_rects[i])            
            i += 1

        #Update weapon stats
        self.text[0].update_string('%s' % SETTINGS.inventory[self.selected].name)
        self.text[1].update_string('DAMAGE            : %s' % SETTINGS.inventory[self.selected].dmg)
        self.text[2].update_string('SPREAD              : %s' % SETTINGS.inventory[self.selected].accuracy)
        self.text[3].update_string('ACCURACY    : %s / 100' % SETTINGS.inventory[self.selected].hit_percent)
        self.text[4].update_string('RANGE                 : %s' % SETTINGS.inventory[self.selected].range)
        self.text[5].update_string('MAG SIZE      : %s' % SETTINGS.inventory[self.selected].mag_size)
        self.text[6].update_string('REL TIME      : %s' % SETTINGS.inventory[self.selected].rlspeed)
        self.text[7].update_string('AMMO TYP  : %s' % SETTINGS.inventory[self.selected].ammo_type)

        #Update text
        x = 0
        for string in self.text:
            if x == 0:
                string.update_pos(self.mousepos[0]+5, self.mousepos[1]+8)
            elif x == 8:
                string.update_pos(self.mousepos[0]+55, self.mousepos[1]+x*20+15)
            else:
                string.update_pos(self.mousepos[0]+5, self.mousepos[1]+x*20+12)
            string.draw(canvas)
            x += 1

        #Drop weapon
        if self.submenu_rects[-1].collidepoint(pygame.mouse.get_pos()):
            self.submenus[-1].fill((45,45,45))
            if pygame.mouse.get_pressed()[0] and self.timer >= 0.5:
                self.timer = 0
                #Find a place to drop item
                if [x for x in SETTINGS.all_tiles if x.map_pos == [SETTINGS.player_map_pos[0]+1, SETTINGS.player_map_pos[1]] and not SETTINGS.tile_solid[x.ID]] and not [x for x in SETTINGS.all_items if x.map_pos == [SETTINGS.player_map_pos[0]+1, SETTINGS.player_map_pos[1]]]:
                    itempos = [SETTINGS.player_map_pos[0]+1, SETTINGS.player_map_pos[1]]
                elif [x for x in SETTINGS.all_tiles if x.map_pos == [SETTINGS.player_map_pos[0]-1, SETTINGS.player_map_pos[1]] and not SETTINGS.tile_solid[x.ID]] and not [x for x in SETTINGS.all_items if x.map_pos == [SETTINGS.player_map_pos[0]-1, SETTINGS.player_map_pos[1]]]:
                    itempos = [SETTINGS.player_map_pos[0]-1, SETTINGS.player_map_pos[1]]
                elif [x for x in SETTINGS.all_tiles if x.map_pos == [SETTINGS.player_map_pos[0], SETTINGS.player_map_pos[1]+1] and not SETTINGS.tile_solid[x.ID]] and not [x for x in SETTINGS.all_items if x.map_pos == [SETTINGS.player_map_pos[0], SETTINGS.player_map_pos[1]+1]]:
                    itempos = [SETTINGS.player_map_pos[0], SETTINGS.player_map_pos[1]+1]
                elif [x for x in SETTINGS.all_tiles if x.map_pos == [SETTINGS.player_map_pos[0], SETTINGS.player_map_pos[1]-1] and not SETTINGS.tile_solid[x.ID]] and not [x for x in SETTINGS.all_items if x.map_pos == [SETTINGS.player_map_pos[0], SETTINGS.player_map_pos[1]-1]]:
                    itempos = [SETTINGS.player_map_pos[0], SETTINGS.player_map_pos[1]-1]
                else:
                    itempos = SETTINGS.player_map_pos
                SETTINGS.all_items.append(ITEMS.Item(itempos, SETTINGS.inventory[self.selected].itemtexture, SETTINGS.inventory[self.selected].guntype, SETTINGS.inventory[self.selected]))

                if SETTINGS.inventory[self.selected].ammo_type:
                    SETTINGS.held_ammo[SETTINGS.inventory[self.selected].ammo_type] += SETTINGS.current_gun.current_mag
                    SETTINGS.inventory[self.selected].current_mag = 0
                if self.selected == SETTINGS.current_gun or SETTINGS.next_gun:
                    SETTINGS.current_gun = None
                    SETTINGS.next_gun = None
                    
                SETTINGS.inventory[self.selected] = None

        else:
            self.submenus[-1].fill((65,65,65))

            


            
                
            


#Ammo types: bullet, shell
#gun types: primary, secondary, melee
