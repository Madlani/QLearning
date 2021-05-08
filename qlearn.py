from textwrap import wrap
import numpy as np
import random

liveReward = -0.1
discountRate = 0.1
learnRate = 0.3

goalReward = 100
forbiddenReward = -100

epsilonGreedy = 0.5
random.seed(1)



class Square:
    def __init__(self, squareType,reward,upQVal,rightQVal,downQVal,leftQVal,index):
        self.type = squareType
        self.reward = reward
        self.upQVal = upQVal
        self.rightQVal = rightQVal
        self.downQVal = downQVal
        self.leftQVal = leftQVal
        self.index = index
    def __str__(self):
        return f'{self.type}'


boardArray = []
#S = start, G = goal, F = forbidden, W = wall, O = open

#Initialize the board to all Open with a reward of -0.1
for i in range (1,17,1):
    boardArray.append(Square('O',-0.1,0,0,0,0,i))



#Taking in user input and preparing to extract info from it
inputString = input ("Enter input-")
inputAsArray = inputString.split(" ")
inputAsArrayLen = len(inputAsArray)

#Extracting relevant info from user input, subtracting 1 to account for indexes 
goalState1Loc = int(inputAsArray[0])-1
goalState2Loc = int(inputAsArray[1])-1
forbiddenStateLoc = int(inputAsArray[2])-1
wallStateLoc = int(inputAsArray[3])-1
outputFormat = inputAsArray[4]
printQValuesIndex = 0

#If our length is 6, then we have to print the Q values
if (inputAsArrayLen == 6):
    printQValuesIndex = inputAsArray[5]-1


#General values needed & Setting up the board with the user input - start reward & wall reward remain -0.1
startIndex = 1

boardArray[startIndex].type = 'S'

boardArray[goalState1Loc].type = 'G'
boardArray[goalState1Loc].reward = 100

boardArray[goalState2Loc].type = 'G'
boardArray[goalState2Loc].reward = 100

boardArray[forbiddenStateLoc].type = 'F'
boardArray[forbiddenStateLoc].reward = -100

boardArray[wallStateLoc].type = 'W'

#for i in range (0,16,1):
#    print("index, type = ",boardArray[i].index, boardArray[i].type)

# print("Set all starting states")
# for i in range (0,16,1):
#     print(boardArray[i].type, "+ ",boardArray[i].reward, boardArray[i].qVal,boardArray[i].index


#We need to limit certain squares, we can't go up for example on top row, store all edge cases
rightBorder = {16,12,8,4}
leftBorder = {13,9,4,1}
upBorder = {13,14,15,16}
downBorder = {1,2,3,4}


def chooseNextState(square,flag):
    #Initialize all values to very negative so we don't take those paths unless they're a possibility
    # upVal = square.upQVal
    # rightVal = square.rightQVal
    # downVal = square.upQVal
    # leftVal = square.leftQVal
    
    upVal = -1000
    rightVal = -1000
    downVal = -1000
    leftVal = -1000

    bestState = 1234
    bestChoice = 5678




    #print("Square index is: ",square.index)
    if ((int)(square.index) in rightBorder):
        #print("entering rightBorder")
        if square.index in upBorder: #Square 16
            #print("entering square 16")
            downVal = square.downQVal
            leftVal = square.leftQVal
        elif square.index in downBorder:#Square 4
            #print("entering square 4")
            upVal = square.upQVal    
            leftVal = square.leftQVal
        else:#Any square right NOT 16/4
            upVal = square.upQVal    
            downVal = square.downQVal
            leftVal = square.leftQVal

    if ((int)(square.index) in leftBorder):
        #print("entering leftBorder")
        if square.index in upBorder: #Square 13
            #print("entering square 13")
            downVal = square.downQVal
            rightVal = square.rightQVal
        elif square.index in downBorder: #Square 1
            #print("entering square 1")
            upVal = square.upQVal    
            rightVal = square.rightQVal
        else:#Any square right NOT 13/1
            #print("entering other squares")
            upVal = square.upQVal    
            downVal = square.downQVal
            rightVal = square.rightQVal

    if ((int)(square.index) in upBorder):
        #print("entering upBorder")
        if square.index in rightBorder: #Square 16
        # print("entering square 16")
            downVal = square.downQVal
            leftVal = square.leftQVal
        elif square.index in leftBorder:#Square 13
            #print("entering square 13")
            downVal = square.downQVal
            rightVal = square.rightQVal
        else:#Any square right NOT 16/13
            #print("entering other squares")
            downVal = square.downQVal
            rightVal = square.rightQVal
            leftVal = square.leftQVal

        
    if ((int)(square.index) in downBorder):
        #print("entering downBorder")
        if square.index in rightBorder: #Square 4
            #print("entering square4")
            upVal = square.upQVal
            leftVal = square.leftQVal
        elif square.index in leftBorder:#Square 1
            #print("entering square1")
            upVal = square.upQVal
            rightVal = square.rightQVal
        else:#Any square right NOT 4/1
            #print("entering other squares")
            upVal = square.upQVal
            rightVal = square.rightQVal
            leftVal = square.leftQVal
    
    # print("upVal, rightVal, downVal, leftVal = ", upVal, rightVal, downVal, leftVal)
    maxVal = max(upVal, rightVal, downVal, leftVal)

    #stateWMove = []
    if maxVal==upVal:
        if (square.index-1+4) 
        bestState = boardArray[square.index-1+4]
        bestChoice = "up"
        
    elif maxVal==rightVal:
        bestState = boardArray[square.index-1+1]
        bestChoice = "right"

    elif maxVal==downVal:
        bestState = boardArray[square.index-1-4]
        bestChoice = "down"
    
    elif maxVal==leftVal:
        bestState = boardArray[square.index-1-1]
        bestChoice = "left"


    randVal = random.random()
    if ((randVal >= (1-epsilonGreedy)) or flag == 1):
        return [bestState,bestChoice]

    else:
        #print("DOING RANDOM TINGSSSS")
        randInt = random.randint(0,3)
        if ((randInt == 0) and (rightVal > -999)):
            # print("ENTERING RANDINT = 0")
            bestState = boardArray[square.index-1+1]
            # if bestState.type == "W":
            #     #bestState = boardArray[square.index-1]
            #     bestChoice = "wall-square"
            # else:
            bestChoice = "right"
        elif ((randInt == 1) and (leftVal > -999)):
            # print("ENTERING RANDINT = 1")
            bestState = boardArray[square.index-1-1]
            # if bestState.type == "W":
            #     #bestState = boardArray[square.index-1]
            #     bestChoice = "wall-square"
            # else:
            bestChoice = "left"
        elif ((randInt == 2) and (upVal > -999)):
            # print("ENTERING RANDINT = 2")
            bestState = boardArray[square.index-1+4]
            # if bestState.type == "W":
            #     #bestState = boardArray[square.index-1]
            #     bestChoice = "wall-square"
            # else:
            bestChoice = "up"
        elif ((randInt == 3) and (downVal > -999)):
            # print("ENTERING RANDINT = 3")
            bestState = boardArray[square.index-1-4]
            # if bestState.type == "W":
            #     #bestState = boardArray[square.index-1]
            #     bestChoice = "wall-square"
            # else:
            bestChoice = "down"
        
        return [bestState,bestChoice]

