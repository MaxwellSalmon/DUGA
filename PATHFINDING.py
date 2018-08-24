import SETTINGS
import random

#There is some whack error handling. This is because this might be used manually by a human and therefore it needs some human-friendly feedback.
#This is the A* pathfinding algorithm for NPC movement and more
#G = Distance from start
#H = Distance to end
#F = G + H
#open/closedlist syntax = [G, H, F, parent]
#Parent is from where the node is checked.

def pathfind(start, end):
    #print(start, end)
    '''== A* Pathfinding ==\npathfind(start, end) -> Shortest path from start to end\nFormat is list with tile objects'''
    openlist = {}
    closedlist = {}
    path = []
    error = False

    #Reports if a node is outside the map
    if start[0] > max(SETTINGS.all_tiles, key=lambda x: x.map_pos).map_pos[0] or start[1] > max(SETTINGS.all_tiles, key=lambda x: x.map_pos).map_pos[1]:
        print("=== WARNING: ===")
        print("Start point in pathfinding is outiside map!")
        error = True
    elif end[0] > max(SETTINGS.all_tiles, key=lambda x: x.map_pos).map_pos[0] or end[1] > max(SETTINGS.all_tiles, key=lambda x: x.map_pos).map_pos[1]:
        print("=== WARNING: ===")
        print("End point in pathfinding is outside map!")
        error = True
              
    if not error:
        start_point = [x for x in SETTINGS.all_tiles if x.map_pos == start][0]
        end_point = [x for x in SETTINGS.all_tiles if x.map_pos == end][0]
        
        #Report errors
        if SETTINGS.tile_solid[start_point.ID] and (start_point.type != 'hdoor' and start_point.type != 'vdoor'):
            print("=== WARNING: ===")
            print("Error! Start point in pathfinding is a solid block!")
            print(start_point.map_pos, start_point.ID)
            print()
            error = True
        if SETTINGS.tile_solid[end_point.ID] and (end_point.type != 'hdoor' and end_point.type != 'vdoor'):
            print("=== WARNING: ===")
            print("Error! End point in pathfinding is a solid block!")
            print(end_point.map_pos, end_point.ID)
            print()
            error = True

        if error:
            end_point = [x for x in SETTINGS.all_tiles if x.map_pos == find_near_position(end)]
            if end_point:
                end_point = end_point[0]
                error = False
                    
                

    if not error:
        #f_value has to be determined after creation of node.
        openlist[start_point] = [0, find_distance(start_point, end_point), 0, None]
        openlist[start_point][2] = f_value(start_point, openlist)
        current_point = start_point

        while current_point != end_point:
            try:
                current_point = min(openlist, key=lambda k: (openlist[k][2], openlist[k][1]))
            except:
                error = True
                break
            
            closedlist[current_point] = openlist[current_point]
            del openlist[current_point]

            #Find adjacent nodes
            adjacent = []
            
            adj_up = [x for x in SETTINGS.all_tiles if x.map_pos[0] == current_point.map_pos[0] and x.map_pos[1] == current_point.map_pos[1]-1]
            adj_right = [x for x in SETTINGS.all_tiles if x.map_pos[0] == current_point.map_pos[0]+1 and x.map_pos[1] == current_point.map_pos[1]]
            adj_down = [x for x in SETTINGS.all_tiles if x.map_pos[0] == current_point.map_pos[0] and x.map_pos[1] == current_point.map_pos[1]+1]
            adj_left = [x for x in SETTINGS.all_tiles if x.map_pos[0] == current_point.map_pos[0]-1 and x.map_pos[1] == current_point.map_pos[1]]
            
            if adj_up:
                adjacent.append(adj_up[0])
            if adj_right:
                adjacent.append(adj_right[0])
            if adj_down:
                adjacent.append(adj_down[0])
            if adj_left:
                adjacent.append(adj_left[0])

            #Add adjecent nodes to openlist if they are not in closedlist and are not solid
            for adj in adjacent:
                
                if (adj.type == 'hdoor' or adj.type == 'vdoor' or not SETTINGS.tile_solid[adj.ID]) and adj not in closedlist:
                    if (adj in openlist and openlist[adj][0] > closedlist[current_point][0]+1) or adj not in openlist:
                        openlist[adj] = [closedlist[current_point][0]+1, find_distance(adj, end_point), 0, current_point]
                        openlist[adj][2] = f_value(adj, openlist)
        
        try:
            while closedlist[current_point][3] != None:
                path.append(current_point)
                current_point = closedlist[current_point][3]
        except:
            pass
            
        path.append(start_point)
        path = list(reversed(path))

        if error:
            return closedlist
        else:
            return path

def find_near_position(position):
    adjacent_tiles = [x for x in SETTINGS.walkable_area if (x.map_pos[0] == position[0] + 1 or x.map_pos[0] == position[0] -1 or x.map_pos[0] == position[0])
                      and (x.map_pos[1] == position[1] + 1 or x.map_pos[1] == position[1] - 1 or x.map_pos[1] == position[1])]
    #convert coordinates to a tile
    chosen_tiles = [x for x in SETTINGS.all_tiles if x.map_pos in adjacent_tiles]

    if chosen_tiles:
        return random.choice(chosen_tiles)
    else:
        return None
    
        
def find_distance(point, end):
    x = point.map_pos[0] + point.map_pos[1]
    y = end.map_pos[0] + end.map_pos[1]
    h = abs(x - y)
    return h
    

def f_value(point, openlist):
    f = openlist[point][2] = openlist[point][0] + openlist[point][1]
    return f

def random_point(start):
    #cpos = Current pos
    closedlist = []
    cpos = start
    closedlist.append(cpos)
    for x in range(random.randint(50,200)):
        #adjacent = up, right, down, left
        adjacent = [[cpos[0], cpos[1]-1],
                    [cpos[0]+1, cpos[1]],
                    [cpos[0], cpos[1]+1],
                    [cpos[0]-1, cpos[1]]]
        
        ranadj = random.choice(adjacent)
        ranadj_tile = [x for x in SETTINGS.all_tiles if ranadj == x.map_pos]
        
        if not SETTINGS.tile_solid[ranadj_tile[0].ID] and ranadj not in closedlist:
            cpos = ranadj
            closedlist.append(cpos)

    return cpos
        
        
        





