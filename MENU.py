import pygame
import pickle
import os
import random
import SETTINGS
import TEXT
import SOUND

SETTINGS.menu_showing = True

class Controller:

    def __init__(self, canvas):
        self.current_menu = 'main'
        self.current_type = 'main'
        self.canvas = canvas

        self.load_settings()
        self.esc_pressed = False
        self.new_pressed = False

        self.mainMenu = MainMenu()
        self.newMenu = NewMenu()
        self.optionsMenu = OptionsMenu(self.current_settings)
        self.creditsMenu = CreditsMenu()
        self.gMainMenu = GMainMenu()

    def load_settings(self):
        #This script does not change the settings themselves, but only the settings.dat
        with open(os.path.join('data', 'settings.dat'), 'rb') as file1:
            settings = pickle.load(file1)

        self.current_settings = settings

    def save_settings(self):
        with open(os.path.join('data', 'settings.dat'), 'wb') as file2:
            pickle.dump(self.optionsMenu.current_settings, file2)

    def control(self):
        if self.current_type == 'main':
            if self.current_menu == 'main':
                self.mainMenu.draw(self.canvas)
                if self.mainMenu.new_button.get_clicked():
                    self.current_menu = 'new'
                elif self.mainMenu.options_button.get_clicked():
                    self.current_menu = 'options'
                elif self.mainMenu.credits_button.get_clicked():
                    self.current_menu = 'credits'
                elif self.mainMenu.quit_button.get_clicked():
                    SETTINGS.quit_game = True
                
            elif self.current_menu == 'new':
                self.newMenu.draw(self.canvas)
                if self.newMenu.back_button.get_clicked():
                    self.current_menu = 'main'
                
                elif self.newMenu.new_button.get_clicked():
                    self.newMenu.reset_inventory()
                    self.newMenu.loading.draw(self.canvas)
                    self.new_pressed = True
                #Check if new levels have been loaded and loading string is showing
                elif self.new_pressed:
                    SETTINGS.playing_new = True
                    self.new_pressed = False
                elif SETTINGS.playing_new:
                    self.current_type = 'game'
                    self.current_menu = 'main'
                    SETTINGS.menu_showing = False
                    SETTINGS.playing_new = False

                    
                elif self.newMenu.custom_button.get_clicked():
                    self.newMenu.reset_inventory()
                    SETTINGS.playing_customs = True
                #Check if custom levels have been loaded
                elif SETTINGS.playing_customs:
                    self.current_type = 'game'
                    self.current_menu = 'main'
                    SETTINGS.menu_showing = False
                    SETTINGS.playing_customs = False
                    

            elif self.current_menu == 'options':
                self.optionsMenu.draw(self.canvas)
                if self.optionsMenu.back_button.get_clicked():
                    self.save_settings()
                    self.current_menu = 'main'

            elif self.current_menu == 'credits':
                self.creditsMenu.draw(self.canvas)
                if self.creditsMenu.back_button.get_clicked():
                    self.current_menu = 'main'

        #Show menu in game 
        elif self.current_type == 'game':
            key = pygame.key.get_pressed()
            if self.current_menu == 'main':
                self.gMainMenu.draw(self.canvas)
                if self.gMainMenu.resume_button.get_clicked() or (self.esc_pressed and not key[pygame.K_ESCAPE]):
                    SETTINGS.menu_showing = False
                    self.esc_pressed = False
                elif self.gMainMenu.exit_button.get_clicked():
                    self.current_type = 'main'

            if key[pygame.K_ESCAPE]:
                self.esc_pressed = True
                

class Menu:

    def __init__(self, title):
        self.title = TEXT.Text(0,0, title, SETTINGS.BLACK, "DUGAFONT.ttf", 120)
        self.title.update_pos((SETTINGS.canvas_actual_width/2)-(self.title.layout.get_width()/2)+8, 20)

        self.background_image = None


