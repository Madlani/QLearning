from textwrap import wrap
import numpy as np

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
for i in range (0,16,1):
    boardArray.append(Square('O',0,-1,i))


print("Initialized all to -1 = ")
for i in range (0,16,1):
    print(boardArray[i].type, "+ ",boardArray[i].reward)

inputString = input ("Enter input-")
inputAsArray = inputString.split(" ")
inputAsArrayLen = len(inputAsArray)

print(inputAsArray)

goalState1Loc = int(inputAsArray[0])
goalState2Loc = int(inputAsArray[1])
forbiddenStateLoc = int(inputAsArray[2])
wallStateLoc = int(inputAsArray[3])
outputFormat = inputAsArray[4]

if (inputAsArrayLen == 5):
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
    print(boardArray[i].type, "+ ",boardArray[i].qVal)



def isTerminalState (Square square):
    if square.reward == 100:
        return True
    else if square.reward == -100:
        return True
    else:
        return False

def chooseNextState(Square square):
    rightVal = boardArray[square.index+1].qVal
    leftVal = boardArray[square.index-1].qVal
    upVal = boardArray[square.index+4].qVal
    downVal = boardArray[square.index-4].qVal
    maxVal = max(rightVal, leftVal, upVal, downVal)
    
    bestState = None 

    if maxVal==rightVal:
        bestState = boardArray[square.index+1]
        bestChoicesArray.append("right")
    else if maxVal==leftVal:
        bestState = boardArray[square.index-1]
        bestChoicesArray.append("left")
    else if maxVal==upVal:
        bestState = boardArray[square.index+4]
        bestChoicesArray.append("up")
    else if maxVal==downVal:
        bestState = boardArray[square.index-4]
        bestChoicesArray.append("down")

    if  np.random.random() < epsilonGreedy:
        return bestState

    else:
        switch(np.random.randint(4)){
            case 0:
                bestState = boardArray[square.index+1]
            case 1:
                bestState = boardArray[square.index-1]  
            case 2:
                bestState = boardArray[square.index+4]
            case 3:
                bestState = boardArray[square.index-4]
        }
        return bestState


def updateQVal (Square state):
    print("current q val = ",state.qVal)
    newQVal = chooseNextState (state).qVal
    tempQval = ((1-learnRate) * state.qVal) + learnRate[state.reward + discountRate *newQVal]
    state.qVal = tempQval
    print("new q val = ",state.qVal)



#set q values
for i in range 0,100000,1:
    for i in range (0,16,1):
        updateQVal(boardArray[i])
    
    


#for i in range 1,17,1:
#    print(i, " " ,bestChoicesArray[i])



