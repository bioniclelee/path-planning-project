import sys
import re
import heapq as hq
import math

rows = 0
cols = 0
board = []
pred = []
queue = []
isComplete = False
numNodesVisited = 0
goalList = []

def parseFile(file):
    global rows
    global cols
    global board

    with open(file) as f:
        lines = f.readlines()
    
    rows = int(lines[0].split(":")[1])
    cols = int(lines[1].split(":")[1])
    board = [[[" ", 1, False] for j in range(cols)] 
                        for i in range(rows)] # board print, path cost, visited status
    insertObstacles(lines)
    insertGoal(lines)
    lineNum = insertPathCost(lines)
    lineNum = insertEnemyPieces(lines, lineNum)
    lineNum = insertAllyPieces(lines, lineNum)

def insertGoal(lines):
    global board
    global goalList
    goals = lines[-1].rstrip("\n").split(":")[1].split(" ")
    for i in range(0, len(goals)):
        coord = coordStrToInt(goals[i])
        goalList.append(coord)
        board[coord[0]][coord[1]][0] = "G"

def insertAllyPieces(lines, lineNum):
    global board
    global start
    global queue
    numAllyPieces = 0
    for n in list(lines[lineNum][64:].rstrip("\n").replace(" ","")):
        numAllyPieces += int(n)
    lineNum += 2
    while lines[lineNum][0] == "[":
        rawEntry = lines[lineNum].rstrip("\n").replace("[","").replace("]","").split(",")
        start = coordStrToInt(rawEntry[1])
        if rawEntry[0] == "King": allyBoardInput = "P"
        if rawEntry[0] == "Queen":allyBoardInput = "I"
        if rawEntry[0] == "Bishop": allyBoardInput = "U"
        if rawEntry[0] == "Rook": allyBoardInput = "Y"
        if rawEntry[0] == "Knight": allyBoardInput = "T"
        board[start[0]][start[1]][0] = allyBoardInput
        lineNum += 1
    queue = []
    hq.heappush(queue, (getHeuristic(start), start))
    return lineNum

def insertEnemyPieces(lines, lineNum):
    global board
    numEnemyPieces = 0
    for n in list(lines[lineNum][66:].rstrip("\n").replace(" ","")):
        numEnemyPieces += int(n)
    lineNum += 2
    while lines[lineNum][0] == "[":
        rawEntry = lines[lineNum].rstrip("\n").replace("[","").replace("]","").split(",")
        coord = coordStrToInt(rawEntry[1])
        if rawEntry[0] == "King": 
            enemyBoardInput = "K"
            enemyKingThreat(coord)
        if rawEntry[0] == "Queen":
            enemyBoardInput = "Q"
            enemyQueenThreat(coord)
        if rawEntry[0] == "Bishop":
            enemyBoardInput = "B"
            enemyBishopThreat(coord)
        if rawEntry[0] == "Rook":
            enemyBoardInput = "R"
            enemyRookThreat(coord)
        if rawEntry[0] == "Knight":
            enemyBoardInput = "H"
            enemyKnightThreat(coord)
        board[coord[0]][coord[1]][0] = enemyBoardInput
        lineNum += 1
    return lineNum

def enemyKingThreat(pos):
    global board
    row = pos[0]
    col = pos[1]
    for i in range (-1, 2):
        for j in range (-1, 2):
            if 0 <= row + i < rows and 0 <= col + j < cols:
                board[row + i][col + j][0] = "X"

def enemyQueenThreat(pos):
    global board
    enemyRookThreat(pos)
    enemyBishopThreat(pos)

def enemyRookThreat(pos):
    global board
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and board[row - i][col][0] != "X":
        board[row - i][col][0] = "X"
        i += 1
    
    i = 1
    while 0 <= row + i < rows and board[row + i][col][0] != "X":
        board[row + i][col][0] = "X"
        i += 1

    i = 1
    while 0 <= col - i < cols and board[row][col - i][0] != "X":
        board[row][col - i][0] = "X"
        i += 1

    i = 1
    while 0 <= col + i < cols and board[row][col + i][0] != "X":
        board[row][col + i][0] = "X"
        i += 1

