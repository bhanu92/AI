import sys
import copy
import math
import time

openList = []
closedList = []
initialState = []
finalState = [1, 2, 3, 8, 0, 4, 7, 6, 5]
# nodeDictionary = {}
outFiles = ['OutfileHeuristic1.txt',
            'OutfileHeuristic2.txt',
            'OutfileHeuristic3.txt']

# 3,6,4,0,1,2,8,7,5


class eightPuzzle():
    global openList
    global closedList
    # global nodeDictionary

    def __init__(self):
        pass

    def getDisplacedTiles(self, currState, finState):
        count = 0
        for i in range(len(currState)):
            if currState[i] != finState[i] and currState[i] != 0:
                count = count + 1
        return count

    def getManhattanDistance(self, currState, finState):
        distance = 0
        for i in range(len(currState)):
            if (currState[i] != 0 and currState[i] != finState[i]):
                j = 0
                for j in range(0, 9):
                    if finState[j] == currState[i]:
                        break
                distance += abs(int(i / 3) - int(j / 3)) + abs(
                    int(i % 3) - int(j % 3))
        return distance

    def heuristicFunction(self, currState, finState):
        h1 = self.getDisplacedTiles(currState, finState)
        h2 = self.getManhattanDistance(currState, finState)
        return [h1, h2, h1 + h2]

    def generateNodes(self, currState, cost, heuristic):
        # print("List in generateNodes function: ", currState)
        nodeSuccessors = []
        for i in range(len(currState)):
            # print(i)
            # print(currState)
            if currState[i] == 0:
                # print("Zero'th position in current node is :", i)
                x = int(i / 3)
                # print(x)
                y = int(i % 3)
                # print(y)
                break

        ''' move right '''
        if y >= 0 and y < 2:
            tempList = copy.copy(currState)
            tempList[i] = copy.copy(currState[i + 1])
            tempList[i + 1] = 0
            pathCost = cost + 1
            heuristicCost = self.heuristicFunction(
                tempList, finalState)
            rightNode = [tempList, currState,
                         pathCost, heuristicCost[heuristic], 'right']
            # print("Move right: ", tempList)
            nodeSuccessors.append(rightNode)

        ''' move left '''
        if y <= 2 and y > 0:
            tempList = copy.copy(currState)
            tempList[i] = copy.copy(currState[i - 1])
            tempList[i - 1] = 0
            pathCost = cost + 1
            heuristicCost = self.heuristicFunction(
                tempList, finalState)
            leftNode = [tempList, currState,
                        pathCost, heuristicCost[heuristic], 'left']
            # print("Move left: ", tempList)
            nodeSuccessors.append(leftNode)

        ''' move up '''
        if x <= 2 and x > 0:
            tempList = copy.copy(currState)
            tempList[i] = copy.copy(currState[i - 3])
            tempList[i - 3] = 0
            pathCost = cost + 1
            heuristicCost = self.heuristicFunction(tempList, finalState)
            finalCost = pathCost + heuristicCost[2]
            upNode = [tempList, currState, pathCost,
                      heuristicCost[heuristic], 'up']
            # print("Move up: ", tempList)
            nodeSuccessors.append(upNode)

        ''' move down '''
        if x >= 0 and x < 2:
            tempList = copy.copy(currState)
            tempList[i] = copy.copy(currState[i + 3])
            tempList[i + 3] = 0
            pathCost = cost + 1
            heuristicCost = self.heuristicFunction(tempList, finalState)
            downNode = [tempList, currState,
                        pathCost, heuristicCost[heuristic], 'down']
            # print("Move down: ", tempList)
            nodeSuccessors.append(downNode)

        return nodeSuccessors

    def solve(self, heuristic):
        j = 0
        # print(i)
        while len(openList) > 0:
            # print("entered while")
            #print(j, "th iteration ")
            # print(openList)
            currentState = []
            minCost = 100
            pathCost = 0
            popIndex = 0
            tempIndex = []
            for index in range(len(openList)):
                tempList = copy.copy(openList[index])
                # print("temp list", tempList)
                totalCost = tempList[2] + tempList[3]
                if totalCost < minCost:
                    minCost = totalCost
                    currentState = tempList[0]
                    pathCost = tempList[2]
                    popIndex = index
            closedList.append(openList[popIndex])
            # print("closedList last element", closedList[-1])
            openList.pop(popIndex)
            # print("closedList", closedList)
            # print("currentState in while loop is: ", currentState)

            if currentState == finalState or j > 1000:
                print("Final State is found in ", j, " iterations")
                break
            successors = self.generateNodes(currentState, pathCost, heuristic)
            # print("Number of successors for node ",
            # currentState, "is ", len(successors))
            for i in range(len(successors)):
                notPresent = True
                node = successors[i]
                # print("successor", i, " is ", node)
                for i in range(len(closedList)):
                    temp = closedList[i]
                    if temp[0] == node[0] and (node[2] + node[3]) < (temp[2] + temp[3]):
                        openList.append(node)
                        notPresent = False
                        break
                for i in range(len(openList)):
                    temp = openList[i]
                    if temp[0] == node[0] and (node[2] + node[3]) < (temp[2] + temp[3]):
                        openList.pop(i)
                        openList.append(node)
                        notPresent = False
                        break
                if notPresent is True:
                    openList.append(node)
            '''
            print("Adding node to closed list", tempList)
            print("******************************************")
            print("Current OpenList length ", len(openList))
            for i in range(len(openList)):
                print(openList[i])
            print("Current ClosedList length ", len(closedList))
            for i in range(len(closedList)):
                print(closedList[i])
            print("******************************************")
            # time.sleep(3)
            '''
            j += 1
        return

    def shortestPath(self):
        path = []
        closedList.reverse()
        for i in range(len(closedList)):
            node = copy.copy(closedList[i])
            if node[0] == finalState:
                path.append([node[0], node[1], node[4]])

        while True:
            for i in range(len(closedList)):
                if path[-1][1] == closedList[i][0]:
                    path.append([closedList[i][0], closedList[
                                i][1], closedList[i][4]])
                    break
                if path[-1][0] == initialState:
                    return path
                    return (path)


