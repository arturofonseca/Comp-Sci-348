import common

def nextTurn(turn):
	if turn == common.constants.X:
		return common.constants.O
	if turn == common.constants.O:
		return common.constants.X

def checkTie(board):
	return not 0 in board

def terminalValue(board, turn):
	status = common.game_status(board)
	if status == turn:
		return 1
	elif status == nextTurn(turn):
		return -1
	else:
		return 0

def maxValue(board, player, turn, a, b):
	# check if we're in a terminal state
	won = terminalValue(board, player)
	if won or checkTie(board):
		return won
	
	next = nextTurn(turn)
	v = float(('-inf'))
	emptySpaces = [i for i, space in enumerate(board) if space == common.constants.NONE]
	for space in emptySpaces:
		copy = board[:]
		copy[space] = turn
		v = max(v, minValue(copy, player, next, a, b))

		if not a and not b:
			continue

		if v >= b:
			return v
		a = max(a, v)

	return v

def minValue(board, player, turn, a, b):
	# check if we're in a terminal state
	won = terminalValue(board, player)
	if won or checkTie(board):
		return won

	next = nextTurn(turn)
	v = float(('inf'))
	emptySpaces = [i for i, space in enumerate(board) if space == common.constants.NONE]
	for space in emptySpaces:
		copy = board[:]
		copy[space] = turn
		v = min(v, maxValue(copy, player, next, a, b))
		
		if not a and not b:
			continue

		if v <= a: return v
		b = min(b, v)

	return v

def minmax_tictactoe(board, turn):
	#put your code here:
	#it must return common.constants.X(1), common.constants.O(2) or common.constants.NONE(0) for tie.
	#use the function common.game_status(board), to evaluate a board
	#it returns common.constants.X(1) if X wins, common.constants.O(2) if O wins or common.constants.NONE(0) if tie or game is not finished
	#the program will keep track of the number of boards evaluated
	#result = common.game_status(board);
	player = turn

	a, b = None, None
	won = maxValue(board, player, turn, a, b)

	if won == 1:
		return player
	if won == -1:
		return nextTurn(player)
	if won == 0:
		return common.constants.NONE

def abprun_tictactoe(board, turn):
	#put your code here:
	#it must return common.constants.X(1), common.constants.O(2) or common.constants.NONE(0) for tie.
	#use the function common.game_status(board), to evaluate a board
	#it returns common.constants.X(1) if X wins, common.constants.O(2) if O wins or common.constants.NONE(0) if tie or game is not finished
	#the program will keep track of the number of boards evaluated
	#result = common.game_status(board);
	player = turn

	a, b = float('-inf'), float('inf')
	won = maxValue(board, player, turn, a, b)

	if won == 1:
		return player
	if won == -1:
		return nextTurn(player)
	if won == 0:
		return common.constants.NONE