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



#initialize the lp
tsp_lp = initialize_tsp_lp(g, g_inv, optimal, n, m)



x_best = np.zeros(m)



for i in range(len(visited) - 1):
	index = g[visited[i]][visited[i+1]][1]
	x_best[index] = 1





#this queue stores the upper and lower bounds of each variable. 
subprob_queue = deque([[]])
obj = np.inf
	
while True:
	sub_lp = subprob_queue.popleft()
	print sub_lp
	
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
	
	lb_for_sub_lp = np.zeros(m)
	ub_for_sub_lp = np.zeros(m)


	#print sub_lp
	if sub_lp:
		id = sub_lp[0]
		if sub_lp[1] == 0:
			x[id].ub = 0
		elif sub_lp[1] == 1:
			x[id].lb = 1

	# for constraint in sub_lp:
	# 	if len(constraint) == 0:
	# 		break
	# 	#constraint[0] is the index, constraint[1] is the prescribed value
	# 	#we want to create two vectors and then update the model
	# 	if constraint[1] == 0:       	
	# 		x[constraint[0]].ub = 0
	# 	elif constraint[1] == 1:
	# 		x[constraint[0]].lb = 1


	# for v in tsp_lp.getVars()[lb_for_sub_lp]:
	# 	v.lb = 1
	# for v in tsp_lp.getVars()[ub_for_sub_lp]:
	# 	v.ub = 0

	# tsp_lp.setAttr("lb", lb_for_sub_lp)
	# tsp_lp.setAttr("ub", ub_for_sub_lp)
	
	
	
	tsp_lp.update()
	tsp_lp.optimize()


	

	#tsp_lp is now an updated lp at our node that we're considering.
	#we want its objective value.

	status = tsp_lp.status

	if status == GRB.Status.OPTIMAL:
		obj_val = tsp_lp.ObjVal
		intstatus = 0
		zero_test = np.zeros(len(tsp_lp.X))
		ones_test = np.ones(len(tsp_lp.X))
		intstatus = np.zeros(len(tsp_lp.X))

		intstatus = np.isclose(tsp_lp.X, zero_test) + np.isclose(tsp_lp.X, ones_test)
		if sum(intstatus) == len(tsp_lp.X):
			node_status = 'integral'
		else:
			node_status = 'branch'
	elif status == GRB.Status.INFEASIBLE:
		node_status = 'prune'

	constraint_binder = []


	if obj_val >= upper_bound: 
		node_status = 'prune'
	# elif node_status == 'integral':
	# 	upper_bound = obj_val
	# 	x_best = tsp_lp.X
	else:
		#previous_cut = []
		while True:
			#try to find a cut from the cut factory 
			print('status', tsp_lp.status)

			if node_status == 'prune':
				break 
			cut_edges = mySECs.SECs(tsp_lp.X, g_inv)
			#print('cut_edges:', cut_edges) 
			#print('x:', tsp_lp.X)
			if cut_edges:
				new_constr = tsp_lp.addConstr(
					sum(1*x[i] for i in cut_edges) >= 2
				)
				# if set(previous_cut) == set(cut_edges):
				# 	print('again')
				# 	break
				constraint_binder.append(new_constr)
				tsp_lp.update()
				tsp_lp.optimize()
				previous_cut = cut_edges
			else:
				break
		
		intstatus = 0
		zero_test = np.zeros(len(tsp_lp.X))
		ones_test = np.ones(len(tsp_lp.X))
		intstatus = np.zeros(len(tsp_lp.X))

		intstatus = np.isclose(tsp_lp.X, zero_test) + np.isclose(tsp_lp.X, ones_test)
		if sum(intstatus) == len(tsp_lp.X):
			node_status = 'integral'
		else:
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

		if node_status == 'integral':
			if obj <= upper_bound:
				upper_bound = obj   
				x_best = x
		elif node_status == 'branch':
			#Put two subproblems in the queue. We use the index that's closest to 0.5. 
			
			arr = np.abs([num - 0.5 for num in x])
			index_for_split = arr.argmin()
			zero_branch = [index_for_split, 0] 
			one_branch = [index_for_split, 1] 
			#Each new subprob will have all the boundary constraints of its parent, plus the new boundary constraint.
			subprob_queue.append(zero_branch)
			subprob_queue.append(one_branch)

		
	if not subprob_queue:
		break

	#print('x',len(x))

# TODO: print outputs

print x_best
print obj

end = time.time()
print('\nTime = {} seconds'.format(end - start))