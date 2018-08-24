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
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7)))
    
    #Double Barrel Shotgun - 1
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'shotgun_spritesheet.png'),
         'item': path.join('graphics', 'items', 'shotgun.png')
         },{
            'dmg' : 10,
            'spread' : 200,
            'hitchance': 65,
            'firerate': 0.3,
            'range': 7,
            'magsize': 2,
            'rlspeed': 1.4,
            'zoom': 8,
            'ammotype': 'shell',
            'guntype': 'primary',
            'name': 'DB Shotgun'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot4.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
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
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin2.ogg'))]
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
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
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
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10)))
    
   # Gauss - 5
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
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7)))

    #Shotgun pistol - 6
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'sgp_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'shotpistol.png')
         },{
             'dmg' : 6,
             'spread': 100,
             'hitchance': 60,
             'firerate': 0.2,
             'range': 6,
             'magsize': 1,
             'rlspeed': 0.5,
             'zoom': 1,
             'ammotype': 'shell',
             'guntype': 'secondary',
             'name': 'SG Pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37,6)))
    
    # ------ SPECIAL WEAPONS ----------
    #Fast Brass Knuckles - 7
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'brass_brass_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'brassbrassitem.png')
         },{
             'dmg' : 1,
             'spread': 30, 
             'hitchance': 100,
             'firerate': 0,
             'range': 2,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Light Knuckles'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10)))

    #Bloody Brass Knuckles - 8
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'blood_brass_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'bloodbrassitem.png')
         },{
             'dmg' : 20,
             'spread': 60, 
             'hitchance': 100,
             'firerate': 2,
             'range': 1,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Rampage Knuckles'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10)))
    
    #Sharp Knife - 9
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'shiny_knife_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'shinyknifeitem.png')
         },{
             'dmg' : 3,
             'spread': 40, 
             'hitchance': 100,
             'firerate': 0.3,
             'range': 1.5,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Sharp Knife'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10)))

    #Fast Knife - 10
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'desert_knife_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'desertknifeitem.png')
         },{
             'dmg' : 2,
             'spread': 30, 
             'hitchance': 100,
             'firerate': 0.1,
             'range': 1.8,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Light Knife'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10)))
    
    #Modded Double Barrel Shotgun - 11
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'modded_shotgun_spritesheet.png'),
         'item': path.join('graphics', 'items', 'moddedshotgun.png')
         },{
            'dmg' : 15,
            'spread' : 220,
            'hitchance': 65,
            'firerate': 0.3,
            'range': 6,
            'magsize': 3.1415, #lol bad code.
            'rlspeed': 1.4,
            'zoom': 8,
            'ammotype': 'shell',
            'guntype': 'primary',
            'name': 'Modified Shotgun'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot4.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (34,10)))

    #Impossible Double Barrel Shotgun - 12
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'shotgun_spritesheet.png'),
         'item': path.join('graphics', 'items', 'weirdshotgun.png')
         },{
            'dmg' : 8,
            'spread' : 200,
            'hitchance': 65,
            'firerate': 0.5,
            'range': 8,
            'magsize': 3,
            'rlspeed': 1.4,
            'zoom': 8,
            'ammotype': 'shell',
            'guntype': 'primary',
            'name': 'TB Shotgun'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot4.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (34,10)))

    #AK 74 - 13
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'ak74_spritesheet.png'),
         'item': path.join('graphics', 'items', 'ak74item.png')
         },{
            'dmg' : 4,
            'spread' : 30,
            'hitchance': 80,
            'firerate': 0.08,
            'range': 10,
            'magsize': 30,
            'rlspeed': 1,
            'zoom': 8,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'AK-74'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7)))

    #Extended mag AK - 14
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'akext_spritesheet.png'),
         'item': path.join('graphics', 'items', 'akextitem.png')
         },{
            'dmg' : 3,
            'spread' : 50,
            'hitchance': 80,
            'firerate': 0.08,
            'range': 10,
            'magsize': 40,
            'rlspeed': 1.2,
            'zoom': 6,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'Ext Mag AK-47'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7)))

    #Camo AK-47 - 15
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'camo_ak_spritesheet.png'),
         'item': path.join('graphics', 'items', 'camoakitem.png')
         },{
            'dmg' : 3,
            'spread' : 50,
            'hitchance': 90,
            'firerate': 0.04,
            'range': 10,
            'magsize': 30,
            'rlspeed': 0.8,
            'zoom': 6,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'Camo AK-47'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7)))

    #Light AK-47 - 16
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'ak_spritesheet.png'),
         'item': path.join('graphics', 'items', 'lightakitem.png')
         },{
            'dmg' : 3,
            'spread' : 60,
            'hitchance': 80,
            'firerate': 0.08,
            'range': 10,
            'magsize': 20,
            'rlspeed': 0.1,
            'zoom': 4,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'Light AK-47'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7)))

    #Gauss Hand gun - 17
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'gauss_pistol_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'gaussgun.png')
         },{
             'dmg' : 9,
             'spread': 30,
             'hitchance': 98,
             'firerate': 0.25,
             'range': 12,
             'magsize': 10,
             'rlspeed': 0.8,
             'zoom': 8,
             'ammotype': 'ferromag',
             'guntype': 'secondary',
             'name': 'Anomaly Pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (37,6)))

    #High power Hand gun - 18
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'pistol_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'hpgun.png')
         },{
             'dmg' : 3,
             'spread': 40,
             'hitchance': 85,
             'firerate': 0.25,
             'range': 8,
             'magsize': 10,
             'rlspeed': 0.8,
             'zoom': 2,
             'ammotype': 'bullet',
             'guntype': 'secondary',
             'name': 'HP Pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'hpp_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'hpp_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'hpp_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin2.ogg'))]
                }, (37,6)))

    #Modded Gauss - 19
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'modded_gauss_spritesheet.png'),
         'item': path.join('graphics', 'items', 'moddedgaussitem.png')
         },{
            'dmg' : 9,
            'spread' : 10,
            'hitchance': 85,
            'firerate': 0.5,
            'range': 15,
            'magsize': 12,
            'rlspeed': 1,
            'zoom': 9,
            'ammotype': 'ferromag',
            'guntype': 'primary',
            'name': 'Modded gauss'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7)))

    #bump Gauss - 20
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'bump_gauss_spritesheet.png'),
         'item': path.join('graphics', 'items', 'bumpgaussitem.png')
         },{
            'dmg' : 6,
            'spread' : 20,
            'hitchance': 70,
            'firerate': 0.15,
            'range': 15,
            'magsize': 8,
            'rlspeed': 1,
            'zoom': 7,
            'ammotype': 'ferromag',
            'guntype': 'primary',
            'name': 'Bump gauss'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7)))

    #Black Shotgun pistol - 21
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'black_sgp_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'blackshotpistol.png')
         },{
             'dmg' : 8,
             'spread': 100,
             'hitchance': 60,
             'firerate': 0.2,
             'range': 6,
             'magsize': 1,
             'rlspeed': 0.4,
             'zoom': 1,
             'ammotype': 'shell',
             'guntype': 'secondary',
             'name': 'Modded SGP'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37,6)))

    #TWO Shotgun pistol - 22
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'wtf_sgp_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'wtfshotpistol.png')
         },{
             'dmg' : 12,
             'spread': 150,
             'hitchance': 60,
             'firerate': 0.2,
             'range': 6,
             'magsize': 2,
             'rlspeed': 0.8,
             'zoom': 1,
             'ammotype': 'shell',
             'guntype': 'secondary',
             'name': 'What??'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37,6)))

    #Auto Hand gun - 23
    SETTINGS.gun_list.append(GUNS.Gun(
        {'spritesheet' : path.join('graphics', 'weapon', 'auto_pistol_spritesheet.png'),
         'item' : path.join('graphics', 'items', 'autogun.png')
         },{
             'dmg' : 2,
             'spread': 40,
             'hitchance': 90,
             'firerate': 0.05,
             'range': 8,
             'magsize': 12,
             'rlspeed': 0.9,
             'zoom': 2,
             'ammotype': 'bullet',
             'guntype': 'secondary',
             'name': 'Auto pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin2.ogg'))]
                }, (37,6)))

