import pygame
import SETTINGS
import ITEMS
import TEXT
import random

title = TEXT.Text(0,0, "None :-)", SETTINGS.BLACK, "DUGAFONT.ttf", 60)
author = TEXT.Text(0,0, "None :-)", SETTINGS.BLACK, "DUGAFONT.ttf", 40)

hurt_intensity = 128
dead_intensity = 0
heal_intensity = 85
armor_intensity = 85
fade_value = 0
title_timer = 0

int_to_string = {
    0 : 'FIRST',
    1 : 'SECOND',
    2 : 'THIRD',
    3 : 'FOURTH',
    4 : 'FIFTH',
    5 : 'SIXTH',
    6 : 'SEVENTH',
    7 : 'EIGHTH',
    8 : 'NINTH',
    9 : 'TENTH',
    10 : 'ELEVENTH',
    11 : 'TWELVTH',
    12 : 'THIRTEENTH',
    13 : 'FOURTEENTH',
    14 : 'FIFTEENTH',
    15 : 'SIXTEENTH',
    16 : 'SEVENTEENTH',
    17 : 'EIGHTTEENTH',
    18 : 'NINETEENTH',
    19 : 'TWENTIETH',
    }

def render(canvas):
    if SETTINGS.screen_shake > 0:
        screen_shake()
    if SETTINGS.player_states['hurt'] or SETTINGS.player_states['dead']:
        player_hurt(canvas)
    if SETTINGS.player_states['heal']:
        player_heal(canvas)
    if SETTINGS.player_states['armor']:
        player_armor(canvas)
    if SETTINGS.player_states['fade'] or SETTINGS.player_states['black']:
        fade_black(canvas)
    if SETTINGS.player_states['title']:
        show_title(canvas)
        

def screen_shake():
    if SETTINGS.screen_shake > 0:
        SETTINGS.axes = (random.randint(-SETTINGS.screen_shake,SETTINGS.screen_shake), random.randint(-SETTINGS.screen_shake,SETTINGS.screen_shake))
        SETTINGS.screen_shake /= 2
        SETTINGS.screen_shake = int(SETTINGS.screen_shake)
        if SETTINGS.screen_shake == 0:
            SETTINGS.screen_shake = 0
            SETTINGS.axes = (0,0)
    
    
def player_hurt(canvas):
    global hurt_intensity, dead_intensity

    blood = pygame.Surface((SETTINGS.canvas_actual_width, SETTINGS.canvas_target_height)).convert_alpha()

    if SETTINGS.player_states['hurt']:
        blood.fill((255, 0, 0, max(min(hurt_intensity, 255), 0)))
        hurt_intensity = int(hurt_intensity / (2-SETTINGS.dt))
        if hurt_intensity == 0:
            SETTINGS.player_states['hurt'] = False
            hurt_intensity = 128

    elif SETTINGS.player_states['dead']:
        blood.fill((255, 0, 0, dead_intensity))
        if dead_intensity <= 120:
            dead_intensity += 10
    canvas.blit(blood, (0,0))

def player_heal(canvas):
    global heal_intensity
    
    heal = pygame.Surface((SETTINGS.canvas_actual_width, SETTINGS.canvas_target_height)).convert_alpha()

    heal.fill((0, 255, 0, heal_intensity))
    heal_intensity = int(heal_intensity / (2-SETTINGS.dt))
    
    if heal_intensity == 0:
        SETTINGS.player_states['heal'] = False
        heal_intensity = 85
    canvas.blit(heal, (0,0))

def player_armor(canvas):
    global armor_intensity

    armor = pygame.Surface((SETTINGS.canvas_actual_width, SETTINGS.canvas_target_height)).convert_alpha()

    armor.fill((0, 0, 225, armor_intensity))
    armor_intensity = int(armor_intensity / (2-SETTINGS.dt))
    if armor_intensity == 0:
        SETTINGS.player_states['armor'] = False
        armor_intensity = 85
    canvas.blit(armor, (0,0))

def fade_black(canvas):
    global fade_value

    black = pygame.Surface((SETTINGS.canvas_actual_width, SETTINGS.canvas_target_height)).convert_alpha()
    black.fill((0, 0, 0, max(0, min(fade_value, 255))))
    if SETTINGS.player_states['fade'] and not SETTINGS.player_states['black']:
        if fade_value < 400:
            fade_value += 15
        else:
            SETTINGS.player_states['black'] = True
            SETTINGS.player_states['fade'] = False
            
    elif SETTINGS.player_states['fade'] and SETTINGS.player_states['black']:
        if fade_value > 0:
            fade_value -= 20
        elif fade_value <= 0:
            fade_value = 0
            SETTINGS.player_states['black'] = False
            SETTINGS.player_states['fade'] = False
            
    canvas.blit(black, (0,0))

def show_title(canvas):
    global title_timer, title, author, white_titles, white_authors, int_to_string

    if SETTINGS.levels_list == SETTINGS.clevels_list or SETTINGS.levels_list == SETTINGS.tlevels_list:
        title.update_string(SETTINGS.levels_list[SETTINGS.current_level].name)
        title.update_pos((SETTINGS.canvas_actual_width/2)-(title.layout.get_width()/2)+8, 200)

        white_box = pygame.Surface((title.layout.get_width()+5, title.layout.get_height()+5)).convert_alpha()
        white_box.fill((255,255,255,180))

        author.update_string("BY  %s" % SETTINGS.levels_list[SETTINGS.current_level].author)
        author.update_pos((SETTINGS.canvas_actual_width/2)-(author.layout.get_width()/2)+8, 262)

        white_box2 = pygame.Surface((author.layout.get_width()+5, author.layout.get_height()-16)).convert_alpha()
        white_box2.fill((255,255,255,180))

        if title_timer <= 3:
            canvas.blit(white_box2, (author.posx-7, author.posy+3))
            author.draw(canvas)

    elif SETTINGS.levels_list == SETTINGS.glevels_list:
        title.update_pos((SETTINGS.canvas_actual_width/2)-(title.layout.get_width()/2)+8, 200)
        if SETTINGS.current_level in int_to_string:
            title.update_string("%s  LEVEL" % int_to_string[SETTINGS.current_level])
        else:
            title.update_string("%s.  LEVEL" % SETTINGS.current_level + 1)
        white_box = pygame.Surface((title.layout.get_width()+5, title.layout.get_height()+5)).convert_alpha()
        white_box.fill((255,255,255,180))

    if title_timer <= 3:
        canvas.blit(white_box, (title.posx-7, title.posy-8))
        title.draw(canvas)
        title_timer += SETTINGS.dt
    else:
        SETTINGS.player_states['title'] = False
        title_timer = 0
        

    

    
            









    
