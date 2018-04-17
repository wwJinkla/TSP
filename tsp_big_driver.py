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
from gurobipy import *

sys.path.insert(0, '/Users/alexteich/Documents/CAAM_571')
from my_utils import *

import myNN
import mySECs


start = time.time()



#get input
input_data = get_single_data('att48.txt')

#create graph data-structures
(g, g_inv, optimal, n, m) = make_graph(input_data)

#get upper bound from heuristics
(visited, upper_bound) = myNN.myNN(g)

initial_upper_bound = upper_bound

#initialize the lp
tsp_lp = initialize_tsp_lp(g, g_inv, optimal, n, m)



x_best = np.zeros(m)

for i in range(len(visited) - 1):
    index = g[visited[i]][visited[i+1]][1]
    x_best[index] = 1


#this queue stores the upper and lower bounds of each variable. 
subprob_queue = deque([[[]]])
branch_choice_list = []
obj = np.inf
sub_lp_parking = []
fractional_parking = -1
nodes_visited = []
constraint_numbers = []
    
while True:
    sub_lp = subprob_queue.popleft()
    nodes_visited.append([sub_lp])

    """
    We apply the constraints from sub_lp to tsp_lp,
    Solve the subproblem,
    Look for cuts and apply them,
    Solve again,
    Clear out the cuts from the model.
    """
    #retrieve list of variables in the model
    x = tsp_lp.getVars()
    for i in range(m):
        x[i].ub = 1.0 
        x[i].lb = 0.0 
    tsp_lp.update()
    #bring in the 0-1 constraints.
    #these are actually introduced as boundaries rather than constraints.
    #they are stored in sub_lp, and here, we introduce them to tsp_lp.
    
    lb_for_sub_lp = np.zeros(m)
    ub_for_sub_lp = np.zeros(m)

    for constraint in sub_lp:
        if isinstance(constraint, float):
    		continue
        elif len(constraint) == 0:
            continue
        #constraint[0] is the index, constraint[1] is the prescribed value
        #we want to create two vectors and then update the model
        if constraint[1] == 0:
            x[constraint[0]].ub = 0.0
        elif constraint[1] == 1:
            x[constraint[0]].lb = 1.0

    
    tsp_lp.update()

    lboundlist = []
    lboundlist.extend(x[i].lb for i in range(m))
    uboundlist = []
    uboundlist.extend(x[i].ub for i in range(m))
     
       
    tsp_lp.optimize()

    sub_lp[0] = tsp_lp.ObjVal    

    if(len(sub_lp) > 1):
        x_try = tsp_lp.X
        x_try = [xi - 0.5 for xi in x_try]
        x_try = np.abs(x_try)
        fractional = sum(x_try)
        #the lower this sum, the more attractive the subproblem is.

        if sub_lp[-1][1] == 0:
            sub_lp_parking = sub_lp
            fractional_parking = fractional
        else:
            if(fractional_parking != -1) and len(sub_lp) == len(sub_lp_parking):
                if(fractional >= fractional_parking):
                    sub_lp_leaving = sub_lp
                    subprob_queue.append(sub_lp_leaving)
                    sub_lp = sub_lp_parking
                else:
                    subprob_queue.append(sub_lp_parking)
                fractional_parking = -1
                sub_lp_parking = []


    if(tsp_lp.Status == 3):
        node_status = 'pruneA'
    else:
        #tsp_lp is now an updated lp at our node that we're considering.
        #we want its objective value.
        obj_val = tsp_lp.ObjVal
        constraint_binder = []
        node_status = ' '

        if obj_val > upper_bound: 
            node_status = 'pruneB'
        else:
            cut_counter = 0
            while True:
                #try to find a cut from the cut factory 
                cut_edges = mySECs.SECs(tsp_lp.X, g_inv)
                if cut_edges:
                    new_constr = tsp_lp.addConstr(
                        sum(1*x[i] for i in cut_edges) >= 2
                    )
                    constraint_binder.append(new_constr)
                    tsp_lp.update()
                    tsp_lp.optimize()
                    cut_counter += 1
                    if cut_counter >= 50:
                        break
                    if(tsp_lp.Status == 3):
                        node_status = 'pruneC'
                        break
                    else:
                        obj_val = tsp_lp.ObjVal
                        if obj_val > upper_bound:
                            node_status = 'pruneD'
                            break
                else:
                    node_status += 'feasible'
                    break

            if node_status.startswith('prune') == False:
                intstatus = 0
                zero_test = np.zeros(len(tsp_lp.X))
                ones_test = np.ones(len(tsp_lp.X))
                intstatus = np.zeros(len(tsp_lp.X))

                intstatus = np.isclose(tsp_lp.X, zero_test) + np.isclose(tsp_lp.X, ones_test)
                if sum(intstatus) == len(tsp_lp.X):
                    node_status += 'integral'
                else:
                    node_status += 'branch'


            # for i in range(len(tsp_lp.X)):
            #     intstatus += (np.isclose([tsp_lp.X[i]], [0])[0] + np.isclose([tsp_lp.X[i]], [1])[0])
            # if intstatus == len(tsp_lp.X):
            #     node_status = 'integral'
            # else 
            #     node_status = 'branch'

    if(tsp_lp.Status != 3):        
        x = tsp_lp.X
        obj = tsp_lp.ObjVal

    constraint_numbers.append(len(constraint_binder))
    tsp_lp.remove(constraint_binder)
    tsp_lp.update()

    """
    The node_status is one of the following:
    prune:  this means the problem is infeasible or the objective is greater than the upper bound.
    integral: we have a candidate for the solution to the TSP. Set the global upper bound and the x that we got.
    branch: we have a non-integral solution with no subtours. Add two subproblems to the queue.
    """

    print('node done. status: {}'.format(node_status))
    if ('integral' in node_status and 'feasible' in node_status) or 'prune' in node_status:
        fractional_parking = -1
        sub_lp_parking = []
    if 'integral' in node_status and 'feasible' in node_status:
        if obj <= upper_bound:
            upper_bound = obj   
            x_best = x
            print obj
            print sub_lp
            for j in range(len(subprob_queue)):
                if subprob_queue[j][0] != None:
                    if subprob_queue[j][0] > upper_bound:
                        print('removing :{}'.format(j))
                        subprob_queue.remove(j)
                        print('removed subprob {}'.format(subprob_queue[j]))

    elif 'branch' in node_status:
        print('hello')
        #Put two subproblems in the queue. We use the index that's closest to 0.5. 
        #We check the list to see if the next branch point has already been decided.
        if len(sub_lp) - 1 < len(branch_choice_list):
            index_for_split = branch_choice_list[len(sub_lp) - 1]
        #If not, we use the index that's closest to 0.5, and add it to the list. 
        else:
            arr = [xi - 0.5 for xi in x]
            arr = np.abs(arr)
            #ensure that an index already on the list (already used) will not be used again.
            for b in branch_choice_list:
                arr[b] += 1
            index_for_split = arr.argmin()
            branch_choice_list.append(index_for_split)
        zero_branch = sub_lp + [[index_for_split, 0]] 
        one_branch = sub_lp + [[index_for_split, 1]] 
        print zero_branch
        print one_branch
        #Each new subprob will have all the boundary constraints of its parent, plus the new boundary constraint.
        subprob_queue.appendleft(one_branch)
        subprob_queue.appendleft(zero_branch)
        



    if not subprob_queue:
        break


# print outputs

print ('Solution: {}'.format(x_best))
print ('Initial UB: {}'.format(initial_upper_bound))
print ('Weight of the cycle: {}'.format(upper_bound))
print ('Nodes visited: {}'.format(nodes_visited))
end = time.time()
print ('Constraints Added: {}'.format(constraint_numbers))
print('\nTime = {} seconds'.format(end - start))