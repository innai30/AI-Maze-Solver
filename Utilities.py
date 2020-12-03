from Entities.Maze import Maze
from Entities.Node import Node


def readInstance(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()

    algorithmName = lines[0].rstrip("\n")
    mazeSize = lines[1].rstrip("\n")
    startPoint = lines[2].rstrip("\n")
    goalPoint = lines[3].rstrip("\n")


    maze = [[0 for x in range(int(mazeSize))] for y in range(int(mazeSize))]

    for i in range (0,int(mazeSize)):
        line = lines[4+i]
        splitted = line.split(',')
        for j in range(0,int(mazeSize)):
            maze[j][i] = int(splitted[j])

    splitSP = startPoint.split(',')
    splitSP[0] = int(splitSP[0])
    splitSP[1] = int(splitSP[1])
    splitGP = goalPoint.split(',')
    splitGP[0] = int(splitGP[0])
    splitGP[1] = int(splitGP[1])
    goalNode = Node(splitGP[0],splitGP[1],maze[splitGP[0]][splitGP[1]])
    startNode = Node(splitSP[0],splitSP[1],maze[splitSP[0]][splitSP[1]],None,maze[splitSP[0]][splitSP[1]],None,0)
    maze = Maze(maze, mazeSize, goalNode)

    return algorithmName,startNode,goalNode,mazeSize,maze


def getCoordsFromDirection(direction, x, y):
    if direction == 'RU':
        return x+1,y-1
    if direction == 'R':
        return x+1,y
    if direction == 'RD':
        return x+1,y+1
    if direction == 'D':
        return x,y+1
    if direction == 'LD':
        return x-1,y+1
    if direction == 'L':
        return x-1,y
    if direction == 'LU':
        return x-1,y-1
    if direction == 'U':
        return x,y-1

    return x,y

def getDirectionFromCoords(currX,currY,fatherX,fatherY):

    if (currX - fatherX) == 0 and (currY - fatherY) == -1:
        return 'U'
    if (currX - fatherX) == -1 and (currY - fatherY) == -1:
        return 'LU'
    if (currX - fatherX) == -1 and (currY - fatherY) == 0:
        return 'L'
    if (currX - fatherX) == -1 and (currY - fatherY) == 1:
        return 'LD'
    if (currX - fatherX) == 0 and (currY - fatherY) == 1:
        return 'D'
    if (currX - fatherX) == 1 and (currY - fatherY) == 1:
        return "RD"
    if (currX - fatherX) == 1 and (currY - fatherY) == 0:
        return 'R'
    if (currX - fatherX) == 1 and (currY - fatherY) == -1:
        return 'RU'
    return 'ERROR'

def evaluateStats(algorithmName,maze,solved,solutionNode,frontierPriorityQueue,exploredCounter,runTime,isHeuristic,heuristicName = None,heuristicAvg = None):

    # stats calculation

    optimalSolutionCost = solutionNode.pathCost
    moves = [] # stack
    movesString = ''
    solutionDepth = 0
    node = solutionNode

    while node.fatherNode is not None:
        direction = (getDirectionFromCoords(node.x, node.y, node.fatherNode.x, node.fatherNode.y))
        direction = direction[::-1]
        moves += direction + '-'
        solutionDepth+=1
        node = node.fatherNode
    while len(moves) is not 0:
        movesString += moves.pop()
    movesString = movesString[1:]

    EBF = exploredCounter**(1/solutionDepth)

    minDepth = None
    maxDepth = None
    sumDepth = 0
    frontierCounter = len(frontierPriorityQueue.heap)

    for i in range(0,frontierCounter):
        node = frontierPriorityQueue.pop()
        sumDepth += node.depth

        if  minDepth == None and maxDepth == None:
            minDepth = node.depth
            maxDepth = node.depth
        else:
            if node.depth < minDepth:
                minDepth = node.depth
            if node.depth > maxDepth:
                maxDepth = node.depth

    avgDepth = sumDepth / frontierCounter



    if isHeuristic == False:
        heuristicName = 'None'
        heuristicAvg =  '-'

    print("algorithm name: {}".format(algorithmName))
    print("moves: {}".format(movesString))
    print("optimal path cost: {}".format(optimalSolutionCost))
    print("epxnaded nodes: {}".format(exploredCounter))
    print("solution depth: {}".format(solutionDepth))
    print("penetration rate: {}".format(solutionDepth / exploredCounter))
    print("solved successfully: {}".format(solved))
    print("run time: {}".format(runTime))
    print("EBF: {}".format(EBF))
    print("heurstic used: {}".format(heuristicName))
    print("average heuristic values: {}".format(heuristicAvg))
    print("min depth: {}".format(minDepth))
    print("average depth: {}".format(avgDepth))
    print("max depth: {}".format(maxDepth))





    return