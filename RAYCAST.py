#This is the script where all the code for raycasting goes. The screen rendering in 2.5D will also go here.

import SETTINGS
import PLAYER
import pygame
import math

pygame.init()

class Slice:

    def __init__(self, location, surface, width, vh):
        self.slice = surface.subsurface(pygame.Rect(location, (1, width))).convert()
        self.rect = self.slice.get_rect(center = (0, SETTINGS.canvas_target_height/2))
        self.distance = None
        self.type = 'slice'
        self.vh = vh
        self.xpos = 0

        if SETTINGS.shade:
            self.shade_slice = pygame.Surface(self.slice.get_size()).convert_alpha()
            sv = SETTINGS.shade_visibility / 10
            self.shade_intensity = [sv*1, sv*2, sv*3, sv*4, sv*5, sv*6, sv*7, sv*8, sv*9, sv*10]
        
    def update_rect(self, new_slice):            
        self.tempslice = new_slice
        self.rect = new_slice.get_rect(center = (self.xpos, int(SETTINGS.canvas_target_height/2)))

        if self.vh == 'v':
            self.darkslice = pygame.Surface(self.tempslice.get_size()).convert_alpha()
            self.darkslice.fill((0,0,0,SETTINGS.texture_darken))

        if SETTINGS.shade:
            #Shade intensity table
            intensity = 0
            if self.distance < self.shade_intensity[0]:
                intensity = 0
            elif self.distance < self.shade_intensity[1]:
                intensity = 0.1
            elif self.distance < self.shade_intensity[2]:
                intensity = 0.2
            elif self.distance < self.shade_intensity[3]:
                intensity = 0.3
            elif self.distance < self.shade_intensity[4]:
                intensity = 0.4
            elif self.distance < self.shade_intensity[5]:
                intensity = 0.5
            elif self.distance < self.shade_intensity[6]:
                intensity = 0.6
            elif self.distance < self.shade_intensity[7]:
                intensity = 0.7
            elif self.distance < self.shade_intensity[8]:
                intensity = 0.8
            elif self.distance < self.shade_intensity[9]:
                intensity = 0.9
            else:
                intensity = 1
            
            self.shade_slice = pygame.Surface(self.tempslice.get_size()).convert_alpha()
            self.shade_slice.fill((SETTINGS.shade_rgba[0]*intensity, SETTINGS.shade_rgba[1]*intensity,
                                   SETTINGS.shade_rgba[2]*intensity, SETTINGS.shade_rgba[3]*intensity))
        

