import time
import argparse
import pprint as pp
from listofpathpoint import input_handler
import numpy as np


num_samples = 1000
num_nodes = 25
node_dim = 4
# include (x,y,waiting_time, visited_times)
temp = input_handler('10&15data/25_chips/25_1.json')
points = temp.final_ver_points()

opts = f"tsp{num_nodes}_concorde.txt"
# set_nodes_coord = np.random.random([num_samples, num_nodes, node_dim])
set_nodes_coord = np.array(points)
set_nodes_coord = np.tile(set_nodes_coord,(num_samples,1,1))
print(set_nodes_coord)
with open(opts, "w") as f:
    for nodes_coord in set_nodes_coord:
        #solver = TSPSolver.from_data(nodes_coord[:,0], nodes_coord[:,1], norm="GEO")
        #solution = solver.solve()
        f.write( " ".join( str(x)+str(" ")+str(y)+str(" ")+str(waiting_time)+str(" ")+str(visited_time) for x,y,waiting_time,visited_time in nodes_coord) )
        f.write( str(" ") + str('output') + str(" ") )
        #f.write( str(" ").join( str(node_idx+1) for node_idx in solution.tour) )
        f.write( "\n" )


