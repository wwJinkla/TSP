import my_utils
from myNN import myNN
import numpy as np

# ww17
# Last updated: 04/15/2018
# This implementation of generating subtour elimations constaints (in cut-set form) is inspired 
# by https://fktpm.ru/file/204-stoer-wagner-a-simple-min-cut-algorithm.pdf


# Get the test graph 
all_data = my_utils.get_all_data()
data_0 = all_data['MinCutTest.txt']
graph_0 = my_utils.make_graph(data_0)[0]
print("test graph came from the paper",  graph_0)
# print 'test0:', myNN(data_0)



def SECs(x,G_inv):
	"""
	Generate subtour elimination constraints.
	Input: 
		x: a list. I
			ndex i of x correspons to index of the edge. x[i] gives the weight on edge(i).
		G_inv: a dictionary.
			Represents the graph by G_inv[edge_index] = (weight, (u,v)).
	"""

	# make the induced graph according to weights given by vector x
	inducedg = my_utils.vector2graph(G_inv,x)
	
	# find the minimum cut on the induced graph
	a = np.random.randint(len(x))
	min_cut, min_w = MinCut(inducedg,a)

	SECs = []

	# Generate SECs if the weight of the min cut is smaller than 2 
	if min_w < 2:
		for u in min_cut:
			for v in inducedg:
				if v not in min_cut:
					SECs.append(inducedg[u][v][1])

	return SECs

def MinCutPhase(G,a):
	"""
	Performed the so called maximum adjacency search
	Input: 
		G: a dictionary of dictionary. G represents the graph by G[u][v] = (weight, edge_index)
		a: int. A node.
	Output:
		G: the graph after performing MinCutPhase
		w: int. The weight of the cut.
		cut: a list. It represents the nodes being cut from the rest of the graph

	"""
	A = [a]
	V = G.keys()

	flag = 0
	while flag == 0:
		# find the mostly connected vertex to A
		v = mostlyConnected(G,A)
		A.append(v)
		if set(A) == set(V):
			flag = 1


	# cut the last added node from the rest of the graph. Note that this node could be either an integer representing
	# a single node, or it could be a frozenset that represents a set of nodes.
	cut_node = A[-1]

	# compute the cut weight
	w = 0
	for n in G[cut_node]:
		w += G[cut_node][n][0]

	# make the cut
	if type(cut_node) == int:
		cut = [cut_node]
	if type(cut_node) == frozenset:
		cut = list(cut_node)

	# merge last two vertices
	G = mergeVertices(G, A[-1], A[-2])
	return G, w, cut

# # Unit test for MinCutPhase
# phase1 = MinCutPhase(graph_0, 2)
# print("After MinCutPhase 1", phase1)
# phase2 = MinCutPhase(phase1[0],2)
# print("After MinCutPhase 2", phase2)
# phase3 = MinCutPhase(phase2[0],2)
# print("After MinCutPhase 3", phase3)


def mostlyConnected(G, A):
	"""
	Compute the mostly connected vertex mc_v in G/A to A
	Input: 
		G: a dictionary of dictionary. 
			G represents the graph by G[u][v] = (weight, edge_index)
		A: a list of int. 
			Each item represents a node in set A.
	Output:
		mc_v. int. 
			Mostly connected vertex.

	"""

	sum_weight = 0
	mc_v = None

	# search for the mostly connected node in G/A to A
	for v in G:
		w = 0
		if v not in A:
			for u in A:
				if u in G[v]:
					w += G[u][v][0]
		if w > sum_weight:
			sum_weight = w
			mc_v = v

	return mc_v

# # Unit test for mostlyConnected
# A1 = [2]
# print mostlyConnected(graph_0,A1)


def mergeVertices(G,u,v):
	"""
	Merge vertices u and v in graph G.
	Input: 
		G: a dictionary of dictionary. 
			G represents the graph by G[u][v] = (weight, edge_index)
		u,v: could be int(a single node), or frozenset(several nodes merged into one). 
			Nodes in G.
	Output:
		G: a dictionary of dictionary. 
			graph after merging u and v.
	"""

	# Remeber the neighbors of u and v, along with the information about the edges. 
	u_neighbors = G[u].copy()	# e.g. G[u][n] = (w, idx), where w is the weight of (u,n), and idx is the edge index of (u,n)
	v_neighbors = G[v].copy()	# Note that we takes shallow copy, becuase G will be modified (merging nodes)

	#print("u_neighbors", u_neighbors)
	#print("v_neighbors", v_neighbors)

	# find out the common neighbors of u and v
	common_neighbors = [n for n in u_neighbors.keys() if n in v_neighbors.keys()]
	#print("common_neighbors", common_neighbors)
	
	# delete u,v as neighbors of other nodes
	del u_neighbors[v]	# we do not want to iterate over u and v
	del v_neighbors[u]
	for node in u_neighbors:
		del G[node][u]
	for node in v_neighbors:
		del G[node][v]

	# delete u,v themselves		
	del G[u]
	del G[v]
	# print("after deletion", G)

	# convert u or v into frozenset if u or v is integer
	if type(u) == int:
		u = frozenset([u])

	if type(v) == int:
		v = frozenset([v])

	# create new nodes
	uv = u.union(v)
	G[uv] = {}

	# create new edges
	for n in common_neighbors:
		G[uv][n] = u_neighbors[n][0] + v_neighbors[n][0], None
		G[n][uv] = u_neighbors[n][0] + v_neighbors[n][0], None

	for node in u_neighbors:
		if node not in common_neighbors:
			G[node][uv] = u_neighbors[node]
			G[uv][node] = u_neighbors[node]
	for node in v_neighbors:
		if node not in common_neighbors:
			G[node][uv] = v_neighbors[node]
			G[uv][node] = v_neighbors[node]

	return G

# # Unit test for mergeVertices
# graph_1 = mergeVertices(graph_0,1,5)
# print('merging 1 and 5', graph_1)
# print('merging 7 and 8', mergeVertices(graph_1,7,8))


def MinCut(G,a):
	"""
	Input: 
		G: a dictionary of dictionary. 
			G represents the graph by G[u][v] = (weight, edge_index)
		a: int. 
			A node.
	Output:
		min_cut: a list of integers. 
			Contains a list of nodes that are cut from the graph by the minimum cut.
		min_w: float or integer, depending on the weight of the input graph. 
			Weight of the minimum cut.
	"""
	min_cut = []
	min_w = float('inf')

	# make a shallow copy of G so that G does not change
	GG = G.copy()

	# perform MinCutPhase
	flag = 0
	while flag == 0:
		GG, w, cut = MinCutPhase(GG,a)
		if w < min_w:
			min_cut = cut
			min_w = w

		if len(GG) <= 1:
			flag = 1

	return min_cut, min_w

# Unit test for MinCut
print MinCut(graph_0,2)