class MainMenu(Menu):
    
    def __init__(self):
        Menu.__init__(self, '')
        self.new_button = Button((SETTINGS.canvas_actual_width/2, 200, 200, 60), "NEW GAME")
        self.options_button = Button((SETTINGS.canvas_actual_width/2, 300, 200, 60), "OPTIONS")
        self.credits_button = Button((SETTINGS.canvas_actual_width/2, 400, 200, 60), "CREDITS")
        self.quit_button = Button((SETTINGS.canvas_actual_width/2, 500, 200, 60), "QUIT")

        self.logo = pygame.image.load(os.path.join('graphics', 'logo_cutout.png')).convert_alpha()
        self.logo_rect = self.logo.get_rect()

        self.logo_surface = pygame.Surface(self.logo.get_size()).convert()
        self.logo_surface_rect = self.logo_surface.get_rect()
        self.logo_surface_rect.center = (SETTINGS.canvas_actual_width/2, 90)
        
        #(image, x-position)
        self.stone_tiles = [[pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_wall.png')).convert(), self.logo_surface_rect.left],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_wall_crack.png')).convert(), self.logo_surface_rect.left + 160],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_wall.png')).convert(), self.logo_surface_rect.left + (2*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_wall.png')).convert(), self.logo_surface_rect.left + (3*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_vent.png')).convert(), self.logo_surface_rect.left + (4*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_wall.png')).convert(), self.logo_surface_rect.left + (5*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_vase.png')).convert(), self.logo_surface_rect.left + (6*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_wall.png')).convert(), self.logo_surface_rect.left + (7*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'stone_wall.png')).convert(), self.logo_surface_rect.left + (8*160)]]

        self.baroque_tiles = [[pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'baroque.png')).convert(), self.logo_surface_rect.left],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'baroque.png')).convert(), self.logo_surface_rect.left + 160],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'baroque_lamps.png')).convert(), self.logo_surface_rect.left + (2*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'baroque.png')).convert(), self.logo_surface_rect.left + (3*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'baroque.png')).convert(), self.logo_surface_rect.left + (4*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'baroque_worn.png')).convert(), self.logo_surface_rect.left + (5*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'baroque.png')).convert(), self.logo_surface_rect.left + (6*160)]]
        
        self.wood_tiles = [[pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'wood_wall.png')).convert(), self.logo_surface_rect.left],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'wood_painting.png')).convert(), self.logo_surface_rect.left + 160],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'wood_wall.png')).convert(), self.logo_surface_rect.left + (2*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'wood_wall.png')).convert(), self.logo_surface_rect.left + (3*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'wood_books.png')).convert(), self.logo_surface_rect.left + (4*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'wood_fireplace.png')).convert(), self.logo_surface_rect.left + (5*160)],
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'wood_wall.png')).convert(), self.logo_surface_rect.left + (5*160)]]

        self.tiles = random.choice((self.stone_tiles, self.baroque_tiles, self.wood_tiles))
                    
        
        for i in range(len(self.tiles)):
            self.tiles[i][0] = pygame.transform.scale(self.tiles[i][0], (160,160)) #??

    def draw(self, canvas):
        self.logo_animation(canvas)
        
        self.new_button.draw(canvas)
        self.options_button.draw(canvas)
        self.credits_button.draw(canvas)
        self.quit_button.draw(canvas)

    def logo_animation(self, canvas):
        for tile in self.tiles:
            self.logo_surface.blit(tile[0], (tile[1], self.logo_rect.top))
            tile[1] -= 1

            if tile[1] < self.logo_surface_rect.left - 160:
                tile[1] += (160 * len(self.tiles))
                

        self.logo_surface.blit(self.logo, (0,0))

        canvas.blit(self.logo_surface, self.logo_surface_rect)
        
        

class NewMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 'NEW GAME')
        self.new_button = Button((SETTINGS.canvas_actual_width/2, 200, 200, 60), "NEW GAME")
        self.custom_button = Button((SETTINGS.canvas_actual_width/2, 300, 200, 60), "CUSTOM MAPS")
        self.back_button = Button((SETTINGS.canvas_actual_width/2, 500, 200, 60), "BACK")

        self.loading = TEXT.Text(0,0, "LOADING...", SETTINGS.BLACK, "DUGAFONT.ttf", 74)
        self.loading.update_pos((SETTINGS.canvas_actual_width/2)-(self.loading.layout.get_width()/2)+8, (SETTINGS.canvas_target_height/2)-(self.loading.layout.get_height()/2))

    def draw(self, canvas):
        self.new_button.draw(canvas)
        self.custom_button.draw(canvas)
        self.back_button.draw(canvas)
        self.title.draw(canvas)

    def reset_inventory(self):
        for i in SETTINGS.inventory:
            SETTINGS.inventory[i] = None

        for i in SETTINGS.held_ammo:
            SETTINGS.held_ammo[i] = 0

        for i in SETTINGS.gun_list:
            i.current_mag = 0

        
        SETTINGS.current_gun = None
        SETTINGS.next_gun = None
        SETTINGS.player_health = SETTINGS.og_player_health
        SETTINGS.player_armor = SETTINGS.og_player_armor

        SETTINGS.player_states['dead'] = False
        SETTINGS.player_states['invopen'] = False
        SETTINGS.player_states['heal'] = False
        SETTINGS.player_states['armor'] = False
        SETTINGS.player_states['cspeed'] = 0
        

