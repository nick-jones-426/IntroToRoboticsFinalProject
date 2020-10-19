from tkinter import *
import time
import sys

# Basic Animation Framework
# adapted from 15-112 website: http://www.krivers.net/15112-s18/notes/notes-animations-part1.html

from tkinter import *
from itertools import permutations

# Define waypoint class

class Node:

	def __init__(self, index, back=-1, dist=-1):
		self.index = index
		self.back = back
		self.dist = dist

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.obstacles = addObstacles(data)
    data.waypoints = addWaypoints(data)
    data.graph = createMatrix(data)
    data.wSize = 3 # waypoints are circles with radius 2
    data.wLabelOffset = 10
    data.buttonBoundsShop = [730, 225, 820, 275]
    data.buttonBoundsLeave = [730, 290, 820, 340]
    data.inShopMode = False
    print("Welcome to Giant Eagle! Click 'Shop' to begin.")

def mousePressed(event, data):
    # use event.x and event.y
    b = data.buttonBoundsShop
    if event.x <= b[2] and event.x >= b[0] and event.y <= b[3] and event.y >= b[1]\
    and not data.inShopMode:
    	data.inShopMode = True
    	shop(data)

    z = data.buttonBoundsLeave
    if event.x <= z[2] and event.x >= z[0] and event.y <= z[3] and event.y >= z[1]:
    	print("Have a nice day!")
    	sys.exit()

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def redrawAll(canvas, data):

    # draw obstacles
	for ob in data.obstacles:
   		canvas.create_polygon(ob, fill='red')

   	# draw waypoints
	r = data.wSize
	L = data.wLabelOffset
	for i in range(len(data.waypoints)):
		way = data.waypoints[i]
		if len(way) == 2:
			text = "%d" % (i)
			canvas.create_oval(way[0]-r, way[1]-r, way[0]+r, way[1]+r, fill='blue')
			canvas.create_text(way[0]+L, way[1]-L, text=text, font=('Times', 12))

	# draw entrance/exit
	canvas.create_text(900, 490, text='(entrance)', fill='black', font=('Times', 12))
	canvas.create_text(120, 490, text='(exit)', fill='black', font=('Times', 12))

	# draw edges
	g = data.graph
	for j in range(len(g)):
		for k in range(len(g)):
			if g[j][k] != 0:
				w1 = data.waypoints[j]
				w2 = data.waypoints[k]
				canvas.create_line(w1, w2, fill='blue')

	# draw buttons
	b = data.buttonBoundsShop
	tpoints = [(b[2] - b[0])//2 + b[0], (b[3] - b[1])//2 + b[1]]
	canvas.create_rectangle(b, fill='black')
	canvas.create_text(tpoints, text='Shop', fill='white', font=('Times', 16))

	x = data.buttonBoundsLeave
	xpoints = [(x[2] - x[0])//2 + x[0], (x[3] - x[1])//2 + x[1]]
	canvas.create_rectangle(x, fill='black')
	canvas.create_text(xpoints, text='Leave', fill='white', font=('Times', 16))

#############################

def addObstacles(data):
	top = 100
	bot = 400
	obstacles = []
	obstacles.append([100, top, 200, top, 200, 400, 100, 350])
	obstacles.append([300, top, 400, top, 400, bot, 300, bot])
	obstacles.append([500, top, 600, top, 600, bot, 500, bot])
	obstacles.append([700, top, 850, 200, 850, bot, 700, bot])
	obstacles.append([900, 0, 1000, 0, 1000, 200, 950, 200, 900, 50])
	obstacles.append([0, 400, 50, 400, 50, 500, 0, 500])
	obstacles.append([300, 480, 800, 480, 800, 500, 300, 500])
	return obstacles

def addWaypoints(data):
	top = 50
	bot = 450
	waypoints = []
	waypoints.append([50, top])  # 0
	waypoints.append([250, top]) # 1
	waypoints.append([450, top]) # 2
	waypoints.append([650, top]) # 3
	waypoints.append([800, top]) # 4
	waypoints.append([900, 200]) # 5
	waypoints.append([50, 350])  # 6
	waypoints.append([250, bot]) # 7
	waypoints.append([450, bot]) # 8
	waypoints.append([650, bot]) # 9
	waypoints.append([900, bot]) # 10
	waypoints.append([950, 490]) # 11 - entrance
	waypoints.append([150, 490]) # 12 - exit
	waypoints.append([150, bot]) # 13
	return waypoints

def createMatrix(data):
	# create an adjacency matrix
	g = []
	g.append([0, 200, 0, 0, 0, 0, 300, 0, 0, 0, 0, 0, 0, 0])     # 0 
	g.append([200, 0, 200, 0, 0, 0, 0, 400, 0, 0, 0, 0, 0, 0])   # 1 
	g.append([0, 200, 0, 200, 0, 0, 0, 0, 400, 0, 0, 0, 0, 0])   # 2
	g.append([0, 0, 200, 0, 150, 0, 0, 0, 0, 400, 0, 0, 0, 0])   # 3
	g.append([0, 0, 0, 150, 0, 180, 0, 0, 0, 0, 0, 0, 0, 0])     # 4
	g.append([0, 0, 0, 0, 180, 0, 0, 0, 0, 0, 250, 0, 0, 0])     # 5
	g.append([300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 172, 141])   # 6
	g.append([0, 400, 0, 0, 0, 0, 0, 0, 200, 0, 0, 0, 108, 100]) # 7
	g.append([0, 0, 400, 0, 0, 0, 0, 200, 0, 200, 0, 0, 0, 0])   # 8
	g.append([0, 0, 0, 400, 0, 0, 0, 0, 200, 0, 250, 0, 0, 0])   # 9
	g.append([0, 0, 0, 0, 0, 250, 0, 0, 0, 250, 0, 64, 0, 0])    # 10
	g.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64, 0, 0, 0])        # 11
	g.append([0, 0, 0, 0, 0, 0, 172, 108, 0, 0, 0, 0, 0, 40])    # 12
	g.append([0, 0, 0, 0, 0, 0, 141, 100, 0, 0, 0, 0, 40, 0])    # 13
	return g

