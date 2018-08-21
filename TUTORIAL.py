import pygame
import TEXT
import SETTINGS

class Controller:

    def __init__(self): 
        self.text = TEXT.Text(0,0, "INTET!", SETTINGS.BLACK, "DUGAFONT.ttf", 26)

        #Strings
        self.welcome = {
            'string' : "WELCOME  TO  DUGA!  PRESS  'E'  TO  OPEN  THE  DOOR",
            'tiles' : [[1,11], [1,10],
                       [2,10], [2,11], [2,12],
                       [3,10], [3,11], [3,12],
                       [4,10], [4,11], [4,12],
                       [5,11]]
            }

        self.items1 = {
            'string' : "PICK  UP  THE  ARMOR  AND  HEALTH  ON  THE  GROUND",
            'tiles' : [[2,6],[3,6],[4,6],
                       [2,7],[3,7],[4,7],]
            }

        self.arrow = {
            'string' : "FOLLOW  THE  GREEN  ARROW  IN  THE  LOWER  CORNER",
            'tiles' : [[2,5],[3,5],[4,5]]
            }

        self.exits = {
            'string' : "PRESS  'E' ON  THE  EXIT  TO  FINISH  THE  FIRST  TUTORIAL",
            'tiles': [[2,1],[3,1],[4,1],
                      [2,2],[3,2],[4,2],]
            }

        self.second = {
            'string' : "DUGA  HAS  PRIMARY,  SECONDARY  AND  MELEE  WEPONS",
            'tiles' : [[2,17],[3,16],[3,17],[3,18],
                       [4,16], [4,17]]
            }

        self.weapons = {
            'string' : "PICK  UP  THE  WEAPONS  AND  SWITCH  WITH  '1, 2, 3'",
            'tiles' : [       [2,12], [3,12], [4,12],
                       [1,13],[2,13], [3,13], [4,13],[5,13],
                       [1,14],[2,14], [3,14], [4,14],[5,14]]
            }

        self.ammo = {
            'string' : "EACH  GUN  HAS  A  TYPE  OF  AMMO.  RELOAD  WITH  'R'",
            'tiles' : [[2,7], [3,7], [4,7],
                       [2,8], [3,8], [4,8],
                       [2,9], [3,9], [4,9]]
            }

        self.compare = {
            'string' : "FOR  BETTER  AIM,  RIGHT  CLICK.  GO  STAND  ON  THE  GUN",
            'tiles' : [[2,3],        [4,3],
                       [2,4], [3,4], [4,4],
                       [2,5], [3,5], [4,5]]
            }

        self.gauss = {
            'string' : "OPEN  INVENTORY  WITH  'I'  AND  CLICK  ON  GROUND  SLOT",
            'tiles' : [[3,3]]
            }

        self.combat = {
            'string' : "TIME  FOR  SOME  COMBAT!",
            'tiles' : [[2,14], [3,14],
                       [2,15], [3,15], [4,15],
                       [2,16], [3,16], [4,16],]
            }

        self.items = {
            'string' : "ENEMIES  HAVE  DIFFERENT  BEHAVIOURS.  NOW, GEAR  UP!",
            'tiles' : [[2,10], [3,10], [4,10],
                       [2,11], [3,11], [4,11],
                       [2,12], [3,12], [4,12],]
            }

        self.enemy = {
            'string' : "KILL HIM!!  LEFT  CLICK  TO  SHOOT!",
            'tiles' : [      [2,4], [3,4], [4,4],[5,4],
                       [1,5],[2,5], [3,5], [4,5],[5,5],
                       [1,6],[2,6], [3,6], [4,6],[5,6],
                       [1,7],[2,7], [3,7], [4,7],[5,7],
                       [1,8],[2,8], [3,8], [4,8],[5,8],]
            }

        self.done = {
            'string' : "WELL  DONE!  NOW,  LET'S  PLAY!",
            'tiles' : [[2,1], [3,1], [4,4],
                              [3,2], [4,2],]
            }

    def control(self, canvas):
        if SETTINGS.current_level == 0:
            if SETTINGS.player_map_pos in self.welcome['tiles']:
                self.draw(self.welcome, canvas)
            elif SETTINGS.player_map_pos in self.items1['tiles']:
                self.draw(self.items1, canvas)
            elif SETTINGS.player_map_pos in self.arrow['tiles']:
                self.draw(self.arrow, canvas)
            elif SETTINGS.player_map_pos in self.exits['tiles']:
                self.draw(self.exits, canvas)
                

        elif SETTINGS.current_level == 1:
            if SETTINGS.player_map_pos in self.second['tiles']:
                self.draw(self.second, canvas)
            elif SETTINGS.player_map_pos in self.weapons['tiles']:
                self.draw(self.weapons, canvas)
            elif SETTINGS.player_map_pos in self.ammo['tiles']:
                self.draw(self.ammo, canvas)
            elif SETTINGS.player_map_pos in self.compare['tiles']:
                self.draw(self.compare, canvas)
            elif SETTINGS.player_map_pos in self.gauss['tiles']:
                self.draw(self.gauss, canvas)

        elif SETTINGS.current_level == 2:
            if SETTINGS.player_map_pos in self.combat['tiles']:
                self.draw(self.combat, canvas)
            elif SETTINGS.player_map_pos in self.items['tiles']:
                self.draw(self.items, canvas)
            elif SETTINGS.player_map_pos in self.enemy['tiles']:
                self.draw(self.enemy, canvas)
            elif SETTINGS.player_map_pos in self.done['tiles']:
                self.draw(self.done, canvas)


    def draw(self, string, canvas):
        self.text.update_string(string['string'])
        self.text.update_pos((SETTINGS.canvas_actual_width/2)-(self.text.layout.get_width()/2), 480)
        self.box = pygame.Surface((self.text.layout.get_width()+6, self.text.layout.get_height()+6)).convert_alpha()
        self.box.fill((255,255,255,180))
        canvas.blit(self.box, (self.text.posx-3, self.text.posy-3))
        self.text.draw(canvas)
                
            
