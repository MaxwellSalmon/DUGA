#Settings for DUGA

'''Game settings'''
current_level = 0
fps = 31
caption = "DUGA v09 - %s"
mode = 1
#Below this point are the non-configurable game variables.
current_level_size = None
changing_level = False
dt = 0

'''Level settings'''
#These are non-configurable.
levels_list = []
segments_list = []


'''Canvas settings'''
canvas_target_width = 800    #700
canvas_target_height = 550    #600
#Below this point are the non-configurable canvas variables.
canvas_actual_width = 0
canvas_map_width = None
canvas_map_height = None
window_height = int(canvas_target_height + (canvas_target_height *0.15))
switch_mode = False
axes = (0, 0)
screen_shake = 0


'''Raycasting settings'''
resolution = 140
fov = 60
render = 10
shade = True
shade_rgba = (0,0,0,255)
shade_visibility = 200

#Below this point are the non-configurable raycasting variables.
zbuffer = []
middle_slice_len = None
middle_slice = None
middle_ray_pos = None
raylines = []


'''Tile settings'''
tile_size = 64
#Below this point are the non-configurable tile variables.
all_tiles = []
trigger_tiles = []
all_solid_tiles = []
rendered_tiles = []
walkable_area = []
all_doors = []


'''Player settings'''
#Speed in px/s
player_speed = 256
sensitivity = 0.25
player_angle = 270
player_health = 25
player_armor = 0
godmode = False
#Below this point are the non-configurable player variables.
player_pos = [0,0]
player_map_pos = []
player_rect = None
mouse_btn_active = False
mouse2_btn_active = False
reload_key_active = False
aiming = False
player_states = {
    'dead' : False,
    'hurt' : False,
    'heal' : False,
    'armor' : False,
    'invopen' : False,
    'fade' : False,
    'black' : False,
    'cspeed' : 0,
    }
player = None


'''Texture settings'''
#Wall textures and sprites go here.
texture_darken = 100
texture_list = []

'''Weapon settings'''
#Settings for guns and ammo go here.
unlimited_ammo = False
current_gun = None
#Below this point are non-configurable variables.
next_gun = None
prev_gun = None
gun_list = []

'''NPC settings'''
#NPC information goes here
ignore_player = False
#Below this point are non-configurable variables.
npc_list = []
npc_types = []
npc_soundpacks = []


'''Inventory settings'''
#This is for scripts to access inventory data - Not configurable
held_ammo = {}
max_ammo = {}
inventory = {
    'primary': None,
    'secondary': None,
    'melee': None}
item_types = []

'''Tile configurations'''
#Assign each kind of tile with a texture or sprite
tile_texture = {}
tile_solid = {
    0 : False,
    1 : True,
    2 : True,
    3 : True,
    4 : True,
    5 : True,
    6 : True,
    7 : True,
    8 : False,
    9 : True,
    10 : True,
    11 : True,
    12 : True,
    13 : True,
    }
tile_visible = { #Sprite tiles are not visible
    0 : False,
    1 : True,
    2 : True,
    3 : True,
    4 : True,
    5 : True,
    6 : False,
    7 : False,
    8 : False,
    9 : True,
    10 : True,
    11 : True,
    12 : True,
    13 : False,
    }
texture_type = { #air, wall, trigger, sprite
    0 : 'air',
    1 : 'wall',
    2 : 'wall',
    3 : 'wall',
    4 : 'end',
    5 : 'wall',
    6 : 'sprite',
    7 : 'sprite',
    8 : 'sprite',
    9 : 'vdoor',
    10 : 'hdoor',
    11 : 'wall',
    12 : 'wall',
    13 : 'sprite',
    }

'''Sprite settings'''
all_sprites = []

'''Item settings'''
all_items = []


'''Colours'''
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (140, 50, 20)
DARKGRAY = (50, 50, 50)
DARKRED = (80, 0, 0)
DARKGREEN = (0, 100, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
LIGHTBLUE = (100, 100, 225)
LIGHTGRAY = (150, 150, 150)
LIGHTGREEN = (100, 255, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#Create a new tile / sprite tile:
#1. Create texture and add it to TEXTURES.py in the marked area for tiles.
#2. Give the tile by ID the settings you want in dictionaries above.
#3. Make sure that all tiles has a texture or sprite. Invisible tiles can use null.png
#4. Note that Sprite tiles are not visible. The tile itself is not rendered.
#Note: A tile can be solid, but invisible, but not vice versa

#Create a new sprite (NPC):
#1. Create the texture and add it to TEXTURES.py in the marked area for NPC's
#2. Assign the sprite an ID and make sure the sprite is added to SETTINGS.all_sprites.
#3. Add the sprite (ID) to the texture_type dictionary above. Call it 'sprite'.
#4. Fill out the arguments to make a sprite (pos, path)

#Controls
#Overvej at lave justerbare controls

temp = []
