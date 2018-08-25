import pygame
import pickle
import os
import copy
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
        self.shut_up = False

        self.load_settings()
        self.esc_pressed = False
        self.new_pressed = False

        self.mainMenu = MainMenu()
        self.newMenu = NewMenu(self.current_settings)
        self.optionsMenu = OptionsMenu(self.current_settings)
        self.creditsMenu = CreditsMenu()
        self.gMainMenu = GMainMenu()
        self.supportSplash = SupportSplash()
        self.scoreMenu = ScoreMenu()

    def load_settings(self):
        #This script does not change the settings themselves, but only the settings.dat
        with open(os.path.join('data', 'settings.dat'), 'rb') as file1:
            settings = pickle.load(file1)

        self.current_settings = settings

        #self.current_settings = {'fov': 60, 'fullscreen': False, 'sensitivity': 0.25, 'graphics': (140, 12), 'volume': 0.5, 'music volume' : 0, 'shut up' : False}

        self.shut_up = self.current_settings['shut up']        
        
    def save_settings(self):
        current_settings = self.optionsMenu.current_settings
        current_settings['shut up'] = self.shut_up
        
        with open(os.path.join('data', 'settings.dat'), 'wb') as file2:
            pickle.dump(current_settings, file2)
            

    def check_mouse(self):
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)

    def control(self):
        self.check_mouse()
        if self.current_type == 'main':
            if self.current_menu == 'main':
                self.mainMenu.draw(self.canvas)
                if self.mainMenu.new_button.get_clicked():
                    self.current_menu = 'new'
                elif self.mainMenu.options_button.get_clicked():
                    self.current_menu = 'options'
                elif self.mainMenu.score_button.get_clicked():
                    self.current_menu = 'score'
                elif self.mainMenu.credits_button.get_clicked():
                    self.current_menu = 'credits'
                elif self.mainMenu.quit_button.get_clicked():
                    SETTINGS.quit_game = True
                #Splash screen
                if SETTINGS.statistics['playtime'] >= 120 and not self.shut_up:
                    self.supportSplash.draw(self.canvas)
                    if self.supportSplash.button.get_clicked():
                        self.shut_up = True
                        self.save_settings()
                
            elif self.current_menu == 'new':
                self.newMenu.draw(self.canvas)
                if self.newMenu.back_button.get_clicked():
                    self.current_menu = 'main'

                #Play generated maps
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
                    SETTINGS.current_level = 0
                    SETTINGS.menu_showing = False
                    SETTINGS.playing_new = False

                #Play custom maps
                elif self.newMenu.custom_button.get_clicked():
                    if SETTINGS.clevels_list:
                        self.newMenu.reset_inventory()
                        SETTINGS.playing_customs = True
                    else:
                        self.newMenu.no_levels_on = True
                #Check if custom levels have been loaded
                elif SETTINGS.playing_customs:
                    self.current_type = 'game'
                    self.current_menu = 'main'
                    SETTINGS.current_level = 0
                    SETTINGS.menu_showing = False
                    SETTINGS.playing_customs = False

                #Play tutorial
                elif self.newMenu.tutorial_button.get_clicked():
                    self.newMenu.reset_inventory()
                    SETTINGS.playing_tutorial = True
                elif SETTINGS.playing_tutorial:
                    self.current_type = 'game'
                    self.current_menu = 'main'
                    SETTINGS.current_level = 0
                    SETTINGS.menu_showing = False
                    SETTINGS.playing_tutorial = False                    

            elif self.current_menu == 'options':
                self.optionsMenu.draw(self.canvas)
                if self.optionsMenu.back_button.get_clicked():
                    self.current_menu = 'main'
                if self.optionsMenu.save:
                    self.save_settings()
                    self.optionsMenu.save = False

            elif self.current_menu == 'score':
                self.scoreMenu.draw(self.canvas)
                if self.scoreMenu.back_button.get_clicked():
                    self.current_menu = 'main'

            elif self.current_menu == 'credits':
                self.creditsMenu.draw(self.canvas, self.shut_up)
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
        self.options_button = Button((SETTINGS.canvas_actual_width/2, 270, 200, 60), "OPTIONS")
        self.score_button = Button((SETTINGS.canvas_actual_width/2, 340, 200, 60), "STATISTICS")
        self.credits_button = Button((SETTINGS.canvas_actual_width/2, 410, 200, 60), "CREDITS")
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
                      [pygame.image.load(os.path.join('graphics', 'tiles', 'walls', 'wood_wall.png')).convert(), self.logo_surface_rect.left + (6*160)]]

        self.tiles = random.choice((self.stone_tiles, self.baroque_tiles, self.wood_tiles))
                    
        
        for i in range(len(self.tiles)):
            self.tiles[i][0] = pygame.transform.scale(self.tiles[i][0], (160,160)) #??

    def draw(self, canvas):
        self.logo_animation(canvas)
        
        self.new_button.draw(canvas)
        self.options_button.draw(canvas)
        self.score_button.draw(canvas)
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

    def __init__(self, settings):
        Menu.__init__(self, 'NEW GAME')
        self.new_button = Button((SETTINGS.canvas_actual_width/2, 200, 200, 60), "NEW GAME")
        self.custom_button = Button((SETTINGS.canvas_actual_width/2, 270, 200, 60), "CUSTOM  MAPS")
        self.tutorial_button = Button((SETTINGS.canvas_actual_width/2, 325, 200, 30), "TUTORIAL")
        self.back_button = Button((SETTINGS.canvas_actual_width/2, 500, 200, 60), "BACK")

        self.loading = TEXT.Text(0,0, "LOADING...", SETTINGS.BLACK, "DUGAFONT.ttf", 74)
        self.loading.update_pos((SETTINGS.canvas_actual_width/2)-(self.loading.layout.get_width()/2)+8, (SETTINGS.canvas_target_height/2)-(self.loading.layout.get_height()/2))

        self.nolevels = TEXT.Text(0,0, "NO  CUSTOM  LEVELS", SETTINGS.RED, "DUGAFONT.ttf", 50)
        self.nolevels.update_pos((SETTINGS.canvas_actual_width/2)-(self.nolevels.layout.get_width()/2)+8, (SETTINGS.canvas_target_height/2)-(self.nolevels.layout.get_height()/2))
        self.timer = 0
        self.no_levels_on = False
        self.settings = settings

    def draw(self, canvas):
        self.new_button.draw(canvas)
        self.custom_button.draw(canvas)
        self.tutorial_button.draw(canvas)
        self.back_button.draw(canvas)
        self.title.draw(canvas)

        if self.no_levels_on:
            self.draw_no_levels(canvas)
        else:
            self.timer = 0

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
        SETTINGS.current_level = 0

        SETTINGS.player_states['dead'] = False
        SETTINGS.player_states['invopen'] = False
        SETTINGS.player_states['heal'] = False
        SETTINGS.player_states['armor'] = False
        SETTINGS.player_states['cspeed'] = 0

        SETTINGS.statistics['last enemies'] = 0
        SETTINGS.statistics['last dtaken'] = 0
        SETTINGS.statistics['last ddealt'] = 0
        SETTINGS.statistics['last shots'] = 0
        SETTINGS.statistics['last levels'] = 0

        SETTINGS.fov = self.settings['fov']
        SETTINGS.player_states['cspeed'] = SETTINGS.player_speed
        SETTINGS.aiming = False
        SETTINGS.player.update_collide_list = True

    def draw_no_levels(self, canvas):
        if self.timer <= 1.2:
            self.nolevels.draw(canvas)
        else:
            self.no_levels_on = False
            
        self.timer += SETTINGS.dt
        

