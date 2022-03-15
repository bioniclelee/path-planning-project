import sys
import re
import heapq as hq
import math
import random
from copy import deepcopy
 
rows = 0
cols = 0
board = []
queue = []
piecePosList = []
pieceList = []
numFree = 0
numPieces = 0
 
class State:
    def __init__(self, board, numFree, pieceList):
        self.board = board
        self.numFree = numFree
        self.pieceList = pieceList

    def getScore(self):
        score = 0
        for i in range(0, rows):
            for j in range(0, cols):
                if self.board[i][j][0] == " ":
                    score += 1
        return score

    def __lt__(self, other):
        return self.getScore() < other.getScore()
 
    def __le__(self, other):
        return self.getScore() <= other.getScore()
 
def parseFile(file):
    global rows
    global cols
    global board
 
    with open(file) as f:
        lines = f.readlines()
    
    rows = int(lines[0].split(":")[1])
    cols = int(lines[1].split(":")[1])
    board = [[[" ",1, False] for j in range(cols)] 
                        for i in range(rows)] # board print, 1, explored status
    insertObstacles(lines)
    insertPieces(lines)
    
def insertPieces(lines):
    global board
    global pieceList
    global numPieces
    
    for n in list((lines[4].rstrip("\n").split(":"))[1].split(" ")):
        pieceList.append(int(n))
        numPieces += int(n)
    
    
def enemyKingThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    for i in range (-1, 2):
        for j in range (-1, 2):
            if 0 <= row + i < rows and 0 <= col + j < cols:
                threatList.append(rowColToCoord(row + i, col + j))
    threatList.remove(rowColToCoord(row, col))
    return threatList
 
def enemyQueenThreat(pos):
    return enemyRookThreat(pos) + enemyBishopThreat(pos)
 
def enemyRookThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and board[row - i][col][0] != "X":
        threatList.append(rowColToCoord(row - i, col))
        i += 1
    
    i = 1
    while 0 <= row + i < rows and board[row + i][col][0] != "X":
        threatList.append(rowColToCoord(row + i, col))
        i += 1
 
    i = 1
    while 0 <= col - i < cols and board[row][col - i][0] != "X":
        threatList.append(rowColToCoord(row, col - i))
        i += 1
 
    i = 1
    while 0 <= col + i < cols and board[row][col + i][0] != "X":
        threatList.append(rowColToCoord(row, col + i))
        i += 1
    
    return threatList
 
def enemyBishopThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and 0 <= col - i < cols and board[row - i][col - i][0] != "X":
        threatList.append(rowColToCoord(row - i, col - i))
        i += 1
 
    i = 1
    while 0 <= row - i < rows and 0 <= col + i < cols and board[row - i][col + i][0] != "X":
        threatList.append(rowColToCoord(row - i, col + i))
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col - i < cols and board[row + i][col - i][0] != "X":
        threatList.append(rowColToCoord(row + i, col - i))
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col + i < cols and board[row + i][col + i][0] != "X":
        threatList.append(rowColToCoord(row + i, col + i))
        i += 1
    
    return threatList
 
def enemyKnightThreat(pos):
    threatList = []
    row = pos[0]
    col = pos[1]
 
    for i in range (0, 2):
        coeff1 = (-1) ** i
        
        for j in range (0, 2):
            # vertical L-path
            coeff2 = (-1) ** j
            newRow = row + coeff1 * 2
            newCol = col + coeff2 * 1
            if 0 <= newRow < rows and 0 <= newCol < cols and board[newRow][newCol][0] != "X":
                threatList.append(rowColToCoord(newRow, newCol))
 
            # horizontal L-path
            newRow = row + coeff1 * 1
            newCol = col + coeff2 * 2
            if 0 <= newRow < rows and 0 <= newCol < cols and board[newRow][newCol][0] != "X":
                threatList.append(rowColToCoord(newRow,newCol))
 
    return threatList
 
