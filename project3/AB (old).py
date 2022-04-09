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
maxTurns = 3
 
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
    # print("king pos = {}".format(pos))
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
    # print(pos, coordToStrIntTuple(pos))
    if colour == "White":
        coeff = -1
    else:
        # print("Black coeff = 1")
        coeff = 1
    for i in range (-1, 2):
        if 0 <= row - (i * coeff) < rows and 0 <= col < cols and not isFriendly(colour, state, rowColToCoord(row - (i * coeff), col)):
            # print("true again")
            threatList.append(tuple(rowColToCoord(row - (i * coeff), col)))
        if 0 <= row - (i * coeff) < rows and 0 <= col + 1 < cols and isEnemy(colour, state, rowColToCoord(row - (i * coeff), col + 1)):
            threatList.append(tuple(rowColToCoord(row - (i * coeff), col + 1)))
        if 0 <= row - (i * coeff) < rows and 0 <= col - 1 < cols and isEnemy(colour, state, rowColToCoord(row - (i * coeff), col - 1)):
            threatList.append(tuple(rowColToCoord(row - (i * coeff), col - 1)))
    # print("pawn threatList = {}".format(threatList))
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

# both originalPos and newPos should be in (int, int) form
def calcHeuristic(state, originalPos):
    # print("calcHeuristic: originalPos = {}".format(originalPos))
    materialScore = {'King': 0, 'Pawn': 1, 'Bishop': 1, 'Knight': 1, 'Rook': 5, 'Queen': 9}
    white = set()
    black = set()
    whiteScore = 0
    blackScore = 0
    
    # checking to see if an enemy piece is consumed
    for coord in state.gameboard:
        piece, colour = state.gameboard[coord]
        if not coord == originalPos:
            threatList = genThreatList(piece, colour, state, strIntTupleToCoord(coord))
            if colour == "White":
                white.union(set(threatList))
                whiteScore = whiteScore + materialScore[piece]
            else:
                black.union(set(threatList))
                blackScore = blackScore + materialScore[piece]
    # print("heuristic = {}".format(2 ** (whiteScore + len(white)) - 2 ** (blackScore + len(black))))
    return 2 ** (whiteScore + len(white)) - 2 ** (blackScore + len(black))
 
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
 
def isFriendly(originalColour, state, coordToCheck):
    # print('pos in isFriendly = {}'.format(pos))
    if coordToStrIntTuple(coordToCheck) in state.gameboard:
        piece, colour = state.gameboard[coordToStrIntTuple(coordToCheck)]
        return colour == originalColour
    else:
        return False

def isEnemy(originalColour, state, coordToCheck):
    if coordToStrIntTuple(coordToCheck) in state.gameboard:
        piece, colour = state.gameboard[coordToStrIntTuple(coordToCheck)]
        return colour != originalColour
    else:
        return False

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
 
# def isOccupied(coord, stateToCheck):
#     threatenedSpacesSet = set(stateToCheck.threatenedSpaces)
#     return tuple(coord) in threatenedSpacesSet
 
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
    
    for coord in stateToExpand.gameboard:
        # print("coord = {}".format(coord))
        # print(strIntTupleToCoord(coord))
        piece, colour = stateToExpand.gameboard[coord]
        # print(piece)
        # print(strIntTupleToCoord(coord))
        if stateToExpand.isMaxPlayer():
            colour = "White"
        else:
            colour = "Black"
        
        threatList = genThreatList(piece, colour, stateToExpand, strIntTupleToCoord(coord))
            # print(threatList)

        for threat in threatList:
            # print("threat = {}".format(threat))
            # print("coord2 = {}".format(coord))
            # score = calcHeuristic(newStateToExpand, threat)
            # print("whiteScore = {} | blackScore = {}".format(whiteScore, blackScore))
            placementQueue.append((coord, coordToStrIntTuple(threat)))
    return placementQueue

def genNewState(state, start, stop):
    # print("genNewState: start = {} | stop = {}".format(start, stop))
    newGameboard = dict(state.gameboard)
    piece, colour = newGameboard[start]
    newGameboard.pop(start)
    if stop in newGameboard:
        newGameboard.pop(stop)
    newGameboard[stop] = (piece, colour)
    # print(state.turn -1)
    return State(newGameboard, state.turn - 1)