def search(data, startNode, endNode):
	# imlement Dijkstra's Search algorithm using specified endpoints
	# startNode, endNode are integers on interval [0, 13]
	# open list O contains Node objects
	# startNode backpoints to -1

	g = data.graph
	beginNode = Node(startNode, -1, 0)
	O = [beginNode]
	C = []
	node = O.pop(0)
	while node.index != endNode:
		for i in range(len(g)):
			inClosed = checkMembership(data, C, i)
			if inClosed == -1 and g[node.index][i] != 0:
				edge = g[node.index][i]
				newDist = node.dist + edge
				newNode = Node(i, node.index, newDist)
				O.append(newNode)

		C.append(node)
		if len(O) > 0:
			nextNode = getShortestDist(data, O) # returns index in open list
		else:
			return [] # no path found
		node = O.pop(nextNode)
		
	# add last node
	C.append(node)				

	# create path list from backpointers and reverse
	pathNode = C.pop() # endNode
	path = []
	while pathNode.index != startNode:
		path.append(pathNode.index)
		nextNode = pathNode.back
		for j in range(len(C)):
			sample = C[j]
			if sample.index == nextNode:
				pathNode = C.pop(j)
				break
	path.append(startNode)
	path.reverse()
	# print(path)

	return path

def getShortestDist(data, O):
	# returns index of shortest dist in open list

	minDist = 1000000
	minOpenIndex = -1
	for j in range(len(O)):
		node = O[j]
		if node.dist < minDist:
			minDist = node.dist
			minOpenIndex = j
	return minOpenIndex


def checkMembership(data, L, node):
	# checks if node is in a list
	# returns index or -1

	result = -1
	for i in range(len(L)):
		elt = L[i]
		if elt.index == node:
			result = i
	return result 

def shop(data):
	# take user input, output grocery list

	print("***************************************************")
	print("Enter a shopping list of nodes, one at a time.")
	print("Node 11 is the store's entrance.")
	print("Node 12 is the store's exit.")
	print("Therefore, you cannot shop for nodes 11 or 12.")
	print("List as many grocery nodes as you'd like.")
	print("Press 'enter' when finished entering nodes.")
	print("***************************************************")

	node = input("Node: ")
	nodes = []
	acceptable = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '13']
	while node != 'done' and node != '':
		if node not in acceptable: 
			print("Invalid entry, please try again.")
			node = input("Node: ")
			continue
		nodeInt = int(node)
		if nodeInt not in nodes:
			nodes.append(nodeInt)
		node = input("Node: ")

	shortestPath = []
	shortestDist = 1000000

	if len(nodes) < 8:
		possiblePaths = list(permutations(nodes)) # horribly inefficient approach
		# buying max 12 items yields ~479,000,000 permutations, which is a few too many
		# For today, the Traveling Salesman problem remains unsolved :(

		# find shortest path
		for elt in possiblePaths:
			option = list(elt)
			option.insert(0, 11)
			option.append(12)
			comp = compositePath(data, option)
			length = getPathLength(data, comp)
			if length < shortestDist:
				shortestDist = length
				shortestPath = comp
	else:
		nodes.insert(0, 11)
		nodes.append(12)
		shortestPath = compositePath(data, nodes)
		# sacrifice path length optimization for computational efficiency

	print("")
	print("Shopping list:")
	print(nodes)
	print("")
	if len(nodes) < 10:
		print("Shortest path required to get every item on your list:")
	else:
		print("Path required to get every item on your list:")
	print(shortestPath)
	print("")
	print("Click 'Shop' to test another list.")

	data.inShopMode = False

	return 0

def compositePath(data, nodes):
	# visit a series of waypoints in specified order
	# nodes is a list 

	if len(nodes) < 2:
		return nodes

	fullPath = []
	i = 1
	j = 2
	fullPath.append(search(data, nodes[0], nodes[1]))
	if len(nodes) > 2:
		while i < len(nodes) - 2:
			path = search(data, nodes[i], nodes[j])
			fullPath.append(path[1:])
			i += 1
			j += 1
		fullPath.append(search(data, nodes[i], nodes[j])[1:])

	# flatten list
	flatFullPath = []
	for sub in fullPath:
		for item in sub:
			flatFullPath.append(item)

	return flatFullPath

def getPathLength(data, path):
	# take list of nodes and compute path length

	if len(path) < 2:
		return 0

	i = 0
	j = 1
	totalLength = 0
	while i < len(path) - 1:
		l = data.graph[path[i]][path[j]]
		totalLength = totalLength + l
		i += 1
		j += 1

	return totalLength

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

run(1000, 500)