class OptionsMenu(Menu):
    
    def __init__(self, settings):
        Menu.__init__(self, 'OPTIONS')
        self.save = False

        self.strings = ['LOW', 'MED', 'HIGH']
        self.music_strings = ['OFF', 'MED', 'HIGH']
        self.degrees = ['50', '60', '70']
        self.onoff = ['ON', 'OFF']
        
        self.strings_to_data = {
            #'graphics' : [(resolution, render), (), ()]
            'graphics' : [(100, 10), (140, 12), (175, 14)],
            'fov' : [50, 60, 70],
            'sensitivity' : [0.15, 0.25, 0.35], #Tjek den her
            'volume' : [0.1, 0.5, 1],
            'music volume' : [0, 0.5, 1],
            'fullscreen' : [True, False],}

        self.graphics_index = self.strings_to_data['graphics'].index(settings['graphics'])
        self.fov_index = self.strings_to_data['fov'].index(settings['fov'])
        self.sens_index = self.strings_to_data['sensitivity'].index(settings['sensitivity'])
        self.vol_index = self.strings_to_data['volume'].index(settings['volume'])
        self.music_index = self.strings_to_data['music volume'].index(settings['music volume'])
        self.fs_index = self.strings_to_data['fullscreen'].index(settings['fullscreen'])

        self.update_strings()


    def update_strings(self):
        
        self.graphics_button = Button((SETTINGS.canvas_actual_width/2, 150, 300, 30), "GRAPHICS: %s" % self.strings[self.graphics_index])
        self.fov_button = Button((SETTINGS.canvas_actual_width/2, 200, 300, 30), "FOV: %s" % self.degrees[self.fov_index])
        self.sensitivity_button = Button((SETTINGS.canvas_actual_width/2, 250, 300, 30), "SENSITIVITY: %s" % self.strings[self.sens_index])
        self.volume_button = Button((SETTINGS.canvas_actual_width/2, 300, 300, 30), "MASTER  VOLUME: %s" % self.strings[self.vol_index])
        self.music_button = Button((SETTINGS.canvas_actual_width/2, 350, 300, 30), "MUSIC  VOLUME: %s" % self.music_strings[self.music_index])
        self.fullscreen_button = Button((SETTINGS.canvas_actual_width/2, 400, 300, 30), "FULLSCREEN: %s" % self.onoff[self.fs_index])
        self.back_button = Button((SETTINGS.canvas_actual_width/2, 500, 200, 60), "BACK")

        self.restart = TEXT.Text(0,0, 'RESTART GAME TO APPLY CHANGES', SETTINGS.LIGHTGRAY, "DUGAFONT.ttf", 20)
        self.restart.update_pos((SETTINGS.canvas_actual_width/2)-(self.restart.layout.get_width()/2), 580)

        self.current_settings = {
            'graphics' : self.strings_to_data['graphics'][self.graphics_index],
            'fov' : self.strings_to_data['fov'][self.fov_index],
            'sensitivity' : self.strings_to_data['sensitivity'][self.sens_index],
            'volume' : self.strings_to_data['volume'][self.vol_index],
            'music volume' : self.strings_to_data['music volume'][self.music_index],
            'fullscreen' : self.strings_to_data['fullscreen'][self.fs_index],}

        self.save = True

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

        elif self.music_button.get_clicked():
            self.music_index += 1
            if self.music_index >= len(self.music_strings):
                self.music_index = 0
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
        self.music_button.draw(canvas)
        self.fullscreen_button.draw(canvas)
        self.back_button.draw(canvas)
        self.title.draw(canvas)
        self.restart.draw(canvas)

        self.control_options()
        

class ScoreMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 'STATISTICS')

        self.area = pygame.Surface((600, 300))
        self.area_rect = self.area.get_rect()
        self.area_rect.center = (SETTINGS.canvas_actual_width / 2, SETTINGS.canvas_target_height / 2)
        self.area.fill((200,200,200))

        self.middle_area = pygame.Surface((200, 300))
        self.middle_area.fill((180,180,180))

        self.back_button = Button((SETTINGS.canvas_actual_width/2, 500, 200, 60), "BACK")
        self.score_testing = copy.copy(SETTINGS.statistics)

        self.highlights = []
        for i in range(6):
            if i == 0:
                self.highlights.append(pygame.Surface((600, 35)).convert_alpha())
            else:
                self.highlights.append(pygame.Surface((600, 30)).convert_alpha())
            self.highlights[i].fill((0,0,0,20))

        #High scores
        self.best_scores = ['HIGHEST SCORES',
                        'ENEMIES  KILLED : %s' % SETTINGS.statistics['best enemies'],
                        'DAMAGE  DEALT : %s' % SETTINGS.statistics['best ddealt'],
                        'DAMAGE  TAKEN : %s' % SETTINGS.statistics['best dtaken'],
                        'SHOTS  FIRED : %s' % SETTINGS.statistics['best shots'],
                        'LEVEL  STREAK : %s' % SETTINGS.statistics['best levels']]

        self.texts = []
        self.pos = 10

        for i in range(len(self.best_scores)):
            if i == 0:
                self.texts.append(TEXT.Text(0, 0, self.best_scores[i], SETTINGS.DARKGRAY, "DUGAFONT.ttf", 18))
            else:
                self.texts.append(TEXT.Text(0, 0, self.best_scores[i], SETTINGS.WHITE, "DUGAFONT.ttf", 18))
            self.texts[i].update_pos(10, self.pos)
            self.pos += 30

        #Last play scores
        self.last_scores = ['LAST PLAY',
                        'ENEMIES  KILLED : %s' % SETTINGS.statistics['last enemies'],
                        'DAMAGE  DEALT : %s' % SETTINGS.statistics['last ddealt'],
                        'DAMAGE  TAKEN : %s' % SETTINGS.statistics['last dtaken'],
                        'SHOTS  FIRED : %s' % SETTINGS.statistics['last shots'],
                        'LEVEL  STREAK : %s' % SETTINGS.statistics['last levels']]
        self.last_texts = []
        self.pos = 10

        for i in range(len(self.last_scores)):
            if i == 0:
                self.last_texts.append(TEXT.Text(0, 0, self.last_scores[i], SETTINGS.DARKGRAY, "DUGAFONT.ttf", 18))
            else:
                if self.last_scores[i] == self.best_scores[i] and self.last_scores[i].find(' 0') == -1:
                    self.last_texts.append(TEXT.Text(0, 0, self.last_scores[i], (100,100,200), "DUGAFONT.ttf", 18))
                else:
                    self.last_texts.append(TEXT.Text(0, 0, self.last_scores[i], SETTINGS.WHITE, "DUGAFONT.ttf", 18))
            self.last_texts[i].update_pos(210, self.pos)
            self.pos += 30

        #all time statistics
        #format play time
            
        self.all_scores = ['ALL TIME',
                        'ENEMIES  KILLED : %s' % SETTINGS.statistics['all enemies'],
                        'DAMAGE  DEALT : %s' % SETTINGS.statistics['all ddealt'],
                        'DAMAGE  TAKEN : %s' % SETTINGS.statistics['all dtaken'],
                        'SHOTS  FIRED : %s' % SETTINGS.statistics['all shots'],
                        'LEVEL  STREAK : %s' % SETTINGS.statistics['all levels'],
                        'TIME PLAYED : {:02d}h {:02d}m'.format(*divmod(SETTINGS.statistics['playtime'], 60))]
        self.all_texts = []
        self.pos = 10

        for i in range(len(self.all_scores)):
            if i == 0:
                self.all_texts.append(TEXT.Text(0, 0, self.all_scores[i], SETTINGS.DARKGRAY, "DUGAFONT.ttf", 18))
            else:
                self.all_texts.append(TEXT.Text(0, 0, self.all_scores[i], SETTINGS.WHITE, "DUGAFONT.ttf", 18))
            self.all_texts[i].update_pos(410, self.pos)
            self.pos += 30

    def draw(self, canvas):
        if self.score_testing != SETTINGS.statistics:
            self.__init__()
        
        self.title.draw(canvas)
        self.back_button.draw(canvas)
        self.area.fill((200,200,200))
        self.area.blit(self.middle_area, (200,0))

        pos = 0
        for i in self.highlights:
            self.area.blit(i, (0, pos))
            if pos == 0:
                pos = 5
            pos += 60

        for i in self.texts:
            i.draw(self.area)

        for i in self.last_texts:
            i.draw(self.area)

        for i in self.all_texts:
            i.draw(self.area)

        canvas.blit(self.area, self.area_rect)

            
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
        
        self.eli = TEXT.Text(0,0, 'HUD-LUM @ SOUNDCLOUD', SETTINGS.DARKGRAY, "DUGAFONT.ttf", 30)
        self.eli.update_pos((SETTINGS.canvas_actual_width/2)-(self.eli.layout.get_width()/2)+8, 240)

        #Maps
        self.contributions = TEXT.Text(0,0, 'THANKS  TO', SETTINGS.LIGHTGRAY, "DUGAFONT.ttf", 20)
        self.contributions.update_pos((SETTINGS.canvas_actual_width/2)-(self.contributions.layout.get_width()/2)+8, 290)

        self.contributors = TEXT.Text(0,0, 'POELE,  OLE,  ROCKETTHEMINIFIG,  ANDY BOY,  J4CKINS' , SETTINGS.DARKGRAY, "DUGAFONT.ttf", 20)
        self.contributors.update_pos((SETTINGS.canvas_actual_width/2)-(self.contributors.layout.get_width()/2)+8, 320)
        self.contributors2 =  TEXT.Text(0,0, 'THEFATHOBBITS,  STARLITEPONY' , SETTINGS.DARKGRAY, "DUGAFONT.ttf", 20)
        self.contributors2.update_pos((SETTINGS.canvas_actual_width/2)-(self.contributors2.layout.get_width()/2)+8, 345)

        self.specialthanks = TEXT.Text(0,0, 'THANKS  TO  THE  PYGAME  COMMUNITY  FOR  HELP  AND  MOTIVATION', SETTINGS.DARKGRAY, "DUGAFONT.ttf", 15)
        self.specialthanks.update_pos((SETTINGS.canvas_actual_width/2)-(self.specialthanks.layout.get_width()/2)+8, 380)

        self.and_you = TEXT.Text(0,0, 'THANKS  TO  YOU  FOR  PLAYING!' , SETTINGS.GREEN, "DUGAFONT.ttf", 22)
        self.and_you.update_pos((SETTINGS.canvas_actual_width/2)-(self.and_you.layout.get_width()/2)+8, 410)


    def draw(self, canvas, show):
        self.back_button.draw(canvas)
        self.title.draw(canvas)
        self.createdby.draw(canvas)
        self.musicby.draw(canvas)
        self.eli.draw(canvas)
        self.contributions.draw(canvas)
        self.contributors.draw(canvas)
        self.contributors2.draw(canvas)
        self.specialthanks.draw(canvas)
        self.maxwellsalmon.draw(canvas)

        if show or SETTINGS.statistics['playtime'] >= 120:
            self.and_you.draw(canvas)
        

