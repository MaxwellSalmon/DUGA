#This is the MAIN script of DUGA. This is where the main loop is located and this is where all resources are loaded.
#All the classes will be located at the bottom of this script.

import pygame
import math
import os
import pickle
import logging
import sys
#-- Engine imports--
import SETTINGS
import PLAYER
import TEXTURES
import MAP
import RAYCAST
import SPRITES
import NPC
import LEVELS
import GUNS
import PATHFINDING
import TEXT
#-- Game imports --
import EFFECTS
import HUD
import ITEMS
import INVENTORY
import ENTITIES
import SEGMENTS
import GENERATION
import MENU
import MUSIC
import TUTORIAL

pygame.init()
pygame.font.init()
pygame.display.set_mode((1,1))

#Load resources
class Load:

    def load_resources(self):
        ID = 0
        current_texture = 0
        self.timer = 0
        for texture in TEXTURES.all_textures:
            if SETTINGS.texture_type[ID] == 'sprite':
                SETTINGS.texture_list.append(pygame.image.load(texture))
            else:
                SETTINGS.texture_list.append(Texture(texture, ID))
            ID += 1
        #Update the dictionary in SETTINGS
        for texture in SETTINGS.texture_list:
            SETTINGS.tile_texture.update({current_texture : texture})
            current_texture += 1

        #Mixer goes under here as well
        pygame.mixer.init()

        #Load custom settings
        with open(os.path.join('data', 'settings.dat'), 'rb') as settings_file:
            settings = pickle.load(settings_file)
            
        SETTINGS.fov = settings['fov']
        SETTINGS.sensitivity = settings['sensitivity']
        SETTINGS.volume = settings['volume']
        SETTINGS.music_volume = settings['music volume']
        SETTINGS.resolution = settings['graphics'][0]
        SETTINGS.render = settings['graphics'][1]
        SETTINGS.fullscreen = settings['fullscreen']

        #Load statistics
        with open(os.path.join('data', 'statistics.dat'), 'rb') as stats_file:
            stats = pickle.load(stats_file)

        SETTINGS.statistics = stats

    def get_canvas_size(self):
        SETTINGS.canvas_map_width = len(SETTINGS.levels_list[SETTINGS.current_level].array[0])*SETTINGS.tile_size
        SETTINGS.canvas_map_height = len(SETTINGS.levels_list[SETTINGS.current_level].array)*SETTINGS.tile_size
        SETTINGS.canvas_actual_width = int(SETTINGS.canvas_target_width / SETTINGS.resolution) * SETTINGS.resolution
        SETTINGS.player_map_pos = SETTINGS.levels_list[SETTINGS.current_level].player_pos
        SETTINGS.player_pos[0] = int((SETTINGS.levels_list[SETTINGS.current_level].player_pos[0] * SETTINGS.tile_size) + SETTINGS.tile_size/2)
        SETTINGS.player_pos[1] = int((SETTINGS.levels_list[SETTINGS.current_level].player_pos[1] * SETTINGS.tile_size) + SETTINGS.tile_size/2)
        if len(SETTINGS.gun_list) != 0:
            for gun in SETTINGS.gun_list:
                gun.re_init()

    def load_entities(self):
        ENTITIES.load_guns()
        ENTITIES.load_npc_types()
        ENTITIES.load_item_types()

    def load_custom_levels(self):
        if not os.stat(os.path.join('data', 'customLevels.dat')).st_size == 0:
            with open(os.path.join('data', 'customLevels.dat'), 'rb') as file:
                custom_levels = pickle.load(file)
                
            for level in custom_levels:
                SETTINGS.clevels_list.append(LEVELS.Level(level))

        with open(os.path.join('data', 'tutorialLevels.dat'), 'rb') as file:
            tutorial_levels = pickle.load(file)

        for level in tutorial_levels:
            SETTINGS.tlevels_list.append(LEVELS.Level(level))

    def load_new_level(self):    
        #Remove old level info
        SETTINGS.npc_list = []
        SETTINGS.all_items = []
        SETTINGS.walkable_area = []
        SETTINGS.all_tiles = []
        SETTINGS.all_doors = []
        SETTINGS.all_solid_tiles = []
        SETTINGS.all_sprites = []
        
        #Retrieve new level info
        self.get_canvas_size()
        gameMap.__init__(SETTINGS.levels_list[SETTINGS.current_level].array)
        SETTINGS.player_rect.center = (SETTINGS.levels_list[SETTINGS.current_level].player_pos[0]*SETTINGS.tile_size, SETTINGS.levels_list[SETTINGS.current_level].player_pos[1]*SETTINGS.tile_size)
        SETTINGS.player_rect.centerx += SETTINGS.tile_size/2
        SETTINGS.player_rect.centery += SETTINGS.tile_size/2
        gamePlayer.real_x = SETTINGS.player_rect.centerx
        gamePlayer.real_y = SETTINGS.player_rect.centery

        if SETTINGS.shade and SETTINGS.levels_list[SETTINGS.current_level].shade:
            SETTINGS.shade_rgba = SETTINGS.levels_list[SETTINGS.current_level].shade_rgba
            SETTINGS.shade_visibility = SETTINGS.levels_list[SETTINGS.current_level].shade_visibility

        if SETTINGS.current_level > 0:
            SETTINGS.changing_level = False
            SETTINGS.player_states['fade'] = True
        else:
            SETTINGS.player_states['fade'] = True
            SETTINGS.player_states['black'] = True

        SETTINGS.player_states['title'] = True
                
        SETTINGS.walkable_area = list(PATHFINDING.pathfind(SETTINGS.player_map_pos, SETTINGS.all_tiles[-1].map_pos))
        gameMap.move_inaccessible_entities()
        ENTITIES.spawn_npcs()
        ENTITIES.spawn_items()

