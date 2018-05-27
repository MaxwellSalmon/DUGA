import SETTINGS
import GUNS
import NPC
import ITEMS

from os import *
import pygame
import copy
import random

#When creating guns, remember to create an item for the gun as well. 

def load_guns():
    #AK 47 - 0
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'ak_spritesheet.png'),
         'item': path.join('graphics', 'items', 'akitem.png')
         },{
            'dmg' : 3,
            'spread' : 50,
            'hitchance': 80,
            'firerate': 0.08,
            'range': 10,
            'magsize': 30,
            'rlspeed': 1,
            'zoom': 6,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'AK-47'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_magin2.ogg'))]
                },(38,7)))
    
    #Double Barrel Shotgun - 1
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'shotgun_spritesheet.png'),
         'item': path.join('graphics', 'items', 'shotgun.png')
         },{
            'dmg' : 12,
            'spread' : 200,
            'hitchance': 65,
            'firerate': 0.3,
            'range': 8,
            'magsize': 2,
            'rlspeed': 1.4,
            'zoom': 8,
            'ammotype': 'shell',
            'guntype': 'primary',
            'name': 'DB Shotgun'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'SH_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'SH_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'SH_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'SH_shot4.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'gunempty.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'SH_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'SH_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'SH_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'SH_magin2.ogg'))]
                }, (34,10)))

    #Hand gun - 2
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'pistol_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'gun.png')
         },{
             'dmg' : 2,
             'spread': 40,
             'hitchance': 90,
             'firerate': 0.25,
             'range': 8,
             'magsize': 10,
             'rlspeed': 0.8,
             'zoom': 2,
             'ammotype': 'bullet',
             'guntype': 'secondary',
             'name': 'Pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_shot2.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'gunempty.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'gunreload1.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'gunreload2.ogg'))]
                }, (37,6)))

    #Knife - 3
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'knife_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'knifeitem.png')
         },{
             'dmg' : 2,
             'spread': 40, 
             'hitchance': 100,
             'firerate': 0.3,
             'range': 1.5,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Knife'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'KN_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'KN_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'KN_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'none.ogg'))]
                }, (37,10)))

    #Brass Knuckles - 4
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'brass_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'brassitem.png')
         },{
             'dmg' : 1,
             'spread': 30, 
             'hitchance': 100,
             'firerate': 0.2,
             'range': 1.5,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Brass Knuckles'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'KN_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'KN_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'KN_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'none.ogg'))]
                }, (37,10)))
    
    #Gauss - 5
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'gauss_spritesheet.png'),
         'item': path.join('graphics', 'items', 'gaussitem.png')
         },{
            'dmg' : 6,
            'spread' : 10,
            'hitchance': 85,
            'firerate': 0.5,
            'range': 15,
            'magsize': 8,
            'rlspeed': 1,
            'zoom': 8,
            'ammotype': 'ferromag',
            'guntype': 'primary',
            'name': 'Gauss rifle'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'AK_magin2.ogg'))]
                },(38,7)))

def load_npc_types():
    SETTINGS.npc_types = [
        {
            'pos': [0,0],
            'face': 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(12,15),
            'speed': 40,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'hitscan',
            'atckrate': 1,
            'id': 0,
            'filepath' : ('graphics', 'npc', 'soldat_spritesheet.png'),
            'name' : 'idle soldier',
            'soundpack' : 'soldier',
            },
        
        #Soldier Patrouling
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(12,15),
            'speed': 40,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'hitscan',
            'atckrate': 1,
            'id': 1,
            'filepath' : ('graphics', 'npc', 'soldat_spritesheet.png'),
            'name' : 'patroul soldier',
            'soundpack' : 'soldier',
            },
            
        #Ninja idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.10,
            'dmg': 3,
            'health': 11,
            'speed': 60,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.8,
            'id': 2,
            'filepath' : ('graphics', 'npc', 'ninja_spritesheet.png'),
            'name' : 'idle ninja',
            'soundpack' : 'ninja',
            },

        #Ninja patrouling
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.10,
            'dmg': 3,
            'health': 12,
            'speed': 60,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'melee',
            'atckrate': 0.8,
            'id': 3,
            'filepath' : ('graphics', 'npc', 'ninja_spritesheet.png'),
            'name' : 'patroul ninja',
            'soundpack' : 'ninja',
            },

        #Zombie patroling hostile no dmg
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 3.1415, #lol this is used to randomize dmg.
            'health': 6,
            'speed': 30,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'melee',
            'atckrate': 0.6,
            'id': 4,
            'filepath' : ('graphics', 'npc', 'zombie_spritesheet.png'),
            'name' : 'hostile zombie',
            'soundpack' : 'zombie hostile',
            },

        #Zombie idle shy 
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 0,
            'health': 6,
            'speed': 30,
            'mind': 'shy',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.6,
            'id': 5,
            'filepath' : ('graphics', 'npc', 'zombie_spritesheet.png'),
            'name' : 'shy zombie',
            'soundpack' : 'zombie shy',
            },

        #Boss idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 5,
            'health': 62,
            'speed': 20,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'hitscan',
            'atckrate': 3,
            'id': 6,
            'filepath' : ('graphics', 'npc', 'boss_spritesheet.png'),
            'name' : ' idle boss',
            'soundpack' : 'soldier',
            },
        ]

    load_npc_sounds()