class Raycast:
    '''== Raycasting class ==\ncanvas -> Game canvas'''
    def __init__(self, canvas, canvas2):
        self.res = SETTINGS.resolution
        self.fov = SETTINGS.fov
        self.render = SETTINGS.render
        self.tile_size = SETTINGS.tile_size
        self.door_size = self.tile_size / 2
        self.wall_width = int(SETTINGS.canvas_target_width / self.res)
        self.canvas = canvas
        self.canvas2 = canvas2

        self.current_vtile = None
        self.current_htile = None
        

    def calculate(self):
        self.res = SETTINGS.resolution
        self.fov = SETTINGS.fov
        angle = SETTINGS.player_angle
        
        step = self.fov / self.res
        fov = int(self.fov/2)
        ray = -fov
        ray_number = 0

        for tile in SETTINGS.all_solid_tiles:
            tile.distance = tile.get_dist(SETTINGS.player_rect.center)

        while ray < fov:
            degree = angle - ray
            if degree <= 0:
                degree += 360
            elif degree > 360:
                degree -= 360

            self.beta = abs(degree - angle)
             
            self.cast(SETTINGS.player_rect, degree, ray_number)

            ray_number += 1
            ray += step


    def find_offset(self, position, ray_number, angle, tile, hv):
        #position is H_x or V_y
        if hv == 'v':
            if tile.type == 'vdoor':
                offset = abs(int(position - tile.rect.y)) - tile.open
            else:
                offset = abs(int(position - tile.rect.y))

        else:
            if tile.type == 'hdoor':
                offset = abs(int(position - tile.rect.x)) - tile.open
            else:
                offset = abs(int(position - tile.rect.x))

        #Fuck it. Catch all the crashes.
        if offset >= SETTINGS.tile_size:
            offset = SETTINGS.tile_size - 1
        return(offset)

    def check_hit(self, V_hit, H_hit, H_distance, V_distance, full_check):
        #Break loop if any ray has hit a wall            
        if H_hit and V_hit:
            return True

        elif full_check:
            if H_hit:
                if H_distance < V_distance:
                    return True

            elif V_hit:
                if V_distance < H_distance:
                    return True
            

    def cast(self, player_rect, angle, ray_number):
        H_hit = False
        V_hit = False
        H_offset = V_offset = 0
        end_pos = (0, 0)
        angle -= 0.001

        #Horizontal
        if angle < 180:
            H_y = int(player_rect.center[1] / self.tile_size) * self.tile_size
        else:
            H_y = int(player_rect.center[1] / self.tile_size) * self.tile_size + self.tile_size

        H_x = player_rect.center[0] + (player_rect.center[1] - H_y) / math.tan(math.radians(angle))

        #Vertical
        if angle > 270 or angle < 90:
            V_x = int(player_rect.center[0] / self.tile_size) * self.tile_size + self.tile_size
        else:
            V_x = int(player_rect.center[0] / self.tile_size) * self.tile_size

        V_y = player_rect.center[1] + (player_rect.center[0] - V_x) * math.tan(math.radians(angle))

        #Extend
        for x in range(0, SETTINGS.render):
            
            H_distance = abs((player_rect.center[0] - H_x) / math.cos(math.radians(angle)))
            V_distance = abs((player_rect.center[0] - V_x) / math.cos(math.radians(angle)))

            if self.check_hit(V_hit, H_hit, H_distance, V_distance, True):
                break
                
            for tile in SETTINGS.rendered_tiles:
                
                if self.check_hit(V_hit, H_hit, H_distance, V_distance, False):
                    break
                
                if not H_hit:
                    if (H_y == tile.rect.bottom and H_x >= tile.rect.bottomleft[0] and H_x <= tile.rect.bottomright[0]) and player_rect.centery > tile.rect.bottom:
                        H_hit = True
                        H_texture = SETTINGS.tile_texture[tile.ID]
                        self.current_htile = tile
                        if tile.type == 'hdoor':
                            H_y -= self.door_size
                            H_x += self.door_size / math.tan(math.radians(angle))
                            H_offset = offset = self.find_offset(H_x, ray_number, angle, tile, 'h')
                            if H_offset < 0:
                                H_hit = False
                                H_y += self.door_size
                                H_x -= self.door_size / math.tan(math.radians(angle))
                        else:
                            H_offset = offset = self.find_offset(H_x, ray_number, angle, tile, 'h')
                            
                    elif (H_y == tile.rect.top and H_x >= tile.rect.topleft[0] and H_x <= tile.rect.topright[0]) and player_rect.centery < tile.rect.top:
                        H_hit = True
                        H_texture = SETTINGS.tile_texture[tile.ID]
                        self.current_htile = tile
                        if tile.type == 'hdoor':
                            H_y += self.door_size
                            H_x -= self.door_size / math.tan(math.radians(angle))
                            H_offset = offset = self.find_offset(H_x, ray_number, angle, tile, 'h')
                            if H_offset < 0:
                                H_hit = False
                                H_y -= self.door_size
                                H_x += self.door_size / math.tan(math.radians(angle))
                        else:
                            H_offset = self.find_offset(H_x, ray_number, angle, tile, 'h')
                                
                if self.check_hit(V_hit, H_hit, H_distance, V_distance, False):
                    break      
                        
                if not V_hit:
                    if (V_x == tile.rect.left and V_y >= tile.rect.topleft[1] and V_y <= tile.rect.bottomleft[1]) and player_rect.centerx < tile.rect.left:
                        V_hit = True
                        V_texture = SETTINGS.tile_texture[tile.ID]
                        self.current_vtile = tile
                        if tile.type == 'vdoor':
                            V_x += self.door_size
                            V_y -= self.door_size * math.tan(math.radians(angle))
                            V_offset = self.find_offset(V_y, ray_number, angle, tile, 'v')
                            if V_offset < 0:
                               V_hit = False
                               V_x -= self.door_size
                               V_y += self.door_size * math.tan(math.radians(angle))
                        else:
                            V_offset = self.find_offset(V_y, ray_number, angle, tile, 'v')
                            
                    elif (V_x == tile.rect.right and V_y >= tile.rect.topright[1] and V_y <= tile.rect.bottomright[1]) and player_rect.centerx > tile.rect.right:
                        V_hit = True
                        V_texture = SETTINGS.tile_texture[tile.ID]
                        self.current_vtile = tile
                        if tile.type == 'vdoor':
                            V_x -= self.door_size
                            V_y += self.door_size * math.tan(math.radians(angle))
                            V_offset = self.find_offset(V_y, ray_number, angle, tile, 'v')
                            if V_offset < 0:
                               V_hit = False
                               V_x += self.door_size
                               V_y -= self.door_size * math.tan(math.radians(angle))
                        else:
                            V_offset = self.find_offset(V_y, ray_number, angle, tile, 'v')
                               
            #Extend actual ray
            if not H_hit:
                if angle < 180:
                    H_y -= self.tile_size
                else:
                    H_y += self.tile_size
                if angle >= 180:
                    H_x -= self.tile_size / math.tan(math.radians(angle))
                else:
                    H_x += self.tile_size / math.tan(math.radians(angle))                

            if not V_hit:
                if angle > 270 or angle < 90: # ->
                    V_x += self.tile_size
                else:
                    V_x -= self.tile_size
                if angle >= 270 or angle < 90: # <-
                    V_y -= self.tile_size * math.tan(math.radians(angle))
                else:
                    V_y += self.tile_size * math.tan(math.radians(angle))


        if V_hit and H_hit:
            H_hit, V_hit = False, False
            if H_distance < V_distance:
                end_pos = (H_x, H_y)
                texture = H_texture
                tile_len = H_distance
                offset = H_offset
                current_tile = self.current_htile
                H_hit = True
            else:
                end_pos = (V_x, V_y)
                texture = V_texture
                tile_len = V_distance
                offset = V_offset
                current_tile = self.current_vtile
                V_hit = True

        elif H_hit and not V_hit:
            end_pos = (H_x, H_y)
            texture = H_texture
            tile_len = H_distance
            offset = H_offset
            current_tile = self.current_htile

        elif V_hit and not H_hit:
            end_pos = (V_x, V_y)
            texture = V_texture
            tile_len = V_distance
            offset = V_offset
            current_tile = self.current_vtile

        else:
            end_pos = (SETTINGS.player_rect[0],SETTINGS.player_rect[1])
            texture = None
            tile_len = None
            offset = 0
            current_tile = None

        if V_hit:
            vh = 'v'
        else:
            vh = 'h'
            
        #Mode
        self.control(end_pos, ray_number, tile_len, player_rect, texture, offset, current_tile, vh)
        

    def control(self, end_pos, ray_number, tile_len, player_rect, texture, offset, current_tile, vh):
        if SETTINGS.mode == 1:
            if tile_len:
                wall_dist = tile_len * math.cos(math.radians(self.beta))
            else:
                wall_dist = None
            self.render_screen(ray_number, wall_dist, texture, int(offset), current_tile, vh, end_pos)
            
        else:
            self.draw_line(player_rect, end_pos)
            
            

    def render_screen(self, ray_number, wall_dist, texture, offset, current_tile, vh, end_pos):
        if wall_dist:
            wall_height = int((self.tile_size / wall_dist) * (360 / math.tan(math.radians(SETTINGS.fov * 0.8))))
            SETTINGS.zbuffer.append(Slice((texture.slices[offset], 0), texture.texture, texture.rect.width, vh))
            SETTINGS.zbuffer[ray_number].distance = wall_dist
            rendered_slice = pygame.transform.scale(SETTINGS.zbuffer[ray_number].slice, (self.wall_width, wall_height))
            SETTINGS.zbuffer[ray_number].update_rect(rendered_slice)
            SETTINGS.zbuffer[ray_number].xpos = ((ray_number) * self.wall_width)

        else:
            SETTINGS.zbuffer.append(None)
            
        #Middle ray info
        if ray_number == int(self.res/2):
            SETTINGS.middle_slice_len = wall_dist
            SETTINGS.middle_slice = current_tile
            SETTINGS.middle_ray_pos = end_pos
            

    def draw_line(self, player_rect, end_pos):
        SETTINGS.raylines.append((player_rect.center, end_pos))


