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

import my_utils
import myNN
import mySECs


start = time.time()

#get input
input_data = get_single_data('berlin52.txt')

#create graph data-structures
g = make_graph(input_data)

#get upper bound from heuristics
(visited, upper_bound) = myNN(input_data)

#initialize the lp
tsp_lp = initialize_tsp_lp(...)

x_best = None

#this queue stores the upper and lower bounds of each variable. 
subprob_queue = deque([[[]]])
obj = np.inf
    
while True:
    sub_lp = subprob_queue.popleft()
    
    """
    We apply the constraints from sub_lp to tsp_lp,
    Solve the subproblem,
    Look for cuts and apply them,
    Solve again,
    Clear out the cuts from the model.
    """
    #retrieve list of variables in the model
    x = tsp_lp.getVars()
    #bring in the 0-1 constraints.
    #these are actually introduced as boundaries rather than constraints.
    #they are stored in sub_lp, and here, we introduce them to tsp_lp.
    
    lb_for_sub_lp = 0.0
    ub_for_sub_lp = 1.0

    for constraint in sub_lp:
        #constraint[0] is the index, constraint[1] is the prescribed value
        #we want to create two vectors and then update the model
        if constraint[1] == 0
            ub_for_sub_lp[constraint[0]] = 0.0
        elif constraint[1] == 1
            lb_for_sub_lp[constraint[0]] = 1.0
    tsp_lp.setAttr("LB", lb_for_sub_lp)
    tsp_lp.setAttr("UB", ub_for_sub_lp)
    tsp_lp.update()
    tsp_lp.optimize()

    #tsp_lp is now an updated lp at our node that we're considering.
    #we want its objective value.
    obj_val = tsp_lp.ObjVal
    constraint_binder = []

    if obj_val > upper_bound: 
        node_status = 'prune'
    else:
        while True:
            #try to find a cut from the cut factory 
            cut_edges = mySECs.SECs(x, G_inv)
            if cut_edges:
                new_constr = tsp_lp.addConstr(
                    sum(1*x[i] for i in cut_edges) <= 2
                )
                constraint_binder.append(new_constr)
                tsp_lp.update()
                tsp_lp.optimize()
            else 
                break
        
        intstatus = 0
        for i in range(len(tsp_lp.X))
            intstatus += np.isclose([tsp_lp.X[i]], [0])[0] + np.isclose([tsp_lp.X[i]], [1])[0]
        if intstatus == len(tsp_lp.X) 
            node_status = 'integral'
        else 
            node_status = 'branch'
            
    x = tsp_lp.X
    obj = tsp_lp.ObjVal

    tsp_lp.remove(constraint_binder)
    tsp_lp.update()

    """
    The node_status is one of the following:
    prune:  this means the problem is infeasible or the objective is greater than the upper bound.
    integral: we have a candidate for the solution to the TSP. Set the global upper bound and the x that we got.
    branch: we have a non-integral solution with no subtours. Add two subproblems to the queue.
    """

    if node_status == 'integral'
        if obj <= upper_bound
            upper_bound = obj   
            x_best = x
    elif node_status == 'branch'
        #Put two subproblems in the queue. We use the index that's closest to 0.5. 
        arr = np.abs(x - 0.5)
        index_for_split = arr.argmin()
        zero_branch = sub_lp + [index_for_split, 0] 
        one_branch = sub_lp + [index_for_split, 1] 
        #Each new subprob will have all the boundary constraints of its parent, plus the new boundary constraint.
        subprob_queue.extend([zero_branch, one_branch])

        
    if not sub_problem_queue 
        break

# TODO: print outputs


end = time.time()
print('\nTime = {} seconds'.format(end - start))