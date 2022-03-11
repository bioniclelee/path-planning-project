import sys
import re
import heapq as hq
import math
import random

rows = 0
cols = 0
k = 0
board = []
queue = []
piecePosList = []
pieceList = []

# class Piece:

#     pos = 0
#     type = None
#     threatList = None

#     def __init__(self, pos, type, threatList):
#         self.pos = pos
#         self.type = type
#         self.threatList = threatList  


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
    insertK(lines)
    insertPieces(lines)

def insertK(lines):
    global k
    k = int(lines[4].split(":")[1])
    
def insertPieces(lines):
    global board
    global piecePosList
    
    numPieces = 0
    for n in list((lines[5].rstrip("\n").split(":"))[1].split(" ")):
        numPieces += int(n)

    lineNum = 7
    while lineNum < len(lines):
        threatList = []
        # print(lineNum)
        # print("{} when lineNum = {}".format(lines[lineNum], lineNum))
        rawEntry = lines[lineNum].rstrip("\n").replace("[","").replace("]","").split(",")
        
        coord = coordStrToInt(rawEntry[1])
        piecePosList.append(coord)
        if rawEntry[0] == "King": 
            enemyBoardInput = "K"
            threatList = enemyKingThreat(coord)
        if rawEntry[0] == "Queen":
            enemyBoardInput = "Q"
            threatList = enemyQueenThreat(coord)
        if rawEntry[0] == "Bishop":
            enemyBoardInput = "B"
            threatList = enemyBishopThreat(coord)
        if rawEntry[0] == "Rook":
            enemyBoardInput = "R"
            threatList = enemyRookThreat(coord)
        if rawEntry[0] == "Knight":
            enemyBoardInput = "H"
            threatList = enemyKnightThreat(coord)
        board[coord[0]][coord[1]][0] = enemyBoardInput
        
        pieceList.append((rawEntry[0], coord, threatList))

        lineNum += 1

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
    numObstacles = int(lines[2].split(":")[1])
    obstacleList = lines[3].split(":")[1].rstrip("\n").split(" ")
    for i in range(0, numObstacles):
        coord = coordStrToInt(obstacleList[i])
        board[coord[0]][coord[1]][0] = "X"

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

def isComplete():
    global queue
    global k

    if len(queue) == k:
        for elem in queue:
            if elem[0] != 0:
                return False
        return True

def isEmpty(coord):
    return (board[coord[0]][coord[1]][0] == " ")

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

def getScore(posList, threatList):
    # print("score = {}".format(len([x for x in threatList if x in posList and x in threatList])))
    return len([x for x in threatList if x in posList and x in threatList])

def listMatch(l1, l2):
    return not [x for x in l1 + l2 if x not in l1 or x not in l2]

def getLines():
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    return lines

def pushAllToQueue(tempPieceList, tempPiecePosList):
    global queue
    queue = []
    for i in range(0, len(tempPieceList)):
        pieceType, piecePos, pieceThreatList = tempPieceList[i]
        hq.heappush(queue, (-1 * getScore(tempPiecePosList, pieceThreatList), pieceType, piecePos))
        if (pieceType == "Knight"):
            pieceRepr = "H"
        else:
            pieceRepr = pieceType[0]
        board[piecePos[0]][piecePos[1]][0] = pieceRepr

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