#Texturing
class Texture:
    
    def __init__(self, file_path, ID):
        self.slices = []
        self.texture = pygame.image.load(file_path).convert()
        self.rect = self.texture.get_rect()
        self.ID = ID

        self.create_slices()

    def create_slices(self): # Fills list - Nothing else
        row = 0
        for row in range(self.rect.width):
            self.slices.append(row)
            row += 1


#Canvas
class Canvas:
    '''== Create game canvas ==\nwidth -> px\nheight -> px'''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.res_width = 0
        if SETTINGS.mode == 1:
            self.width = int(SETTINGS.canvas_target_width / SETTINGS.resolution) * SETTINGS.resolution
            self.height = SETTINGS.canvas_target_height
            self.res_width = SETTINGS.canvas_actual_width

        if SETTINGS.fullscreen:
            self.window = pygame.display.set_mode((self.width, int(self.height+(self.height*0.15))) ,pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.width, int(self.height+(self.height*0.15))))
        self.canvas = pygame.Surface((self.width, self.height))
        
        pygame.display.set_caption("DUGA")

        self.shade = [pygame.Surface((self.width, self.height)).convert_alpha(),
                      pygame.Surface((self.width, self.height/1.2)).convert_alpha(),
                      pygame.Surface((self.width, self.height/2)).convert_alpha(),
                      pygame.Surface((self.width, self.height/4)).convert_alpha(),
                      pygame.Surface((self.width, self.height/8)).convert_alpha(),
                      pygame.Surface((self.width, self.height/18)).convert_alpha()]
        self.rgba = [SETTINGS.shade_rgba[0], SETTINGS.shade_rgba[1], SETTINGS.shade_rgba[2], int(min(255, SETTINGS.shade_rgba[3]*(50/SETTINGS.shade_visibility)))]

    def change_mode(self):
        if SETTINGS.mode == 1: #1 - 3D / 0 - 2D
            SETTINGS.mode = 0
            self.__init__(SETTINGS.canvas_actual_width, SETTINGS.canvas_target_height)
        else:
            SETTINGS.mode = 1
            self.__init__(self.res_width, SETTINGS.canvas_target_height)
        SETTINGS.switch_mode = False

    def draw(self):
        if SETTINGS.mode == 1:
            self.canvas.fill(SETTINGS.levels_list[SETTINGS.current_level].sky_color)
            self.window.fill(SETTINGS.BLACK)
            pygame.draw.rect(self.canvas, SETTINGS.levels_list[SETTINGS.current_level].ground_color, (0, self.height/2, self.width, self.height/2))

            if SETTINGS.shade:
                for i in range(len(self.shade)):
                    if i != 5:
                        self.shade[i].fill((self.rgba[0], self.rgba[1], self.rgba[2], self.rgba[3]))
                    else:
                        self.shade[i].fill((self.rgba[0], self.rgba[1], self.rgba[2], SETTINGS.shade_rgba[3]))
                    self.canvas.blit(self.shade[i], (0, self.height/2 - self.shade[i].get_height()/2))

        else:
            self.window.fill(SETTINGS.WHITE)

