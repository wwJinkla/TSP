"""
TSP Driver
"""
import sys
import time
import numpy as np

import branch_and_cut as bnc

start = time.time()

# parse input data.

# create graph data-structures.

# get upper bound from heuristics

# formulate initial LP
tsp_lp = bnc.initialize_tsp_lp()

# set up branch and cut.

my_branch_and_cut = bnc.BranchAndCut(tsp_lp, ...)

# execute branch and cut procedure.
branch_and_cut.run()

# print outputs


end = time.time()
print('\nTime = {} seconds'.format(end - start))