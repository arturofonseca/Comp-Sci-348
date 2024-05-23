import common

def setMap(map: list, data: list) -> None:
	"""Update map with data"""
	for y in range(6):
		for x in range(6):
			map[y][x] = data[y][x]

def findStartingPositions(map: list, policies: list, values: list,
	     delivery_fee: float, battery_drop_cost: float, dronerepair_cost: float, discount: float) -> list:
	"""Returns starting, ending, and rival positions"""
	init = [None, None, []]
	for y in range(6):
		for x in range (6):
			if map[y][x] == common.constants.PIZZA:
				init[0] = (y, x)
			elif map[y][x] == common.constants.CUSTOMER:
				init[1] = (y, x)
			elif map[y][x] == common.constants.RIVAL:
				init[2].append((y, x))
	return init

def calcNextPos(pos: tuple, direction: common.constants) -> tuple:
	"""Given a current position and a direction to go in, return the position we'll end up in"""
	y, x = pos
	if direction == common.constants.SOUTH:
		if y == 5: return (y, x)
		else: return (y + 1, x)
	if direction == common.constants.WEST:
		if x == 0: return (y, x)
		else: return (y, x - 1)
	if direction == common.constants.NORTH:
		if y == 0: return (y, x)
		else: return (y - 1, x)
	if direction == common.constants.EAST:
		if x == 5: return (y, x)
		else: return (y, x + 1)

def calcQForPos(values: list, battery_drop_cost: float, discount: float, pos: tuple, action: common.constants) -> float:
	"""Expected utility starting out having taken action from pos and thereafter acting optimally"""
	
	# propulsion off
	if action in list(range(1, 5)):

		# find all possible pos to end up in from action
		if action != 1: leftPos = calcNextPos(pos, action - 1)
		else: leftPos = calcNextPos(pos, 4)
		forwardPos = calcNextPos(pos, action)
		if action != 4: rightPos = calcNextPos(pos, action + 1)
		else: rightPos = calcNextPos(pos, 1)

		# calc left, forward, anc right dir
		return \
		0.15 * (-battery_drop_cost + (discount * values[leftPos[0]][leftPos[1]])) + \
		0.70 * (-battery_drop_cost + (discount * values[forwardPos[0]][forwardPos[1]])) + \
		0.15 * (-battery_drop_cost + (discount * values[rightPos[0]][rightPos[1]]))
	
	# propulsion on
	if action in list(range(5, 9)):

		# find all possible pos to end up in from action
		if action != 5: leftPos = calcNextPos(pos, action-4 - 1)
		else: leftPos = calcNextPos(pos, 4)
		forwardPos = calcNextPos(pos, action-4)
		if action != 8: rightPos = calcNextPos(pos, action-4 + 1)
		else: rightPos = calcNextPos(pos, 1)
	
		# calc left, forward, anc right dir
		return \
		0.10 * (-2*battery_drop_cost + (discount * values[leftPos[0]][leftPos[1]])) + \
		0.80 * (-2*battery_drop_cost + (discount * values[forwardPos[0]][forwardPos[1]])) + \
		0.10 * (-2*battery_drop_cost + (discount * values[rightPos[0]][rightPos[1]]))

def calc_kPlus1_Values(values: list, policies: list, delivery_fee: float, battery_drop_cost: float,
		  dronerepair_cost: float, discount: float, end: tuple, rivalsPos: list) -> tuple:
	"""Returns 1) the values of the k+1-th step given the k-th step values
	and 2) the maximum difference between any two values of the k-th values list and k+1-th values list"""
	# to calculate biggest difference between curr values list and calculate values list
	differences = []

	nextValues = common.init_values()
	for y in range(6):
		for x in range(6):

			# if we're in one of the exit states, no calculations needed
			if (y, x) == end:
				nextValues[y][x] = delivery_fee
				differences.append(0)
				continue
			if (y, x) in rivalsPos:
				nextValues[y][x] = -dronerepair_cost
				differences.append(0)
				continue

			# otherwise, calculate next step
			qStates = []
			# for each action, calculate its q-value
			for action in list(range(1, 9)):
				qValue = calcQForPos(values, battery_drop_cost, discount, (y, x), action)
				qStates.append(qValue)
			# value of a state is the maximum of the q-states
			v = max(qStates)
			# update value of that state
			nextValues[y][x] = v
			# update policy of that state
			# qStates starts at index 0 and ends at 7, so add 1
			policies[y][x] = qStates.index(v) + 1
			# difference of this positions past value to calculated value
			differences.append(abs(v - values[y][x]))

	return (nextValues, max(differences))

def drone_flight_planner(map: list, policies: list, values: list,
			 delivery_fee: float, battery_drop_cost: float, dronerepair_cost: float, discount: float) -> float:
	"""Returns the value of the cell corresponding to the starting position of the drone and updates the optimal policy and values matrices"""
	
	# find the starting, goal, and rivals positions
	startingPos = findStartingPositions(map, policies, values, delivery_fee, battery_drop_cost, dronerepair_cost, discount)
	start, end, rivalsPos = startingPos

	# initialize difference for 0th step, undefined for -1th step
	difference = float('inf')
	# for k=0 step, values_{k=0} = values parameter
	values_k = values
	# while the difference of the next values list is not less than the margin, run another loop
	while difference > 0.001:
		# find the next values from current values and the biggest difference between the values
		values_kPlus1, maxDiff = calc_kPlus1_Values(values_k, policies, delivery_fee, battery_drop_cost, dronerepair_cost, discount, end, rivalsPos)
		# for next iteration, use calculated values as our k-th step to find k+1-th step
		values_k = values_kPlus1
		# update the difference
		difference = maxDiff

	# setting original value map to converged value map
	setMap(values, values_k)

	return values[start[0]][start[1]]