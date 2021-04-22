import collections
 
def ReverseAdjList(adjList):
	reverse_adj_list = {vertex: [] for vertex in adjList}
	for src, dests in adjList.items():
		for d in dests:
			reverse_adj_list[d].append(src)
	return reverse_adj_list
 
def ReferenceCountingTopologicalSort(adjList):
	topological_order = []
	# Build Initial Dep Counts
	dep_counts = {}
	# Use dequeue so both append (add to end) and popleft (remove from front)
	# can be efficient.
	queue = collections.deque()
	for vertex, edges in adjList.items():
		dep_counts[vertex] = len(edges)
		if dep_counts[vertex] == 0:
			queue.append(vertex)
	# Process nodes that reach 0 deps in a loop until everything's done
	reverse_adj_list = ReverseAdjList(adjList)
	while queue:
		curr_vertex = queue.popleft()
		topological_order.append(curr_vertex)
		for vertex in reverse_adj_list[curr_vertex]:
			dep_counts[vertex] -= 1
			if dep_counts[vertex] == 0:
				queue.append(vertex)
	# If we're out of nodes with 0 deps, but not all nodes have been processed.
	if len(topological_order) != len(adjList):
		raise ValueError("adjList was a graph with a cycle")
	return topological_order
 
def DfsToplogicalSort(adjList):
	topological_order = []
	visited = set()
	# Set of what is on the dfs stack. Set for efficient membership check to
	# find back edges.
	dfs_stack_set = set()
 
	# Using a local function to avoid passing as many variables around
	def dfs(vertex):
		if vertex in dfs_stack_set:
			raise ValueError("adjList was a graph with a cycle")
		if vertex in visited:
			return
		visited.add(vertex)
		dfs_stack_set.add(vertex)
		for dest in adjList[vertex]:
			dfs(dest)
		topological_order.append(vertex)
		# Since we're backtracking we won't have this node on the stack anymore
		dfs_stack_set.remove(vertex)
 
	for starting_vertex in adjList:
		# If this is a node already covered by a prior DFS (started at a
		# different node), the visited set will cause it to be skipped.
		dfs(starting_vertex)
 
	return topological_order
 
adjList1 = {
	"A": ["B", "C"],
	"B": ["D"],
	"C": ["D"],
	"D": ["E"],
	"E": [],
}
adjList2 = {
	"A": ["B", "C", "E"],
	"B": ["D", "C"],
	"C": ["D"],
	"D": ["E", "F"],
	"E": [],
	"F": [],
	"G": ["F"],
	"H": [],
}
adjList3 = {
	"A": ["B", "C"],
	"B": ["C"],
	# Circular
	"C": ["A"],
	"D": ["E"],
	"E": [],
}
# Different methods may produce different topological sorts if there is more
# than one valid sort.
print(ReferenceCountingTopologicalSort(adjList1))
print(DfsToplogicalSort(adjList1))
print(ReferenceCountingTopologicalSort(adjList2))
print(DfsToplogicalSort(adjList2))
try:
	ans = ReferenceCountingTopologicalSort(adjList3)
except ValueError as e:
	print(e)
try:
	ans = DfsToplogicalSort(adjList3)
except ValueError as e:
	print(e)
