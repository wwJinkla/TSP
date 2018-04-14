"""
TSP Driver

We want this to contain the graph structure, and 
to break up the functions of branch and cut. (So 
at this point there is no branch_and_cut class, 
all the mechanics are here in the driver)

"""
import sys
import time
import numpy as np
from collections import deque

import gurobipy as gurobi

start = time.time()

#TODO:  parse input data.

#TODO:  create graph data-structures.
g = Graph....

#TODO: get upper bound from heuristics
upper_bound = ...

#TODO: decide where to place the "initialize" 
# function (as a utility?) and what inputs we
# call "initialize" with.
tsp_lp = initialize_tsp_lp(...)

x_best = None
#this queue stores the upper and lower bounds of each variable. 
subprob_queue = deque([[[]]])
obj = np.inf
    
while True:
    sub_lp = subprob_queue.popleft()
    
    """
    We apply the constraints from sub_lp on top of init_lp. 
    Solve the subproblem.
    Look for cuts and apply them.
    Solve again.
    Clear out the cuts from the model.
    """
    #reset x to its original characteristics (clear the upper and lower bounds)
    x = tsp_lp.getVars()
    #bring in the 0-1 constraints.
    #TODO: use addConstr to put the constraints stored in sub_lp into tsp_lp
    for constraint in sub_lp:
        tsp_lp.addConstr(       )
    tsp_lp.update()
    tsp_lp.optimize()

    #tsp_lp is now an updated lp at our node that we're considering.
    #we want its objective value.
    obj_val = tsp_lp.ObjVal

    if obj_val > upper_bound: 
        node_status = 'prune'
    else:
        while True:
            #try to find cuts from the cut_factory 
            if cuts:
                addConstr, update, optimize, continue
        if x is integral
            node_status = 'integral'
        else 
            node_status = 'branch'
            
        
    x = tsp_lp.X
    obj = tsp_lp.ObjVal

    tsp_lp.remove(cuts that we added)
    tsp_lp.update()

    """
    The node_status is one of the following:
    prune:  this means the problem is infeasible or the objective is greater than the upper bound.
    integral: we have a candidate for the solution to the TSP. Set the global upper bound and the x that we got.
    branch: we have a non-integral solution with no subtours. Add two subproblems to the queue.
    """

    if node_status == 'integral'
        upper_bound = obj
        x_best = x
    elif node_status == 'prune'
        continue
    elif node_status == 'branch'
        #TODO: put two subproblems in the queue. Each new subproblem 
        will have all the boundary constraints of its parent, plus the new boundary constraints.
        
    if not sub_problem_queue 
        break

# TODO: print outputs


end = time.time()
print('\nTime = {} seconds'.format(end - start))