#This is the map editor. It does not have anything to do with the game.
#It needs access to LEVELS.py, TEXTURES.py, ENTITIES.py, TEXT.py and SETTINGS.py

import pygame
import copy
import os
import sys
import pickle
import LEVELS
import ENTITIES
import SETTINGS
import TEXTURES
import TEXT

pygame.init()
pygame.font.init()

current_id = 1
current_item = 0
current_npc = 0
npc_face = 90
doors = []
mode = 'tile'
ltype = None
segtypes = ['normal', 'start', 'end']

def determine_mode():
    ENTITIES.load_guns()
    ENTITIES.load_item_types()
    ENTITIES.load_npc_types()
    
    print("What would you like to do?")
    print("new / load")
    pick = input("> ").lower()
    if pick == "new" or pick == 'n':
        determine_type()
        determine_size()
    elif pick == "load" or pick == 'l':
        loader.load_map()
    else:
        print("Invalid argument.")
        determine_mode()

    editorCanvas.load_items()
    editorCanvas.load_npcs()

def determine_type():
    global ltype
    print("What type of map would you like to create?")
    print("level / segment")
    pick = input("> ").lower()
    if pick == "level" or pick == 'l':
        ltype = "level"
    elif pick == "segment" or pick == 's':
        ltype = "segment"
    else:
        print("Invalid argument!")
        determine_type()
    

def determine_size():
    global ltype
    if ltype == 'level':
        width = input("Map width in tiles: ")
        height = input("Map height in tiles: ")
    else:
        width = 9
        height = 9
    try:
        editorCanvas.__init__(int(width)*32 + 170, int(height)*32 + 170)
        currentMap.__init__(int(width), int(height))
    except Exception as e:
        print("Invalid arguments.")
        print(e)
        determine_size()

def what_now():
    global ltype
    isgood = False
    sc = gc = (SETTINGS.WHITE)
    print()
    while not isgood:
        isgood = True
        if ltype == 'level':
            print("What sky colour should your level have? Leave blank for white.")
            sc = input("R,G,B > ")
            if sc:
                try:
                    sc = sc.replace(' ', '')
                    sc = sc.split(',')
                    for i in range(3):
                        sc[i] = int(sc[i])
                    sc = tuple(sc)
                except:
                    print("Error")
                    isgood = False
                    sc = (0,0,0)
            else:
                sc = (255,255,255)
                    
                
            print()
            print("What ground colour should your level have? Leave blank for white.")
            gc = input("R,G,B > ")
            if gc:
                try:
                    gc = gc.replace(' ', '')
                    gc = gc.split(',')
                    for i in range(3):
                        gc[i] = int(gc[i])
                    gc = tuple(gc)
                except:
                    print("Error")
                    isgood = False
                    gc = (0,0,0)
            else:
                gc = (255,255,255)

            for i in gc+sc:
                if i < 0 or i > 255:
                    isgood = False
                    
            if len(gc+sc) > 6:
                isgood = False

            editorCanvas.dict['ground_color'] = gc
            editorCanvas.dict['sky_color'] = sc
        
        print()
        print("Would you like to save the map?")
        yn = input("Y/N > ").lower()
        if yn == 'y' or yn == 'yes':
            if isgood:
                loader.save_map(gc, sc)
                print()
                print("Map saved!")
        elif yn == 'n' or yn == 'no':
            sys.exit(1)
        else:
            isgood = False

        if not isgood:
            if ltype == 'level':
                print("You made an error somewhere. Let's try again. R,G,B must be three values between 0-255 seperated by commas.")
            else:
                print("You made an error somewhere. Please try again.")
            print()