def insertObstacles(lines):
    global board
    global numFree

    numObstacles = int(lines[2].split(":")[1])
    obstacleList = lines[3].split(":")[1].rstrip("\n").split(" ")
    for i in range(0, numObstacles):
        coord = coordStrToInt(obstacleList[i])
        board[coord[0]][coord[1]][0] = "X"
    numFree = rows * cols - numObstacles
 
def removePiece(pos):
    global board
    board[pos[0]][pos[1]][0] = " "
 
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
 
def printBoard(tempBoard):
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
                    tempBoard[int((i-1)/2)][j][0])
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
 
def cleanBoard(tempBoard):
    for i in range(0, rows):
        for j in range(0, cols):
            if tempBoard[i][j][0] == "X":
                tempBoard[i][j][0] = " "
    insertObstacles(getLines())

def isComplete(stateToCheck):
    global pieceList
    global numPieces
    score = 0
    for i in range(0, rows):
        for j in range(0, cols):
            coord = []
            coord.append(i)
            coord.append(j)
            if not isEmpty(stateToCheck.board, coord) and (not isObstacle(stateToCheck.board, coord)):
                score += 1
    return score == numPieces
 
def isEmpty(tempBoard, coord):
    return (tempBoard[coord[0]][coord[1]][0] == " ")
 
def isObstacle(tempBoard, coord):
    return (tempBoard[coord[0]][coord[1]][0] == "X")

def expandState():
    global queue

    score, stateToExpand, expandedBool = queue[0]
    del queue[0]
    queue.insert(0, (score, stateToExpand, True))

    return score, stateToExpand, True
 
def asciiToInt(c):
    return ord(c) - ord('a')
 
def intToAscii(n):
    return chr(n + ord('a'))
 
def rowColToCoord(row, col):
    coord = []
    coord.append(row)
    coord.append(col)
    return coord
 
def getLines():
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    return lines

def getListScore(l):
    listScore = 0
    for i in range(0, len(l)):
        listScore += int(l[i])
    return listScore

def pushNextPiece(l):
    tempList = deepcopy(l)
    print("list of pieces = {}".format(tempList))
    if tempList[1] > 0:
        tempList[1] -= 1
        return "Queen", tempList
    elif tempList[2] > 0:
        tempList[2] -= 1
        return "Bishop", tempList
    elif tempList[3] > 0:
        tempList[3] -= 1
        return "Rook", tempList
    elif tempList[4] > 0:
        tempList[4] -= 1
        return "Knight", tempList
    elif tempList[0] > 0:
        tempList[0] -= 1
        return "King", tempList

def randPushNextPiece(l):
    tempList = deepcopy(l)
    indexToPush = random.randint(0, len(tempList) - 1)
    if tempList[indexToPush] > 0:
        tempList[indexToPush] -= 1
    if indexToPush == 1:
        return "Queen", tempList
    elif indexToPush == 2:
        return "Bishop", tempList
    elif indexToPush == 3:
        return "Rook", tempList
    elif indexToPush == 4:
        return "Knight", tempList
    elif indexToPush == 0:
        return "King", tempList