def sort_distance(x):
    if x == None:
        return 0
    else:
        return x.distance

def sort_atan(x):
    if SETTINGS.middle_ray_pos:
        pos = SETTINGS.middle_ray_pos
    else:
        pos = SETTINGS.player_rect.center
        
    #find the position on each tile that is closest to middle_ray_pos
    xpos = max(x.rect.left, min(pos[0], x.rect.right)) - SETTINGS.player_rect.centerx
    ypos = SETTINGS.player_rect.centery - max(x.rect.top, min(pos[1], x.rect.bottom))
    theta = math.atan2(ypos, xpos)
    theta = math.degrees(theta)
    theta -= SETTINGS.player_angle

    if theta < 0:
        theta += 360
    if theta > 180:
        theta -= 360

    if x.type == 'end':
        SETTINGS.end_angle = theta

    theta = abs(theta)
    
    return(theta)

def render_screen(canvas):
    '''render_screen(canvas) -> Renders everything but NPC\'s'''
    SETTINGS.rendered_tiles = []

    #Get sprite positions
    for sprite in SETTINGS.all_sprites:
        sprite.get_pos(canvas)

    #Sort zbuffer and solid tiles
    SETTINGS.zbuffer = sorted(SETTINGS.zbuffer, key=sort_distance, reverse=True)
    SETTINGS.all_solid_tiles = sorted(SETTINGS.all_solid_tiles, key=lambda x: (x.type, sort_atan(x), x.distance))

    #Calculate which tiles are visible
    for tile in SETTINGS.all_solid_tiles:
        if tile.distance and SETTINGS.tile_visible[tile.ID]:
            if sort_atan(tile) <= SETTINGS.fov:
                if tile.distance < SETTINGS.render * SETTINGS.tile_size:
                    SETTINGS.rendered_tiles.append(tile)
                            
            elif tile.distance <= SETTINGS.tile_size * 1.5:
                SETTINGS.rendered_tiles.append(tile)
                

    #Render all items in zbuffer
    for item in SETTINGS.zbuffer:
        if item == None:
            pass
        elif item.type == 'slice':
            canvas.blit(item.tempslice, (item.xpos, item.rect.y))
            if item.vh == 'v':
                #Make vertical walls slightly darker
                canvas.blit(item.darkslice, (item.xpos, item.rect.y))
            if SETTINGS.shade:
                canvas.blit(item.shade_slice, (item.xpos, item.rect.y))
                
        else:
            if item.new_rect.right > 0 and item.new_rect.x < SETTINGS.canvas_actual_width and item.distance < (SETTINGS.render * SETTINGS.tile_size):
                item.draw(canvas)
                
    #Draw weapon if it is there
    if SETTINGS.current_gun:
        SETTINGS.current_gun.draw(gameCanvas.canvas)
    elif SETTINGS.next_gun:
        SETTINGS.next_gun.draw(gameCanvas.canvas)

    #Draw Inventory and effects
    if SETTINGS.player_states['invopen']:
        gameInv.draw(gameCanvas.canvas)
    EFFECTS.render(gameCanvas.canvas)

    SETTINGS.zbuffer = []

    #Draw HUD and canvas
    gameCanvas.window.blit(canvas, (SETTINGS.axes))
    gameHUD.render(gameCanvas.window)

    #Draw tutorial strings
    if SETTINGS.levels_list == SETTINGS.tlevels_list:
            tutorialController.control(gameCanvas.window)

