import pygame
import os
import SETTINGS
import SOUND

class Music:

    def __init__(self):
        self.settings_volume = SETTINGS.volume * 0.8
        self.base_track = pygame.mixer.Sound(os.path.join('sounds', 'music', 'soft_layer.ogg'))
        self.hard_track = pygame.mixer.Sound(os.path.join('sounds', 'music', 'hard_layer.ogg'))

        self.hard_volume = 0
        self.menu_volume = self.settings_volume * 0.8

        pygame.mixer.Sound.set_volume(self.base_track, max(0, (self.settings_volume - self.menu_volume) * SETTINGS.music_volume))
        pygame.mixer.Sound.set_volume(self.hard_track, max(0, (self.hard_volume - self.menu_volume) * SETTINGS.music_volume))

        if SETTINGS.music_volume > 0:
            pygame.mixer.Sound.play(self.base_track, loops=-1)
            pygame.mixer.Sound.play(self.hard_track, loops=-1)

    def control_music(self):
        if SETTINGS.music_volume > 0:
            if [x for x in SETTINGS.npc_list if x.state == 'attacking' and not x.dead] and not SETTINGS.menu_showing or SETTINGS.player_states['dead']:
                if self.hard_volume < self.settings_volume:
                    self.hard_volume += 0.05
                    pygame.mixer.Sound.set_volume(self.hard_track, max(0, (self.hard_volume - self.menu_volume) * SETTINGS.music_volume))
                
            else:
                if self.hard_volume > 0:
                    self.hard_volume -= 0.005
                    pygame.mixer.Sound.set_volume(self.hard_track, max(0, (self.hard_volume - self.menu_volume) * SETTINGS.music_volume))

            if SETTINGS.menu_showing:
                if self.menu_volume < self.settings_volume * 0.2:
                    self.menu_volume += 0.05
                    pygame.mixer.Sound.set_volume(self.base_track, max(0, (self.settings_volume - self.menu_volume) * SETTINGS.music_volume))
                    pygame.mixer.Sound.set_volume(self.hard_track, max(0, (self.hard_volume - self.menu_volume) * SETTINGS.music_volume))
            else:
                if self.menu_volume > 0:
                    self.menu_volume -= 0.05
                    pygame.mixer.Sound.set_volume(self.base_track, max(0, (self.settings_volume - self.menu_volume) * SETTINGS.music_volume))
                    pygame.mixer.Sound.set_volume(self.hard_track, max(0, (self.hard_volume - self.menu_volume) * SETTINGS.music_volume))
                


        