def placePiece(stateToExpand, piece, remPieceList):
    global queue
    print("piece to be placed = {}".format(piece))

    placementQueue = []
    hq.heapify(placementQueue)
    for i in range(0, rows):
        for j in range(0, cols):
            coord = []
            tempBoard = deepcopy(stateToExpand.board)
            # printBoard(stateToExpand.board)
            # print("stateBoard done")
            coord.append(i)
            coord.append(j)
            if isEmpty(tempBoard, coord):
                print("state.board for {} at {},{} =".format(piece,i,j))
                if piece == "King": 
                    enemyBoardInput = "K"
                    threatList = enemyKingThreat(coord)
                if piece == "Queen":
                    enemyBoardInput = "Q"
                    threatList = enemyQueenThreat(coord)
                if piece == "Bishop":
                    enemyBoardInput = "B"
                    threatList = enemyBishopThreat(coord)
                if piece == "Rook":
                    enemyBoardInput = "R"
                    threatList = enemyRookThreat(coord)
                if piece == "Knight":
                    enemyBoardInput = "H"
                    threatList = enemyKnightThreat(coord)
                
                tempBoard[coord[0]][coord[1]][0] = enemyBoardInput
                
                updatedNumFree = stateToExpand.numFree
                for coord in threatList:
                    tempBoard[coord[0]][coord[1]][0] = "X"
                    updatedNumFree -= 1

                # print("tempBoard =")
                # printBoard(tempBoard)
                # print("tempBoard done")
                
                tempState = State(tempBoard, updatedNumFree, remPieceList)
                print("score of state = {}".format(tempState.getScore()))
                hq.heappush(placementQueue, (-1 * tempState.getScore(), tempState))

    for i in range(0, len(placementQueue)):
        score, tempState = hq.heappop(placementQueue)
        queue.insert(0, (-1 * score, tempState))

def search():
    global board
    global pieceList
    global numFree

    initialBoard = deepcopy(board)
    initialState = State(initialBoard, numFree, pieceList)

    nextPiece, updatedPieceList = pushNextPiece(initialState.pieceList)
    placePiece(initialState, nextPiece, updatedPieceList)

    while queue:
        print("len(queue) before: {}".format(len(queue)))
        score, stateToExpand = queue[0]
        del queue[0]
        if isComplete(stateToExpand):
            return stateToExpand
        if score != 0 and getListScore(stateToExpand.pieceList) != 0 and score >= getListScore(stateToExpand.pieceList):
            print("score of stateToExpand = {}".format(stateToExpand.getScore()))
            print("len(queue) after: {}".format(len(queue)))
            nextPiece, updatedPieceList = pushNextPiece(stateToExpand.pieceList)
            placePiece(stateToExpand, nextPiece, updatedPieceList)
    return None

def randSearch():
    global board
    global pieceList
    global numFree
    global numPieces

    initialBoard = deepcopy(board)
    initialState = State(initialBoard, numFree, pieceList)
    
    for i in range(0, numPieces ** 2):
        nextPiece, updatedPieceList = randPushNextPiece(initialState.pieceList)
        placePiece(initialState, nextPiece, updatedPieceList)

        while queue:
            print("len(queue) before: {}".format(len(queue)))
            score, stateToExpand = queue.pop(0)
            print("element deleted")
            print("score of stateToExpand wew = {}".format(stateToExpand.getScore()))
            print("len(queue) after: {}".format(len(queue)))
            if isComplete(stateToExpand):
                return stateToExpand
            if score != 0 and getListScore(stateToExpand.pieceList) != 0:
                    nextPiece, updatedPieceList = pushNextPiece(stateToExpand.pieceList)
                    placePiece(stateToExpand, nextPiece, updatedPieceList)
        return None

def run_local():
    dict = {}
    parseFile(sys.argv[1])
    
    print("before search:")
    printBoard(board)
    
    finalState = search()
    if finalState:
        for i in range(0, rows):
            for j in range(0, cols):
                entry = finalState.board[i][j][0]
                if entry != " " and entry != "X":
                    if entry == "K": 
                        pieceType = "King"
                    if entry == "Q":
                        pieceType = "Queen"
                    if entry == "B":
                        pieceType = "Bishop"
                    if entry == "R":
                        pieceType = "Rook"
                    if entry == "H":
                        pieceType = "Knight"
                
                    coord = []
                    coord.append(i)
                    coord.append(j)
                    dict[coordToStrIntTuple(coord)] = pieceType

    print("\nAfter search")
    cleanBoard(finalState.board)
    printBoard(finalState.board)
    print("dict = {}".format(dict))
    
    return dict
 
if __name__ == "__main__":
    # print(run_local())
    run_local()