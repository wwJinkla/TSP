import os
from collections import defaultdict
import numpy as np
from gurobipy import *
# ww17
# Last updated: 04/15/2018


"""
Instructions:

script_dir is the dicrectory of this script (my_utils.py). It is assumed that this scrpit is stored in a folder A 
which contains another folder B that contains the input txt files (for me, the folder B is called 'TSP')  

For any input txt file, it has the following format:

n m // # of nodes and # of edges
end1 end2 weight // for edge(0)
...
end1 end2 weight // for edge(m-1)

There is a also potentially a number at the last line of the file indicating the opitmal value of the TSP tour.

"""

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, 'TSP')     # change 'TSP' into your own data directory 


def get_all_data():
	"""
	This function gets all the data file in data_dir.
	Input: 
		none.
	Output: 
		all_files: dictionary, with fname as key, and the data entry (lists of lists) as values.
	"""
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
	"""
	This function gets the entries in the file fname
	Input: 
		fname: string. 
			Name of the file, e.g. 'st70.txt'
	Output: 
		data: a list of lists. 
			data[0] gives [#nodes #edges]
			data[1:] gives [node1 node2 weight]
			data[-1] potentially gives the minimum weight
	"""
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




def make_graph(data):
	"""
	This function makes a graph out of the input data. It gives two different representations of the graph.
	Input: 
		data: a list of lists. 
			data[0] gives [#nodes #edges]
			data[1:] gives [node1 node2 weight]
			data[-1] potentially gives the minimum weight (if provided)
	Output: 
		graph: a dictionary.
			Represents the graph by graph[u][v] = (weight, edge_index)
		graph_inv: a dictionary.
			Represents the graph by graph_inv[edge_index] = (weight, (u,v)).
		optimal: int.
			the minimum weight provided by the input file
	"""

	graph = {}
	graph_inv = {}
	optimal = None

	edge_index = -1
	for item in data:
		if len(item) ==1:
			optimal = item[0] # minimum weight
		if len(item) == 2:
			n = item[0]  # number of nodes
			m = item[1]  # number of edges
		if len(item) ==3:
			u = item[0]  # first node
			if u not in graph:
				graph[u] = {}
			v = item[1] # second node
			if v not in graph:
				graph[v] = {}
			# symmetric TSP graph
			weight = item[2]
			graph[u][v] = weight, edge_index
			graph[v][u] = weight, edge_index
			graph_inv[edge_index] = weight, (u,v)
		edge_index += 1

	return graph, graph_inv, optimal, n, m


# # Testing get_single_data and make_graph
# myTest_1 = get_single_data('WeiTest.txt')
# print myTest_1
# test_graph_1 = make_graph(myTest_1)[0]
# test_graph_inv_1 = make_graph(myTest_1)[1]

# print("weight of edge (0,2):", test_graph_1[0][2][0])
# print("index of edge (0,2):", test_graph_1[0][2][1])

# print("weight of edge 1:", test_graph_inv_1[1][0])
# print("nodes of edge 1:", test_graph_inv_1[1][1])


def vector2graph(g_inv,x):
	"""
	Convert a vector of weights into a new graph.
	Input: 
		g_inv: a dictionary of dictionary. 
			The global graph given in the inverse form. For each edge index i, 
			graph[i] = (weight, (u,v)), where (u,v) corresponds to the edge(i).
		x: a list. 
			The indices i of x correspond to the indices of the edges in g, and x[i] gives the weight that
			we want to set up for edge(i) in the new graph.
	Output:
		new_graph: a dictionary of dictionary. The new graph according to x.
	"""
	new_graph ={}

	for i in range(len(x)):
		node1 = g_inv[i][1][0]
		if node1 not in new_graph:
			new_graph[node1] = {}
		node2 = g_inv[i][1][1]
		if node2 not in new_graph:
			new_graph[node2] = {}
		new_graph[node1][node2] = x[i], i
		new_graph[node2][node1] = x[i], i

	return new_graph

# test_x_1 = [1.0/2, 0, 1.0/2, 0, 1.0/2, 1]
# print vector2graph(test_graph_inv_1,test_x_1)



def initialize_tsp_lp(graph, graph_inv, optimal, n, m):
	#Solve an LP relaxation of TSP
	#Input: 
	#		graph
	#Output:
	#		x_star: 

	#Create LP model
	tsp_lp = Model("tsp_lp")

	c_min = -1 #minimal cost associated wit this LP relaxation

	#x_star = np.zeros(m) #initialize solution

	# n = graph[3] #Number of nodes in graph
	x = tsp_lp.addVars(m, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS) #, name="x")
	#x_reference  = x.getVarByName("x")


	for u in range(0, n):
		constr_edges = []
		for v in range (0, n):
			twople_w_index = None
			if u != v:      
				twople_w_index = graph[u][v]
			if twople_w_index:
				constr_edges.append(twople_w_index[1])
		tsp_lp.addConstr( sum(1*x[i] for i in constr_edges) == 2)
     
	# m = graph[4] #Number of edges in graph
	
	weights = graph_inv.values()
	weights = [x[0] for x in weights]

	tsp_lp.update()	


	# for edge in graph_inv:
	# 	weights[edge] = graph_inv[edge][0]
	tsp_lp.setObjective(np.dot(tsp_lp.getVars(), np.transpose(weights)))
	#tsp_lp.setObjective(tsp_lp.x.prod(weights), GRB.MINIMIZE)
	tsp_lp.write('model.lp')

	tsp_lp.update()
	
	return tsp_lp
