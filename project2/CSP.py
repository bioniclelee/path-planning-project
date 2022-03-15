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
    board = [[[" ", 1, False] for j in range(cols)] 
                        for i in range(rows)] # board print, path cost, visited status
    insertObstacles(lines)
    insertPieces(lines)
    
def insertPieces(lines):
    global board
    global pieceList
    
    numPieces = 0
    for n in list((lines[4].rstrip("\n").split(":"))[1].split(" ")):
        pieceList.append(int(n))
    
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

def isComplete(stateToCheck):
    score = 0
    for i in range(0, len(stateToCheck.pieceList)):
        score += stateToCheck.pieceList[i]
    return score == 0
 
def isEmpty(tempBoard, coord):
    return (tempBoard[coord[0]][coord[1]][0] == " ")
 
def isObstacle(coord):
    return (board[coord[0]][coord[1]][0] == "X")
 
def asciiToInt(c):
    return ord(c) - ord('a')
 
def intToAscii(n):
    return chr(n + ord('a'))
 
def rowColToCoord(row, col):
    coord = []
    coord.append(row)
    coord.append(col)
    return coord

def listMatch(l1, l2):
    return not [x for x in l1 + l2 if x not in l1 or x not in l2]
 
def getLines():
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    return lines
 
def popFromQueue(tempPieceList, tempPiecePosList):
    global queue
    pieceScore, pieceType, piecePos = hq.heappop(queue)
    h = 0
    for elem in tempPieceList:
        if piecePos == elem[1]:
            break
        h += 1
    # print("h = {}".format(h))
    del tempPieceList[h]
    del tempPiecePosList[h]
    board[piecePos[0]][piecePos[1]][0] = " "
    return pieceScore, pieceType, piecePos

def pushNextPiece(tempList):
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

def placePiece(stateToExpand, piece, remPieceList):
    global queue

    placementQueue = []
    hq.heapify(placementQueue)
    for i in range(0, rows):
        for j in range(0, cols):
            coord = []
            tempBoard = deepcopy(stateToExpand.board)
            coord.append(i)
            coord.append(j)
            if isEmpty(tempBoard, coord):
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
                
                tempState = State(tempBoard, updatedNumFree, remPieceList)
                hq.heappush(placementQueue, (tempState.getScore(), tempState))

    for i in range(0, len(placementQueue)):
        score, tempState = hq.heappop(placementQueue)
        queue.insert(0, (score, tempState))

def search():
    global board
    global pieceList
    global numFree

    initialBoard = deepcopy(board)
    initialState = State(initialBoard, numFree, pieceList)

    nextPiece, updatedPieceList = pushNextPiece(initialState.pieceList)
    placePiece(initialState, nextPiece, updatedPieceList)

    while queue:
        score, stateToExpand = queue[0]
        if isComplete(stateToExpand):
            return stateToExpand
        elif score != 0:
            nextPiece, updatedPieceList = pushNextPiece(stateToExpand.pieceList)
            placePiece(stateToExpand, nextPiece, updatedPieceList)
        del queue[0]

    return None

def run_CSP():
    dict = {}
    parseFile(sys.argv[1])
    
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
    
    return dict
 
if __name__ == "__main__":
    print(run_CSP())