def load_npc_types():
    SETTINGS.npc_types = [
        #soldier idle
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
            'filepath' : ('graphics', 'npc', 'soldier_spritesheet.png'),
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
            'filepath' : ('graphics', 'npc', 'soldier_spritesheet.png'),
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

        #Zombie patroling hostile (no dmg?)
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 3.1415, #lol this is used to randomize dmg.
            'health': 6,
            'speed': 70,
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
            'speed': 50,
            'mind': 'shy',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.6,
            'id': 5,
            'filepath' : ('graphics', 'npc', 'zombie_spritesheet.png'),
            'name' : 'shy zombie',
            'soundpack' : 'zombie shy',
            },

        #random NPC
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0,
            'dmg': 0,
            'health': 0,
            'speed': 0,
            'mind': None,
            'state': None,
            'atcktype': None,
            'atckrate': 0,
            'id': 6,
            'filepath' : ('graphics', 'npc', 'random_spritesheet.png'),
            'name' : 'random',
            'soundpack' : None,
            },

        #SPECIAL NPCS --------
        #Boss idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.10,
            'dmg': 5,
            'health': 40,
            'speed': 20,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'hitscan',
            'atckrate': 3,
            'id': 7,
            'filepath' : ('graphics', 'npc', 'red_soldier_spritesheet.png'),
            'name' : 'idle red',
            'soundpack' : 'red soldier',
            },
        
        #black soldier idle
        {
            'pos': [0,0],
            'face': 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(15,20),
            'speed': 30,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'hitscan',
            'atckrate': 0.5,
            'id': 8,
            'filepath' : ('graphics', 'npc', 'black_soldier_spritesheet.png'),
            'name' : 'black idle',
            'soundpack' : 'soldier',
            },
        

        #black soldier patroul
        {
            'pos': [0,0],
            'face': 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(15,20),
            'speed': 30,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'hitscan',
            'atckrate': 1.5,
            'id': 9,
            'filepath' : ('graphics', 'npc', 'black_soldier_spritesheet.png'),
            'name' : 'black patroul',
            'soundpack' : 'soldier',
            },

        #green ninja idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 3,
            'health': random.randint(8, 11),
            'speed': 100,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.5,
            'id': 10,
            'filepath' : ('graphics', 'npc', 'green_ninja_spritesheet.png'),
            'name' : 'idle green',
            'soundpack' : 'ninja',
            },

        #green ninja patrouling
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(8, 11),
            'speed': 100,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'melee',
            'atckrate': 0.5,
            'id': 11,
            'filepath' : ('graphics', 'npc', 'green_ninja_spritesheet.png'),
            'name' : 'idle green',
            'soundpack' : 'ninja',
            },

        #blue ninja idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.1,
            'dmg': 4,
            'health': 14,
            'speed': 35,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'melee',
            'atckrate': 1.1,
            'id': 12,
            'filepath' : ('graphics', 'npc', 'blue_ninja_spritesheet.png'),
            'name' : 'idle blue',
            'soundpack' : 'ninja',
            },

        #Zombie yellow patrouling
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 5, 
            'health': 20,
            'speed': 20,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'melee',
            'atckrate': 1,
            'id': 13,
            'filepath' : ('graphics', 'npc', 'sick_zombie_spritesheet.png'),
            'name' : 'patroul sick',
            'soundpack' : 'zombie hostile',
            },

        #zombie yellow idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 6,
            'health': 20,
            'speed': 20,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.8,
            'id': 14,
            'filepath' : ('graphics', 'npc', 'sick_zombie_spritesheet.png'),
            'name' : 'idle sick',
            'soundpack' : 'zombie hostile',
            },

        #zombie yellow idle shy
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 10,
            'health': 35,
            'speed': 20,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 1.2,
            'id': 15,
            'filepath' : ('graphics', 'npc', 'sick_zombie_spritesheet.png'),
            'name' : 'shy sick',
            'soundpack' : 'zombie hostile',
            },

        #blurry zombie hostile
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 8,
            'health': 5,
            'speed': 45,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'melee',
            'atckrate': 0.4,
            'id': 16,
            'filepath' : ('graphics', 'npc', 'blurry_zombie_spritesheet.png'),
            'name' : 'hostile blurry',
            'soundpack' : 'blurry zombie',
            },

        #blurry zombie hostile hitscan??
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 1,
            'health': 15,
            'speed': 45,
            'mind': 'hostile',
            'state': 'patrouling',
            'atcktype': 'hitscan',
            'atckrate': 0.4,
            'id': 17,
            'filepath' : ('graphics', 'npc', 'blurry_zombie_spritesheet.png'),
            'name' : 'hostile blurry',
            'soundpack' : 'blurry zombie',
            },
        ]

    load_npc_sounds()

