# i and j are the true variables of recursion, grid is constant, cache
# just gives access to the cache
def MaxPathHelper(x, y, grid, cache):
	# Part 1: check if in cache, and if so return right away
	# For non-Python folks: (x, y) constructs a 2-tuple with x and y.
	if (x, y) in cache:
		return cache[(x,y)]
 
	# Part 2: If we get here because answer's not in cache, compute answer.
 
	# The way grid is stored, can see that grid[y][x] refers
	# to value at position (x, y). We already checked grid is not size 0.
	maxY = len(grid) - 1
	maxX = len(grid[0]) - 1
 
	# Check base cases.
	if y == maxY and x == maxX:
		retVal = grid[y][x]
	elif y > maxY or x > maxX:
		# Give value of negative inf so we never make a choice to go out of bounds.
		# An alternative approach is to exclude the invalid choice from the recursion.
		retVal = float("-inf")
	# General case
	else:
		# In this case, we get the value from the current cell plus the better
		# of the optimal values for each of the two ways to continue collecting
		# coins (go right or go down)
		retVal = grid[y][x] + max(
			MaxPathHelper(x+1, y, grid, cache), MaxPathHelper(x, y+1, grid, cache))
 
	# Part 3: Store answer to cache
	cache[(x,y)] = retVal
 
	# Part 4: return as usual
	return retVal
 
 
 
def GetMaxPathInGridTopDown(grid):
	# Preliminary check so we don't have to worry about it in recursive helper.
	if len(grid) == 0 or len(grid[0]) == 0:
		return 0
	# Ideally we should check all rows are same size. I'll just skip it here.
 
	# We want the answer when we start from top left. Initialize cache with
	# empty map.
	return MaxPathHelper(0, 0, grid, dict())
 
 
def GetMaxPathInGridBottomUp(grid):
	if len(grid) == 0 or len(grid[0]) == 0:
		return 0
	# Ideally we should check all rows are same size. I'll just skip it here
 
	# The way grid is stored, can see that grid[y][x] refers
	# to value at position (x, y). We already checked grid is not size 0.
	maxY = len(grid) - 1
	maxX = len(grid[0]) - 1
 
	cache = dict()
 
	# Sometimes it's more convenient to fill base cases before going into loops.
	# Sometimes you'll see it done here. I think for this problem, more convenient
	# to just do it inside loop.
 
	# Process rows (y) bottom to top, then within each row, process x right to left.
	# This is a valid processing order since every position's calculation depends
	# on the positions below and to the right of it.
	# For non-Python folks, this is just a backwards counting loop from maxY+1 to 0 inclusive.
	# We need to start at maxY + 1 because maxY will reference maxY + 1 and only
	# maxY + 1 is a base case.
	for y in range(maxY + 1, -1, -1):
		for x in range (maxX + 1, -1, -1):
			# Note this logic is very similar to top-down solution: not a coincidence!
			# Top-down and bottom-up are doing the same thing, just a matter of whether
			# we explicitly supply the subproblem evaluation order or let recursion do it!
			# Check base cases.
			if y == maxY and x == maxX:
				solutionForPosition = grid[y][x]
			elif y > maxY or x > maxX:
				# Give value of negative inf so we never make a choice to go out of bounds.
				# An alternative approach is to exclude the invalid choice from the below general case.
				solutionForPosition = float("-inf")
			# General case
			else:
				solutionForPosition = grid[y][x] + max(cache[(x+1, y)], cache[(x, y+1)])
 
			cache[(x, y)] = solutionForPosition
 
	# The solution for the top left corner is the final answer.
	return cache[(0, 0)]
 
 
# Best path has value 38: 4 -> 12 -> 6 -> 10 -> 2 -> 4
print (GetMaxPathInGridTopDown(
	[[4, 5, 6, 2],
	[12, 2, 9, 1],
	[6, 10, 2, 4]]
))
print (GetMaxPathInGridBottomUp(
	[[4, 5, 6, 2],
	[12, 2, 9, 1],
	[6, 10, 2, 4]]
))
 
# Best path has value 55: 4 -> 12 -> 2 -> 9 -> 10 -> 11 -> 3 -> 4
print (GetMaxPathInGridTopDown(
	[[4, 5, 6, 2],
	[12, 2, 9, 1],
	[3, 6, 10, 4],
	[7, 10, 11, 3],
	[6, 10, 2, 4]]
))
print (GetMaxPathInGridBottomUp(
	[[4, 5, 6, 2],
	[12, 2, 9, 1],
	[3, 6, 10, 4],
	[7, 10, 11, 3],
	[6, 10, 2, 4]]
))