def ab(state, pos, alpha, beta):
    if state.turn == 0:
        return calcHeuristic(state, pos)
    
    placementQueue = genPlacementQueue(state)
    # print("placement queue in ab: {}".format(placementQueue))
    if state.isMaxPlayer():
        for child in placementQueue:
            # print("max eval")
            maxEval = -math.inf
            start, stop = child
            newState = genNewState(state, start, stop)
            eval = ab(newState, stop, alpha, beta)
            maxRes = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
        
    else:
        for child in placementQueue:
            # print("min eval")
            minEval = math.inf
            start, stop = placementQueue.pop()
            newState = genNewState(state, start, stop)
            eval = ab(newState, stop, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
 
    # for i in range(0, rows):
    #     for j in range(0, cols):
    #         coord = []
    #         coord.append(i)
    #         coord.append(j)
 
    #         if not isOccupied(coord, stateToExpand):
    #             if piece == "King": 
    #                 threatList = kingThreat(stateToExpand, coord)
    #             if piece == "Queen":
    #                 threatList = queenThreat(stateToExpand, coord)
    #             if piece == "Bishop":
    #                 threatList = bishopThreat(stateToExpand, coord)
    #             if piece == "Rook":
    #                 threatList = rookThreat(stateToExpand, coord)
    #             if piece == "Knight":
    #                 threatList = knightThreat(stateToExpand, coord)
    #             threatList.append(tuple(coord))
 
    #             if not threatenIfInserted(stateToExpand.piecesPlaced, threatList):
    #                 tempPiecesPlaced = []
    #                 tempPiecesPlaced.append((piece, tuple(coord)))
    #                 tempPiecesPlaced.extend(stateToExpand.piecesPlaced)
    #                 threatList.extend(stateToExpand.threatenedSpaces)
    #                 tempThreatenedSpacesSet = set(threatList)
    #                 tempThreatenedSpaces = list(tempThreatenedSpacesSet)
 
    #                 updatedNumFree = rows * cols - len(tempThreatenedSpaces) - len(obstacleList)
 
    #                 tempState = State(updatedNumFree, remPieces, tempPiecesPlaced, tempThreatenedSpaces)
    #                 hq.heappush(placementQueue, (-1 * tempState.numFree, tempState))
    
    # limit = 3
    # if len(placementQueue) < limit:
    #     limit = len(placementQueue)
    # for i in range(0, limit):
    #     score, start, stop = hq.heappop(placementQueue)
    #     queue.insert(0, (score, start, stop))

# def ab():

    # initialRemPieces = deepcopy(pieceList)
    # initialState = State(numFree, initialRemPieces, [], [])
 
    # nextPiece, updatedRemPieces = pushNextPiece(initialState.remPieces)
    # placePiece(initialState, nextPiece, updatedRemPieces)
 
    # counter = 0
    # while queue:
    #     score, stateToExpand = queue.pop(0)
    #     if isComplete(stateToExpand):
    #         return stateToExpand, counter
    #     if score > 0 and len(stateToExpand.remPieces) > 0 and score >= len(stateToExpand.remPieces):
    #         nextPiece, updatedRemPieces = pushNextPiece(stateToExpand.remPieces)
    #         placePiece(stateToExpand, nextPiece, updatedRemPieces)
    #     counter += 1
 
    # return None, 0

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
    moveList = genPlacementQueue(gameState)
    evaluatedMoves = []
    hq.heapify(evaluatedMoves)
    for move in moveList:
        # print("new move")
        start, stop = move
        hq.heappush(evaluatedMoves, (-1 * ab(gameState, stop, -math.inf, math.inf), start, stop))
    selectedScore, selectedStart, selectedStop = hq.heappop(evaluatedMoves)
    # print(selectedStart, selectedStop)
    return selectedStart, selectedStop #Format to be returned (('a', 0), ('b', 3))

# if __name__ == "__main__":

#     gameboard = initializeGameboard()
#     studentAgent(gameboard)

