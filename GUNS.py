#GUN CLASS - See self.stats structure in the bottom of script.

import SETTINGS
import SOUND
import pygame
import random
import math
import os

class Gun:
    '''== Create a weapon ==\nspritesheet -> .png | stats -> explained in GUNS.py\nsounds -> explained in GUNS.py | aim_pos = Sight pos in px'''
    
    #Aim pos is the position of the sight on the individual sprite. Reload_speed is seconds.
    #accuracy is the how much spread the gun has. Hit percent is how big chance there is for an NPC to be hit within the accuracy. 1-100
    def __init__(self, textures, stats, sounds, aim_pos):#  damage, spread, hit_percent, magazine_size, reload_speed, zoom, aim_pos):
        #Configure sprite sheet
        self.spritesheet = pygame.image.load(textures['spritesheet'])
        self.itemtexture = textures['item']
        self.subitemtexture = pygame.transform.scale(pygame.image.load(self.itemtexture).subsurface(0,112,64,16).convert_alpha(), (256, 64))
        self.rect = self.spritesheet.get_rect()
        self.spritesheet = pygame.transform.scale(self.spritesheet, (int(self.rect.width * 6), int(self.rect.height * 6)))
        self.aim =     [self.spritesheet.subsurface(0,0,420,360).convert_alpha(), self.spritesheet.subsurface(0,360,420,360).convert_alpha(), self.spritesheet.subsurface(0  ,720,420,360).convert_alpha()]
        self.hipfire = [self.spritesheet.subsurface(420,0,420,360).convert_alpha(), self.spritesheet.subsurface(420,360,420,360).convert_alpha(), self.spritesheet.subsurface(420,720,420,360).convert_alpha()]
        self.aimdown = [self.spritesheet.subsurface(840,0,420,360).convert_alpha(), self.spritesheet.subsurface(840,360,420,360).convert_alpha(), self.spritesheet.subsurface(840,720,420,360).convert_alpha()]
        self.reload =  [self.spritesheet.subsurface(0,0,420,360).convert_alpha(), self.spritesheet.subsurface(1260,0,420,360).convert_alpha(), self.spritesheet.subsurface(1260,360,420,360).convert_alpha(), self.spritesheet.subsurface(1260,720,420,360).convert_alpha(), self.spritesheet.subsurface(1260,1080,420,360).convert_alpha(), self.spritesheet.subsurface(1260,1440,420,360).convert_alpha()]

        self.sounds = sounds
        self.hit_marker = pygame.mixer.Sound(os.path.join('sounds', 'other', 'hitmarker.ogg'))
        
        #Weapon stats
        self.dmg = stats['dmg']
        self.accuracy = stats['spread']*2
        self.firerate = stats['firerate']
        
        if stats['hitchance'] > 100 or stats['hitchance'] < 0:
            print("###HIT CHANCE ON A GUN IS ABOVE 100 OR BELOW 0!###")
            quit()
        self.hit_percent = stats['hitchance']            
        self.rlspeed = stats['rlspeed']
        self.aim_pos = [SETTINGS.canvas_actual_width/2 - aim_pos[0] * 6, SETTINGS.canvas_target_height/2 - aim_pos[1] * 6]
        self.OG_aim_pos = [SETTINGS.canvas_actual_width/2 - aim_pos[0] * 6, SETTINGS.canvas_target_height/2 - aim_pos[1] * 6]
        self.raw_aim_pos = aim_pos
        self.mag_size = stats['magsize']
        if stats['magsize'] == 3.1415:
            self.mag_size = 2
        self.zoom = stats['zoom']
        self.ammo_type = stats['ammotype']
        self.guntype = stats['guntype']
        self.name = stats['name']
        self.stats = stats
        
        if self.guntype != 'melee':
            self.range = stats['range']*SETTINGS.tile_size
        else:
            self.range = SETTINGS.tile_size * 0.9
        

        self.hit_rect = pygame.Rect((SETTINGS.canvas_actual_width/2)-(self.accuracy/2), 0, self.accuracy, 600)

        #setup
        self.current_img = self.aim[0]
        self.current_mag = 0
        self.timer = 0
        self.firetimer = self.firerate
        
        self.aim_busy = False
        self.aim_is_up = False
        self.shoot_busy = False
        self.reload_busy = False

        self.go_reload_next_my_gun = False
        self.have_shot = False
        self.sintemp = 0
        self.swing = 10 
        self.wobble = 20 

        self.ID = hash(self)

        if self.guntype != 'melee':
            self.shoottime = 0.03
        else:
            self.shoottime = 0.1

    def update_rect(self, accuracy_added):
        self.hit_rect.width = self.hit_rect.width * accuracy_added
        self.hit_rect.centerx = SETTINGS.canvas_actual_width / 2

    def aim_animation(self):
        if self.guntype != 'melee':
            if not self.aim_is_up:
                #Raise the gun
                self.aim_busy = True
                if self.current_img != self.aim[-1] and self.timer >= 0.08:
                    x = self.aim.index(self.current_img)+1
                    self.current_img = self.aim[x]
                    SETTINGS.fov -= self.zoom
                    self.timer = 0
                elif self.current_img == self.aim[-1]:
                    self.aim_busy = False
                    self.aim_is_up = True
                    self.update_rect(0.5)
                    self.hit_percent += 20
                    SETTINGS.aiming = True
                    
            elif self.aim_is_up:
                #Lower the gun
                self.aim_busy = True
                if self.current_img != self.aim[0] and self.timer >= 0.10:
                    x = self.aim.index(self.current_img)-1
                    self.current_img = self.aim[x]
                    SETTINGS.fov += self.zoom
                    self.timer = 0
                elif self.current_img == self.aim[0]:
                    self.aim_busy = False
                    self.aim_is_up = False
                    self.update_rect(2)
                    self.hit_percent -= 20
                    SETTINGS.aiming = False
        else:
            SETTINGS.aiming = False

    def shoot_animation(self):
        if self.current_mag > 0 or self.guntype == 'melee':
            if self.firetimer >= self.firerate:
                #Hitscan gun animation
                if not self.aim_is_up and self.guntype != 'melee':
                    #Hip fire
                    if self.current_img not in self.hipfire:
                        self.current_img = self.hipfire[random.randint(0,1)]
                        self.shoot_busy = True
                        SOUND.play_sound(random.choice(self.sounds['shot']), 0)
                        SETTINGS.screen_shake = self.dmg * 2
                        self.damage()
                        self.timer = 0

                    elif self.hipfire.index(self.current_img) <= 1 and self.timer >= self.shoottime:
                        self.current_img = self.hipfire[-1]
                        self.timer = 0
                    elif self.current_img == self.hipfire[-1] and self.timer >= self.shoottime:
                        self.current_img = self.aim[0]
                        self.shoot_busy = False
                        self.current_mag -= 1
                        SETTINGS.statistics['last shots'] += 1
                        if self.stats['magsize'] == 3.1415:
                            self.current_mag -= 1
                            SETTINGS.statistics['last shots'] += 1
                        self.firetimer = 0

                #Melee weapon animation
                elif self.guntype == 'melee':
                    if self.current_img not in self.hipfire:
                        self.current_img = self.hipfire[0]
                        self.shoot_busy = True
                        SOUND.play_sound(random.choice(self.sounds['shot']), 0)
                        self.damage()
                        self.timer = 0
                        
                    elif self.hipfire.index(self.current_img) < 2 and self.timer >= self.shoottime:
                        self.current_img = self.hipfire[self.hipfire.index(self.current_img)+1]
                        self.timer = 0
                    elif self.current_img == self.hipfire[-1] and self.timer >= self.shoottime:
                        self.current_img = self.aim[0]
                        self.shoot_busy = False
                        self.firetimer = 0
                        
                        
                        
                elif self.aim_is_up:
                    #ADS fire
                    if self.current_img not in self.aimdown:
                        self.current_img = self.aimdown[random.randint(0,1)]
                        self.shoot_busy = True
                        SOUND.play_sound(random.choice(self.sounds['shot']), 0)
                        SETTINGS.screen_shake = self.dmg * 2
                        self.damage()
                        self.timer = 0

                    elif self.aimdown.index(self.current_img) <= 1 and self.timer >= self.shoottime:
                        self.current_img = self.aimdown[-1]
                        self.timer = 0
                    elif self.current_img == self.aimdown[-1] and self.timer >= self.shoottime:
                        self.current_img = self.aim[-1]
                        self.shoot_busy = False
                        self.current_mag -= 1
                        SETTINGS.statistics['last shots'] += 1
                        if self.stats['magsize'] == 3.1415:
                            self.current_mag -= 1
                            SETTINGS.statistics['last shots'] += 1
                        self.firetimer = 0
        else:
            if self.firetimer >= self.firerate:
                SOUND.play_sound(random.choice(self.sounds['click']), 0)
                self.firetimer = 0
                           

    def damage(self):
        if SETTINGS.middle_slice_len:
            target_npcs = [x for x in SETTINGS.npc_list if x.hit_rect.colliderect(self.hit_rect) and x.dist < SETTINGS.middle_slice_len]
        else:
            target_npcs = [x for x in SETTINGS.npc_list if x.hit_rect.colliderect(self.hit_rect)]

        if len(target_npcs) > 3:
            target_npcs = sorted(target_npcs, key=lambda x: x.sprite.theta)[:3]
            
        for npc in target_npcs:
            if npc.dist <= self.range and not npc.dead:
                if npc.dist <= SETTINGS.tile_size*2:
                    cap = 100
                else:
                    cap = (self.hit_percent * 0.96 ** (npc.dist*((100-self.hit_percent)/100)))
                        
                if cap >= random.randint(0,int(npc.dist*(1/self.range))):
                    SOUND.play_sound(self.hit_marker, 0)

                    #Damage less if NPC is far away from center.
                    if self.hit_rect.width < 120 or (npc.hit_rect.centerx > self.hit_rect.left + self.hit_rect.width/3 and npc.hit_rect.centerx < self.hit_rect.right - self.hit_rect.width/3):
                        #Critical hit
            
                        if (npc.state == 'idle' or npc.state == 'patrouling') and not npc.player_in_view:
                            npc.health -= self.dmg * 2
                            SETTINGS.statistics['last ddealt'] += self.dmg*2
                        else:
                            npc.health -= self.dmg
                            SETTINGS.statistics['last ddealt'] += self.dmg
                    else:
                        if (npc.state == 'idle' or npc.state == 'patrouling') and not npc.player_in_view:
                            npc.health -= self.dmg
                            SETTINGS.statistics['last ddealt'] += self.dmg*2
                        else:
                            npc.health -= self.dmg / 2
                            SETTINGS.statistics['last ddealt'] += self.dmg
                    npc.timer = 0
                    npc.hurting = True
                    if npc.health <= 0:
                        npc.knockback = self.dmg * (SETTINGS.tile_size/2)

    def reload_animation(self):
        if SETTINGS.held_ammo[self.ammo_type] > 0 or SETTINGS.unlimited_ammo:
            #Change sprite list to reload.
            if self.current_img not in self.reload:
                self.current_img = self.reload[0]
                SOUND.play_sound(random.choice(self.sounds['magout']), 0)
                
            self.reload_busy = True
            #Make sure the magazine is out of view for some time.
            if (self.current_img == self.reload[3] and self.timer > self.rlspeed) or (self.current_img != self.reload[-1] and self.current_img != self.reload[3] and self.timer >= 0.15):
                x = self.reload.index(self.current_img)+1
                self.current_img = self.reload[x]
                self.timer = 0
            elif self.current_img == self.reload[-1] and self.timer >= 0.15:
                #Done reloading
                self.current_img = self.aim[0]
                self.reload_busy = False
                self.timer = 0
                SOUND.play_sound(random.choice(self.sounds['magin']), 0)
                #Change actual ammo
                if not SETTINGS.unlimited_ammo:
                    taken_ammo = self.mag_size - self.current_mag
                    if SETTINGS.held_ammo[self.ammo_type] >= taken_ammo:
                        self.current_mag = self.mag_size
                        SETTINGS.held_ammo[self.ammo_type] -= taken_ammo
                    elif SETTINGS.held_ammo[self.ammo_type] < taken_ammo:
                        self.current_mag = SETTINGS.held_ammo[self.ammo_type] + self.current_mag
                        SETTINGS.held_ammo[self.ammo_type] = 0
                else:
                    self.current_mag = self.mag_size

    def draw(self, canvas):
        swing = self.swing
        wobble = self.wobble
        
        if not SETTINGS.player_states['dead']:
            self.timer += SETTINGS.dt
            self.firetimer += SETTINGS.dt
            
            #Reload gun if aimed
            if SETTINGS.reload_key_active and self.aim_is_up and (self.current_mag < self.mag_size or SETTINGS.unlimited_ammo):
                self.aim_animation()
                self.go_reload_next_my_gun = True

            #Aim gun
            elif (SETTINGS.mouse2_btn_active or self.aim_busy) and (not self.shoot_busy and not self.reload_busy):
                self.aim_animation()

            #Shoot gun
            elif (SETTINGS.mouse_btn_active or self.shoot_busy) and (not self.aim_busy and not self.reload_busy):
                self.shoot_animation()
                swing *= 2
                wobble /= 2

            #Reload gun
            elif ((SETTINGS.reload_key_active or self.reload_busy) and (not self.aim_busy and not self.shoot_busy)) or self.go_reload_next_my_gun:
                if not self.aim_is_up and self.current_mag < self.mag_size:
                    self.reload_animation()
                self.go_reload_next_my_gun = False
                swing *= 2
                wobble /= 2

            if self.aim_is_up:
                swing *= 20
                wobble /= 20

            #Move gun from side to side when walking
            if SETTINGS.player_states['cspeed'] > 0 and SETTINGS.next_gun == SETTINGS.current_gun:
                self.sintemp += math.pi/14 * (25 * SETTINGS.dt)
                self.aim_pos[0] = math.sin(self.sintemp)*(SETTINGS.canvas_actual_width/swing) + self.OG_aim_pos[0]
                self.aim_pos[1] = math.sin(self.sintemp*2) * wobble + (self.OG_aim_pos[1]+10)
            
            #Return gun to default pos
            elif SETTINGS.player_states['cspeed'] == 0:
                if self.aim_pos[0] > self.OG_aim_pos[0]:
                    self.aim_pos[0] -= int((self.aim_pos[0] - self.OG_aim_pos[0])/2)
                    if int((self.aim_pos[0] - self.OG_aim_pos[0])/2) == 0:
                        self.aim_pos[0] = self.OG_aim_pos[0]
                        
                elif self.aim_pos[0] < self.OG_aim_pos[0]:
                    self.aim_pos[0] += int((self.OG_aim_pos[0] - self.aim_pos[0])/2)
                    if int((self.OG_aim_pos[0] - self.aim_pos[0])/2) == 0:
                        self.aim_pos[0] = self.OG_aim_pos[0]
                    
                if self.sintemp != 0 or self.sintemp!= -math.pi:
                    self.sintemp = random.choice([0, -math.pi])

                if self.aim_pos[1] > self.OG_aim_pos[1] and SETTINGS.next_gun == SETTINGS.current_gun:
                    self.aim_pos[1] -= int((self.aim_pos[1] - self.OG_aim_pos[1])/2)
                    if int((self.aim_pos[1] - self.OG_aim_pos[1])/2) == 0:
                        self.aim_pos[1] = self.OG_aim_pos[1]
                    
            

        #Move gun down when player is dead
        if SETTINGS.player_states['dead'] and self.aim_pos[1] <= SETTINGS.canvas_target_height:
            self.aim_pos[1] += 10 

        if not SETTINGS.current_gun:
            SETTINGS.current_gun = self
            SETTINGS.prev_gun = self

        #Change gun
        elif SETTINGS.next_gun != SETTINGS.current_gun:
            if not self.aim_is_up and not self.reload_busy and not self.shoot_busy:
                if self.aim_pos[1] <= SETTINGS.canvas_target_height:
                    self.aim_pos[1] += 80
                else:
                    SETTINGS.prev_gun = SETTINGS.current_gun
                    SETTINGS.current_gun = SETTINGS.next_gun
            elif self.aim_is_up:
                self.aim_animation()
                
        elif SETTINGS.prev_gun != SETTINGS.current_gun and self.aim_pos[1] != self.OG_aim_pos[1]: #Gennemse
            if self.aim_pos[1] > self.OG_aim_pos[1]:
                self.aim_pos[1] -= 80
                if self.aim_pos[1] < self.OG_aim_pos[1]:
                    self.aim_pos[1] = self.OG_aim_pos[1]
            else:
                SETTINGS.prev_gun = SETTINGS.current_gun

        canvas.blit(self.current_img, self.aim_pos)

    def re_init(self):
        self.aim_pos = [SETTINGS.canvas_actual_width/2 - self.raw_aim_pos[0] * 6, SETTINGS.canvas_target_height/2 - self.raw_aim_pos[1] * 6]
        self.OG_aim_pos = [SETTINGS.canvas_actual_width/2 - self.raw_aim_pos[0] * 6, SETTINGS.canvas_target_height/2 - self.raw_aim_pos[1] * 6]
        self.hit_rect = pygame.Rect((SETTINGS.canvas_actual_width/2)-(self.accuracy/2), 0, self.accuracy, 600)


#Textures:
            #{
            #'spritesheet' : spritesheet file path,
            #'item': item texture file path
            #}
#
#stats
#{
#    'dmg' : int(damage),
#    'spread' : int(spread - lower = better),
#    'hitchance': int(1 to 100),
#    'firerate': seconds between shots,
#    'range': range - higher = better,
#    'magsize': int(magazine size),
#    'rlspeed': reload speed,
#    'zoom': int(FOV zoom),
#    'ammotype': 'bullet' / 'shell' / ???,
#    'guntype': 'primary'/'secondary'/'melee',
#    'name': 'name for the weapon'
#    }

#All sounds are lists of loaded sounds - if you want more sounds for the same thing
#pygame.mixer.Sound(path)
#{
#    'shot' : [shooting],
#    'click' : [mag empty],
#    'magout' : [reloading mag],
#    'magin' : [reloaded mag]
#    }
            

