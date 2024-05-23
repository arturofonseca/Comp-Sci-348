import common

# helpful, but not needed


class variables:
    counter = 0


def domainCopy(domain: list) -> list:
    """Returns a copy of the domain"""
    copy = []
    for row in domain:
        rowCopy = []
        for node in row:
            rowCopy.append(node[:])
        copy.append(rowCopy)
    return copy[:]


def checkComplete(sudoku: list) -> bool:
    """Returns true if the given board is full and doesn't violate any constraints"""
    for y in range(9):
        for x in range(9):
            value = sudoku[y][x]
            if value == 0:
                return False
            sudoku[y][x] = 0
            valid = common.can_yx_be_z(sudoku, y, x, value)
            sudoku[y][x] = value
            if not valid:
                return False
    return True


def initDomain() -> list:
    """Returns the domain of empty sudoku board"""
    domain = []
    for y in range(9):
        row = []
        for x in range(9):
            row.append(list(range(1, 10)))
        domain.append(row)
    return domain


def calculateNextDomain(domain: list, y: int, x: int, value: int) -> list:
    """Returns future domain if i were to be in sudoku(y,x)"""
    for i in range(9):
        # remove all values from row
        nodeDomAlongRow = domain[y][i]
        nodeDomAlongCol = domain[i][x]
        nodeDomAlongGroup = domain[int(y/3)*3+int(i/3)][int(x/3)*3+i % 3]
        if i != x and value in nodeDomAlongRow:
            nodeDomAlongRow.remove(value)
        if i != y and value in nodeDomAlongCol:
            nodeDomAlongCol.remove(value)
        if (int(y/3)*3+int(i/3), int(x/3)*3+i % 3) != (y, x) and \
                value in nodeDomAlongGroup:
            nodeDomAlongGroup.remove(value)
    return domain


def checkDomainEmpty(domain: list) -> bool:
    """Returns true if the given domain has a node with an empty domain"""
    for row in domain:
        for node in row:
            if len(node) == 0:
                return True
    return False


def recursiveBacktracking(sudoku: list) -> bool:
    """Recursive function returning true if next empty value in board
    can be chosen given that the current node is a certain value"""
    variables.counter += 1
    if checkComplete(sudoku):
        return True
    for y in range(9):
        for x in range(9):
            value = sudoku[y][x]

            # if value is not zero, we stop
            if value != 0:
                continue

            # assigning each empty spot a value 1-9
            for i in range(1, 10):
                if common.can_yx_be_z(sudoku, y, x, i):
                    sudoku[y][x] = i

                    # jump to next node
                    done = recursiveBacktracking(sudoku)
                    if done:
                        # if next node possible, we continue to next node
                        return True
                    else:
                        # if next node can't have any value 1-9 due to
                        # current node having value i, then current changes to i+1
                        sudoku[y][x] = 0
            # if no value can be assigned to the current cell, then False
            return False


def recursiveForwardChecking(sudoku: list, domain) -> bool:
    """Recursive function returning true if next empty value in board
    can be chosen given that the current node is a certain value"""
    variables.counter += 1

    if domain == None:
        init = initDomain()
        for y in range(9):
            for x in range(9):
                if sudoku[y][x] == 0:
                    continue
                init = calculateNextDomain(init, y, x, sudoku[y][x])
        # domain = get_domain(sudoku)
        domain = init

    if checkComplete(sudoku):
        return True
    for y in range(9):
        for x in range(9):
            value = sudoku[y][x]

            # if value is not zero, we stop
            if value != 0:
                continue

            # assigning each empty spot a value 1-9
            for i in range(1, 10):
                if common.can_yx_be_z(sudoku, y, x, i):
                    copy = domainCopy(domain)
                    nextDomain = calculateNextDomain(copy, y, x, i)
                    nextDomainEmpty = checkDomainEmpty(nextDomain)

                    # stop on fail
                    if not nextDomainEmpty:
                        sudoku[y][x] = i
                        result = recursiveForwardChecking(sudoku, nextDomain)
                        if result:
                            return True
                        # if next node not possible, then change current node to i+1 or change previous node to i+1...
                        sudoku[y][x] = 0
            # if no value can be assigned to current cell, then False
            return False


def sudoku_backtracking(sudoku: list) -> int:
    """Takes a sudoku board and solves it using backtracking"""
    variables.counter = 0
    # put your code here
    recursiveBacktracking(sudoku)
    return variables.counter


def sudoku_forwardchecking(sudoku: list) -> int:
    """Takes a sudoku board and solves it using forward checking"""
    variables.counter = 0
    # put your code here
    recursiveForwardChecking(sudoku, None)
    return variables.counter
