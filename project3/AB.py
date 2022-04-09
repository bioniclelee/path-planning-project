import sys
import re
import heapq as hq
from copy import deepcopy
import math
 
rows = 5
cols = 5
board = []
queue = []
numFree = 0
numPieces = 0
maxTurns = 2

class State:
    def __init__(self, gameboard, turn):
        self.gameboard = gameboard
        self.turn = turn

    def isMaxPlayer(self):
        global maxTurns
        return maxTurns % 2 == self.turn % 2

    def __lt__(self, other):
        return self.score < other.score
 
    def __le__(self, other):
        return self.score <= other.score
    
    def __str__(self):
        return str(self.gameboard)
 
def parseFile(file):
    global rows
    global cols
    global board
 
    with open(file) as f:
        lines = f.readlines()
    
    rows = 5
    cols = 5
    
def initializeGameboard():

    return {('a', 1): ('Pawn', 'White'), ('b', 1): ('Pawn', 'White'), ('c', 1): ('Pawn', 'White'),
         ('d', 1): ('Pawn', 'White'), ('e', 1): ('Pawn', 'White'), ('a', 3): ('Pawn', 'Black'),
         ('b', 3): ('Pawn', 'Black'), ('c', 3): ('Pawn', 'Black'), ('d', 3): ('Pawn', 'Black'),
         ('e', 3): ('Pawn', 'Black'), ('a', 0): ('Rook', 'White'), ('b', 0): ('Knight', 'White'),
         ('c', 0): ('Bishop', 'White'), ('d', 0): ('Queen', 'White'), ('e', 0): ('King', 'White'),
         ('a', 4): ('Rook', 'Black'), ('b', 4): ('Knight', 'Black'), ('c', 4): ('Bishop', 'Black'),
         ('d', 4): ('Queen', 'Black'), ('e', 4): ('King', 'Black')}
    
def kingThreat(colour, state, pos):
    global rows
    global cols

    threatList = []
    row = pos[0]
    col = pos[1]
    for i in range (-1, 2):
        for j in range (-1, 2):
            if 0 <= row + i < rows and 0 <= col + j < cols and not isFriendly(colour, state, rowColToCoord(row + i, col + j)):
                threatList.append(tuple(rowColToCoord(row + i, col + j)))
    return threatList
 
def queenThreat(colour, state, pos):
    return rookThreat(colour, state, pos) + bishopThreat(colour, state, pos)
 