class OptionsMenu(Menu):
    def __init__(self, settings):
        Menu.__init__(self, 'OPTIONS')

        self.strings = ['LOW', 'MED', 'HIGH']
        self.degrees = ['50', '60', '70']
        self.onoff = ['ON', 'OFF']
        
        self.strings_to_data = {
            #'graphics' : [(resolution, render), (), ()]
            'graphics' : [(100, 10), (140, 12), (175, 14)],
            'fov' : [50, 60, 70],
            'sensitivity' : [0.15, 0.25, 0.35], #Tjek den her
            'volume' : [0.1, 0.5, 1],
            'fullscreen' : [True, False]}

        self.graphics_index = self.strings_to_data['graphics'].index(settings['graphics'])
        self.fov_index = self.strings_to_data['fov'].index(settings['fov'])
        self.sens_index = self.strings_to_data['sensitivity'].index(settings['sensitivity'])
        self.vol_index = self.strings_to_data['volume'].index(settings['volume'])
        self.fs_index = self.strings_to_data['fullscreen'].index(settings['fullscreen'])

        self.update_strings()


    def update_strings(self):
        
        self.graphics_button = Button((SETTINGS.canvas_actual_width/2, 200, 300, 30), "GRAPHICS: %s" % self.strings[self.graphics_index])
        self.fov_button = Button((SETTINGS.canvas_actual_width/2, 250, 300, 30), "FOV: %s" % self.degrees[self.fov_index])
        self.sensitivity_button = Button((SETTINGS.canvas_actual_width/2, 300, 300, 30), "SENSITIVITY: %s" % self.strings[self.sens_index])
        self.volume_button = Button((SETTINGS.canvas_actual_width/2, 350, 300, 30), "VOLUME: %s" % self.strings[self.vol_index])
        self.fullscreen_button = Button((SETTINGS.canvas_actual_width/2, 400, 300, 30), "FULLSCREEN: %s" % self.onoff[self.fs_index])
        self.back_button = Button((SETTINGS.canvas_actual_width/2, 500, 200, 60), "BACK")

        self.restart = TEXT.Text(0,0, 'RESTART GAME TO APPLY CHANGES', SETTINGS.LIGHTGRAY, "DUGAFONT.ttf", 20)
        self.restart.update_pos((SETTINGS.canvas_actual_width/2)-(self.restart.layout.get_width()/2), 580)

        self.current_settings = {
            'graphics' : self.strings_to_data['graphics'][self.graphics_index],
            'fov' : self.strings_to_data['fov'][self.fov_index],
            'sensitivity' : self.strings_to_data['sensitivity'][self.sens_index],
            'volume' : self.strings_to_data['volume'][self.vol_index],
            'fullscreen' : self.strings_to_data['fullscreen'][self.fs_index]}

    def control_options(self):
        if self.graphics_button.get_clicked():
            self.graphics_index += 1
            if self.graphics_index >= len(self.strings):
                self.graphics_index = 0
            self.update_strings()

        elif self.fov_button.get_clicked():
            self.fov_index += 1
            if self.fov_index >= len(self.degrees):
                self.fov_index = 0
            self.update_strings()

        elif self.sensitivity_button.get_clicked():
            self.sens_index += 1
            if self.sens_index >= len(self.strings):
                self.sens_index = 0
            self.update_strings()

        elif self.volume_button.get_clicked():
            self.vol_index += 1
            if self.vol_index >= len(self.strings):
                self.vol_index = 0
            self.update_strings()

        elif self.fullscreen_button.get_clicked():
            self.fs_index += 1
            if self.fs_index >= len(self.onoff):
                self.fs_index = 0
            self.update_strings()
            

    def draw(self, canvas):
        self.graphics_button.draw(canvas)
        self.fov_button.draw(canvas)
        self.sensitivity_button.draw(canvas)
        self.volume_button.draw(canvas)
        self.fullscreen_button.draw(canvas)
        self.back_button.draw(canvas)
        self.title.draw(canvas)
        self.restart.draw(canvas)

        self.control_options()

            