def load_npc_sounds():
    SETTINGS.npc_soundpacks = [
        #Soldier soundpack
        {
            'name' : 'soldier',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'gunshot.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'soldier_spot.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'std_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'std_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'std_hurt3.ogg')), pygame.mixer.Sound(path.join('sounds', 'std_hurt4.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'soldier_die1.ogg')),],
            },
        
        #Ninja Soundpack
        {
            'name' : 'ninja',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'KN_shot1.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'none.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'ninja_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'ninja_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'ninja_hurt3.ogg')), pygame.mixer.Sound(path.join('sounds', 'ninja_hurt4.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'ninja_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'ninja_die2.ogg'))],
            },

        #Zombie shy soundpack
        {
            'name' : 'zombie shy',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'none.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'zombie_spot2.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'zombie_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'zombie_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'zombie_hurt3.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'zombie_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'zombie_die2.ogg'))],
            },

        #Zombie hostile soundpack
        {
            'name' : 'zombie hostile',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'zombie_attack.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'zombie_spot1.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'zombie_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'zombie_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'zombie_hurt3.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'zombie_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'zombie_die2.ogg'))],
            },
        ]


def spawn_npcs():
    for npc in SETTINGS.levels_list[SETTINGS.current_level].npcs:
        stats = copy.deepcopy([x for x in SETTINGS.npc_types if x['id'] == npc[2]][0])
        try:
            sounds = ([x for x in SETTINGS.npc_soundpacks if x['name'] == stats['soundpack']][0])
        except:
            print("Error loading NPC! No soundpack with name ", stats['soundpack'])
        stats['pos'] = npc[0]
        stats['face'] = npc[1]
        SETTINGS.npc_list.append(NPC.Npc(stats, sounds, path.join(*stats['filepath'])))


def load_item_types():
    SETTINGS.item_types = [
            #Health kit
            {
                'filepath' : ('graphics', 'items', 'firstaid.png'),
                'type' : 'health',
                'effect' : 10,
                'id' : 0,
                },
            #Helmet
            {
                'filepath' : ('graphics', 'items', 'helmet.png'),
                'type' : 'armor',
                'effect': 15,
                'id': 1,
                },
            #Bullet
            {
                'filepath' : ('graphics', 'items', 'bullet.png'),
                'type' : 'bullet',
                'effect': 10,
                'id': 2
                },
            #Shell
            {
                'filepath' : ('graphics', 'items', 'shell.png'),
                'type' : 'shell',
                'effect': 6,
                'id': 3
                },
            #Knife
            {
                'filepath' : tuple(SETTINGS.gun_list[3].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[3].guntype,
                'effect': SETTINGS.gun_list[3],
                'id': 4
                },
            #Pistol
            {
                'filepath' : tuple(SETTINGS.gun_list[2].itemtexture.split('\\')),
                'type': SETTINGS.gun_list[2].guntype,
                'effect': SETTINGS.gun_list[2],
                'id': 5
                },
            #AK-47
            {
                'filepath' : tuple(SETTINGS.gun_list[0].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[0].guntype,
                'effect': SETTINGS.gun_list[0],
                'id': 6
                },
            #DB Shotgun
            {
                'filepath' : tuple(SETTINGS.gun_list[1].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[1].guntype,
                'effect': SETTINGS.gun_list[1],
                'id': 7
                },
            #Brass Knuckles
            {
                'filepath' : tuple(SETTINGS.gun_list[4].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[4].guntype,
                'effect': SETTINGS.gun_list[4],
                'id': 8
                },
            #Gauss rifle
            {
                'filepath' : tuple(SETTINGS.gun_list[5].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[5].guntype,
                'effect': SETTINGS.gun_list[5],
                'id': 9,
                },
            #ferromag ammo
            {
                'filepath' : ('graphics', 'items', 'ferromag.png'),
                'type' : 'ferromag',
                'effect': 6,
                'id': 10,
                },
            ]

def spawn_items():
    for item in SETTINGS.levels_list[SETTINGS.current_level].items:
        stats = [x for x in SETTINGS.item_types if x['id'] == item[1]][0] #KAN godt, men hvis det kan kopieres nemt, ville det være godt.
        if stats['type'] not in ('primary', 'secondary', 'melee'):
            stats = copy.deepcopy([x for x in SETTINGS.item_types if x['id'] == item[1]][0])
        
        SETTINGS.all_items.append(ITEMS.Item(item[0], path.join(*stats['filepath']), stats['type'], stats['effect']))






