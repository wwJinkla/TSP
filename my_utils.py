import os
from collections import defaultdict
from gurobipy import *


# ww17
# 04/11/2018


"""
Instructions:

script_dir is the dicrectory of this script (my_utils.py). It is assumed that this scrpit is stored in a folder A 
which contains another folder B that contains the input txt files (for me, the folder B is called 'TSP')  

"""

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, 'TSP')     # change 'TSP' into your own data directory 


def get_all_data():
	'''
	This function gets all the data file in data_dir.
	Input: 
		none.
	Output: 
		all_files: dictionary, with fname as key, and the data entry (lists of lists) as values.
	'''
	os.chdir(data_dir)

	all_files = {}
	for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
	    for fname in filenames:
	    	if fname[-3:] == "txt":
				print "Reading file: " + fname
	    	current_txt = []
	    	f = open(fname,"r")
	    	f1 = f.readlines()
	    	for line in f1:
	    		line = line.split()
	    		if line:
	    			line = [int(i) for i in line]
	    			current_txt.append(line)
	    	all_files[fname] = current_txt

	return all_files


def get_single_data(fname):
	'''
	This function gets the entries in the file fname
	Input: 
		fname:  string. Name of the file, e.g. 'st70.txt'
	Output: 
		data: a list of lists. 
			data[0] gives [#nodes #edges]
			data[1:] gives [node1 node2 weight]
			data[-1] potentially gives the minimum weight
	'''
	print "Reading file: " + fname
	data = []
	f = open(os.path.join(data_dir, fname),"r")
	f1 = f.readlines()
	for line in f1:
		line = line.split()
		if line:
			line = [int(i) for i in line]
			data.append(line)
	return data



# # Testing get_all_data
# input_data = get_all_data()
# print('we have the following input files', input_data.keys())


# make graph using defaultdict. In fact we could simply use dictionary.
# The usage of defaultdict is redundant, since for our problem the graph is a complete. 
def make_graph(data):
	'''
	This function makes a graph out of the input data.
	Input: 
		data: a list of lists. 
			data[0] gives [#nodes #edges]
			data[1:] gives [node1 node2 weight]
			data[-1] potentially gives the minimum weight if provided in the file
	Output: 
		graph: defaultdict.
			Represnet the graph in the following way: {u {v : weight}}. By setting the default factory, if the edege
			(u,v) does not exist, graph[u][v] returns float("inf").
		optimal: float.
			the minimum weight provided by the input file
	'''
	edges = defaultdict(lambda:float("inf"))
	graph = defaultdict(lambda:edges)
	optimal = None

	for item in data:
		if len(item) ==1:
			optimal = item[0] # minimum weight
		if len(item) == 2:
			n = item[0]  # number of nodes
			m = item[1]  # number of edges
		if len(item) ==3:
			u = item[0]  # first node
			if u not in graph:
				graph[u] = defaultdict(lambda:float("inf"))
			v = item[1] # second node
			if v not in graph:
				graph[v] = defaultdict(lambda:float("inf"))
			# symmetric TSP
			graph[u][v] = item[2]
			graph[v][u] = item[2]

	return graph, optimal

# # Testing get_single_data and make_graph
# myTest_1 = get_single_data('st70.txt')
# print(myTest_1)
# test_graph_1 = make_graph(myTest_1)
# print(test_graph_1[0][58][64])
# print(test_graph_1[1])



#Solve an LP relaxation of TSP
#Input: 
#		x0: vector of all edges in graph, with 1s corresponding to visited edges, 0s elsewhere
#		weights: costs associated with each edge 
#Output:
#		x_star: 
def initialize_tsp_lp(x0, weights):


try:

	#Create LP model
	tsp_lp = Model("tsp_lp")

	n = sum(x0) * 2 # number of nodes in tour
	m = sum(x0) #number of edges in tour
	x_star = np.zeros(x0.shape) #initialize solution

	x = tsp_lp.addVars(n, m, vtype=GRB.BINARY)

	tsp_lp.setObjective()

	m.addConstraint()

	m.optimize()

	if tsp_lp.status == GRB.Status.INF_OR_UNBD:
	    # Turn presolve off to determine whether model is infeasible
	    # or unbounded
	    tsp_lp.setParam(GRB.Param.Presolve, 0)
	    tsp_lp.optimize()

	if tsp_lp.status == GRB.Status.OPTIMAL:
	    print('Optimal objective: %g' % model.objVal)
	    model.write('model.sol')
	    exit(0)
	elif tsp_lpq.status != GRB.Status.INFEASIBLE:
	    print('Optimization was stopped with status %d' % model.status)
	    exit(0)


	print x

# 	variables = tsp_lp.addVars(x0, )

# 	#
# 	for i in range(I):
#     	for k in range(len(rangevalue)):
#         	t = E[i]
#         	y[i+1, rangevalue[k] - t] = m.addVar(vtype=GRB.BINARY, name="y%s" % str([i+1, rangevalue[k] - t]))
# m.update()        
#y       



