def search():
    global queue
    global k
    global board
    global pieceList
    global piecePosList

    tempPieceList = []
    tempPiecePosList = []

    for i in range(0, len(pieceList)):
        tempPieceList.append(pieceList[i])
        tempPiecePosList.append(piecePosList[i])

    # set to -1 to let a normal heapq iteration run first
    counter = -1
    ind = counter

    pushAllToQueue(pieceList, piecePosList)

    while not isComplete():

        # print("normal heapq run")

        # print("length of queue = {}".format(len(queue)))
        # print("length of pieceList = {}".format(len(pieceList)))
        # print("length of queue in remove = {}".format(len(queue)))


        if len(queue) == k:
            print("counter = {}".format(counter))
            if counter == len(pieceList) - 1:
                counter = 0
                ind += 1

                tempPieceList = []
                tempPiecePosList = []
                for i in range(0, len(pieceList)):
                    tempPieceList.append(pieceList[i])
                    tempPiecePosList.append(piecePosList[i])
                
                if -1 < ind < len(pieceList):
                    print("ind = {} | piece deleted = {}".format(ind, tempPieceList[ind]))
                    del tempPieceList[ind]
                    del tempPiecePosList[ind]

                pushAllToQueue(tempPieceList, tempPiecePosList)            
                # queue = []
                # for j in range(0, len(tempPieceList)):
                #     pieceType, piecePos, pieceThreatList = tempPieceList[j]
                #     hq.heappush(queue, (-1 * getScore(tempPiecePosList, pieceThreatList), pieceType, piecePos))
            
            else:
                pushAllToQueue(tempPieceList, tempPiecePosList)
                min = -1 * math.inf
                minInd = 0
                for x in range(0, len(pieceList)):
                    elem = pieceList[x]
                    if not elem in tempPieceList:
                        pieceType, piecePos, pieceThreatList = elem
                        newScore = -1 * getScore(tempPiecePosList, pieceThreatList)
                        # print("tempPiecePosList = {}".format(tempPiecePosList))
                        currHeadScore = queue[0][0]
                        # print("currHeadScore = {} | newScore = {}".format(currHeadScore, newScore))
                        if newScore > currHeadScore and newScore > min:
                            min = newScore
                            minInd = x
                
                if min != -1 * math.inf:
                    elemToInsert = pieceList[minInd]
                    pieceType, piecePos, pieceThreatList = elemToInsert
                    print("{} inserted".format(elemToInsert))
                    tempPieceList.append(elemToInsert)
                    tempPiecePosList.append(piecePos)
                    pushAllToQueue(tempPieceList, tempPiecePosList)
                    print("queue: {}".format(queue))
                    pieceScore, pieceType, piecePos = popFromQueue(tempPieceList, tempPiecePosList)
                    # pieceScore, pieceType, piecePos = hq.heappop(queue)
                    # h = 0
                    # for elem in tempPieceList:
                    #     if piecePos == elem[1]:
                    #         break
                    #     h += 1
                    # # print("h = {}".format(h))
                    # del tempPieceList[h]
                    # del tempPiecePosList[h]
                    pushAllToQueue(tempPieceList, tempPiecePosList)
                    print("popped queue: {}".format(queue))
                    
                    # elemCounter = -1
                    # plateauPieceList = []
                    # for elem in queue:
                    #     pieceScore, pieceType, piecePos = elem
                    #     if pieceScore == currHeadScore:
                    #         print("currHeadScore = {} | pieceScore = {}".format(currHeadScore, pieceScore))
                    #         for tempElem in tempPieceList:
                    #             if piecePos == tempElem[1]:
                    #                 break
                    #         print("{} to be pushed into plateauPieceList".format(tempElem))
                    #         plateauPieceList.append(tempElem)
                    #         elemCounter += 1

                    # print("plateau list = {}".format(plateauPieceList))
                    # for platInd in range(0, len(plateauPieceList)):
                    #     queueCounter = 0
                    #     for elem in queue:
                    #         pieceScore, pieceType, piecePos = elem
                    #         if plateauPieceList[platInd][2] == pieceScore:
                    #             break
                    #         queueCounter += 1
                    #     print("queueCounter = {}".format(queueCounter))
                    #     plateauQueueEntry = queue[queueCounter]
                    #     del queue[queueCounter]

                    #     h = 0
                    #     for elem in plateauPieceList:
                    #         if piecePos == elem[1]:
                    #             break
                    #         h += 1
                        
                    #     tempPieceListEntry = tempPieceList[h]
                    #     tempPiecePosListEntry = tempPiecePosList[h]
                    #     print("removing plateau piece = {}".format(tempPieceListEntry))
                    #     del tempPieceList[h]
                    #     del tempPiecePosList[h]
                    #     pushAllToQueue(tempPieceList, tempPiecePosList)

                    if isComplete():
                        print("queue = {}".format(queue))
                        return queue
                        # else:
                        #     print("reinserting plateau piece: {}".format(tempPieceListEntry))
                        #     tempPieceList.append(tempPieceListEntry)
                        #     tempPiecePosList.append(tempPiecePosListEntry)
                        #     pushAllToQueue(tempPieceList, tempPiecePosList)
                        #     print("len(queue) after plateau piece reinsertion = {} | len(tempPieceList) = {}".format(len(queue), len(tempPieceList)))
                        
                        
                    # print("len(queue) after insertion = {} when {} is inserted".format(len(queue), elem))
                counter += 1

        else:
            pieceScore, pieceType, piecePos = hq.heappop(queue)
            print("{} at {} with score {} is removed".format(pieceType, piecePos, pieceScore))
            removePiece(piecePos)

            h = 0
            for elem in tempPieceList:
                if piecePos == elem[1]:
                    break
                h += 1
            # print("h = {}".format(h))
            del tempPieceList[h]
            del tempPiecePosList[h]
            
            pushAllToQueue(tempPieceList, tempPiecePosList)
            # queue = []

            # for i in range(0, len(tempPieceList)):
            #     # print("piecePosList = {}".format(piecePosList))
            #     # print("pieceThreatList = {}".format(pieceThreatList))
            #     # print("pieceType = {}".format(pieceType))
            #     pieceType, piecePos, pieceThreatList = tempPieceList[i]
            #     # print("pushing {} at {} with score = {}".format(pieceType, piecePos,getScore(tempPiecePosList, pieceThreatList)))
            #     hq.heappush(queue, (-1 * getScore(tempPiecePosList, pieceThreatList), pieceType, piecePos))
            #     if (pieceType == "Knight"):
            #         pieceRepr = "H"
            #     else:
            #         pieceRepr = pieceType[0]
            #     board[piecePos[0]][piecePos[1]][0] = pieceRepr
        
        if ind == len(piecePosList):
            # for iter in range(0, 10000):
            #     tempPieceList = []
            #     tempPiecePosList = []
            #     for i in range(0, len(pieceList)):
            #         # print(pieceList[i][0])
            #         tempPieceList.append(pieceList[i])
            #         tempPiecePosList.append(piecePosList[i])
                
            #     randPieceList = []
            #     randPiecePosList = []
            #     for iter2 in range(0, k):
            #         randInd = random.randint(0, len(tempPieceList) - 1)
            #         # print("randInd = {}".format(randInd))
            #         randPieceList.append(tempPieceList[randInd])
            #         randPiecePosList.append(tempPiecePosList[randInd])
            #         del tempPieceList[randInd]
            #         del tempPiecePosList[randInd]
                
            #     # print(len(randPieceList))
            #     randScoreList = []
            #     for r in range(0, len(randPieceList)):
            #         pieceType, piecePos, pieceThreatList = randPieceList[r]
            #         hq.heappush(queue, (-1 * getScore(randPiecePosList, pieceThreatList), pieceType, piecePos))
            #         randScoreList.append(getScore(randPiecePosList, pieceThreatList))
            #         if len([a for a in randScoreList if a == 0]) == len(randPieceList):
            #             return queue
            #         else:
            #             break
            return None
    return queue

def run_local():
    dict = {}
    parseFile(sys.argv[1])
    
    print("before search:")
    printBoard(board)

    if search():
        while queue:
            pieceScore, pieceType, piecePos = hq.heappop(queue)
            # print("{} at {} with score {} remains".format(pieceType, piecePos, pieceScore))
            coordString = coordToStrIntTuple(piecePos)
            newCoord = []
            newCoord.append(coordString[0])
            newCoord.append(int(coordString[1]))
            dict[tuple(newCoord)] = (pieceType, pieceScore)

        print("\nAfter search")
        printBoard(board)
    # print("dict = {}".format(dict))
    
    return dict

if __name__ == "__main__":
    print(run_local())