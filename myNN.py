import my_utils
import numpy as np

# ww17
# 04/11/2018

def myNN(data):
	'''
	Implementation of nearest neighbor heuristics: https://web.tuke.sk/fei-cit/butka/hop/htsp.pdf 
	Input:
		data: a list of lists. 
			data[0] gives [#nodes #edges]
			data[1:] gives [node1 node2 weight]
			data[-1] potentially gives the minimum weight
	Output:
		visited: a list of visited nodes that form the tour.
		optimal: intger. Total weight of the tour.
	'''
	
	graph = my_utils.make_graph(data)[0]
	n = data[0][0] # number of nodes
	m = data[0][1] # number of edges

	nodes = range(n)
	visited = []

	# randomly select a start node
	start_node = np.random.randint(n)
	total_weight = 0

	# start visiting. Only stop when all nodes are visited 
	current_node = start_node
	visited.append(current_node)
	while set(visited) != set(nodes):
		neighbors = graph[current_node]

		# search for the nearest unvisited neighbor nn 
		w = float("inf")
		for v in neighbors:
			if v not in visited:
				if neighbors[v] < w:
					nn = v
					w = neighbors[nn]

		# update visited and total weight of the tour
		visited.append(nn)
		total_weight += w 
		current_node = nn

	# return to start node
	visited.append(start_node)
	total_weight += graph[nn][start_node]

	return visited, total_weight


# Test
all_data = my_utils.get_all_data()

data_0 = all_data['ulysses22.txt']
print 'test0:', myNN(data_0)

data_1 = all_data['st70.txt']
print 'test1:', myNN(data_1)