class CreditsMenu(Menu):
    def __init__(self):
        Menu.__init__(self, 'CREDITS')
        self.back_button = Button((SETTINGS.canvas_actual_width/2, 500, 200, 60), "BACK")

        #Created by
        self.createdby = TEXT.Text(0,0, 'CREATED  BY', SETTINGS.LIGHTGRAY, "DUGAFONT.ttf", 24)
        self.createdby.update_pos((SETTINGS.canvas_actual_width/2)-(self.createdby.layout.get_width()/2)+8, 130)

        self.maxwellsalmon = TEXT.Text(0,0, 'MAXWELLSALMON', SETTINGS.DARKGRAY, "DUGAFONT.ttf", 38)
        self.maxwellsalmon.update_pos((SETTINGS.canvas_actual_width/2)-(self.maxwellsalmon.layout.get_width()/2)+8, 160)

        #Music
        self.musicby = TEXT.Text(0,0, 'MUSIC  BY', SETTINGS.LIGHTGRAY, "DUGAFONT.ttf", 20)
        self.musicby.update_pos((SETTINGS.canvas_actual_width/2)-(self.musicby.layout.get_width()/2)+8, 210)
        
        self.eli = TEXT.Text(0,0, 'EIK  SOELBERG', SETTINGS.DARKGRAY, "DUGAFONT.ttf", 30)
        self.eli.update_pos((SETTINGS.canvas_actual_width/2)-(self.eli.layout.get_width()/2)+8, 240)

        #Maps
        self.contributions = TEXT.Text(0,0, 'MAP  CONTRIBUTIONS', SETTINGS.LIGHTGRAY, "DUGAFONT.ttf", 20)
        self.contributions.update_pos((SETTINGS.canvas_actual_width/2)-(self.contributions.layout.get_width()/2)+8, 290)

        self.contributors = TEXT.Text(0,0, 'ANDY BOY,   NONSENSE REPLIES', SETTINGS.DARKGRAY, "DUGAFONT.ttf", 20)
        self.contributors.update_pos((SETTINGS.canvas_actual_width/2)-(self.contributors.layout.get_width()/2)+8, 320)

    def draw(self, canvas):
        self.back_button.draw(canvas)
        self.title.draw(canvas)
        self.createdby.draw(canvas)
        self.musicby.draw(canvas)
        self.eli.draw(canvas)
        self.contributions.draw(canvas)
        self.contributors.draw(canvas)
        self.maxwellsalmon.draw(canvas)

#---------------------------------------- IN-GAME MENUS ----------------------------------------------------------------------------

class GMainMenu(Menu):
    
    def __init__(self):
        Menu.__init__(self, 'DUGA')
        self.resume_button = Button((SETTINGS.canvas_actual_width/2, 200, 200, 60), "RESUME")
        self.exit_button = Button((SETTINGS.canvas_actual_width/2, 500, 200, 60), "EXIT GAME")

        self.background = pygame.Surface((SETTINGS.canvas_actual_width, SETTINGS.canvas_target_height)).convert_alpha()
        self.background.fill((100,100,100,10))
        
    def draw(self, canvas):
        canvas.blit(self.background, (0,0))
        self.resume_button.draw(canvas)
        self.exit_button.draw(canvas)
        self.title.draw(canvas)


class Button:

    def __init__(self, xywh, text):
        #ADD CLICK SOUND
        self.surface = pygame.Surface((xywh[2], xywh[3]))
        self.rect = self.surface.get_rect()
        self.rect.center = (xywh[0], xywh[1])
        self.clicked = False

        self.text = TEXT.Text(0,0, text, SETTINGS.WHITE, "DUGAFONT.ttf", 24)
        self.text.update_pos(xywh[0] - self.text.layout.get_width()/2, xywh[1] - (self.text.layout.get_height() / 2)+2)

        self.filling = SETTINGS.LIGHTGRAY
        self.sound = pygame.mixer.Sound(os.path.join('sounds', 'button.ogg'))
        

    def draw(self, canvas):
        self.surface.fill(self.filling)
        canvas.blit(self.surface, self.rect)
        self.text.draw(canvas)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.filling = SETTINGS.DARKGRAY
        else:
            self.filling = SETTINGS.LIGHTGRAY

    def get_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
            if not pygame.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                SOUND.play_sound(self.sound, 0)
                return True
            else:
                return False
        else:
            return False
