from textwrap import wrap
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

def isValidMove(square, action):
    if ((int)(square.index) in rightBorder):
    #print("entering rightBorder")
        if square.index in upBorder: #Square 16
            if ((action == "up") or (action == "right")):
                return False
        elif square.index in downBorder:#Square 4
            if ((action == "down") or (action == "right")):
                return False
        else:#Any square right NOT 16/4
            if (action == "right"):
                return False
            else:
                return True

    if ((int)(square.index) in leftBorder):
        #print("entering leftBorder")
        if square.index in upBorder: #Square 13
            if ((action == "up") or (action == "left")):
                return False
        elif square.index in downBorder: #Square 1
            if ((action == "down") or (action == "left")):
                return False
        else:#Any square right NOT 13/1
            if (action == "left"):
                return False
            else:
                return True

    if ((int)(square.index) in upBorder):
        #print("entering upBorder")
        if square.index in rightBorder: #Square 16
            if ((action == "up") or (action == "right")):
                return False
        elif square.index in leftBorder:#Square 13
            if ((action == "up") or (action == "left")):
                return False
        else:#Any square right NOT 16/13
            if (action == "up"):
                return False
            else:
                return True

        
    if ((int)(square.index) in downBorder):
        #print("entering downBorder")
        if square.index in rightBorder: #Square 4
            if ((action == "down") or (action == "right")):
                return False
        elif square.index in leftBorder:#Square 1
            if ((action == "down") or (action == "left")):
                return False
        else:#Any square right NOT 4/1
            if (action == "down"):
                return False
            else:
                return True

#If we have a square that tries to make an illegal move outside of border, calculate the Q-value for that square using itself
def calcQValWithSelf(square, action):

    stateUpQVal = square.upQVal
    stateRightQVal = square.rightQVal
    stateDownQVal = square.downQVal
    stateLeftQVal = square.leftQVal



    maxQVal = max(stateUpQVal,stateRightQVal,stateDownQVal,stateLeftQVal)

    updatedUpQVal = ((1-learnRate) * square.upQVal) + learnRate*(square.reward + discountRate * maxQVal)
    updatedRightQVal = ((1-learnRate) * square.rightQVal) + learnRate*(square.reward + discountRate *maxQVal)
    updatedDownQVal = ((1-learnRate) * square.downQVal) + learnRate*(square.reward + discountRate *maxQVal)
    updatedLeftQVal = ((1-learnRate) * square.leftQVal) + learnRate*(square.reward + discountRate *maxQVal)

    nextActionPicked = action
    if (nextActionPicked == "up"):
        square.upQVal = updatedUpQVal
    elif (nextActionPicked == "right"):
        square.rightQVal = updatedRightQVal
    elif (nextActionPicked == "down"):
        square.downQVal = updatedDownQVal
    elif (nextActionPicked == "left"):
        square.leftQVal = updatedLeftQVal
    


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

    squareUpVal = square.upQVal
    squareRightVal = square.rightQVal
    squareDownVal = square.downQVal
    squareLeftVal = square.leftQVal





    # #print("Square index is: ",square.index)
    # if ((int)(square.index) in rightBorder):
    #     #print("entering rightBorder")
    #     if square.index in upBorder: #Square 16
    #         #print("entering square 16")
    #         downVal = square.downQVal
    #         leftVal = square.leftQVal
    #     elif square.index in downBorder:#Square 4
    #         #print("entering square 4")
    #         upVal = square.upQVal    
    #         leftVal = square.leftQVal
    #     else:#Any square right NOT 16/4
    #         upVal = square.upQVal    
    #         downVal = square.downQVal
    #         leftVal = square.leftQVal

    # if ((int)(square.index) in leftBorder):
    #     #print("entering leftBorder")
    #     if square.index in upBorder: #Square 13
    #         #print("entering square 13")
    #         downVal = square.downQVal
    #         rightVal = square.rightQVal
    #     elif square.index in downBorder: #Square 1
    #         #print("entering square 1")
    #         upVal = square.upQVal    
    #         rightVal = square.rightQVal
    #     else:#Any square right NOT 13/1
    #         #print("entering other squares")
    #         upVal = square.upQVal    
    #         downVal = square.downQVal
    #         rightVal = square.rightQVal

    # if ((int)(square.index) in upBorder):
    #     #print("entering upBorder")
    #     if square.index in rightBorder: #Square 16
    #     # print("entering square 16")
    #         downVal = square.downQVal
    #         leftVal = square.leftQVal
    #     elif square.index in leftBorder:#Square 13
    #         #print("entering square 13")
    #         downVal = square.downQVal
    #         rightVal = square.rightQVal
    #     else:#Any square right NOT 16/13
    #         #print("entering other squares")
    #         downVal = square.downQVal
    #         rightVal = square.rightQVal
    #         leftVal = square.leftQVal

        
    # if ((int)(square.index) in downBorder):
    #     #print("entering downBorder")
    #     if square.index in rightBorder: #Square 4
    #         upVal = square.upQVal
    #         leftVal = square.leftQVal
    #     elif square.index in leftBorder:#Square 1
    #         upVal = square.upQVal
    #         rightVal = square.rightQVal
    #     else:#Any square right NOT 4/1
    #         upVal = square.upQVal
    #         rightVal = square.rightQVal
    #         leftVal = square.leftQVal
    
    #maxVal = max(upVal, rightVal, downVal, leftVal)
    maxVal = max(squareUpVal, squareRightVal, squareDownVal, squareLeftVal)

    if maxVal==squareUpVal:
        if isValidMove(square, "up"):
            bestState = boardArray[square.index-1+4]
            bestChoice = "up"
        else:
            calcQValWithSelf(square, "up")
            bestState = square

    elif maxVal==squareRightVal:
        if isValidMove(square, "right"):
            bestState = boardArray[square.index-1+1]
            bestChoice = "right"
        else:
            calcQValWithSelf(square, "right")
            bestState = square

    elif maxVal==squareDownVal:
        if isValidMove(square, "down"):
            bestState = boardArray[square.index-1-4]
            bestChoice = "down"
        else:
            calcQValWithSelf(square, "down")
            bestState = square

    elif maxVal==squareLeftVal:
        if isValidMove(square, "left"):
            bestState = boardArray[square.index-1-1]
            bestChoice = "left"
        else:
            calcQValWithSelf(square, "left")
            bestState = square


    randVal = random.random()
    if ((randVal >= (1-epsilonGreedy)) or flag == 1):
        return [bestState,bestChoice]

    else:
        #print("DOING RANDOM TINGSSSS")
        randInt = random.randint(0,3)
        if (randInt == 0):
            if isValidMove(square,"right"):
                bestState = boardArray[square.index-1+1]
                bestChoice = "right"
            else:
                bestState = square
        elif (randInt == 1):
            if isValidMove(square,"left"):
                bestState = boardArray[square.index-1-1]
                bestChoice = "left"
            else:
                bestState = square
        elif (randInt == 2):
            if isValidMove(square,"up"):
                bestState = boardArray[square.index-1+4]
                bestChoice = "up"
            else:
                bestState = square
        elif (randInt == 3):
            if isValidMove(square,"down"):
                bestState = boardArray[square.index-1-4]
                bestChoice = "down"
            else:
                bestState = square
        
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
