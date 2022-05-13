import math
from functools import cmp_to_key
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import json
import sys
import optparse

class MotherBoardInput:
    def __init__(self, photo_name, json_name):
        img = mpimg.imread(photo_name)
        self.json_name = json_name
        self.gray = img[:, :, 2]
        self.visit_time_range = 4

    # Return a tuple(regions, gluewidth),
    #   where regions is a list of rectangles,
    #   where rectangle is represented as a list of it's four vertices,
    #   where each vertex is a 2D coordinate.
    def info_extraction(self):
        with open(self.json_name, 'r') as file:
            data = json.load(file)
        shapes = data['shapes']
        regions = []
        gluewidth = -1.
        j = 0
        real_idx = []
        real_idx_accumulation = []
        for item in shapes:
            if item['label'] == 'gluewidth':
                gluewidth = item['points'][1][1] - item['points'][0][1]
            else:
                j+=1
                #for a in item['points']:
                    #a = sorted(a)
                    #print(tuple(map(int, a)))
                #regions.append([tuple(map(int, a)) for a in item['points']])
                np.random.seed(j-1)
                visited_time = np.random.choice(range(1,self.visit_time_range),1).tolist()[0]
                real_idx_accumulation.append(visited_time)
                for i in range(visited_time):
                    real_idx.append(j-1)
                    regions.append(sort_verices([tuple(map(int, a)) for a in item['points']]))
        return regions, gluewidth, self.gray, real_idx, real_idx_accumulation

    # Return the rectangle region based on the index of mother board image
    def target_area(self, x, y, x2, y2):
        ta = self.gray[int(y): int(y2), int(x): int(x2)]
        return ta

    # process the regions info and label info
    # for path constructing
    def shapes_extrat(self, item_in_shapes):
        if item_in_shapes['label'] == "gluewidth":
            gluewidth = item_in_shapes['points'][1][1] - item_in_shapes['points'][0][1]
            start_point = (-1, -1)
            return (gluewidth, gluewidth)
        else:
            # print(item_in_shapes['points'])
            return item_in_shapes['points']
class PathToolBox:
    def __init__(self, target_regions, gluewidth, img):
        self.target_regions = target_regions
        self.gluewidth = gluewidth
        self.gray = img
    def get_shortest_side(self, rect):
        side1 = self.dist_euler(rect[0], rect[1])
        side2 = self.dist_euler(rect[1], rect[2])
        if side1 < side2:
            return 0, side1
        else:
            return 1, side2

    def get_outcorner(self, rect_index, incorner):
        # precomputed with high precision super algorithm:
        #
        # 0 3
        # 1 2
        #
        # 0 even:1 odd:2 | even:3 odd:2
        # 1 even:0 odd:3 | even:2 odd:3
        # 2 even:3 odd:0 | even:1 odd:0
        # 3 even:2 odd:1 | even:0 odd:1
        look_up = [[(1, 2), (0, 3), (3, 0), (2, 1)], [(3, 2), (2, 3), (1, 0), (0, 1)]]
        rect = self.target_regions[rect_index]
        short_side = self.get_shortest_side(rect)
        turns = int(short_side[1] / self.gluewidth)
        return look_up[short_side[0]][incorner][turns % 2]

    def dist_euler(self, a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def dist_max(self, a, b):
        edge1 = abs(a[0] - b[0])
        edge2 = abs(a[1] - b[1])
        if edge1 > edge2:
            return edge1
        else:
            return edge2
if __name__ == "__main__":
    mb_info = MotherBoardInput('mother_board.png', '10&15data/25_chips/25_1.json').info_extraction()
    rect_list = mb_info[0]
    glue_width = mb_info[1]
    path_tool = PathToolBox(rect_list, glue_width, mb_info[2])