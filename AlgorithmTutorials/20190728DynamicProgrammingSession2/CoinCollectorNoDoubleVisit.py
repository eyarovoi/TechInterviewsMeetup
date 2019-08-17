# This is one of the problems discussed during the Dynamic Programming Part 2 class
# (Part 3 on Youtube). Channel: https://www.youtube.com/channel/UCDHkPnEcrEf3B9-isB4jXIw
#
# Given an MxN grid of values, if you start at the upper left corner and need to get to
# the lower right corner and you can go right, down, *and up* (this is where the problem
# differs from the standard problem), what is the maximum value you can collect? In this
# version, you are *not allowed* to visit the same cell twice.

# Enum
LEFT = 0
DOWN = 1
UP = 2

# x and y are the current x,y position and d is the direction we just came from.
def MaxPathHelper(x, y, d, grid, cache):
	# For non-Python folks: (x, y, d) constructs a 3-tuple with x and y.
	if (x, y, d) in cache:
		return cache[(x, y, d)]
 
	# The way grid is stored, can see that grid[y][x] refers
	# to value at position (x, y). We already checked grid is not size 0.
	maxY = len(grid) - 1
	maxX = len(grid[0]) - 1
 
	# Check base cases.
	if y == maxY and x == maxX:
		retVal = grid[y][x]
	elif y > maxY or x > maxX or y < 0 or x < 0:
		# Give value of negative inf so we never make a choice to go out of bounds.
		# An alternative approach is to exclude the invalid choice from the recursion.
		retVal = float("-inf")
	# General case
	else:
		# In this case, we get the better of the optimal values for each of the
		# decisions we can make. What decisions are available to us depends on
		# which direction we came from. We also add the value at the current
		# grid position.
		
		# If came from above, can now move lower or to the right.
		if d == UP:
			retVal = grid[y][x] + max(
				MaxPathHelper(x, y+1, UP, grid, cache),
				MaxPathHelper(x+1, y, LEFT, grid, cache)
			)
		# If came from below, can now move higher, or to the right.
		elif d == DOWN:
			retVal = grid[y][x] + max(
				MaxPathHelper(x, y-1, DOWN, grid, cache),
				MaxPathHelper(x+1, y, LEFT, grid, cache)
			)
		# If came from left, can now move higher, lower, or to the right.
		elif d == LEFT:
			retVal = grid[y][x] + max(
				MaxPathHelper(x, y+1, UP, grid, cache),
				MaxPathHelper(x, y-1, DOWN, grid, cache),
				MaxPathHelper(x+1, y, LEFT, grid, cache)
			)
 
	cache[(x, y, d)] = retVal
	return retVal

 
def GetMaxPathInGridTopDown(grid):
	# Preliminary check so we don't have to worry about it in recursive helper.
	if len(grid) == 0 or len(grid[0]) == 0:
		return 0
	# Ideally we should check all rows are same size. I'll just skip it here.
 
	# We want the answer when we start from top left. Initialize cache with
	# empty map. At first we are free to choose any movement so pass LEFT
	# as the direction to indicate this.
	return MaxPathHelper(0, 0, LEFT, grid, dict())
 
 
def GetMaxPathInGridBottomUp(grid):
	if len(grid) == 0 or len(grid[0]) == 0:
		return 0
	# Ideally we should check all rows are same size. I'll just skip it here
 
	# The way grid is stored, can see that grid[y][x] refers
	# to value at position (x, y). We already checked grid is not size 0.
	maxY = len(grid) - 1
	maxX = len(grid[0]) - 1
 
	cache = dict()
	
	# Now init the base out-of-bounds cases.
	for x in range(maxX+2):
		for d in range(3):
			cache[(x, maxY+1, d)] = float("-inf")
			cache[(x, -1, d)] = float("-inf")
	for y in range(maxY+2):
		for d in range(3):
			cache[(maxX+1, y, d)] = float("-inf")
			cache[(-1, y, d)] = float("-inf")
	# Init the "we reached the final destination" base case.
	for d in range(3):
		cache[(maxX, maxY, d)] = grid[maxY][maxX]
 
	# Process columns right to left, as explained in the class. It is because
	# F(x, ...) can depend on higher values of x's but not on lower x's.
	# Within each column, process UP, DOWN, and only then LEFT directions. Each
	# direction has its own necessary sweep order in terms of y, depending
	# on which direction it is.
	
	# For non-Python folks, this is just a backwards counting loop from maxX to 0 inclusive.
	for x in range(maxX, -1, -1):
		# If we are on rightmost x column, don't compute values for the
		# right lower corner, as that was a base case.
		yRange = (maxY-1) if (x == maxX) else maxY
		
		# do UP states. Sweep from greatest to least y here, since lower y
		# depend on higher values.
		for y in range (yRange, -1, -1):
			# Just the UP rule from the top-down solution. Here we are splitting
			# up the logic of the top-down solution a little since we need
			# different order of iteration depending on direction.
			cache[(x, y, UP)] = grid[y][x] + max(cache[(x, y+1, UP)], cache[(x+1, y, LEFT)])
			
		# do DOWN states. Sweep from least to greatest y here since higher y
		# depend on lower y.
		for y in range (yRange + 1):
			cache[(x, y, DOWN)] = grid[y][x] + max(cache[(x, y-1, DOWN)], cache[(x+1, y, LEFT)])

		# do LEFT states. Sweep order can be anything here as LEFT states
		# don't depend on other LEFT states (except for the x+1 ones). But
		# they do depend on UP and DOWN which is why we had to do those first.
		for y in range (yRange + 1):
			cache[(x, y, LEFT)] = grid[y][x] + max(
				cache[(x, y-1, DOWN)], 
				cache[(x, y+1, UP)],
				cache[(x+1, y, LEFT)]
			)
			
 
	# The solution for the top left corner in LEFT direction is the final answer.
	return cache[(0, 0, LEFT)]
 
 
# Best path is to collect everything and is sum of matrix: 78
print (GetMaxPathInGridTopDown(
	[[4, 5, 6, 2, 5],
	[12, 2, 9, 1, 5],
	[6, 10, 2, 4, 5]]
))
print (GetMaxPathInGridBottomUp(
	[[4, 5, 6, 2, 5],
	[12, 2, 9, 1, 5],
	[6, 10, 2, 4, 5]]
))

# Best path is 5 -> 11 -> 0 -> 13 -> -5 -> 25 -> -5 -> 10 -> 10 = 64
print (GetMaxPathInGridTopDown(
	[[5, -100, -5, 25],
	[11,   0,   13, -5],
	[10, -100,  5,  10],
	[10, -100,  8,  10]]
))
# Best path is 5 -> 11 -> 0 -> 13 -> -5 -> 25 -> -5 -> 10 -> 10 = 64
print (GetMaxPathInGridBottomUp(
	[[5, -100, -5, 25],
	[11,   0,   13, -5],
	[10, -100,  5,  10],
	[10, -100,  8,  10]]
))