def main():
    '''
    initialState = [1, 2, 3, 7, 0, 4, 6, 8, 5]
    finalState = [1, 2, 3, 6, 5, 4, 0, 7, 8]
    '''
    try:
        f = open('inputFile.txt', 'r')
        for num in f.read().strip().split(','):
            initialState.append(int(num))
        f.close()
    except IOError:
        print("Unable to open the inputFile.txt")
        sys.exit()

    if len(initialState) != 9 and len(initialState) != len(set(initialState)):
        print("Wrong input values in the inputFile.txt")
        sys.exit()
    puzzle = eightPuzzle()
    for i in range(1, 3):
        initialHeuristic = puzzle.heuristicFunction(
            initialState, finalState)
        openList.clear()
        closedList.clear()
        openList.append([initialState, [], 0, initialHeuristic[i], 'root'])
        outputFile = open(outFiles[i], 'w')
        sys.stdout = outputFile
        if i == 0:
            print(
                "Solving 8-puzzle with A* algorithm using Displaced Tiles as a heuristic\n")
        elif i == 1:
            print(
                "Solving 8-puzzle with A* algorithm using Manhattan Distance as a heuristic\n")
        else:
            print("Solving 8-puzzle with A* algorithm using sum of Displaced Tiles and Manhattan Distance as a heuristic\n")

        print("Initial State of the puzzle: ", initialState)
        print("Final State of the puzzle: ", finalState)
        # print(openList)
        puzzle.solve(i)
        print("Total Number of Nodes expanded to find the solution are: ",
              len(closedList) + len(openList))
        path = puzzle.shortestPath()
        path.reverse()
        print(
            "\nList Format [Current State, Previous State, gVal, hVal, Action]")
        for j in range(len(path)):
            for k in range(len(closedList)):
                if path[j][0] == closedList[k][0] and path[j][1] == closedList[k][1]:
                    print(closedList[k])
                    break
        print("Puzzle Solved")


if __name__ == "__main__":
    main()
