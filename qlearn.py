from textwrap import wrap
import numpy as np
import random

liveReward = -0.1
discountRate = 0.1
learnRate = 0.3

goalReward = 100
forbiddenReward = -100
wallReward = -0.1

epsilonGreedy = 0.5

randSeed = 1

convergenceVal = 100000


bestChoicesArray = []

class Square:
    def __init__(self, squareType,qVal,reward,index):
        self.type = squareType
        self.reward = reward
        self.qVal = qVal
        self.index = index


boardArray = []
#S = start, G = goal, F = forbidden, W = wall, O = ordinary

#Initialize the board to all Open with a reward of 
for i in range (1,17,1):
    boardArray.append(Square('O',-0.1,0,i))


# print("Initialize square indexes ")
# for i in range (0,16,1):
#     print(boardArray[i].index)

inputString = input ("Enter input-")
inputAsArray = inputString.split(" ")
inputAsArrayLen = len(inputAsArray)

#print(inputAsArray)

goalState1Loc = int(inputAsArray[0])-1
goalState2Loc = int(inputAsArray[1])-1
forbiddenStateLoc = int(inputAsArray[2])-1
wallStateLoc = int(inputAsArray[3])-1
outputFormat = inputAsArray[4]

if (inputAsArrayLen == 6):
    printQValuesIndex = inputAsArray[5]

startLoc = 2
boardArray[startLoc].type = 'S'
boardArray[startLoc].reward = 0


boardArray[goalState1Loc].type = 'G'
boardArray[goalState1Loc].reward = 100

boardArray[goalState2Loc].type = 'G'
boardArray[goalState2Loc].reward = 100

boardArray[forbiddenStateLoc].type = 'F'
boardArray[forbiddenStateLoc].reward = -100

boardArray[wallStateLoc].type = 'W'


print("Set all starting states")
for i in range (0,16,1):
    print(boardArray[i].type, "+ ",boardArray[i].reward, boardArray[i].qVal,boardArray[i].index)


#ef tiebreak(upval, rightval, downval, leftval):



def isTerminalState (square):
    if square.reward == 100:
        return True
    elif square.reward == -100:
        return True
    else:
        return False

rightBorder = {16,12,8,4}
leftBorder = {13,9,4,1}
upBorder = {13,14,15,16}
downBorder = {1,2,3,4}
#we need to limit certain squares,
# #can't go up for example on top row,
# 