def load_npc_sounds():
    SETTINGS.npc_soundpacks = [
        #Soldier soundpack
        {
            'name' : 'soldier',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_shoot.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_spot.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt3.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt4.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_die.ogg')),],
            },
        
        #boss soldier soundpack
        {
            'name' : 'red soldier',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_shoot_heavy.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_spot.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt3.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt4.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_die.ogg')),],
            },
        
        #Ninja Soundpack
        {
            'name' : 'ninja',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_attack.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_hurt3.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_hurt4.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_die2.ogg'))],
            },

        #Zombie shy soundpack
        {
            'name' : 'zombie shy',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_spot2.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt3.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_die2.ogg'))],
            },

        #Zombie hostile soundpack
        {
            'name' : 'zombie hostile',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_attack.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_spot1.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt3.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_die2.ogg'))],
            },

        #Zombie blurry soundpack
        {
            'name' : 'blurry zombie',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_attack.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_spot.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_hurt3.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_die2.ogg'))],
            },
        ]


def spawn_npcs():
    seed = SETTINGS.current_level + SETTINGS.seed
    for npc in SETTINGS.levels_list[SETTINGS.current_level].npcs:
        if [x for x in SETTINGS.npc_types if x['id'] == npc[2]][0]['name'] == 'random':
            random.seed(seed)
            seed += 0.001
            stats = copy.deepcopy(random.choice([x for x in SETTINGS.npc_types if x['name'] != 'random']))
            print(stats['name'])
        else: 
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
            #Health
            {
                'filepath' : ('graphics', 'items', 'firstaid.png'),
                'type' : 'health',
                'effect' : 10,
                'id' : 0,
                },
            #Armor
            {
                'filepath' : ('graphics', 'items', 'kevlar.png'),
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
                'effect': 4,
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
            #Shotgun pistol
            {
                'filepath' : tuple(SETTINGS.gun_list[6].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[6].guntype,
                'effect': SETTINGS.gun_list[6],
                'id': 11,
                },

            #Random any item
            {
                'filepath' : ('graphics', 'items', 'random.png'),
                'type' : 'random',
                'effect': ['health', 'armor', 'bullet', 'shell', 'ferromag',
                           'health', 'armor', 'bullet', 'shell', 'ferromag',
                           'melee', 'secondary', 'primary'],
                'id': 12,
                },


            #Random weapon
            {
                'filepath' : ('graphics', 'items', 'randomgun.png'),
                'type' : 'random',
                'effect': ['melee', 'secondary', 'primary'],
                'id': 13,
                },

            #Random item
            {
                'filepath' : ('graphics', 'items', 'randomitem.png'),
                'type' : 'random',
                'effect': ['health', 'armor', 'bullet', 'shell', 'ferromag'],
                'id': 14,
                },

            #Light Brass Knuckles
            {
                'filepath' : tuple(SETTINGS.gun_list[7].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[7].guntype,
                'effect': SETTINGS.gun_list[7],
                'id': 15
                },

            #Bloody Brass Knuckles
            {
                'filepath' : tuple(SETTINGS.gun_list[8].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[8].guntype,
                'effect': SETTINGS.gun_list[8],
                'id': 16
                },

            #shiny knife
            {
                'filepath' : tuple(SETTINGS.gun_list[9].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[9].guntype,
                'effect': SETTINGS.gun_list[9],
                'id': 17
                },

            #desert knife
            {
                'filepath' : tuple(SETTINGS.gun_list[10].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[10].guntype,
                'effect': SETTINGS.gun_list[10],
                'id': 18
                },

            #modded shotgun
            {
                'filepath' : tuple(SETTINGS.gun_list[11].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[11].guntype,
                'effect': SETTINGS.gun_list[11],
                'id': 19
                },

            #Impossible Shotgun
            {
                'filepath' : tuple(SETTINGS.gun_list[12].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[12].guntype,
                'effect': SETTINGS.gun_list[12],
                'id': 20
                },

            #AK 74
            {
                'filepath' : tuple(SETTINGS.gun_list[13].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[13].guntype,
                'effect': SETTINGS.gun_list[13],
                'id': 21
                },

            #AK 47 extended magazine
            {
                'filepath' : tuple(SETTINGS.gun_list[14].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[14].guntype,
                'effect': SETTINGS.gun_list[14],
                'id': 22
                },

            #Camo AK-47
            {
                'filepath' : tuple(SETTINGS.gun_list[15].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[15].guntype,
                'effect': SETTINGS.gun_list[15],
                'id': 23
                },

            #Light AK-47
            {
                'filepath' : tuple(SETTINGS.gun_list[16].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[16].guntype,
                'effect': SETTINGS.gun_list[16],
                'id': 24
                },

            #Gauss pistol
            {
                'filepath' : tuple(SETTINGS.gun_list[17].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[17].guntype,
                'effect': SETTINGS.gun_list[17],
                'id': 25
                },

            #HP Pistol
            {
                'filepath' : tuple(SETTINGS.gun_list[18].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[18].guntype,
                'effect': SETTINGS.gun_list[18],
                'id': 26
                },

            #Modded Gauss
            {
                'filepath' : tuple(SETTINGS.gun_list[19].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[19].guntype,
                'effect': SETTINGS.gun_list[19],
                'id': 27
                },

            #Bump Gauss
            {
                'filepath' : tuple(SETTINGS.gun_list[20].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[20].guntype,
                'effect': SETTINGS.gun_list[20],
                'id': 28
                },

            #Black Shotgun Pistol
            {
                'filepath' : tuple(SETTINGS.gun_list[21].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[21].guntype,
                'effect': SETTINGS.gun_list[21],
                'id': 29
                },

            #wtf shotgun pistol
            {
                'filepath' : tuple(SETTINGS.gun_list[22].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[22].guntype,
                'effect': SETTINGS.gun_list[22],
                'id': 30
                },

            #auto pistol
            {
                'filepath' : tuple(SETTINGS.gun_list[23].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[23].guntype,
                'effect': SETTINGS.gun_list[23],
                'id': 31
                },
            ]

def spawn_items():
    seed = SETTINGS.current_level + SETTINGS.seed
    for item in SETTINGS.levels_list[SETTINGS.current_level].items:
        stats = [x for x in SETTINGS.item_types if x['id'] == item[1]][0]
        if stats['type'] == 'random':
            random.seed(seed)
            possible_items = [x for x in SETTINGS.item_types if x['type'] in stats['effect']]
            stats = random.choice(possible_items)
            seed += 0.001
            
        elif stats['type'] not in ('primary', 'secondary', 'melee'):
            stats = copy.deepcopy([x for x in SETTINGS.item_types if x['id'] == item[1]][0])
        
        SETTINGS.all_items.append(ITEMS.Item(item[0], path.join(*stats['filepath']), stats['type'], stats['effect']))






