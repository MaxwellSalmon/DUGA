import random
import math
import copy
import os
import SEGMENTS
import SETTINGS
import TEXTURES
import LEVELS

class Generator:

    def __init__(self):

        self.segpath = []
        self.all_segs = []
        self.seed = None
        self.spawnable_area = []

        #Constants
        #Item probability
        self.max_item_amount =  15 #Multiplied by amount of segments
        self.max_items_per_segment = 5
        self.spawn_chance = 8
        self.spawn_chance_high = 40 #Also influenced
        self.ammo_spawn_chance = 35 #Also influenced
        
        self.item_probability = []
        self.item_spawns = {
            0 : 28, #health
            1 : 30, #Kevlar
            2 : 25, #bullet
            3 : 18, #shell
            4 : 15, #knife
            5 : 16, #pistol
            6 : 13, #ak47
            7 : 10, #shotgun
            8 : 11, #knuckles
            9 : 7, #gauss
            10 : 20, #ferromag
            11 : 14, #sg pistol  --¤¤¤¤--
            12 : 8, #light knuckles
            13 : 1, #blood knuckles
            14 : 8, #shiny knife
            15 : 10, #desert knife
            16 : 6, #modded shotgun
            17 : 6, #impossible shotgun
            18 : 8, #ak74
            19 : 10, #ak47 ext mag
            20 : 12, #camo ak47
            21 : 12, #light ak47
            22 : 1, #gauss pistol
            23 : 8, #hp pistol
            24 : 4, #modded gauss
            25 : 3, #bump gauss
            26 : 5, #black sg pistol
            27 : 1, # wtf pistol
            28 : 8, #hp pistol
            29 : 6, #black sgp
            30 : 2, #wtf sgp
            31 : 8, #auto pistol
            }
        
        for i in self.item_spawns:
            for x in range(self.item_spawns[i]):
                self.item_probability.append(i)

        #NPC probability
        self.max_npc_amount = SETTINGS.current_level+1 #Will be multiplied by amount of segments
        self.max_npcs_per_segment = 3
        self.min_npcs_per_level = 3
        self.npc_spawn_chance = 20 + SETTINGS.current_level*1.5 #Also influenced
        self.npc_probability = [0,0,
                                1,1,
                                2,2,
                                3,3,
                                4,4,
                                5,5,
                                7,
                                8,
                                9,
                                10,
                                11,
                                12,
                                13,
                                15,
                                16,
                                17
                                ]

        #Color list
        self.ground_colors = [SETTINGS.GRAY, SETTINGS.LIGHTGRAY, SETTINGS.DARKGRAY, SETTINGS.DARKRED, SETTINGS.DARKGREEN]
        self.sky_colors = [SETTINGS.GRAY, SETTINGS.LIGHTGRAY, SETTINGS.LIGHTBLUE, SETTINGS.BLUE, SETTINGS.LIGHTGREEN]
        self.shade_colors = [(0,0,0,255), (255,255,255,255)]
        

    def create_seed(self, seed):
        if seed:
            self.seed = seed[0]
        else:
            self.seed = random.random()

        SETTINGS.seed = self.seed

        random.seed(self.seed)
        print("Seed: ", self.seed)

    def generate_levels(self, amount, size, *seed):
        #Generate sequence of levels and append to SETTINGS.all_levels
        self.create_seed(seed)
        SETTINGS.glevels_list = []
            
        for i in range(amount):
            self.generate_level(size, seed)
            self.seed += 0.001
            self.segpath = []
        

    def generate_level(self, size, *seed):
        if not self.seed:
            self.create_seed(seed[0])
        
        #Rotate segments in all directions.
        if not self.all_segs:
            for seg in SETTINGS.segments_list:
                self.all_segs.append(seg)
                for i in range(3):
                    self.all_segs.append(self.rotate_segment(self.all_segs[-1]))
            
        num = 0
        #Create empty grid.
        array = []
        for i in range(size):
            array.append([None]*size)

        path = []
        checklist = []

        #Pick a random starting point from top row.
        x = random.randint(0,size-1)
        y = 0
        #([x,y], parent)
        path.append(([x,y], None))

        #Recursive function, which adds or subtracts 1 to x or y.
        def seg_pos_increment(temppos):
            tempx, tempy = temppos[0], temppos[1]
            inc = random.choice([-1, 1])
            if random.randint(0,1) == 1:
                tempx += inc
            else:
                tempy += inc

            if -1 in [tempx, tempy] or size in [tempx, tempy] or ([tempx, tempy]) in checklist:
                return seg_pos_increment(temppos)
            else:
                return([tempx, tempy], temppos)

        #Checks if the adjacent coordinates are vacant.
        def check_adjacents(temppos):
            ax = temppos[0]
            ay = temppos[1]
            adjacents = [[ax+1, ay], [ax-1, ay], [ax, ay+1], [ax, ay-1]]
            for coords in adjacents:
                if (-1 not in coords and size not in coords) and coords not in checklist:
                    return True
            return False

        #Find an end point on the bottom row.
        end_point = [random.randint(0,size-1), size-1]

        #Add coordinates to the path until it reaches the end.
        while path[num][0] != end_point:
            if path[num][0] not in checklist:
                    checklist.append(path[num][0])
                    
            if check_adjacents(path[num][0]):
                path.append(seg_pos_increment(path[num][0]))
                num += 1
            else:
                del(path[num])
                num -= 1            

        #Place segments that will be accessible from previous placed segment.
        for i in range(len(path)):
            cpos = path[i][0]
            if i > 0:
                ppos = path[i-1][0]
            else:
                ppos = None
                
            if i < len(path)-1:
                npos = path[i+1][0]
            else:
                npos = None

            #Place the segments.
            if not ppos:
                array[cpos[1]][cpos[0]] = self.suitable_segment(array, None, cpos, npos, 'start')
                
            elif ppos and npos:
                array[cpos[1]][cpos[0]] = self.suitable_segment(array, ppos, cpos, npos, None)

            else:
                array[cpos[1]][cpos[0]] = self.suitable_segment(array, ppos, cpos, None, 'end')

        #Place dead ends.
        for seg in self.segpath:
            right = [max(seg.level_pos[0], min(len(array[0])-1, seg.level_pos[0]+1)), seg.level_pos[1]]
            left = [max(seg.level_pos[0], min(len(array[0])-1, seg.level_pos[0]-1)), seg.level_pos[1]]
            up = [seg.level_pos[0], max(seg.level_pos[1], min(len(array)-1, seg.level_pos[1]-1))]
            down = [seg.level_pos[0], max(seg.level_pos[1], min(len(array)-1, seg.level_pos[1]+1))]
            
            if 360 in seg.doors and not array[right[1]][right[0]]:
                array[right[1]][right[0]] = self.suitable_segment(array, seg.level_pos, right, None, None)
            if 180 in seg.doors and not array[left[1]][left[0]]:
                array[left[1]][left[0]] = self.suitable_segment(array, seg.level_pos, left, None, None)
            if 90 in seg.doors and not array[up[1]][up[0]]:
                array[up[1]][up[0]] = self.suitable_segment(array, seg.level_pos, up, None, None)
            if 270 in seg.doors and not array[down[1]][down[0]]:
                array[down[1]][down[0]] = self.suitable_segment(array, seg.level_pos, down, None, None)

        #Place emptyness where there should be emptyness...
        empty = []
        for i in range(self.all_segs[0].height):
            empty.append([0] * self.all_segs[0].width)
        for row in range(len(array)):

            for col in range(len(array[row])):
                if not array[row][col]:
                    array[row][col] = SEGMENTS.Segment({'id' : None, 'items' : [], 'npcs' : [], 'array' : empty, 'doors' : [], 'type' : 'empty'})

        self.place_random_items()
        self.spawn_random_npcs()
            
        self.translate_map(self.kill_dead_ends(array), size)

    def rotate_segment(self, segment):
        #Rotate array
        rotseg = copy.deepcopy(segment)
        rotseg.array = list(zip(*reversed(rotseg.array)))
        for i in range(len(rotseg.array)):
            rotseg.array[i] = list(rotseg.array[i])

            t = 0
            for tile in rotseg.array[i]:
                if SETTINGS.texture_type[tile] == 'hdoor' or SETTINGS.texture_type[tile] == 'vdoor':
                    
                    for y in range(len(TEXTURES.all_textures)):
                        if y != tile and os.path.samefile(TEXTURES.all_textures[y], TEXTURES.all_textures[tile]):
                            rotseg.array[i][t] = y
                            
                t += 1  

        #Rotate doors
        for i in range(len(rotseg.doors)):
            rotseg.doors[i] -= 90
            if rotseg.doors[i] <= 0:
                rotseg.doors[i] += 360

        #Rotate items        
        origin = [int(len(rotseg.array[0])/2), int(len(rotseg.array)/2)]
        x = 0
        for item in rotseg.items:
            tempx = item[0][0] - origin[0]
            tempy = item[0][1] - origin[1]

            tempx1 = math.cos(math.radians(90)) * tempx - math.sin(math.radians(90)) * tempy
            tempy1 = math.sin(math.radians(90)) * tempx + math.cos(math.radians(90)) * tempy

            tempx1 += origin[0]
            tempy1 += origin[1]

            rotseg.items[x] = ([int(tempx1), int(tempy1)], item[1])

            x += 1
        
        #rotate npc
        x = 0
        for npc in rotseg.npcs:
            tempx = npc[0][0] - origin[0]
            tempy = npc[0][1] - origin[1]
            
            tempx1 = math.cos(math.radians(90)) * tempx - math.sin(math.radians(90)) * tempy
            tempy1 = math.sin(math.radians(90)) * tempx + math.cos(math.radians(90)) * tempy

            tempx1 += origin[0]
            tempy1 += origin[1]

            tempnpc = npc[1]
            tempnpc -= 90
            if tempnpc < 0:
                tempnpc += 360
            
            rotseg.npcs[x] = ([int(tempx1), int(tempy1)], tempnpc, npc[2])
            x += 1
            
        if rotseg.player_pos:
            tempx = rotseg.player_pos[0] - origin[0]
            tempy = rotseg.player_pos[1] - origin[1]

            tempx1 = math.cos(math.radians(90)) * tempx - math.sin(math.radians(90)) * tempy
            tempy1 = math.sin(math.radians(90)) * tempx + math.cos(math.radians(90)) * tempy

            tempx1 += origin[0]
            tempy1 += origin[1]

            rotseg.player_pos = [int(tempx1), int(tempy1)]

        return rotseg

    def suitable_segment(self, array, prev, current, nex, special):
        #Convert coords to degrees.
        enter, leave, segment = None, None, None
        if nex:
            if nex[0] == current[0] + 1: #right
                enter = 360
            elif nex[0] == current[0] - 1: #left
                enter = 180
            elif nex[1] == current[1] + 1: #down
                enter = 270
            elif nex[1] == current[1] - 1: #up
                enter = 90
                
        if prev:
            if prev[0] == current[0] + 1: #right
                leave = 360
            elif prev[0] == current[0] - 1: #left
                leave = 180
            elif prev[1] == current[1] + 1: #down
                leave = 270
            elif prev[1] == current[1] - 1: #up
                leave = 90
                
        #Find suitable adjacents
        if enter and leave:
            segment = [x for x in self.all_segs if enter in x.doors and leave in x.doors and x.type == 'normal']
        elif enter and not leave and not special:
            segment = [x for x in self.all_segs if enter in x.doors and x.type == 'normal']
        elif leave and not enter and not special:
            segment = [x for x in self.all_segs if leave in x.doors and x.type == 'normal']
        #Place start/stop segments. Enter and leave seems to be swapped, but who cares?
        elif enter and not leave and special:
            segment = [x for x in self.all_segs if enter in x.doors and x.type == 'start']
        elif leave and not enter and special:
            segment = [x for x in self.all_segs if leave in x.doors and x.type == 'end']

        #Check if segment doors hit dead ends.
        if segment:
            temppos = [None, None]
            opposite = None

            for seg in segment:
                for door in seg.doors:
                    if door == 360:
                        opposite = 180
                        temppos = [current[0]+1, current[1]]
                    elif door == 90:
                        opposite = 270
                        temppos = [current[0], current[1]-1]
                    elif door == 180:
                        opposite = 360
                        temppos = [current[0]-1, current[1]]
                    elif door == 270:
                        opposite = 90
                        temppos = [current[0], current[1]+1]

                    temppos[0] = max(0 , min(len(array[0])-1, temppos[0]))
                    temppos[1] = max(0, min(len(array)-1, temppos[1]))
                    
                    if array[temppos[1]][temppos[0]]:
                        if opposite not in array[temppos[1]][temppos[0]].doors:
                            segment.remove(seg)
                            break
                
        #Return segment
        if segment:
            finalsegment = copy.deepcopy(random.choice(segment))
            finalsegment.array = copy.deepcopy(finalsegment.array)
            finalsegment.level_pos = current
            self.segpath.append(finalsegment)
            
            return finalsegment
        else:
            print("Did not have a segment with enter: ", enter, "and leave: ", leave)

    def kill_dead_ends(self, array):
        #Change segments with doors leading nowhere.
        changesegs = []
        i = 0
        for seg in self.segpath:
            #Compare segment with adjacent segments.
            rightseg = [x for x in self.segpath if x.level_pos == [seg.level_pos[0]+1, seg.level_pos[1]]]
            leftseg = [x for x in self.segpath if x.level_pos == [seg.level_pos[0]-1, seg.level_pos[1]]]
            upseg = [x for x in self.segpath if x.level_pos == [seg.level_pos[0], seg.level_pos[1]-1]]
            downseg = [x for x in self.segpath if x.level_pos == [seg.level_pos[0], seg.level_pos[1]+1]]

            access = []
            
            for deg in seg.doors:
                if deg == 360 and rightseg:
                    if 180 in rightseg[0].doors:
                        access.append(360)
                    
                elif deg == 90 and upseg:
                    if 270 in upseg[0].doors:
                        access.append(90)
                    
                elif deg == 180 and leftseg:
                    if 360 in leftseg[0].doors:
                        access.append(180)
                    
                elif deg == 270 and downseg:
                    if 90 in downseg[0].doors:
                        access.append(270)

            #Find a suitable segment to replace with if necessary.
            if set(access) != set(seg.doors):
                newseg = [x for x in self.all_segs if set(access) == set(x.doors) and seg.type == x.type]
                if newseg:
                    newseg = copy.deepcopy(random.choice(newseg))
                    newseg.level_pos = seg.level_pos
                    changesegs.append((newseg, i)) #Gritty way of doing it...
                else:
                    print("WARNING: No segment with doors: ", access, " of type ", x.type)
            i += 1

        #Finally replace array and self.segpath segments with new segments.
        for x in changesegs:
            newseg = x[0]
            i = x[1]

            npcs = self.segpath[i].npcs
            self.segpath[i] = newseg
            newseg.npcs = npcs
            array[newseg.level_pos[1]][newseg.level_pos[0]] = newseg

        return array

    def translate_map(self, segs, size):
        array = []
        offset = 0

        self.segpath[0].array[0][0] = 0

        #Place all segment grids in one, big grid.
        for i in range(size):
            offset = (segs[0][0].height * i)
            for seg in segs[i]:
                for row in range(len(seg.array)):
                    array.append([])
                    for tile in seg.array[row]:
                        array[row + offset].append(tile)

        newarray = []         
        for x in array:
            if x:
                newarray.append(x)

        #Translate player pos
        calcstart = [0,0]
        calcstart[0] = self.segpath[0].player_pos[0] + self.segpath[0].width * self.segpath[0].level_pos[0]
        calcstart[1] = self.segpath[0].player_pos[1] + self.segpath[0].height * self.segpath[0].level_pos[1]

        #Translate item pos
        translated_items = []
        for seg in self.segpath:
            for item in seg.items:
                x = item[0][0] + seg.width * seg.level_pos[0]
                y = item[0][1] + seg.height * seg.level_pos[1]
                translated_items.append(((x,y), item[1]))

        #Translate NPC pos
        translated_npcs = []
        for seg in self.segpath:
            for npc in seg.npcs:
                x = npc[0][0] + seg.width * seg.level_pos[0]
                y = npc[0][1] + seg.height * seg.level_pos[1]
                translated_npcs.append(((x,y), npc[1], npc[2]))
        
        SETTINGS.glevels_list.append(LEVELS.Level({
            'items' : translated_items,
            'ground_color' : random.choice(self.ground_colors),
            'sky_color' : random.choice(self.sky_colors),
            'array' : newarray,
            'lvl_number' : len(SETTINGS.glevels_list),
            'npcs' : translated_npcs,
            'player_pos' : calcstart,
            'shade' : (bool(random.getrandbits(1)), random.choice(self.shade_colors), random.randint(150, 1000))
            }))

    def place_random_items(self):
        items = 0
        seed = SETTINGS.current_level + self.seed

        #If there are too many items, return
        for seg in self.segpath:
            for item in seg.items:
                items += 1

        if items >= self.max_item_amount * len(self.segpath):
            return
        
        #Higher chance of spawning items in dead ends.
        for i in range(len(self.segpath)):    
            seg = self.segpath[i]
            for y in range(self.max_items_per_segment):
                random.seed(seed)
                if (len(seg.doors) <= 1 and self.spawn_chance_high >= random.randint(0,100)) or (len(seg.doors) > 1 and self.spawn_chance >= random.randint(0,100)):
                    is_good = False
                    while not is_good:
                        randomx = random.randint(0, len(seg.array)-1)
                        randomy = random.randint(0, len(seg.array)-1)
                        occupied = [x for x in seg.items if list(x[0]) == [randomx, randomy]]
                        
                        if not SETTINGS.tile_solid[seg.array[randomy][randomx]] and not occupied:
                            item = random.choice(self.item_probability)
                            self.segpath[i].items.append(((randomx, randomy), item))

                            #Higher chance of ammo spawning next to weapons
                            if SETTINGS.item_types[item]['type'] in ['primary', 'secondary']:
                                ammo = [x for x in SETTINGS.item_types if x['type'] == SETTINGS.item_types[item]['effect'].ammo_type][0]
                                adjacents = [[randomx+1, randomy], [randomx, randomy+1], [randomx-1, randomy], [randomx, randomy-1]]
                                for pos in adjacents:
                                    occupied = [x for x in seg.items if x[0] == (max(0, min(pos[0], len(seg.array)-1)), max(0, min(pos[1], len(seg.array)-1)))]
                                    if self.ammo_spawn_chance >= random.randint(0, 100) and not SETTINGS.tile_solid[self.segpath[i].array[max(0, min(pos[0], len(seg.array)-1))][max(0, min(pos[1], len(seg.array)-1))]] and not occupied:
                                        self.segpath[i].items.append(((pos[0], pos[1]), ammo['id']))
                                        
                            is_good = True
                            seed += 0.001
        

    def spawn_random_npcs(self):
        seed = SETTINGS.current_level + self.seed
        npcs = 0
        degrees = [90, 180, 270, 360]

        for seg in self.segpath:
            for npc in seg.npcs:
                npcs += 1

        if npcs >= self.max_npc_amount * len(self.segpath):
            return

        spawned_npcs = 0
        #Spawn NPCs randomly
        for i in range(len(self.segpath)):
            seg = self.segpath[i]
            if seg.type != 'start':
                for y in range(self.max_npcs_per_segment):
                    seed += 0.001
                    random.seed(seed)
                    if self.npc_spawn_chance + len(self.segpath) >= random.randint(0,100):
                        is_good = False
                        while not is_good:
                            randomx = random.randint(0, len(seg.array)-1)
                            randomy = random.randint(0, len(seg.array)-1)
                            occupied = [x for x in seg.npcs if list(x[0]) == [randomx, randomy]]

                            if not SETTINGS.tile_solid[seg.array[randomy][randomx]] and not occupied:
                                npc = random.choice(self.npc_probability)
                                self.segpath[i].npcs.append(((randomx, randomy), random.choice(degrees), npc))

                                is_good = True
                                spawned_npcs += 1
                                

        #If there were no NPCs, place minimum amount
        npc_amount = 0
        for i in self.segpath:
            for npc in i.npcs:
                npc_amount += 1

        while npc_amount < self.min_npcs_per_level:
            seed += 0.00001
            random.seed(seed)
            segment = random.choice(self.segpath)
            index = self.segpath.index(segment)
            randomx = random.randint(0, len(segment.array)-1)
            randomy = random.randint(0, len(segment.array)-1)
            occupied = [x for x in segment.npcs if list(x[0]) == [randomx, randomy]]

            if not SETTINGS.tile_solid[segment.array[randomy][randomx]] and not occupied:
                npc = random.choice(self.npc_probability)
                self.segpath[index].npcs.append(((randomx, randomy), random.choice(degrees), npc))
                npc_amount += 1
            
        