def update_game():
    if SETTINGS.npc_list:
        for npc in SETTINGS.npc_list:
            if not npc.dead:
                npc.think()

    SETTINGS.ground_weapon = None
    for item in SETTINGS.all_items:
        item.update()

    if (SETTINGS.changing_level and SETTINGS.player_states['black']) or SETTINGS.player_states['dead']:
        if SETTINGS.current_level < len(SETTINGS.levels_list)-1 and SETTINGS.changing_level:
            SETTINGS.current_level += 1
            SETTINGS.statistics['last levels']
            gameLoad.load_new_level()
        
        elif (SETTINGS.current_level == len(SETTINGS.levels_list)-1 or SETTINGS.player_states['dead']) and gameLoad.timer < 4 and not SETTINGS.player_states['fade']:
            if not SETTINGS.player_states['dead'] and SETTINGS.current_level == len(SETTINGS.levels_list)-1 and text.string != 'YOU  WON':
                text.update_string('YOU  WON')
            elif SETTINGS.player_states['dead'] and text.string != 'GAME  OVER':
                text.update_string('GAME  OVER')
            text.draw(gameCanvas.window)
            if not SETTINGS.game_won:
                gameLoad.timer = 0
            SETTINGS.game_won = True
            gameLoad.timer += SETTINGS.dt
            
        #Reset for future playthroughs
        elif SETTINGS.game_won and gameLoad.timer >= 4:
            gameLoad.timer = 0
            SETTINGS.game_won = False
            menuController.current_type = 'main'
            menuController.current_menu = 'score'
            calculate_statistics()
            SETTINGS.menu_showing = True
            SETTINGS.current_level = 0

def calculate_statistics():
    #Update 'all' stats
    SETTINGS.statistics['all enemies'] += SETTINGS.statistics['last enemies']
    SETTINGS.statistics['all ddealt'] += SETTINGS.statistics['last ddealt']
    SETTINGS.statistics['all dtaken'] += SETTINGS.statistics['last dtaken']
    SETTINGS.statistics['all shots'] += SETTINGS.statistics['last shots']
    SETTINGS.statistics['all levels'] += SETTINGS.statistics['last levels']

    #Update 'best' stats
    if SETTINGS.statistics['best enemies'] < SETTINGS.statistics['last enemies']:
        SETTINGS.statistics['best enemies'] = SETTINGS.statistics['last enemies']
    if SETTINGS.statistics['best ddealt'] < SETTINGS.statistics['last ddealt']:
        SETTINGS.statistics['best ddealt'] = SETTINGS.statistics['last ddealt']
    if SETTINGS.statistics['best dtaken'] < SETTINGS.statistics['last dtaken']:
        SETTINGS.statistics['best dtaken'] = SETTINGS.statistics['last dtaken']
    if SETTINGS.statistics['best shots'] < SETTINGS.statistics['last shots']:
        SETTINGS.statistics['best shots'] = SETTINGS.statistics['last shots']
    if SETTINGS.statistics['best levels'] < SETTINGS.statistics['last levels']:
        SETTINGS.statistics['best levels'] = SETTINGS.statistics['last levels']
    #'last' statistics will be cleared when starting new game in menu.
    with open(os.path.join('data', 'statistics.dat'), 'wb') as saved_stats:
        pickle.dump(SETTINGS.statistics, saved_stats)
    


#Main loop
def main_loop():
    game_exit = False
    clock = pygame.time.Clock()
    logging.basicConfig(filename = os.path.join('data', 'CrashReport.log'), level=logging.WARNING)

#    allfps = []
    
    while not game_exit:
        SETTINGS.zbuffer = []
        if SETTINGS.play_seconds >= 60:
            SETTINGS.statistics['playtime'] += 1
            SETTINGS.play_seconds = 0
        else:
            SETTINGS.play_seconds += SETTINGS.dt
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT or SETTINGS.quit_game:
                game_exit = True