def chooseNextState(square,flag):
    upVal = -100000
    downVal = -100000
    leftVal = -100000
    rightVal = -100000
    #print("Square index is: ",square.index)
    if ((int)(square.index) in rightBorder):
        #print("entering rightBorder")
        if square.index in upBorder: #Square 16
            #print("entering square 16")
            downVal = boardArray[square.index-1-4].qVal
            leftVal = boardArray[square.index-1-1].qVal
        elif square.index in downBorder:#Square 4
            #print("entering square 4")
            upVal = boardArray[square.index-1+4].qVal    
            leftVal = boardArray[square.index-1-1].qVal
        else:#Any square right NOT 16/4
            #print("entering other squares")
            #print("board length is:",len(boardArray))
            upVal = boardArray[square.index-1+4].qVal    
            downVal = boardArray[square.index-1-4].qVal
            leftVal = boardArray[square.index-1-1].qVal

    if ((int)(square.index) in leftBorder):
        #print("entering leftBorder")
        if square.index in upBorder: #Square 13
            #print("entering square 13")
            downVal = boardArray[square.index-1-4].qVal
            rightVal = boardArray[square.index-1+1].qVal
        elif square.index in downBorder: #Square 1
            #print("entering square 1")
            upVal = boardArray[square.index-1+4].qVal    
            rightVal = boardArray[square.index-1+1].qVal
        else:#Any square right NOT 13/1
            #print("entering other squares")
            upVal = boardArray[square.index-1+4].qVal    
            downVal = boardArray[square.index-1-4].qVal
            rightVal = boardArray[square.index-1+1].qVal

    if ((int)(square.index) in upBorder):
        #print("entering upBorder")
        if square.index in rightBorder: #Square 16
           # print("entering square 16")
            downVal = boardArray[square.index-1-4].qVal
            leftVal = boardArray[square.index-1-1].qVal
        elif square.index in leftBorder:#Square 13
            #print("entering square 13")
            downVal = boardArray[square.index-1-4].qVal
            rightVal = boardArray[square.index-1+1].qVal
        else:#Any square right NOT 16/13
            #print("entering other squares")
            downVal = boardArray[square.index-1-4].qVal
            rightVal = boardArray[square.index-1+1].qVal
            leftVal = boardArray[square.index-1-1].qVal

        
    if ((int)(square.index) in downBorder):
        #print("entering downBorder")
        if square.index in rightBorder: #Square 4
            #print("entering square4")
            upVal = boardArray[square.index-1+4].qVal
            leftVal = boardArray[square.index-1-1].qVal
        elif square.index in leftBorder:#Square 1
            #print("entering square1")
            upVal = boardArray[square.index-1+4].qVal
            rightVal = boardArray[square.index-1+1].qVal
        else:#Any square right NOT 4/1
            #print("entering other squares")
            upVal = boardArray[square.index-1+4].qVal
            rightVal = boardArray[square.index-1+1].qVal
            leftVal = boardArray[square.index-1-1].qVal
    

    # maxVal = None
    # if rightVal != None:
    #     if leftVal != None:
    #         if upVal != None:
    #             if downVal != None:
    #                 maxVal = max(rightVal, leftVal, upVal, downVal)




    maxVal = max(upVal, rightVal, downVal, leftVal)
    bestState = None 

    #stateWMove = []
    bestChoice = 0
    if maxVal==rightVal:
        bestState = boardArray[square.index-1+1]
        bestChoicesArray.append("right")
       # stateWMove.append(bestState,"right")
        bestChoice = "right"
    elif maxVal==leftVal:
        bestState = boardArray[square.index-1-1]
        bestChoicesArray.append("left")
        #stateWMove.append(bestState,"left")
        bestChoice = "left"
    elif maxVal==upVal:
        bestState = boardArray[square.index-1+4]
        bestChoicesArray.append("up")
        #stateWMove.append(bestState,"up")
        bestChoice = "up"
    elif maxVal==downVal:
        bestState = boardArray[square.index-1-4]
        bestChoicesArray.append("down")
        #stateWMove.append(bestState,"down")
        bestChoice = "down"

    if ((np.random.random() >= epsilonGreedy) or flag == 'optimal'):
        return [bestState,bestChoice]

    else:
        randInt = random.randint(0,3)
        #print("randInt is = ", randInt)
        if ((randInt == 0) and (rightVal > -10)):
            bestState = boardArray[square.index-1+1]
            bestChoice = "right"
        elif ((randInt == 1) and (leftVal > -10)):
            bestState = boardArray[square.index-1-1]
            bestChoice = "left"
        elif ((randInt == 2) and (upVal > -10)):
            bestState = boardArray[square.index-1+4]
            bestChoice = "up"
        elif ((randInt == 3) and (downVal > -10)):
            bestState = boardArray[square.index-1-4]
            bestChoice = "down"
        return [bestState,bestChoice]


def updateQVal (state):
    #print("current q val = ",state.qVal)
    bestState = (chooseNextState(state,'optimal'))[0]
    newQVal = bestState.qVal
    tempQval = ((1-learnRate) * state.qVal) + learnRate*(state.reward + discountRate *newQVal)
    state.qVal = tempQval
    nextState = (chooseNextState(state,'doesntNeedOpt'))[0]
    return nextState

   # print("new q val = ",state.qVal)

#set q values
# for i in range (0,100,1):
#     for j in range (0,16,1):
#         updateQVal(boardArray[j])

    
atGoalState = False
atExitState = False
iterationCount = 10
startState = boardArray[1]
for i in range (0,iterationCount,1):
    currentState = startState
    while(not atExitState):
        #print("line 246")
        if iterationCount == 0:
            epsilonGreedy = 0
        currentState = updateQVal(currentState) #start updating from the starting square
        #print("currentState.type = :",currentState.type)
        if (currentState.type == ('G' or 'F')):
            atExitState = True

pathAtGoalState = False


pathArray = []



pathStart = boardArray[0]
currState = pathStart
for i in range (0,16,1):
    #print("not at goal state yet")
    chosenState = (chooseNextState(currState,'optimal'))
    pathArray.append(chosenState[1])
    nextState = chosenState[0]
    if (currState.type == ('G' or 'F')):
            pathAtGoalState = True
    #print("currState.index = :",currState.index)
    #print("currState.type = :",currState.type)
    currState = nextState

pathArray[goalState1Loc] = 'goal'
pathArray[goalState2Loc] = 'goal'
pathArray[forbiddenStateLoc] = 'forbid'
pathArray[wallStateLoc] = 'wall-square'
# print("printing patharray")
# print("pathArray  = ", pathArray)
# print("length is = ", len(pathArray))
for i in range(0,16,1):
    print(i+1, pathArray[i])










#for i in range 1,17,1:
#    print(i, " " ,bestChoicesArray[i])