class Canvas:

    def __init__(self, width, height):
        global mode, ltype, segtypes
        if width > 0 and height > 0:
            self.width = max(width, 438)
            self.height = max(height, 438)
        else:
            self.width = 1
            self.height = 1
        self.canvas = pygame.display.set_mode((self.width, self.height))
        self.segtype = 0
        pygame.display.set_caption("DUGA Map Editor")
        self.stop = False
        self.items = []
        self.showauthor = False
        self.exit = False

        self.tile_textures = []
        for i in range(len(TEXTURES.all_textures)):
            texture = TEXTURES.all_textures[i]
            t = pygame.image.load(texture).convert_alpha()
            t = pygame.transform.scale(t, (64,64))
            if SETTINGS.texture_type[i] == 'vdoor':
                t = pygame.transform.rotate(t, 90)
            self.tile_textures.append(t)

        #Author
        self.authortext = TEXT.Text(self.width - 135, 5, 'Author: %s', SETTINGS.LIGHTGRAY, 'DUGAFONT.ttf', 11)

        #Export
        self.exporttext = TEXT.Text(20, self.height-32, 'EXPORT', SETTINGS.BLACK, 'DUGAFONT.ttf', 14)
        self.exportbtn = pygame.Surface((64,32))
        self.exportrct = self.exportbtn.get_rect()
        self.exportrct.topleft = (15, self.height-40)
        self.exportbtn.fill(SETTINGS.WHITE)

        #Selected mode
        self.selecttext = TEXT.Text(100, self.height-32, mode, SETTINGS.GREEN, 'DUGAFONT.ttf', 24)

        #Tile
        self.nxttext = TEXT.Text(self.width-28, 60, '>', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
        self.nexttile = pygame.Surface((30, 40))
        self.nexttilerct = self.nexttile.get_rect()
        self.nexttilerct.topleft = (self.width-40, 50)
        self.nexttile.fill(SETTINGS.WHITE)
        self.prvtext = TEXT.Text(self.width-135, 60, '<', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
        self.prevtile = pygame.Surface((30, 40))
        self.prevtilerct = self.prevtile.get_rect()
        self.prevtilerct.topleft = (self.width-140, 50)
        self.prevtile.fill(SETTINGS.WHITE)
        self.tiletypetext = TEXT.Text(self.width-95, 15, 'TEXTURE TYPE', SETTINGS.WHITE, 'DUGAFONT.ttf', 20)
        
        self.tilerect = self.tile_textures[current_id].get_rect()
        self.tilerect.topleft = (self.width-107, 40)

        #startpos
        self.startpossurf = pygame.Surface((64,64))
        self.startposrct = self.startpossurf.get_rect()
        self.startposrct.topleft = (self.width-105, 335)
        self.startpossurf.fill(SETTINGS.DARKRED)
        self.startpostxt = TEXT.Text(self.width-95, 345, 'START', SETTINGS.WHITE, 'DUGAFONT.ttf', 15)
        self.startpostxt2 = TEXT.Text(self.width-95, 370, 'POS', SETTINGS.WHITE, 'DUGAFONT.ttf', 15)

        #Segment?
        if ltype == "segment":
            #Doors
            self.doortxt = TEXT.Text(30, self.height-110, 'ENTRANCES', SETTINGS.BLUE, 'DUGAFONT.ttf', 20)
            #up
            self.doorup = pygame.Surface((20,20))
            self.dooruprct = self.doorup.get_rect()
            self.dooruprct.topleft = (30, self.height-80)
            self.doorup.fill(SETTINGS.WHITE)
            self.dooruptxt = TEXT.Text(36, self.height-76, '^', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
            #down
            self.doordown = pygame.Surface((20, 20))
            self.doordownrct = self.doordown.get_rect()
            self.doordownrct.topleft = (55, self.height-80)
            self.doordown.fill(SETTINGS.WHITE)
            self.doordowntxt = TEXT.Text(60, self.height-80, 'v', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
            #left
            self.doorleft = pygame.Surface((20, 20))
            self.doorleftrct = self.doorleft.get_rect()
            self.doorleftrct.topleft = (80, self.height-80)
            self.doorleft.fill(SETTINGS.WHITE)
            self.doorlefttxt = TEXT.Text(85, self.height-80, '<', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
            #right
            self.doorright = pygame.Surface((20, 20))
            self.doorrightrct = self.doorright.get_rect()
            self.doorrightrct.topleft = (105, self.height-80)
            self.doorright.fill(SETTINGS.WHITE)
            self.doorrighttxt = TEXT.Text(110, self.height-80, '>', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)

            #typeleft
            self.segtypeleft = pygame.Surface((20,20))
            self.segtypeleftrct = self.segtypeleft.get_rect()
            self.segtypeleftrct.topleft = (20, self.height-140)
            self.segtypeleft.fill(SETTINGS.WHITE)
            self.segtypelefttxt = TEXT.Text(25, self.height-140, '<', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)

            #segtype
            self.segtypetxt = TEXT.Text(20, self.height-160, 'SEGMENT TYPE', SETTINGS.DARKGREEN, 'DUGAFONT.ttf', 20)
            self.csegtypetxt = TEXT.Text(45, self.height-140, segtypes[self.segtype], SETTINGS.LIGHTGREEN, 'DUGAFONT.ttf', 20)

            #typeright
            self.segtyperight = pygame.Surface((20,20))
            self.segtyperightrct = self.segtypeleft.get_rect()
            self.segtyperightrct.topleft = (130, self.height-140)
            self.segtyperight.fill(SETTINGS.WHITE)
            self.segtyperighttxt = TEXT.Text(135, self.height-140, '>', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)

    def load_items(self):
        print("Loading")
        self.item_names = []
        self.item_ids = []
        for i in SETTINGS.item_types:
            img = pygame.image.load(os.path.join(*i['filepath']))
            img = pygame.transform.scale(img, (64, 64))
            self.items.append(img)
            
            self.item_ids.append(i['id'])
            self.item_names.append(i['type'])
            
        self.nextitemtext = TEXT.Text(self.width-28, 165, '>', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
        self.nextitem = pygame.Surface((30, 40))
        self.nextitemrct = self.nextitem.get_rect()
        self.nextitemrct.topleft = (self.width-40, 150)
        self.nextitem.fill(SETTINGS.WHITE)

        self.previtemtext = TEXT.Text(self.width-135, 165, '<', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
        self.previtem = pygame.Surface((30, 40))
        self.previtemrct = self.previtem.get_rect()
        self.previtemrct.topleft = (self.width-140, 150)
        self.previtem.fill(SETTINGS.WHITE)

        self.itemtypetext = TEXT.Text(self.width-140, 110, 'ITEM TYPE', SETTINGS.WHITE, 'DUGAFONT.ttf', 20)
        self.itemrect = self.items[current_item].get_rect()
        self.itemrect.topleft = (self.width-107, 110)

    def load_npcs(self):
        global current_npc, npc_face
        self.npc_stats = []
        self.npc_textures = []

        for i in SETTINGS.npc_types:
            self.npc_stats.append(i)
            
            img = pygame.image.load(os.path.join(*i['filepath']))
            img2 = img.subsurface(0,0,64,128).convert_alpha()
            img2 = pygame.transform.scale(img2, (64,64))
            self.npc_textures.append(img2)

        self.npcrect = self.npc_textures[current_npc].get_rect()
        self.npcrect.topleft = (self.width-107, 210)
        self.npctypetext = TEXT.Text(self.width-140, 195, self.npc_stats[current_npc]['name'], SETTINGS.WHITE, 'DUGAFONT.ttf', 20)

        self.nextnpctext = TEXT.Text(self.width-28, 235, '>', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
        self.nextnpc = pygame.Surface((30, 40))
        self.nextnpcrct = self.nextnpc.get_rect()
        self.nextnpcrct.topleft = (self.width-40, 230)
        self.nextnpc.fill(SETTINGS.WHITE)

        self.prevnpctext = TEXT.Text(self.width-135, 235, '<', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
        self.prevnpc = pygame.Surface((30, 40))
        self.prevnpcrct = self.prevnpc.get_rect()
        self.prevnpcrct.topleft = (self.width-135, 230)
        self.prevnpc.fill(SETTINGS.WHITE)

        #face
        self.npcfacetext = TEXT.Text(self.width-100, 290, str(npc_face), SETTINGS.WHITE, 'DUGAFONT.ttf', 24)

        self.npcfrect = pygame.Rect(self.width-100, 280, 64, 64)
        
        self.nextnpcftext = TEXT.Text(self.width-28, 295, '>', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
        self.nextnpcf = pygame.Surface((30, 40))
        self.nextnpcfrct = self.nextnpcf.get_rect()
        self.nextnpcfrct.topleft = (self.width-40, 280)
        self.nextnpcf.fill(SETTINGS.WHITE)

        self.prevnpcftext = TEXT.Text(self.width-135, 295, '<', SETTINGS.BLACK, 'DUGAFONT.ttf', 20)
        self.prevnpcf = pygame.Surface((30, 40))
        self.prevnpcfrct = self.prevnpcf.get_rect()
        self.prevnpcfrct.topleft = (self.width-135, 280)
        self.prevnpcf.fill(SETTINGS.WHITE)
            
          
    def draw(self):
        global current_id, current_item, mode, current_npc
        self.canvas.fill(SETTINGS.BLACK)

        #Author
        if self.showauthor:
            self.authortext.draw(self.canvas)

        #Export
        self.canvas.blit(self.exportbtn, self.exportrct)
        self.exporttext.draw(self.canvas)

        #Mode
        self.selecttext.update_string("PLACING: " + mode)
        self.selecttext.draw(self.canvas)

        #Tile
        self.canvas.blit(self.nexttile, self.nexttilerct)
        self.nxttext.draw(self.canvas)
        self.canvas.blit(self.prevtile, self.prevtilerct)
        self.prvtext.draw(self.canvas)
        self.tiletypetext.draw(self.canvas)
        self.canvas.blit(self.tile_textures[current_id], self.tilerect)

        #Item
        self.canvas.blit(self.items[current_item], self.itemrect)
        self.canvas.blit(self.nextitem, self.nextitemrct)
        self.nextitemtext.draw(self.canvas)
        self.canvas.blit(self.previtem, self.previtemrct)
        self.previtemtext.draw(self.canvas)
        self.itemtypetext.draw(self.canvas)
        currentMap.add_item(self.items[current_item], self.item_ids[current_item])

        #NPC
        self.canvas.blit(self.npc_textures[current_npc], self.npcrect)
        self.canvas.blit(self.nextnpc, self.nextnpcrct)
        self.nextnpctext.draw(self.canvas)
        self.canvas.blit(self.prevnpc, self.prevnpcrct)
        self.prevnpctext.draw(self.canvas)
        self.npctypetext.draw(self.canvas)

        #Npc face
        self.npcfacetext.draw(self.canvas)
        self.canvas.blit(self.nextnpcf, self.nextnpcfrct)
        self.nextnpcftext.draw(self.canvas)
        self.canvas.blit(self.prevnpcf, self.prevnpcfrct)
        self.prevnpcftext.draw(self.canvas)
        currentMap.add_npc(self.npc_textures[current_npc], current_npc)

        #Doors
        if ltype == "segment":
            self.doortxt.draw(self.canvas)
            self.canvas.blit(self.doorup, self.dooruprct)
            self.dooruptxt.draw(self.canvas)
            self.canvas.blit(self.doordown, self.doordownrct)
            self.doordowntxt.draw(self.canvas)
            self.canvas.blit(self.doorleft, self.doorleftrct)
            self.doorlefttxt.draw(self.canvas)
            self.canvas.blit(self.doorright, self.doorrightrct)
            self.doorrighttxt.draw(self.canvas)

            #seg types
            self.canvas.blit(self.segtypeleft, self.segtypeleftrct)
            self.segtypelefttxt.draw(self.canvas)
            self.segtypetxt.draw(self.canvas)
            self.canvas.blit(self.segtyperight, self.segtyperightrct)
            self.segtyperighttxt.draw(self.canvas)
            self.csegtypetxt.draw(self.canvas)

        #startpos
        if (ltype =='segment' and segtypes[self.segtype] == 'start') or ltype == 'level':
            self.canvas.blit(self.startpossurf, self.startposrct)
            self.startpostxt.draw(self.canvas)
            self.startpostxt2.draw(self.canvas)

    def export(self, gc, sc, printit):
        global ltype, doors, segtypes
        if ltype == 'level':
            self.dict = {
                'lvl_number' : None,
                'sky_color' : sc,
                'ground_color' : gc,
                'npcs' : [],
                'items' : [],
                'player_pos' : None,
                'array' : None,
                'name' : None,
                'shade' : (False, (0,0,0,0), 0)}
        else:
            self.dict = {
                'id' : None,
                'npcs' : [],
                'items' : [],
                'array' : None,
                'doors' : doors,
                'type' : str(segtypes[self.segtype]),
                'name' : None,
                'shade' : (False, (0,0,0,0), 0)}
                
        if not printit or (self.exportrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop):
            for tile in currentMap.tiles:
                if tile.item:
                    self.dict['items'].append((tile.map_pos, tile.item_id))
                if tile.npc:
                    self.dict['npcs'].append((tile.map_pos, tile.npc_face, tile.npc_id))
                if tile.player_pos:
                    self.dict['player_pos'] = tile.player_pos
                    
            self.dict['array'] = currentMap.array

            if printit:
                self.exit = True
                
            self.stop = True
        elif not pygame.mouse.get_pressed()[0]:
            self.stop = False    

    def change_id(self):
        global current_id, mode
        if self.nexttilerct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if current_id < len(TEXTURES.all_textures)-1:
                current_id += 1
                self.stop = True
                mode = 'tile'

        elif self.prevtilerct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if current_id > 1:
                current_id -= 1
                self.stop = True
                mode = 'tile'

        elif self.tilerect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            mode = 'tile'

        elif self.startposrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            mode = 'start pos'

        elif not pygame.mouse.get_pressed()[0]:
            self.stop = False

        self.tiletypetext.update_string(SETTINGS.texture_type[current_id])

    def change_item(self):
        global current_item, mode
        if self.nextitemrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if current_item < len(SETTINGS.item_types)-1:
                current_item += 1
                self.stop = True
                mode = 'item'

        elif self.previtemrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if current_item > 0:
                current_item -= 1
                self.stop = True
                mode = 'item'

        elif self.itemrect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            mode = 'item'

        elif not pygame.mouse.get_pressed()[0]:
            self.stop = False

        self.itemtypetext.update_string(self.item_names[current_item])

    def change_npc(self):
        global current_npc, mode
        if self.nextnpcrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if current_npc < len(self.npc_stats)-1:
                current_npc += 1
                self.stop = True
                mode = 'npc'

        elif self.prevnpcrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if current_npc > 0:
                current_npc -= 1
                self.stop = True
                mode = 'npc'

        elif self.npcrect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            mode = 'npc'

        elif not pygame.mouse.get_pressed()[0]:
            self.stop = False

        self.npctypetext.update_string(self.npc_stats[current_npc]['name'])

    def change_face(self):
        global npc_face, mode
        if self.nextnpcfrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if npc_face < 270:
                npc_face += 90
                self.stop = True
                mode = 'npc'

        elif self.prevnpcfrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if npc_face > 0:
                npc_face -= 90
                self.stop = True
                mode = 'npc'

        elif self.npcfrect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            mode = 'npc'

        elif not pygame.mouse.get_pressed()[0]:
            self.stop = False

        self.npcfacetext.update_string(str(npc_face))

    def click_doors(self):
        global doors
        #up
        if self.dooruprct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if 90 not in doors:
                doors.append(90)
                self.doorup.fill(SETTINGS.RED)
            else:
                doors.remove(90)
                self.doorup.fill(SETTINGS.WHITE)
            self.stop = True

        elif self.doordownrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if 270 not in doors:
                doors.append(270)
                self.doordown.fill(SETTINGS.RED)
            else:
                doors.remove(270)
                self.doordown.fill(SETTINGS.WHITE)
            self.stop = True

        elif self.doorleftrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if 180 not in doors:
                doors.append(180)
                self.doorleft.fill(SETTINGS.RED)
            else:
                doors.remove(180)
                self.doorleft.fill(SETTINGS.WHITE)
            self.stop = True

        elif self.doorrightrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if 360 not in doors:
                doors.append(360)
                self.doorright.fill(SETTINGS.RED)
            else:
                doors.remove(360)
                self.doorright.fill(SETTINGS.WHITE)
            self.stop = True

        elif not pygame.mouse.get_pressed()[0]:
            self.stop = False

    def change_segtype(self):
        global segtypes
        
        if self.segtypeleftrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if self.segtype > 0:
                self.segtype -= 1
                self.csegtypetxt.update_string(segtypes[self.segtype])
            self.stop = True

        elif self. segtyperightrct.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.stop:
            if self.segtype < len(segtypes)-1:
                self.segtype += 1
                self.csegtypetxt.update_string(segtypes[self.segtype])
            self.stop = True

        elif not pygame.mouse.get_pressed()[0]:
            self.stop = False
            
        

class Map:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.Surface((width*32, height*32))
        self.player_pos_set = False

        self.renderitems = []
        self.tiles = []
        self.array = []
        #Create empty array
        for i in range(self.height):
            self.array.append([0] * self.width)
            
        #Add tiles to array
        for row in range(len(self.array)):
            for column in range(len(self.array[row])):
                self.tiles.append(Tile(self.array[row][column], (column, row)))
                
    def draw(self, canvas):
        self.window.fill((255,255,255))
        canvas.blit(self.window, (0,0))

        for tile in self.tiles:
            if tile.ID != 0:
                canvas.blit(tile.texture, tile.rect)
            if tile.item:
                canvas.blit(tile.item, tile.rect)
            if tile.npc:
                canvas.blit(tile.npc, tile.rect)
            if tile.player_pos:
                pygame.draw.rect(canvas, SETTINGS.DARKRED, tile.rect)

    def add_tile(self):
        global current_id, mode
        if pygame.mouse.get_pressed()[0] and mode == 'tile':
            x = 0
            for tile in self.tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    tile = Tile(current_id, tile.map_pos)
                    self.tiles[x] = tile
                    self.array[tile.map_pos[1]][tile.map_pos[0]] = tile.ID
                x += 1

    def remove_tile(self):
        if pygame.mouse.get_pressed()[2]:
            x = 0
            for tile in self.tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    if tile.player_pos:
                        self.player_pos_set = False
                    tile = Tile(0, tile.map_pos)
                    self.tiles[x] = tile
                    self.array[tile.map_pos[1]][tile.map_pos[0]] = 0
                x += 1

    def add_item(self, item, item_id):
        global mode
        if pygame.mouse.get_pressed()[0] and mode == 'item':
            for tile in self.tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    tile.item = pygame.transform.scale(item, (32,32))
                    tile.item_id = item_id

    def add_npc(self, npc, npc_id):
        global mode, npc_face
        if pygame.mouse.get_pressed()[0] and mode == 'npc':
            for tile in self.tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()) and not SETTINGS.tile_solid[tile.ID]:
                    tile.npc = pygame.transform.scale(npc, (32,32))
                    tile.npc = pygame.transform.rotate(tile.npc, (npc_face)-90)
                    tile.npc_id = npc_id
                    tile.npc_face = npc_face

    def add_start(self):
        global mode
        if pygame.mouse.get_pressed()[0] and mode == 'start pos':
            for tile in self.tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()) and not SETTINGS.tile_solid[tile.ID] and not self.player_pos_set:
                    tile.player_pos = list(tile.map_pos)
                    self.player_pos_set = True
        
class Tile:

    def __init__(self, ID, pos):
        self.ID = ID
        self.pos = (pos[0]*32, pos[1]*32)
        self.map_pos = pos
        self.texture = pygame.image.load(TEXTURES.all_textures[ID]).convert_alpha()
        if SETTINGS.texture_type[ID] == 'vdoor':
            self.texture = pygame.transform.rotate(self.texture, 90)
        self.texture = pygame.transform.scale(self.texture, (32, 32))
        self.rect = self.texture.get_rect()
        self.rect.topleft = self.pos
        self.item = None
        self.item_id = None
        self.npc = None
        self.npc_id = None
        self.npc_face = None
        self.player_pos = None

class SaveLoad:

    def __init__(self):
        #open customLevels.dat
        with open(os.path.join('data', 'customLevels.dat'), 'rb') as file:
            try:
                self.levels = pickle.load(file)
            except:
                self.levels = []

        #open customSegments.dat
        with open(os.path.join('data', 'customSegments.dat'), 'rb') as file:
            try:
                self.segments = pickle.load(file)
            except:
                self.segments = []
    
    def print_slots(self, mtype):
        array = None
        if mtype == 'level':
            array = self.levels
        elif mtype == 'segment':
            array = self.segments

        if array:
            for i in array:
                print("[%s] - %s" % (array.index(i), i['name']))
        else:
            print("No occupied slots")

    def save_map(self, gc, sc):
        global ltype
        editorCanvas.export(gc, sc, False)
        print()
        self.done = False
        print("In which slot do you want to save?")
        self.print_slots(ltype)
        while not self.done:
            print("Leave blank to add a new slot.")
            location = input("> ")
            if not location:
                done = True
                break
            else:
                try:
                    location = int(location)
                    self.done = True
                    break
                except:
                    print("Invalid argument.")
                
        print("Do you want to name your map?")
        name = input("> ")
        if name:
            editorCanvas.dict['name'] = name
        else:
            name = ''

        print("Who made this map?")
        author = input('> ')
        if author:
            editorCanvas.dict['author'] = author        
                    
        if ltype == 'level':
            if (location and location < len(self.levels)) or location == 0:
                editorCanvas.dict['lvl_number'] = location
                self.levels[location] = editorCanvas.dict
            elif not location:
                editorCanvas.dict['lvl_number'] = len(self.levels)
                self.levels.append(editorCanvas.dict)
            else:
                print("Invalid save location!")

        elif ltype == 'segment':
            if (location and location < len(self.segments)) or location == 0:
                editorCanvas.dict['id'] = location
                self.segments[location] = editorCanvas.dict
            elif not location:
                editorCanvas.dict['id'] = len(self.segments)
                self.segments.append(editorCanvas.dict)
            else:
                print("Invalid save location!")

        with open(os.path.join('data', 'customLevels.dat'), 'wb') as file:
            pickle.dump(self.levels, file)

        with open(os.path.join('data', 'customSegments.dat'), 'wb') as file2:
            pickle.dump(self.segments, file2)

        self.__init__()

    def load_map(self):
        global ltype
        self.done = False
        while not self.done:
            print()
            print("What type of map would you like to load?")
            mtype = input("level / segment > ").lower()

            if mtype == 'level' or mtype == 'l':
                mtype == 'l'
                self.done = True
            elif mtype == 'segment' or mtype == 's':
                mtype == 's'
                self.done = True
            else:
                print("Invalid argument!")
                
        if mtype == 's' and self.segments or mtype == 'l' and self.levels:
            self.done = False
            while not self.done:
                print()
                print("What slot would you like to load?")
                print("type \"d [slot]\" to delte a slot")
                if mtype == 's':
                    self.print_slots('segment')
                else:
                    self.print_slots('level')
                slot = input("Slot > ")
                if slot[0:2] == 'd ':
                    self.del_map(slot[2], mtype)
                else:
                    try:
                        slot = int(slot)
                        if mtype == 's' and slot < len(self.segments):
                            self.done = True
                        elif mtype == 'l' and slot < len(self.levels):
                            self.done = True
                        else:
                            print("Number is too high!")
                    except:
                        print("Invalid argument!")
        else:
            print("There are no saved maps of this kind.")
            determine_mode()

        if mtype == 'l':
            loadedmap = self.levels[slot]
            ltype = 'level'
        else:
            loadedmap = self.segments[slot]
            ltype = 'segment'

        #transfer to editorCanvas
        width = len(loadedmap['array'][0])
        height = len(loadedmap['array'])
        
        editorCanvas.__init__(int(width)*32 + 170, int(height)*32 + 170)
        currentMap.__init__(int(width), int(height))

        #add tiles
        currentMap.array = loadedmap['array']
        currentMap.tiles = []
        y = 0
        for row in loadedmap['array']:
            x = 0
            for col in row:
                currentMap.tiles.append(Tile(col, (x, y)))
                x += 1
            y += 1

        #add items
        if loadedmap['items']:
            editorCanvas.load_items()
            for item in loadedmap['items']:
                tile = [x for x in currentMap.tiles if tuple(x.map_pos) == item[0]][0]
                tile.item = pygame.transform.scale(editorCanvas.items[item[1]], (32,32))
                tile.item_id = item[1]

        #add NPCs
        if loadedmap['npcs']:
            editorCanvas.load_npcs()
            for npc in loadedmap['npcs']:
                tile = [x for x in currentMap.tiles if tuple(x.map_pos) == npc[0]][0]
                tile.npc = pygame.transform.scale(editorCanvas.npc_textures[npc[2]], (32,32))
                tile.npc = pygame.transform.rotate(tile.npc, npc[1]-90)
                tile.npc_id = npc[2]
                tile.npc_face = npc[1]

        #add start pos
        try:
            if loadedmap['player_pos']:
                start_tile = [x for x in currentMap.tiles if list(x.map_pos) == loadedmap['player_pos']][0]
                start_tile.player_pos = loadedmap['player_pos']
                currentMap.player_pos_set = True
        except:
            pass

        #show author
        try:
            if loadedmap['author']:
                editorCanvas.showauthor = True
                editorCanvas.authortext.update_string('Author: %s' % loadedmap['author'])
        except:
            pass

    def del_map(self, index, mtype):
        try:
            index = int(index)
        except:
            return
        if mtype == 'l':
            array = self.levels
        else:
            array = self.segments

        print()
        print("Are you sure you want to delete this map?")
        print(array[index]['name'])
        yn = input("Y/N > ").lower()
        if yn == 'y' or yn == 'yes':
            if mtype == 'l':
                del self.levels[index]
            else:
                del self.segments[index]
        elif yn == 'n' or yn == 'no':
            return
        else:
            self.del_map(index, mtype)

        with open(os.path.join('data', 'customLevels.dat'), 'wb') as file:
            pickle.dump(self.levels, file)

        with open(os.path.join('data', 'customSegments.dat'), 'wb') as file2:
            pickle.dump(self.segments, file2)

def main_loop():
    global ltype
    editor_exit = False
    clock = pygame.time.Clock()

    while not editor_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or editorCanvas.exit:
                editor_exit = True
                pygame.quit()
                break
        if not editor_exit:
            editorCanvas.draw()
            editorCanvas.export((0,0,0), (0,0,0,), True)
            editorCanvas.change_id()
            editorCanvas.change_item()
            editorCanvas.change_npc()
            editorCanvas.change_face()
            if ltype == 'segment':
                editorCanvas.click_doors()
                editorCanvas.change_segtype()
            currentMap.draw(editorCanvas.canvas)
            currentMap.add_tile()
            currentMap.add_start()
            currentMap.remove_tile()
            
            pygame.display.update()
            
    editor_exit = False

def new():
    main_loop()

def start():
    main_loop()

if __name__ == '__main__':
    editorCanvas = Canvas(0,0)
    currentMap = Map(1, 1)
    loader = SaveLoad()

    determine_mode()
    main_loop()

    what_now()

    sys.exit(1)


'''How to create a level or segment:
Levels are entire hand crafted maps for the game and segments are bits of map, which will be used in level generation.

1) Choose in command prompt if you want to create a level or segment and determine its size.
Segments will be square and must all be the same size. (default = 9x9)

2) When the window is ready, draw your map. Tiles, NPC's and items can be changed in the right.

3) If you create a segment, remember to specify what type of segment you make. A start, normal or end segment. Start must have
start pos for the player and end must have an exit. Also remember to specify where the doors to other segments are.

4) When everything is done, hit export and add to LEVELS.py - This last step should be temporary and is made for developers.

Note:
There are two kinds of doors: horizontal and vertical (hdoor, vdoor) Place them respectively.
NPC's have a direction they are facing when spawning. Specify that under NPC area.'''
