class bcolors:
	RED    = "\x1b[31m"
	GRAY  = "\x1b[30m"
	NORMAL = "\x1b[0m"
	YELLOW = "\x1b[33m"

def init_sudoku():
	return [[0 for x in range(9)] for x in range(9)]

def set_sudoku(sudoku, data):
	for y in range(9):
		for x in range(9):
			sudoku[y][x]=int(data[y*9+x])

def can_yx_be_z(sudoku, y, x, z):
	for i in range(9):
		if (sudoku[y][i]==z):
			return False
		if (sudoku[i][x]==z):
			return False
		if(sudoku[int(y/3)*3+int(i/3)][int(x/3)*3+i%3]==z): 
			return False
	return True

def print_sudoku(sudoku):
	for y in range(9):
		v = ""
		for x in range(9):
			if sudoku[y][x] == 0:
				v += bcolors.GRAY
			else:
				v += bcolors.YELLOW
			v += str(sudoku[y][x])
		print(v)