class Pos:
    def __init__(self, y: int, x: int) -> None:
        self.y = y
        self.x = x


# graphic print of board, feel free to use, or not
def print_board(array):
    print("------------")
    print(
        "{:02d}".format(array[0]),
        "|",
        "{:02d}".format(array[1]),
        "|",
        "{:02d}".format(array[2]),
    )
    print("------------")

    print(
        "{:02d}".format(array[3]),
        "|",
        "{:02d}".format(array[4]),
        "|",
        "{:02d}".format(array[5]),
    )
    print("------------")

    print(
        "{:02d}".format(array[6]),
        "|",
        "{:02d}".format(array[7]),
        "|",
        "{:02d}".format(array[8]),
    )
    print("------------")


def arrayToBoard(array: list) -> list:
    board = []
    for i in range(3):
        board.append([])
        for j in range(3):
            board[i].append(array[3 * i + j])
    return board


def boardToArray(board: list) -> list:
    array = []
    for row in board:
        array += row
    return array


def hForNode(board: list, pos: Pos) -> int:
    num = board[pos.y][pos.x]
    if num == 0:
        return 0
    y = ((num - 1) - ((num - 1) % 3)) // 3
    x = (num - 1) % 3
    goal = Pos(y, x)
    dy = abs(pos.y - goal.y)
    dx = abs(pos.x - goal.x)
    return dy + dx


def h(board: list) -> int:
    cost = 0
    for y in range(3):
        for x in range(3):
            cost += hForNode(board, Pos(y, x))
    return cost


def copyBoard(board: list) -> list:
    array = boardToArray(board)
    return arrayToBoard(array)


def findZero(board: list) -> Pos:
    for y in range(3):
        for x in range(3):
            if board[y][x] == 0:
                return Pos(y, x)
    return Pos(0, 0)


def genChildBoard(board: list, zeroPos: Pos, child: Pos) -> list:
    copy = copyBoard(board)
    copy[zeroPos.y][zeroPos.x] = copy[child.y][child.x]
    copy[child.y][child.x] = 0
    return copy


def findChildren(board: list, zeroPos: Pos) -> list:
    childPos_sequence = []
    if zeroPos.x < 2:
        childPos_sequence.append((Pos(zeroPos.y, zeroPos.x + 1), 1))
    if zeroPos.y < 2:
        childPos_sequence.append((Pos(zeroPos.y + 1, zeroPos.x), 2))
    if zeroPos.x > 0:
        childPos_sequence.append((Pos(zeroPos.y, zeroPos.x - 1), 3))
    if zeroPos.y > 0:
        childPos_sequence.append((Pos(zeroPos.y - 1, zeroPos.x), 0))

    childBoard_sequence = []
    for child in childPos_sequence:
        childBoard = genChildBoard(board, zeroPos, child[0])
        childBoard_sequence.append((childBoard, child[1]))
    return childBoard_sequence


def findMinIndex(frontier: list, frontierfN: list) -> int:
    maxIndex = 0
    maxFrontier = []
    minfN = min(frontierfN)
    for i in range(len(frontierfN)):
        if frontierfN[i] == minfN:
            if boardToArray(frontier[i]) > maxFrontier:
                maxFrontier = boardToArray(frontier[i])
                maxIndex = i
    return maxIndex


def checkSeen(board: list, seen: list):
    array = boardToArray(board)
    if array in seen:
        return True
    else:
        return False


def findDupIndexes(frontier: list, current: list) -> list:
    dupIndexes = []
    for i in range(len(frontier)):
        if frontier[i] == current:
            dupIndexes.append(i)
    return dupIndexes


# astar search
def astar(array: list):
    board = arrayToBoard(array)

    # returning
    expansions = 0
    depth = 0
    path = None

    # tracking our nodes
    seen = []
    frontier = []
    heuristicList = []
    depthList = []
    pathList = []

    frontier.append(board)
    heuristicList.append(h(board))
    depthList.append(0)
    pathList.append([])

    while frontier:
        minFIndex = findMinIndex(frontier, heuristicList)
        currBoard = frontier.pop(minFIndex)
        currH = heuristicList.pop(minFIndex)
        currDepth = depthList.pop(minFIndex)
        currPath = pathList.pop(minFIndex)
        # remove duplicate boards
        dupIndexes = findDupIndexes(frontier, currBoard)

        removed = 0
        for dupIndex in dupIndexes:
            frontier.pop(dupIndex - removed)
            heuristicList.pop(dupIndex - removed)
            depthList.pop(dupIndex - removed)
            pathList.pop(dupIndex - removed)
            removed += 1

        # visited already?
        if checkSeen(currBoard, seen):
            continue

        expansions += 1

        # goal?
        if h(currBoard) == 0:
            depth = currDepth
            path = currPath
            break

        children = findChildren(currBoard, findZero(currBoard))
        childH = currDepth + 1
        for child in children:
            childPath = currPath.copy()
            childPath.append(child[1])
            if checkSeen(child[0], seen):
                continue
            frontier.append(child[0])
            heuristicList.append(childH + h(child[0]))
            depthList.append(childH)
            pathList.append(childPath)

        seen.append(boardToArray(currBoard))
    return depth, expansions, path
