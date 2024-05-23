QUEENS = 10

class Pos:
	def __init__(self, y, x) -> None:
		self.y = y
		self.x = x

def init_board():
	return [[0 for x in range(0,10)] for x in range(0,10)]

def findQueen(board, x):
	for y in range(QUEENS):
		if board[y][x] == 1:
			return Pos(y,x)

def moveQueenTo(board, y, x):
	currPos = findQueen(board, x)
	board[currPos.y][currPos.x] = 0
	board[y][x] = 1

def posAttackCount(board, pos):
	count = 0

	# row
	for i in range(QUEENS):
		if pos.x != i:
			count += board[pos.y][i]

	# diagonal down-right (from origin)
	moveBy = min(pos.y, pos.x)
	startPos = Pos(pos.y - moveBy, pos.x - moveBy)
	for i in range(QUEENS - max(startPos.y, startPos.x)):
		if startPos.y + i != pos.y:
			count += board[startPos.y + i][startPos.x + i]

	# diagonal up-right (from origin)
	moveBy = min((QUEENS - 1) - pos.y, pos.x)
	startPos = Pos(pos.y + moveBy, pos.x - moveBy)
	for i in range(QUEENS - max((QUEENS - 1) - startPos.y, startPos.x)):
		if startPos.y - i != pos.y:
			count += board[startPos.y - i][startPos.x + i]
	return count

def totalAttackCount(board):
	count = 0
	for i in range(QUEENS):
		queenPos = findQueen(board, i)
		count += posAttackCount(board, queenPos)
	return count

def findMinForCol(board, col):
	attacks = []
	for y in range(QUEENS):
		attacks.append(board[y][col])
	minCount = min(attacks)
	minIndex = attacks.index(minCount)
	return (minCount, minIndex)

def findMin(board):
	minCount = board[0][0]
	minIndex = (0,0)
	for i in range(QUEENS):
		count = findMinForCol(board, i)
		if count[0] < minCount:
			minCount = count[0]
			minIndex = (count[1], i)
	return (minCount, minIndex)

def gradient_search(board):
	done = False
	currAttackCount = totalAttackCount(board)
	attackCountBoard = init_board()
	
	while not done:
		for x in range(QUEENS):
			queenPos = findQueen(board, x)
			for y in range(QUEENS):
				if board[y][x] == 1:
					attackCountBoard[y][x] = currAttackCount
				if board[y][x] != 1:
					moveQueenTo(board, y, x)
					attackCountBoard[y][x] = totalAttackCount(board)
					moveQueenTo(board, queenPos.y, queenPos.x)
		nextMin = findMin(attackCountBoard)

		if nextMin[0] < currAttackCount:
			moveQueenTo(board, nextMin[1][0], nextMin[1][1])
			currAttackCount = nextMin[0]
		else:
			done = True
	return currAttackCount == 0
