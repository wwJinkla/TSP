import my_utils
import numpy as np

# ww17
# Last updated 04/15/2018

def myNN(graph):
	"""
	Implementation of nearest neighbor heuristics: https://web.tuke.sk/fei-cit/butka/hop/htsp.pdf 
	Input:
		graoh: a dictionary of dictionary. 
			graph[u][v][0] = weight of (u,v)
			graph[u][v][1] = edge index of (u,v)
	Output:
		visited: a list.
			A list of visited nodes that form the tour.
		total_weight: intger. 
			Total weight of the tour.
	"""
	
	#graph = my_utils.make_graph(data)[0]
	n = len(graph.keys()) # number of nodes
	#m = data[0][1] # number of edges

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
				if neighbors[v][0] < w:
					nn = v
					w = neighbors[nn][0]

		# update visited and total weight of the tour
		visited.append(nn)
		total_weight += w 
		current_node = nn

	# return to start node
	visited.append(start_node)
	total_weight += graph[nn][start_node][0]

	return visited, total_weight


# Test
all_data = my_utils.get_all_data()

data_0 = all_data['ulysses22.txt']
graph_0 = my_utils.make_graph(data_0)[0]
print 'test0:', myNN(graph_0)

data_1 = all_data['st70.txt']
graph_1 = my_utils.make_graph(data_1)[0]
print 'test1:', myNN(graph_1)