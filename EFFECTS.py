import pygame
import SETTINGS
import ITEMS
import random

hurt_intensity = 128
dead_intensity = 0
heal_intensity = 85
armor_intensity = 85
fade_value = 0

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
        blood.fill((255, 0, 0, hurt_intensity))
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
            









    
