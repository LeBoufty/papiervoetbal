from enum import Flag, auto;

class Edges(Flag):
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()
    TOPLEFT = auto()
    TOPRIGHT = auto()
    BOTTOMLEFT  = auto()
    BOTTOMRIGHT = auto()
    EMPTY       = auto() # doesn't actually mean that it has nothing
                         # is instead used to create an empty edge flag
                         # and then add other edges onto it

class Node:
    isEdge = False
    edges = Edges.EMPTY
    xPos = 0
    yPos = 0
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    def getAdjacentPos(self):
        return list(
                filter(lambda x: x[0] >= 0 and x[1] >= 0,
                [(self.xPos + 1, self.yPos), 
                (self.xPos - 1, self.yPos), 
                (self.xPos, self.yPos + 1), 
                (self.xPos, self.yPos - 1)]))

    def getNeighborPos(self):
        return list(
                filter(lambda x: x[0] >= 0 and x[1] >= 0,
                [(self.xPos + 1, self.yPos), 
                (self.xPos - 1, self.yPos), 
                (self.xPos, self.yPos + 1), 
                (self.xPos, self.yPos - 1), 
                (self.xPos + 1, self.yPos + 1), 
                (self.xPos - 1, self.yPos - 1), 
                (self.xPos + 1, self.yPos - 1), 
                (self.xPos - 1, self.yPos + 1)]))

class Board:
    nodes = [[]]
    def __init__(self, bitMap):
        for i in range(0,len(bitMap)):
            self.nodes.append([])
            for j in range(0,len(bitMap[i])):
                self.nodes[i].append(None)
                if (bitMap[i][j]):
                    self.nodes[i][j] = Node(i,j)
        self.setEdges()

    def addEdge(self,x,y,xs,ys):
        # 1
        # 2
        if (x < xs and y == ys):
            self.nodes[x ][y ].edges |= Edges.BOTTOM
            self.nodes[xs][ys].edges |= Edges.TOP

        # 2
        # 1
        if (x > xs and y == ys):
            self.nodes[x ][y ].edges |= Edges.TOP
            self.nodes[xs][ys].edges |= Edges.BOTTOM

        # 1 2
        if (x == xs and y < ys):
            self.nodes[x ][y ].edges |= Edges.RIGHT
            self.nodes[xs][ys].edges |= Edges.LEFT

        # 2 1
        if (x == xs and y > ys):
            self.nodes[x ][y ].edges |= Edges.LEFT
            self.nodes[xs][ys].edges |= Edges.RIGHT
        
        # 1 .
        # . 2
        if (x < xs and y < ys):
            self.nodes[x ][y ].edges |= Edges.BOTTOMRIGHT
            self.nodes[xs][ys].edges |= Edges.TOPLEFT

        # 2 .
        # . 1
        if (x > xs and y > ys):
            self.nodes[x ][y ].edges |= Edges.TOPLEFT
            self.nodes[xs][ys].edges |= Edges.BOTTOMRIGHT

        # . 1
        # 2 .
        if (x < xs and y > ys):
            self.nodes[x ][y ].edges |= Edges.BOTTOMLEFT
            self.nodes[xs][ys].edges |= Edges.TOPRIGHT

        # . 2
        # 1 .
        if (x > xs and y < ys):
            self.nodes[x ][y ].edges |= Edges.TOPRIGHT
            self.nodes[xs][ys].edges |= Edges.BOTTOMLEFT

    def fillNodesEdges(self,x,y):
        if self.nodes[x][y] is None or not self.nodes[x][y].isEdge:
            return
        setAdjacent = False
        for (xs, ys) in self.nodes[x][y].getAdjacentPos():
            try:
                if self.nodes[xs][ys] is None or not self.nodes[xs][ys].isEdge:
                    continue
                self.addEdge(x,y,xs,ys)
                setAdjacent = True
            except IndexError:
                continue
        if setAdjacent:
            return

        for (xs, ys) in self.nodes[x][y].getNeighborPos():
            try:
                if self.nodes[xs][ys] is None or not self.nodes[xs][ys].isEdge:
                    continue
                self.addEdge(x,y,xs,ys)
                setAdjacent = True
            except IndexError:
                continue

    def fillEdges(self):
        for i in range(0, len(self.nodes)):
            for j in range(0, len(self.nodes[i])):
                self.fillNodesEdges(i,j)

    def onBoard(self, i, j):
        return i < len(self.nodes) and j < len(self.nodes[i]) and i >= 0 and j >= 0

    def exists(self, i, j):
        return self.onBoard(i,j) and self.nodes[i][j] is not None
        

    # Checks if node is on the edge, if it is, changes it's isEdge
    def setEdges(self):
        for i in range(0, len(self.nodes)):
            for j in range(0, len(self.nodes[i])):
                if not self.exists(i,j):
                    continue
                existingNeighbors = list(filter(lambda x: self.exists(x[0],x[1]), self.nodes[i][j].getNeighborPos()))
                if len(existingNeighbors) < 8:
                    self.nodes[i][j].isEdge = True
        self.fillEdges()

    # idk how to do flask so have console print instead >:)
    def print(self):
        for row in self.nodes:
            top    = ""
            middle = ""
            bottom = ""
            for node in row:
                if node is None:
                    top    += '   '
                    middle += '   '
                    bottom += '   '
                    continue
                # pretty ugly......
                if Edges.TOPLEFT in node.edges:
                    top += '\\'
                else: 
                    top += ' '
                if Edges.TOP in node.edges:
                    top += '|'
                else: 
                    top += ' '
                if Edges.TOPRIGHT in node.edges:
                    top += '/'
                else: 
                    top += ' '

                if Edges.LEFT in node.edges:
                    middle += '-'
                else: 
                    middle += ' '
                middle +='.'
                if Edges.RIGHT in node.edges:
                    middle += '-'
                else: 
                    middle += ' '

                if Edges.BOTTOMLEFT in node.edges:
                    bottom += '/'
                else: 
                    bottom += ' '
                if Edges.BOTTOM in node.edges:
                    bottom += '|'
                else: 
                    bottom += ' '
                if Edges.BOTTOMRIGHT in node.edges:
                    bottom += '\\'
                else: 
                    bottom += ' '
            print(top)
            print(middle)
            print(bottom)

bitMap = [[0, 0, 1, 1, 1, 0, 0],
          [0, 0, 1, 1, 1, 0, 0],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [0, 0, 1, 1, 1, 0, 0],
          [0, 0, 1, 1, 1, 0, 0]]

board = Board(bitMap)
board.print()