def updateQVal (state, flag):
    #print("current q val = ",state.qVal)
    statePassedIn = state

    nextStatePicked = (chooseNextState(state,flag))[0]
    #print("NEXTSTATEPICKEDREWARD = ", nextStatePicked.reward)
    #print("NEXTSTATEPICKEDTYPE = ", nextStatePicked.type)


# print("NEXTSTATEPICKED IN UPDATEQVAL IS = ",nextStatePicked)
    newStateUpQVal = nextStatePicked.upQVal
    newStateRightQVal = nextStatePicked.rightQVal
    newStateDownQVal = nextStatePicked.downQVal
    newStateLeftQVal = nextStatePicked.leftQVal


    maxQVal = max(newStateUpQVal,newStateRightQVal,newStateDownQVal,newStateLeftQVal)

    updatedUpQVal = ((1-learnRate) * state.upQVal) + learnRate*(nextStatePicked.reward + discountRate * maxQVal)
    updatedRightQVal = ((1-learnRate) * state.rightQVal) + learnRate*(nextStatePicked.reward + discountRate *maxQVal)
    updatedDownQVal = ((1-learnRate) * state.downQVal) + learnRate*(nextStatePicked.reward + discountRate *maxQVal)
    updatedLeftQVal = ((1-learnRate) * state.leftQVal) + learnRate*(nextStatePicked.reward + discountRate *maxQVal)

    nextActionPicked = (chooseNextState(state,flag))[1]
    if (nextActionPicked == "up"):
        state.upQVal = updatedUpQVal
    elif (nextActionPicked == "right"):
        state.rightQVal = updatedRightQVal
    elif (nextActionPicked == "down"):
        state.downQVal = updatedDownQVal
    elif (nextActionPicked == "left"):
        state.leftQVal = updatedLeftQVal
    
    if (nextStatePicked.type == "W"):
        #print("NEXTSTATEPICKED WAS WALL, REVERSE")
        nextStatePicked = statePassedIn

    return nextStatePicked
    # nextState = (chooseNextState(state,'doesntNeedOpt'))[0]
    # return nextState

   # print("new q val = ",state.qVal)

#set q values
# for i in range (0,100,1):
#     for j in range (0,16,1):
#         updateQVal(boardArray[j])


#While we're not at a goal state, iterate until we get there, updating the q-values of states along the way
#Once we get to the goal state, break out, and repeat this process 100,000 times until all Q-values are updated
#         
iterationCount = 100000
startState = boardArray[1]
atExitState = False
for i in range (0,iterationCount,1):
    #print("in loop with i = ", i)
    currentState = startState
    atExitState = False
    while(not atExitState):
        if i == iterationCount:
            epsilonGreedy = 0
        
        #currentState = (chooseNextState(currentState,'doesntNeedOpt'))[0] 
        currentState = updateQVal(currentState, 0) 
        #print("currentState is now, index", currentState.index)
        #print("currentState.type = :",currentState.type)
        if ((currentState.type == 'G') or (currentState.type ==  'F')):
            atExitState = True



pathAtGoalState = False
pathArray = []
pathStart = boardArray[0]
currState = pathStart


optimalPolicy = [] #optimalPolicy = 16 long, contains the best action (highest q val) for each square

for i in range(0,16,1):
    chosenState = chooseNextState(boardArray[i],1)[1]
    optimalPolicy.append(chosenState)

optimalPolicy[goalState1Loc] = 'goal'
optimalPolicy[goalState2Loc] = 'goal'
optimalPolicy[forbiddenStateLoc] = 'forbid'
optimalPolicy[wallStateLoc] = 'wall-square'

#print("PRINTING OPTIMAL POLICY")
for i in range (1,17,1):
    print(i, optimalPolicy[i-1])
