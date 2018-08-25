#This is the script that controls the game maps. It makes the array and the tiles.

import SETTINGS
import SPRITES
import SOUND
import pygame
import math
import random
import os

class Map:
    '''== Create the map ==\narray -> Level to be loaded'''
    def __init__(self, array):
        self.array = array
        self.tile_size = SETTINGS.tile_size
        self.width = len(self.array[0])-1
        self.height = len(self.array)-1
        SETTINGS.current_level_size = (self.width, self.height)

        for row in range(len(self.array)):
            for column in range(len(self.array[row])):
                SETTINGS.all_tiles.append(Tile(self.array[row][column], [column*self.tile_size, row*self.tile_size], [column, row]))
            
        for tile in SETTINGS.all_tiles:
            if SETTINGS.tile_solid[tile.ID]:
                SETTINGS.all_solid_tiles.append(tile)
            if tile.type == 'trigger':
                SETTINGS.trigger_tiles.append(tile)

        #Add a tile that is always outside the walkable area (air)
        SETTINGS.all_tiles.append(Tile(0, [column+1 * self.tile_size, row+1 * self.tile_size],[column+1, row+1]))
                
    def draw(self, canvas):
        for tile in SETTINGS.all_solid_tiles:
            if SETTINGS.tile_visible[tile.ID]:
                tile.draw(canvas)

    def move_inaccessible_entities(self):      
        wa = []
        for i in SETTINGS.walkable_area:
            if i.type != 'hdoor' and i.type != 'vdoor':
                wa.append(i.map_pos)
            
        move_items = [x for x in SETTINGS.levels_list[SETTINGS.current_level].items if list(x[0]) not in wa]
        move_npcs = [x for x in SETTINGS.levels_list[SETTINGS.current_level].npcs if list(x[0]) not in wa]
        
        item_positions = [x[0] for x in SETTINGS.levels_list[SETTINGS.current_level].items if list(x[0]) in wa]
        npc_positions = [x[0] for x in SETTINGS.levels_list[SETTINGS.current_level].npcs if list(x[0]) in wa]

        possible_item_positions = [x for x in wa if tuple(wa) not in item_positions]
        temp_possible_npc_positions = [x for x in wa if tuple(wa) not in npc_positions]
        possible_npc_positions = []
        #Remove npc positions too close to the player
        for pos in temp_possible_npc_positions:
            x = abs(SETTINGS.player_map_pos[0] - pos[0])
            y = abs(SETTINGS.player_map_pos[1] - pos[1])
            
            if math.sqrt(x**2 + y**2) >= 8: #Length of vector between player and NPC
                possible_npc_positions.append(pos)            
        
        for i in range(len(move_items)):
            #print("Moved item from ", move_items[i][0])
            index = SETTINGS.levels_list[SETTINGS.current_level].items.index(move_items[i]) #Get item index
            SETTINGS.levels_list[SETTINGS.current_level].items[index] = ((random.choice(possible_item_positions)), move_items[i][1]) #Choose new location for item
            possible_item_positions.remove(list(SETTINGS.levels_list[SETTINGS.current_level].items[index][0])) #Remove possible location
            #print("to ", SETTINGS.levels_list[SETTINGS.current_level].items[index][0])

        for i in range(len(move_npcs)):
            #print("Moved NPC from ", move_npcs[i][0])
            index = SETTINGS.levels_list[SETTINGS.current_level].npcs.index(move_npcs[i])
            SETTINGS.levels_list[SETTINGS.current_level].npcs[index] = ((random.choice(possible_npc_positions)), move_npcs[i][1], move_npcs[i][2])
            possible_npc_positions.remove(list(SETTINGS.levels_list[SETTINGS.current_level].npcs[index][0]))
            #print("to ", SETTINGS.levels_list[SETTINGS.current_level].npcs[index][0])

        #print("This level has %s items and %s NPC's" % (len(SETTINGS.levels_list[SETTINGS.current_level].items), len(SETTINGS.levels_list[SETTINGS.current_level].npcs)))

class Tile:
    
    def __init__(self, ID, pos, map_pos):
        self.ID = ID
        #position in pixels
        self.pos = pos
        self.type = SETTINGS.texture_type[self.ID]
        #position in tiles
        self.map_pos = map_pos
        self.distance = None
        self.solid = SETTINGS.tile_solid[self.ID]
        #For doors opening
        self.state = None
        self.timer = 0
        
        if self.type == 'sprite':
            current_number = len(SETTINGS.all_sprites)
            #Need some weird coordinates to make it centered.
            self.texture = SPRITES.Sprite(SETTINGS.tile_texture[self.ID], self.ID, (self.pos[0]+SETTINGS.tile_size/3, self.pos[1]+SETTINGS.tile_size/3), 'sprite')
            
            self.rect = pygame.Rect(pos[0], pos[1], SETTINGS.tile_size/2, SETTINGS.tile_size/2)

        else:
            self.texture = SETTINGS.tile_texture[self.ID].texture
            self.icon = pygame.transform.scale(self.texture, (16,16)).convert()
            self.texture = pygame.transform.scale(self.texture, (SETTINGS.tile_size, SETTINGS.tile_size)).convert()
            self.rect = self.texture.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
            
            if self.type == 'vdoor' or self.type == 'hdoor':
                self.open = 0
                self.state = 'closed'
                #states: closed, opening, open, closing

                self.open_sound = pygame.mixer.Sound(os.path.join('sounds', 'other', 'door_open.ogg'))
                self.close_sound = pygame.mixer.Sound(os.path.join('sounds', 'other', 'door_close.ogg'))

                SETTINGS.all_doors.append(self)


    def draw(self, canvas):
        canvas.blit(self.icon, (self.rect.x/4, self.rect.y/4))

    def get_dist(self, pos, *called):
        xpos = self.rect.center[0] - pos[0]
        ypos = pos[1] - self.rect.center[1]
        self.distance = math.sqrt(xpos*xpos + ypos*ypos)

        if (self.state and self.state != 'closed') and called != ('npc',): #lol
            self.sesam_luk_dig_op()
            
        return self.distance

    def sesam_luk_dig_op(self):
        if self.open > SETTINGS.tile_size:
            self.open = SETTINGS.tile_size
        elif self.open < 0:
            self.open = 0
            
        if self.state == 'closed':
            self.state = 'opening'
            
        elif self.state == 'opening':
            if self.open == 0:
                SOUND.play_sound(self.open_sound, self.distance)
                
            if self.open < SETTINGS.tile_size:
                self.open += SETTINGS.tile_size * SETTINGS.dt
            else:
                self.state = 'open'
                self.solid = False
            if self.open > SETTINGS.tile_size/1.4:
                self.solid = False

        elif self.state == 'open':
            self.timer += SETTINGS.dt
            if self.timer > 5 and not self.rect.colliderect(SETTINGS.player_rect):
                for i in SETTINGS.npc_list:
                    if self.rect.colliderect(i.rect):
                        break
                else:   
                    self.state = 'closing'
                    self.solid = True
                    self.timer = 0

        elif self.state == 'closing':
            if self.open >= SETTINGS.tile_size:
                SOUND.play_sound(self.close_sound, self.distance)
            if self.open > 0:
                self.open -= SETTINGS.tile_size * SETTINGS.dt
            else:
                self.state = 'closed'


            
        
