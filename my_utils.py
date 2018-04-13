import os
from collections import defaultdict

# ww17
# 04/11/2018


"""
Instructions:

script_dir is the dicrectory of this script (my_utils.py). It is assumed that this scrpit is stored in a folder A 
which contains another folder B that contains the input txt files (for me, the folder B is called 'TSP')  

For any input txt file, it has the following format:

n m //# of nodes and # of edges
end1 end2 weight // for edge(0)
...
end1 end2 weight // for edge(m-1)

There is a also potentially a number at the last line of the file indicating the opitmal value of the TSP tour.

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
		fname: string. Name of the file, e.g. 'st70.txt'
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
			data[-1] potentially gives the minimum weight (if provided)
	Output: 
		graph: defaultdict.
			Represnet the graph in the following way: graph[u][v] = (weight, edge_index), where weight is the weight
			of edge (u,v), and edge_index is the index of edge (u,v) according to the input txt file.  
			By setting the default factory, if the edege (u,v) does not exist, graph[u][v] returns float("inf").
		optimal: float.
			the minimum weight provided by the input file
	'''
	edges = defaultdict(lambda:float("inf"))
	graph = defaultdict(lambda:edges)
	optimal = None

	edge_index = 0
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
			graph[u][v] = item[2], edge_index
			graph[v][u] = item[2], edge_index
		edge_index += 1

	return graph, optimal


# Testing get_single_data and make_graph
myTest_1 = get_single_data('st70.txt')
print myTest_1
test_graph_1 = make_graph(myTest_1)[0]

print("weight of edge (3,1):", test_graph_1[3][1][1])
print("index of edge (3,1):", test_graph_1[3][1][0])