##                b = 0
##                for x in allfps:
##                    b += x
##                print(b/len(allfps))
                menuController.save_settings()
                calculate_statistics()
                pygame.quit()
                sys.exit(0)

        try:
            #Music
            musicController.control_music()
            
            if SETTINGS.menu_showing and menuController.current_type == 'main':
                gameCanvas.window.fill(SETTINGS.WHITE)
                menuController.control()

                #Load custom maps
                if SETTINGS.playing_customs:
                    SETTINGS.levels_list = SETTINGS.clevels_list
                    gameLoad.get_canvas_size()
                    gameLoad.load_new_level()

                #Load generated maps
                elif SETTINGS.playing_new:
                    mapGenerator.__init__()
                    mapGenerator.generate_levels(SETTINGS.glevels_amount, SETTINGS.glevels_size)
                    SETTINGS.levels_list = SETTINGS.glevels_list
                    gameLoad.get_canvas_size()
                    gameLoad.load_new_level()

                #Or.. If they are playing the tutorial
                elif SETTINGS.playing_tutorial:
                    SETTINGS.levels_list = SETTINGS.tlevels_list
                    gameLoad.get_canvas_size()
                    gameLoad.load_new_level()

            elif SETTINGS.menu_showing and menuController.current_type == 'game':
                menuController.control()
                
            else:
                #Update logic
                gamePlayer.control(gameCanvas.canvas)
                
                if SETTINGS.fov >= 100:
                    SETTINGS.fov = 100
                elif SETTINGS.fov <= 10:
                    SETTINGS.fov = 10

                if SETTINGS.switch_mode:
                    gameCanvas.change_mode()

                #Render - Draw
                gameRaycast.calculate()
                gameCanvas.draw()
                
                
                if SETTINGS.mode == 1:
                    render_screen(gameCanvas.canvas)

                    #BETA
                  #  beta.draw(gameCanvas.window)
                
                elif SETTINGS.mode == 0:
                    gameMap.draw(gameCanvas.window)                
                    gamePlayer.draw(gameCanvas.window)

                    for x in SETTINGS.raylines:
                        pygame.draw.line(gameCanvas.window, SETTINGS.RED, (x[0][0]/4, x[0][1]/4), (x[1][0]/4, x[1][1]/4))
                    SETTINGS.raylines = []

                    for i in SETTINGS.npc_list:
                        if i.rect and i.dist <= SETTINGS.render * SETTINGS.tile_size * 1.2:
                            pygame.draw.rect(gameCanvas.window, SETTINGS.RED, (i.rect[0]/4, i.rect[1]/4, i.rect[2]/4, i.rect[3]/4))
                        elif i.rect:
                            pygame.draw.rect(gameCanvas.window, SETTINGS.DARKGREEN, (i.rect[0]/4, i.rect[1]/4, i.rect[2]/4, i.rect[3]/4))

                update_game()

        except Exception as e:
            menuController.save_settings()
            calculate_statistics()
            logging.warning("DUGA has crashed. Please send this report to MaxwellSalmon, so he can fix it.")
            logging.exception("Error message: ")
            pygame.quit()
            sys.exit(0)

        #Update Game
        pygame.display.update()
        delta_time = clock.tick(SETTINGS.fps)
        SETTINGS.dt = delta_time / 1000.0
        SETTINGS.cfps = int(clock.get_fps())
        #pygame.display.set_caption(SETTINGS.caption % SETTINGS.cfps)

       # allfps.append(clock.get_fps())

#Probably temporary object init
#SETTINGS.current_level = 5 #temporary
if __name__ == '__main__':
    gameLoad = Load()
    gameLoad.load_resources()
    gameLoad.load_entities()
    gameLoad.load_custom_levels()

    mapGenerator = GENERATION.Generator()
    mapGenerator.generate_levels(1,2)
    SETTINGS.levels_list = SETTINGS.glevels_list

    gameLoad.get_canvas_size()

    #Setup and classes

    text = TEXT.Text(0,0,"YOU  WON", SETTINGS.WHITE, "DUGAFONT.ttf", 48)
    beta = TEXT.Text(5,5,"DUGA  BETA  BUILD  V. 1.3", SETTINGS.WHITE, "DUGAFONT.ttf", 20)
    text.update_pos(SETTINGS.canvas_actual_width/2 - text.layout.get_width()/2, SETTINGS.canvas_target_height/2 - text.layout.get_height()/2)

    #Classes for later use
    gameMap = MAP.Map(SETTINGS.levels_list[SETTINGS.current_level].array)
    gameCanvas = Canvas(SETTINGS.canvas_map_width, SETTINGS.canvas_map_height)
    gamePlayer = PLAYER.Player(SETTINGS.player_pos)
    gameRaycast = RAYCAST.Raycast(gameCanvas.canvas, gameCanvas.window)
    gameInv = INVENTORY.inventory({'bullet': 150, 'shell':25, 'ferromag' : 50})
    gameHUD = HUD.hud()

    #More loading - Level specific
    gameLoad.load_new_level()

    #Controller classes
    menuController = MENU.Controller(gameCanvas.window)
    musicController = MUSIC.Music()
    tutorialController = TUTORIAL.Controller()

    #Run at last
    main_loop()

