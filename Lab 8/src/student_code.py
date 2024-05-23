import common

def calcMaxDotProductIndex(data: list, weightsList: list) -> int:
	"""Return max dot product's index"""
	maxValue, maxIndex = float('-inf'), float('-inf')
	for i in range(common.constants.NUM_CLASSES):
		dotProduct = weightsList[i][0]*data[0] + weightsList[i][1]*data[1]
		if dotProduct > maxValue:
			maxValue = dotProduct
			maxIndex = i
	return maxIndex

def calcDotProduct(data: list, weights: list) -> int:
	"""Calculate dot product of feature and weight vectors"""
	if weights[0]*data[0] + weights[1]*data[1] + weights[2] >= 0:
		return 1
	else:
		return 0

def part_one_classifier(data_train: list, data_test: list) -> None:
	"""The function receives:
	- bidimensional structure data_train of size TRAINING_SIZE x 3. Every row contains a value for X in position 0, a value for for Y in position 1 and a value for the class in position 2.
	- bidimensional structure data_test of size TEST_SIZE x 3. Every row contains a value for X in position 0, a value for for Y in position 1 and an empty space for the class in position 2.\n
	The function must modify:
	- The third column of the “data_test ” structure, by entering the right class of each element. Valid values for classes are 0 or 1."""
	weights = [0 for i in range(3)]
	rate = 0.01
	correct = 0
    
	while correct/common.constants.TRAINING_SIZE <= 0.95:
		correct = 0
		for data in data_train:
			x, y, actual = data
			output = calcDotProduct(data, weights)
			if output == actual:
				correct += 1
			else:
				sign = -(output * 2) + 1
				weights[0] += rate * sign * x
				weights[1] += rate * sign * y
				weights[2] += rate * sign * 1 # bias of 1

	for i in range(common.constants.TEST_SIZE):
		data_test[i][2] = calcDotProduct(data_test[i], weights)

def part_two_classifier(data_train: list, data_test: list) -> None:
	"""The function receives:
	- bidimensional structure data_train of size TRAINING_SIZE x 3. Every row contains a value for X in position 0, a value for for Y in position 1 and a value for the class in position 2.
	- bidimensional structure data_test of size TEST_SIZE x 3. Every row contains a value for X in position 0, a value for for Y in position 1 and an empty space for the class in position 2.\n
	The function must modify:
	- The third column of the “data_test ” structure, by entering the right class of each element. Valid values for classes are 0 to 9."""
	weightsList = [[0 for i in range(2)] for i in range(10)]
	rate = 0.01
	correct = 0

	while correct/common.constants.TRAINING_SIZE <= 0.95:
		correct = 0
		for data in data_train:
			x, y, actual = data
			output = calcMaxDotProductIndex(data, weightsList)
			if output == actual:
				correct += 1
			else:
				weightsList[int(actual)][0] += rate * x
				weightsList[int(actual)][1] += rate * y
				weightsList[output][0] += -rate * x
				weightsList[output][1] += -rate * y

	for i in range(common.constants.TEST_SIZE):
		data_test[i][2] = calcMaxDotProductIndex(data_test[i], weightsList)