class SupportSplash:

    def __init__(self):
        self.area = pygame.Surface((200, 300)).convert()
        self.rect = self.area.get_rect()
        self.rect.topleft = SETTINGS.canvas_actual_width - 220, SETTINGS.canvas_target_height - 280
        self.area.fill((200,200,200))

        self.title = TEXT.Text(0,0, 'THANKS   FOR   PLAYING', SETTINGS.DARKGRAY, "DUGAFONT.ttf", 19)
        self.title.update_pos((self.rect.width/2) - (self.title.layout.get_width()/2)+2, 5)

        self.pleas = ['You  have  been  playing  DUGA', 'for  over  two  hours  now.  I', 'really  hope  you  enjoy  it.',
                      'If  you  do,  please  consider', 'buying  it.  If  you  have  al-', 'ready  bought  it,  thank  you', 'very  much!  If  you  don\'t  think',
                      'it  is  worth  money,  please  let', 'me  know  what  to  improve.', 'Well,  I\'m  happy  to  have  you',
                      'playing,  so  I  added  you  to',  'the  credits!']
        self.texts = []

        self.pos = 30

        self.button = Button((SETTINGS.canvas_actual_width - 120, SETTINGS.canvas_target_height - 15, 192, 40), "LEAVE ME ALONE!")

        for i in range(len(self.pleas)):
            self.texts.append(TEXT.Text(0, 0, self.pleas[i], SETTINGS.WHITE, "DUGAFONT.ttf", 15))
            self.texts[i].update_pos((self.rect.width/2) - (self.texts[i].layout.get_width()/2)+2, self.pos)
            self.pos += 17
        

    def draw(self, canvas):
        self.title.draw(self.area)

        for text in self.texts:
            text.draw(self.area)        

        canvas.blit(self.area, self.rect)

        self.button.draw(canvas)



        
        

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
        self.sound = pygame.mixer.Sound(os.path.join('sounds', 'other', 'button.ogg'))
        

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
