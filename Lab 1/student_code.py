import common

class Pos:
	def __init__(self, y, x) -> None:
		self.y = y
		self.x = x

def findStartIndex(map):
	for y in range(common.constants.MAP_HEIGHT):
		for x in range(common.constants.MAP_WIDTH):
			if map[y][x] == 2:
				return Pos(y,x)
	return None

def findNeighbors(map, pos):
	neighbors = []
	if pos.x != common.constants.MAP_WIDTH-1:
		if map[pos.y][pos.x+1] == 0 or map[pos.y][pos.x+1] == 3:
			neighbors.append(Pos(pos.y,pos.x+1))
	if pos.y != common.constants.MAP_HEIGHT-1:
		if map[pos.y+1][pos.x] == 0 or map[pos.y+1][pos.x] == 3:
			neighbors.append(Pos(pos.y+1,pos.x))
	if pos.x != 0:
		if map[pos.y][pos.x-1] == 0 or map[pos.y][pos.x-1] == 3:
			neighbors.append(Pos(pos.y,pos.x-1))
	if pos.y != 0:
		if map[pos.y-1][pos.x] == 0 or map[pos.y-1][pos.x] == 3:
			neighbors.append(Pos(pos.y-1,pos.x))
	return neighbors

stack = []
def df_search(map):

	found = False

	# if this is the first time being run, start with 2
	if findStartIndex(map) != None:
		start = findStartIndex(map)
		map[start.y][start.x] = 4
		stack.append(start)
		curr = start

	# otherwise, we work with first value of stack
	elif len(stack) > 0:
		curr = stack[-1]
		map[curr.y][curr.x] = 4

	else:
		return found

	neighbors = findNeighbors(map, curr)
	if len(neighbors) > 0:
		stack.append(neighbors[0])
		if map[neighbors[0].y][neighbors[0].x] == 3:
			for pos in stack:
				map[pos.y][pos.x] = 5
			found = True
			stack.clear()
			return found
	else:
		stack.pop()

	return df_search(map)

queue = []
def bf_search(map):

	found = False

	# if this is the first time being run, start with 2
	startIndex = findStartIndex(map)
	if startIndex != None:
		curr = [startIndex,[startIndex]]
		path = curr[1]
		map[curr[0].y][curr[0].x] = 4

	# otherwise, we work with first value of stack
	elif len(queue) > 0:
		curr = queue.pop(0)
		path = curr[1]
		if map[curr[0].y][curr[0].x] == 3:
			for pos in path:
				map[pos.y][pos.x] = 5
			queue.clear()
			found = True
			return found
		map[curr[0].y][curr[0].x] = 4

	else:
		return found

	neighbors = findNeighbors(map, curr[0])
	for neighbor in neighbors:
		queue.append((neighbor, path + [neighbor]))

	return bf_search(map)