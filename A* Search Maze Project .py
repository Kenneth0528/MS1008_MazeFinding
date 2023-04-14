import numpy as np
import matplotlib.pyplot as plt
from seaborn import heatmap
import queue
import time

mazeOri = open("maze.txt", "r") #a file of 2601 row with each row having a single boolean value 
matrix = [] #data structure is a list
for i in range(51):
    row = [] #making each row in the maze a list by itself
    for j in range(51): #number of values per row 
        value = mazeOri.readline() #remove the newline character
        row.append(value)
    matrix.append(row) #create a matrix of 51*51 
    
print(type(matrix[0][0])) #assess if the condition paramter used below is string or boolean value 

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == "True\n":
            matrix[i][j] = 1
        else:
            matrix[i][j] = 0
        
print(matrix)
mazeGrid = np.array(matrix) #converting list into a numpy array.

def showBinaryMaze(mazemap):
    (height, width) = mazemap.shape 
    mazemap = mazemap * 255  #scales from 0 and 1 to 0
    f = plt.figure(figsize = (width, height))
    heatmap(mazemap, vmin = 0, vmax = 255, cmap = "Greys", cbar = False) 
    
showBinaryMaze(mazeGrid)
matrix2 = []
for i in range(51):
    row = [] #initialise an empty list that will be the row of the final matrix
    for j in range(51):
        value2 = matrix[j][i] #make the first value of each list into a new list i.e. read the data vertically
        row.append(value2) #add each of the first value to the empty list of row 
    matrix2.append(row) #after 51 values is added, add the row list into the matrix2 

mazeGrid2 = np.array(matrix2) #makes it an array
showBinaryMaze(mazeGrid2) #display matrix2 

def showMazeProblem(maze, start, end): 
    (height, width) = maze.shape
    maze = maze * 255 #scales to fix the problem of a integer matrix
    maze[start[0]][start[1]]=150 #change the colour of the starting point
    maze[end[0]][end[1]]=80 
    f = plt.figure(figsize = (width,height))
    heatmap(maze,  cmap = "YlGnBu", cbar = True)

Start = list(input("Please insert the starting location separated by comma: ").split(","))
Start[0], Start[1]=int(Start[0]), int(Start[1])
Start = tuple(Start) #make the starting point a tuple in the form (x, y)

#if the starting point is on the wall
while not mazeGrid2[Start[0]][Start[1]] == 0:
    print("The starting point is a wall, please select a different point")
    Start = list(input("Please insert the starting location separated by comma: ").split(","))
    Start[0], Start[1]=int(Start[0]), int(Start[1])
    Start = tuple(Start)

Goal = (47, 1) #as required by the project
showMazeProblem(mazeGrid2, Start, Goal)

def heuristic (nodeA, nodeB): #define a distance 
    (xA, yA) = nodeA #coordinate of point A
    (xB, yB) = nodeB #coordinate of point B
    distance = abs(xA-xB) + abs(yA-yB) #absolute distance between A and B
    return distance

def neighbors(maze, node):
    x, y = node[0], node[1] #assign x and y as the coordinate of node 
    neighbors = [] #initiate a empty list
    if 0 <= x+1 <= len(maze[y]) and 0 <= y <= len(maze) and maze[x+1][y] == 0: #assess node on the bottom
        neighbors.append((x+1, y)) #if it is in the maze size and not blocked by  wall, add to list neighbor 
    if 0 <= x-1 <= len(maze[y]) and 0 <= y <= len(maze) and maze[x-1][y] == 0: #assess node on the top
        neighbors.append((x-1, y)) 
    if 0 <= x <= len(maze[y]) and 0 <= y+1 <= len(maze) and maze[x][y+1] == 0: #assess node on the left
        neighbors.append((x, y+1))
    if 0 <= x <= len(maze[y]) and 0 <= y-1 <= len(maze) and maze[x][y-1] == 0: #assess node on the right
        neighbors.append((x, y-1))
    return neighbors #return a list of possible neighbor nodes (coordinates)
        
        
def Search (maze, start, goal): 
    
    frontier = queue.PriorityQueue() #create frontier with the specific data structure priority queue
    frontier.put((0, start)) #Add the starting point with highest priority (smallest number) into the queue, frontier. 
    parent = {} #initiate a dictionary that keep track of child nodes as keys and parent nodes as values
    parent[start] = None #the starting point has no parent node, therefore assigned to none
    pathcost = {start: 0} #the pathcost from one point to the starting point, from start to start is 0. 

    
    while not frontier.empty(): 
        currentNode = frontier.get()[1] 
        
        if currentNode == goal: 
            break 
            
        for neighbor in neighbors(maze, currentNode): 
            new_cost = pathcost[currentNode] + 1 
            if neighbor not in parent or new_cost < pathcost[neighbor]: 
                pathcost[neighbor] = new_cost 
                priority = new_cost + heuristic(neighbor, goal) 
                frontier.put((priority, neighbor)) 
                parent[neighbor] = currentNode 
    
    if goal not in parent:
        print("no path found to the goal")
    return parent, pathcost

def pathfinding(parent, start, goal): #reverse track when the goal has been found
    path = [] #initiate the empty list to track the path
    currentNode = goal #start with the goal that has been identified
    
    while currentNode != start: #while it has not fully backtracked to the starting point
        path.append(currentNode) #add the current node to the path, initially, it is the goal
        currentNode = parent[currentNode] #update the current node as its parent to backtrack the paths 
        

    path.reverse() #reverse to go from start to the end
    path.pop() #remove the goal from the path
    
    return path

ExploredNodes,ExploredPathCost = Search(mazeGrid2, Start, Goal)
PathFound = pathfinding(ExploredNodes, Start, Goal)
print(PathFound)

def ShowMazePath(maze, path, start, goal):
    height, width = maze.shape
    maze = maze * 255 #scales so that the matrix is now full of 0 and 255's. 
    maze[start[0]][start[1]]=60 #makes starting point a different colour
    maze[goal[0]][goal[1]]=190 #makes the ending point a different colour
    
    for node in path:
        maze[node[0]][node[1]] = 125 #for every node in path, change its colour by changing its position value to 125
    
    f = plt.figure(figsize = (width,height))
    heatmap(maze,  cmap = "YlGnBu", cbar = True)


#print("Number of Nodes explored:", len(ExploredNodes)) #print the number of explored nodes
#print("Total nodes visited: ", ProcessedNodes) #print the number of processed nodes
print("Shortest distance: ", len(PathFound) + 1) #print the shortest distance by counting the number of nodes in PathFound
ShowMazePath(mazeGrid2, PathFound, Start, Goal) #show the path, numpy array.

import matplotlib.pyplot as plt
from IPython.display import clear_output
import time
from matplotlib.animation import FuncAnimation

def ShowMazePath_Ani(maze, path, start, goal):
    height, width = maze.shape
    maze = maze * 255
    maze[start[0]][start[1]] = 60
    maze[goal[0]][goal[1]] = 190
    maze_copy = maze.copy()
    
    for i in range(len(path)):
        node = path[i]
        maze_copy[node[0]][node[1]] = 125

        plt.imshow(maze_copy, cmap="YlGnBu")
        plt.axis('off')
        plt.show()
        clear_output(wait=True)
        time.sleep(0.1)
        
ShowMazePath_Ani(mazeGrid2, PathFound, Start, Goal)
        