def enemyBishopThreat(pos):
    global board
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and 0 <= col - i < cols and board[row - i][col - i][0] != "X":
        board[row - i][col - i][0] = "X"
        i += 1

    i = 1
    while 0 <= row - i < rows and 0 <= col + i < cols and board[row - i][col + i][0] != "X":
        board[row - i][col + i][0] = "X"
        i += 1

    i = 1
    while 0 <= row + i < rows and 0 <= col - i < cols and board[row + i][col - i][0] != "X":
        board[row + i][col - i][0]= "X"
        i += 1

    i = 1
    while 0 <= row + i < rows and 0 <= col + i < cols and board[row + i][col + i][0] != "X":
        board[row + i][col + i][0] = "X"
        i += 1

def enemyKnightThreat(pos):
    global board
    row = pos[0]
    col = pos[1]

    for i in range (0, 2):
        coeff1 = (-1) ** i
        
        for j in range (0, 2):
            # vertical L-path
            coeff2 = (-1) ** j
            newRow = row + coeff1 * 2
            newCol = col + coeff2 * 1
            if 0 <=  newRow < rows and 0 <= newCol < cols and board[newRow][newCol][0] != "X":
                board[newRow][newCol][0] = "X"

            # horizontal L-path
            newRow = row + coeff1 * 1
            newCol = col + coeff2 * 2
            if 0 <=  newRow < rows and 0 <= newCol < cols and board[newRow][newCol][0] != "X":
                board[newRow][newCol][0] = "X"

def insertPathCost(lines):
    # print("insertPathCost")
    global board
    i = 5
    while lines[i][0] == "[":
        rawEntry = lines[i].rstrip("\n").replace("[","").replace("]","").split(",")
        coord = coordStrToInt(rawEntry[0])
        board[coord[0]][coord[1]][1] = int(rawEntry[1])
        i += 1
    return i

def insertObstacles(lines):
    global board
    numObstacles = int(lines[2].split(":")[1])
    obstacleList = lines[3].split(":")[1].rstrip("\n").split(" ")
    for i in range(0, numObstacles):
        coord = coordStrToInt(obstacleList[i])
        board[coord[0]][coord[1]][0] = "X"

def genAdjMatrix(pos):
    adjMatrix=[]
    for i in range (-1, 2):
        for j in range (-1, 2):
            coord = []
            coord.append(pos[0] + i) # row
            coord.append(pos[1] + j) # col
            if not (i == 0 and j == 0) and isValid(coord) and not isVisited(coord):
                adjMatrix.append(coord)
    return adjMatrix

def visitSquare(pos):
    global board
    global numNodesVisited
    board[pos[0]][pos[1]][2] = True
    numNodesVisited += 1

def movePiece(pos):
    global board
    board[pos[0]][pos[1]][0] = "O"

def coordStrToInt(str):
    coord = []
    newList = re.split("(\d+)", str)
    row = int(newList[1])
    col = asciiToInt(newList[0])
    coord.append(row)
    coord.append(col)
    return coord

def coordToStrIntTuple(coord):
    row = coord[0]
    col = coord[1]
    temp = []
    temp.append(intToAscii(col))
    temp.append(row)
    return tuple(temp)

def printBoard(board):
    rowRef = 0
    boardRowsRep = []
    for i in range (0, 2 * rows + 2):
        boardColsRep = []
        if (i%2 == 0):    
            for j in range (0, 4 + cols * 4):
                boardColsRep.append("-")            
        elif (i % 2 == 1 and i != 2 * rows + 1):
            boardColsRep.append(rowRef)
            for k in range (0, len(str(rows)) + 1
                                - len(str(rowRef))):
                boardColsRep.append(" ")
            boardColsRep.append("|")
            for j in range (0, cols):
                boardColsRep.append(" ")
                boardColsRep.append(
                    board[int((i-1)/2)][j][0])
                boardColsRep.append(" ")
                boardColsRep.append("|")
            rowRef += 1
        else:
            for k in range (0, len(str(rows)) + 1):
                boardColsRep.append(" ")
            boardColsRep.append("|")
            alphabet = 97
            for j in range (0, cols):
                boardColsRep.append(" ")
                boardColsRep.append("{}".format(chr(alphabet)))
                boardColsRep.append(" ")
                boardColsRep.append("|")
                alphabet += 1
        boardRowsRep.append(boardColsRep)
    for i in range (0, len(boardRowsRep)):
        row = boardRowsRep[i]
        for j in range (0, len(row)):
            print(row[j], end = "")
        print("")