def rookThreat(colour, state, pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and not isFriendly(colour, state, rowColToCoord(row - i, col)):
        threatList.append(tuple(rowColToCoord(row - i, col)))
        if isEnemy(colour, state, rowColToCoord(row - i, col)):
            break
        i += 1
    
    i = 1
    while 0 <= row + i < rows and not isFriendly(colour, state, rowColToCoord(row + i, col)):
        threatList.append(tuple(rowColToCoord(row + i, col)))
        if isEnemy(colour, state, rowColToCoord(row + i, col)):
            break
        i += 1
 
    i = 1
    while 0 <= col - i < cols and not isFriendly(colour, state, rowColToCoord(row, col - i)):
        threatList.append(tuple(rowColToCoord(row, col - i)))
        if isEnemy(colour, state, rowColToCoord(row, col - i)):
            break
        i += 1
 
    i = 1
    while 0 <= col + i < cols and not isFriendly(colour,state, rowColToCoord(row, col + i)):
        threatList.append(tuple(rowColToCoord(row, col + i)))
        if isEnemy(colour, state, rowColToCoord(row, col + i)):
            break
        i += 1
    
    return threatList
 
def bishopThreat(colour, state, pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    i = 1
    while 0 <= row - i < rows and 0 <= col - i < cols and not isFriendly(colour, state, rowColToCoord(row - i, col - i)):
        threatList.append(tuple(rowColToCoord(row - i, col - i)))
        if isEnemy(colour, state, rowColToCoord(row - i, col -i)):
            break
        i += 1
 
    i = 1
    while 0 <= row - i < rows and 0 <= col + i < cols and not isFriendly(colour, state, rowColToCoord(row - i, col + i)):
        threatList.append(tuple(rowColToCoord(row - i, col + i)))
        if isEnemy(colour, state, rowColToCoord(row - i, col + i)):
            break
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col - i < cols and not isFriendly(colour, state, rowColToCoord(row + i, col - i)):
        threatList.append(tuple(rowColToCoord(row + i, col - i)))
        if isEnemy(colour, state, rowColToCoord(row + i, col - i)):
            break
        i += 1
 
    i = 1
    while 0 <= row + i < rows and 0 <= col + i < cols and not isFriendly(colour, state, rowColToCoord(row + i, col + i)):
        threatList.append(tuple(rowColToCoord(row + i, col + i)))
        if isEnemy(colour, state, rowColToCoord(row + i, col + i)):
            break
        i += 1
    
    return threatList
 
def knightThreat(colour, state, pos):
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
            if 0 <= newRow < rows and 0 <= newCol < cols and not isFriendly(colour, state, rowColToCoord(newRow, newCol)):
                threatList.append(tuple(rowColToCoord(newRow, newCol)))
 
            # horizontal L-path
            newRow = row + coeff1 * 1
            newCol = col + coeff2 * 2
            if 0 <= newRow < rows and 0 <= newCol < cols and not isFriendly(colour, state, rowColToCoord(newRow, newCol)):
                threatList.append(tuple(rowColToCoord(newRow,newCol)))
 
    return threatList

def pawnThreat(colour, state, pos):
    threatList = []
    row = pos[0]
    col = pos[1]
    # print(coordToStrIntTuple(pos))
    if colour == "White":
        coeff = 1
    else:
        # print("Black coeff = -1")
        coeff = -1
    
    # print("coeff = {}".format(coeff))
    if 0 <= row + (1 * coeff) < rows and 0 <= col < cols and not isOccupied(colour, state, rowColToCoord(row + (1 * coeff), col)):
        # print("pawn forward = {}".format(coordToStrIntTuple(rowColToCoord(row + (1 * coeff), col))))
        threatList.append(tuple(rowColToCoord(row + (1 * coeff), col)))
    if 0 <= row + (1 * coeff) < rows and 0 <= col + 1 < cols and isEnemy(colour, state, rowColToCoord(row + (1 * coeff), col + 1)):
        # print("col + 1 = {}".format(coordToStrIntTuple(rowColToCoord(row + (1 * coeff), col + 1))))
        threatList.append(tuple(rowColToCoord(row + (1 * coeff), col + 1)))
    if 0 <= row + (1 * coeff) < rows and 0 <= col - 1 < cols and isEnemy(colour, state, rowColToCoord(row + (1 * coeff), col - 1)):
        # print("col - 1 = {}".format(coordToStrIntTuple(rowColToCoord(row + (1 * coeff), col - 1))))
        threatList.append(tuple(rowColToCoord(row + (1 * coeff), col - 1)))
    # print(state.gameboard)
    # print("{} pawn threatList = {}".format(colour, threatList))
    return threatList

# pos should be in (int, int) form
def genEnemyPos(state, pos):
    enemyPos = []
    # print("genEnemyPos = {}".format(pos))
    originalPiece, originalColour = state.gameboard[coordToStrIntTuple(pos)]
    for elem in state.gameboard:
        piece, colour = state.gameboard[elem]
        if colour != originalColour:
            enemyPos.append((strIntTupleToCoord(elem), piece))
    return enemyPos

# coord should be in (int, int) form
def genThreatList(piece, colour, state, coord):
    if piece == "King": 
        threatList = kingThreat(colour, state, coord)
    if piece == "Queen":
        threatList = queenThreat(colour, state, coord)
    if piece == "Bishop":
        threatList = bishopThreat(colour, state, coord)
    if piece == "Rook":
        threatList = rookThreat(colour, state, coord)
    if piece == "Knight":
        threatList = knightThreat(colour, state, coord)
    if piece == "Pawn":
        threatList = pawnThreat(colour, state, coord)
    
    return threatList

# boriginalPos should be in (int, int) form
def calcHeuristic(state):
    # print("calcHeuristic: originalPos = {}".format(originalPos))
    materialScore = {'King': 1000, 'Pawn': 1, 'Bishop': 3, 'Knight': 3, 'Rook': 5, 'Queen': 200}
    white = set()
    black = set()
    whiteScore = 0
    blackScore = 0
    
    # checking to see if an enemy piece is consumed
    for coord in state.gameboard:
        piece, colour = state.gameboard[coord]
        threatList = genThreatList(piece, colour, state, strIntTupleToCoord(coord))
        if colour == "White":
            white.update(set(threatList))
            whiteScore += materialScore[piece]
        else:
            black.update(set(threatList))
            blackScore += materialScore[piece]
    # print("heuristic = {}".format(2 ** (whiteScore + len(white)) - 2 ** (blackScore + len(black))))
    whiteScore += len(white)
    blackScore += len(black)
    finalHeuristic = whiteScore - blackScore
    return finalHeuristic
 
def coordStrToInt(str):
    coord = []
    newList = re.split("(\d+)", str)
    row = int(newList[1])
    col = asciiToInt(newList[0])
    coord.append(row)
    coord.append(col)
    return coord
 
def coordToStrIntTuple(coord):
    coord = list(coord)
    row = coord[0]
    col = coord[1]
    temp = []
    temp.append(intToAscii(col))
    temp.append(row)
    return tuple(temp)

def strIntTupleToCoord(coord):
    coord = list(coord)
    row = coord[1]
    col = coord[0]
    temp = []
    temp.append(int(row))
    temp.append(asciiToInt(col))
    return tuple(temp)
 
def isComplete(stateToCheck):
    global numPieces
    return len(stateToCheck.piecesPlaced) == numPieces

def isOccupied(originalColour, state, coordToCheck):
    return isFriendly(originalColour, state, coordToCheck) or isEnemy(originalColour, state, coordToCheck)

def isFriendly(originalColour, state, coordToCheck):
    # print('pos in isFriendly = {}'.format(pos))
    if coordToStrIntTuple(coordToCheck) in state.gameboard:
        piece, colour = state.gameboard[coordToStrIntTuple(coordToCheck)]
        return colour == originalColour
    return False

def isEnemy(originalColour, state, coordToCheck):
    if coordToStrIntTuple(coordToCheck) in state.gameboard:
        piece, colour = state.gameboard[coordToStrIntTuple(coordToCheck)]
        return colour != originalColour
    return False

def isGameOver(state):
    kings = set()
    threats = set()
    for coord in state.gameboard:
        piece, colour = state.gameboard[coord]
        # print(piece, colour)
        if piece == "King":
            kings.add(strIntTupleToCoord(coord))
        if piece != "King":
            threats.update(set(genEnemyPos(state, strIntTupleToCoord(coord))))
    return len(kings.intersection(threats)) > 0

def asciiToInt(c):
    return ord(c) - ord('a')
 
def intToAscii(n):
    return chr(n + ord('a'))
 
def rowColToCoord(row, col):
    coord = []
    coord.append(row)
    coord.append(col)
    return coord
 
# def getLines():
#     with open(sys.argv[1]) as f:
#         lines = f.readlines()
#     return lines
 
 
# def threatenIfInserted(tempPiecesPlaced, threatList):
#     for elem in tempPiecesPlaced:
#         if tuple(elem[1]) in threatList:
#             return True
#     return False
 
# def pushNextPiece(l):
#     tempList = deepcopy(l)
#     piece = tempList.pop(0)
#     return piece, tempList
 
def genPlacementQueue(stateToExpand):
    placementQueue = []

    if stateToExpand.isMaxPlayer():
        colourToExpand = "White"
    else:
        colourToExpand = "Black"
    
    for coord in stateToExpand.gameboard:
        piece, colour = stateToExpand.gameboard[coord]
        
        if colour == colourToExpand:
            threatList = genThreatList(piece, colour, stateToExpand, strIntTupleToCoord(coord))

            for threat in threatList:
                placementQueue.append((coord, coordToStrIntTuple(threat)))
    return placementQueue

def genNewState(state, start, stop):
    newGameboard = {}
    for i in state.gameboard:
        newGameboard[i] = state.gameboard[i]
    piece, colour = newGameboard[start]
    newGameboard.pop(start)
    if stop in newGameboard:
        newGameboard.pop(stop)
    newGameboard[stop] = (piece, colour)
    return State(newGameboard, state.turn - 1)

def ab(state, alpha, beta):
    if state.turn == 0 or isGameOver(state):
        return calcHeuristic(state), None
    
    placementQueue = genPlacementQueue(state)
    if state.isMaxPlayer():
        maxEval = -math.inf
        bestMove = None
        for child in placementQueue:
            start, stop = child
            newState = genNewState(state, start, stop)
            eval, currMove = ab(newState, alpha, beta)
            if eval > maxEval:
                bestMove = child
                maxEval = eval
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, bestMove
        
    else:
        minEval = math.inf
        bestMove = None
        for child in placementQueue:
            # print("min eval")
            start, stop = child
            newState = genNewState(state, start, stop)
            eval, currMove = ab(newState, alpha, beta)
            if eval < minEval:
                bestMove = child
                minEval = eval
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, bestMove

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, White (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'White'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    global maxTurns
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    # config = sys.argv[1] #Takes in config.txt Optional

    gameState = State(gameboard, maxTurns)
    finalEval, finalMove = ab(gameState, -math.inf, math.inf)
    start, stop = finalMove
    # print(finalMove)
    return (start, stop) #Format to be returned (('a', 0), ('b', 3))

if __name__ == "__main__":

    gameboard = initializeGameboard()
    studentAgent(gameboard)