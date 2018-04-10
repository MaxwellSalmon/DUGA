#This is the MAIN script of DUGA. This is where the main loop is located and this is where all resources are loaded.
#All the classes will be located at the bottom of this script.m 

# Husk at konverte alle teksturer. Dette kan du forsøge dig med og se, om det kører bedre.
import pygame
import math
from os import *
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


pygame.init()
pygame.font.init()
pygame.display.set_mode((1,1))

#Load resources
class Load:

    def load_resources(self):
        ID = 0
        current_texture = 0
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

    def load_new_level(self):
        if SETTINGS.changing_level:
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
            
            SETTINGS.changing_level = False
            SETTINGS.player_states['fade'] = True
            
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

        self.window = pygame.display.set_mode((self.width, int(self.height+(self.height*0.15))))# ,pygame.FULLSCREEN)
        self.canvas = pygame.Surface((self.width, self.height))
        
        pygame.display.set_caption("DUGA")

    def change_mode(self):
        if SETTINGS.mode == 1: #1 - 3D / 0 - 2D
            SETTINGS.mode = 0
            self.__init__(SETTINGS.canvas_map_width, SETTINGS.canvas_map_height)
        else:
            SETTINGS.mode = 1
            self.__init__(self.res_width, SETTINGS.canvas_target_height)
        SETTINGS.switch_mode = False

    def draw(self):
        if SETTINGS.mode == 1:
            self.canvas.fill(SETTINGS.levels_list[SETTINGS.current_level].sky_color)
            self.window.fill(SETTINGS.BLACK)
            pygame.draw.rect(self.canvas, SETTINGS.levels_list[SETTINGS.current_level].ground_color, (0, self.height/2, self.width, self.height/2))
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
        if tile.distance:
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

def update_game():
    if SETTINGS.npc_list:
        for npc in SETTINGS.npc_list:
            if not npc.dead:
                npc.think()

    for item in SETTINGS.all_items:
        item.update()

    if SETTINGS.changing_level and SETTINGS.player_states['black']:
        if SETTINGS.current_level < len(SETTINGS.levels_list)-1:
            SETTINGS.current_level += 1
            gameLoad.load_new_level()
        else:
            thanks.draw(gameCanvas.window)
        


#Main loop
def main_loop():
    game_exit = False
    clock = pygame.time.Clock()

    allfps = []
    
    while not game_exit:
        SETTINGS.zbuffer = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

                b = 0
                for x in allfps:
                    b += x
                print(b/len(allfps))
                
                pygame.quit()
                break
            #    quit()

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
        
        elif SETTINGS.mode == 0:
            gameMap.draw(gameCanvas.window)                
            gamePlayer.draw(gameCanvas.window)

            for x in SETTINGS.raylines:
                pygame.draw.line(gameCanvas.window, SETTINGS.RED, x[0], x[1])
            SETTINGS.raylines = []

            for x in SETTINGS.npc_list:
                if x.rect:
                    pygame.draw.rect(gameCanvas.window, SETTINGS.RED, x.rect)

        update_game()

        #Update Game
        pygame.display.update()
        delta_time = clock.tick(SETTINGS.fps)
        SETTINGS.dt = delta_time / 1000.0
        pygame.display.set_caption(SETTINGS.caption % int(clock.get_fps()))

        allfps.append(clock.get_fps())

#Probably temporary object init
#SETTINGS.current_level = 5 #temporary

gameLoad = Load()
gameLoad.load_resources()
gameLoad.load_entities()

mapGenerator = GENERATION.Generator()
mapGenerator.generate_levels(5,4)

gameLoad.get_canvas_size()

#Setup and classes

thanks = TEXT.Text(150,250,"THANKS  FOR  PLAYING  DUGA  TECH  DEMO", SETTINGS.WHITE, "DUGAFONT.ttf", 24)

#Classes for later use
gameMap = MAP.Map(SETTINGS.levels_list[SETTINGS.current_level].array)
gameCanvas = Canvas(SETTINGS.canvas_map_width, SETTINGS.canvas_map_height)
gamePlayer = PLAYER.Player(SETTINGS.player_pos)
gameRaycast = RAYCAST.Raycast(gameCanvas.canvas, gameCanvas.window)
gameInv = INVENTORY.inventory({'bullet': 150, 'shell':25, 'ferromagnetic' : 50})
gameHUD = HUD.hud(path.join('graphics', 'hud.png'))

#More loading - Level specific
gameLoad.load_new_level()

#Run at last
main_loop()