def getPathCost(coord):
    global board
    return board[coord[0]][coord[1]][1]

def isValid (coord):
    row = coord[0]
    col = coord[1]
    if (0 <= row < rows and 0 <= col < cols):
            return isEmpty(coord) or isGoal(coord)

def isGoal(coord):
    return (board[coord[0]][coord[1]][0] == "G")

def isEmpty(coord):
    return (board[coord[0]][coord[1]][0] == " ")

def isObstacle(coord):
    return (board[coord[0]][coord[1]][0] == "X")

def isVisited(coord):
    return board[coord[0]][coord[1]][2]

def asciiToInt(c):
    return ord(c) - ord('a')

def intToAscii(n):
    return chr(n + ord('a'))

def getHeuristic(coord):
    global board
    global goalList
    heuristic = 0
    minVal = math.inf
    for goal in goalList:
        heuristic = abs(goal[0] - coord[0]) + abs(goal[1] - coord[1]) + ((goal[0] - coord[0]) ** 2 + (goal[1] - coord[1]) ** 2) ** 0.5
        # i = goal[0] - coord[0]
        # j = goal[1] - coord[1]
        # while i < goal[0] or j < goal[1]:
        #     heuristic += 1
        #     i += 1
        #     j += 1
        # if (i == goal[0]):
        #     heuristic += (goal[1] - j)
        # if (j == goal[1]):
        #     heuristic += (goal[0] - i)
        # heuristic = abs(goal[0] - coord[0]) + abs(goal[1] - coord[1])
        # min((abs(goal[0] - coord[0]), abs(goal[1] - coord[1])))
        # ((goal[0] - coord[0]) ** 2 + (goal[1] - coord[1]) ** 2) ** 0.5
        if heuristic < minVal:
            minVal = heuristic
    return minVal

def search():
    global queue
    global isComplete
    global pred

    cumulativeFCost = 0

    pred = [[-1 for j in range(cols)] 
                        for i in range(rows)]
    while queue:
        cumulativeFCost, posToSearch = hq.heappop(queue)
        cumulativeFCost -= getHeuristic(posToSearch)
        if isGoal(posToSearch):
            isComplete = True
            return posToSearch
        adjMat = genAdjMatrix(posToSearch)
        for i in range (0, len(adjMat)):
            if not isVisited(adjMat[i]):
                visitSquare(adjMat[i])
                pred[adjMat[i][0]][adjMat[i][1]] = posToSearch
                hq.heappush(queue, (getPathCost(adjMat[i]) + cumulativeFCost + getHeuristic(adjMat[i]), adjMat[i]))
    
    return None

def run_AStar():
    global pred
    global numNodesVisited

    parseFile(sys.argv[1])

    totPathCost = 0
    orderOfNodes = []
    pathToReturn = []
    crawl = search() # this should be the goal tile or blank
    if isComplete:
        while (crawl != -1):
            totPathCost += getPathCost(crawl)
            orderOfNodes.append(crawl)
            movePiece(crawl)
            if (pred[crawl[0]][crawl[1]] == -1):
                totPathCost -= getPathCost(crawl)
            crawl = pred[crawl[0]][crawl[1]]
        orderOfNodes = orderOfNodes[::-1]

        for i in range(0, len(orderOfNodes)-1):
            nodePair = []
            nodePair.append(coordToStrIntTuple(orderOfNodes[i]))
            nodePair.append(coordToStrIntTuple(orderOfNodes[i+1]))
            pathToReturn.append(nodePair)
    # printBoard(board)
    print(pathToReturn, numNodesVisited, totPathCost)
    return pathToReturn, numNodesVisited, totPathCost

if __name__ == "__main__":
    run_AStar()