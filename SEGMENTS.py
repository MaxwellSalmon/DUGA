#This script contains the level segment objects for level generation.
import SETTINGS
import pickle
import os

class Segment:

    def __init__(self, stats):
        self.stats = stats
        self.ID = stats['id']
        self.array = stats['array']
        self.width = len(self.array[0])
        self.height = len(self.array)
        self.doors = stats['doors']
        self.items = stats['items']
        self.npcs = stats['npcs']
        self.type = stats['type']
        self.level_pos = None
        if 'player_pos' in stats:
            self.player_pos = stats['player_pos']
        else:
            self.player_pos = None

def load_customs():
    segments = []
    with open(os.path.join('data', 'standardSegments.dat'), 'rb') as file:
        segments = pickle.load(file)

    for seg in segments:
        SETTINGS.segments_list.append(Segment(seg))

    #If any custom segments, load those too
    if os.stat(os.path.join('data', 'customSegments.dat')).st_size != 0:
        custom_segs = []
        with open(os.path.join('data', 'customSegments.dat'), 'rb') as file1:
            custom_segs = pickle.load(file1)

        for seg in custom_segs:
            SETTINGS.segments_list.append(Segment(seg))

    


#SETTINGS.segments_list.append(Segment({
        #'id' : Unique ID,
        #'npcs' : [([x,y], face, id)],
        #'items' : [([x,y], id)]),
        #'array' : [array],
        #'doors' : [Entrances to the segment in degrees],
        #}))
load_customs()

