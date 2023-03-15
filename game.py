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
edges = [[Edges.TOPLEFT,    Edges.TOP,      Edges.TOPRIGHT   ],
         [Edges.LEFT,       Edges.EMPTY,    Edges.RIGHT      ],
         [Edges.BOTTOMLEFT, Edges.BOTTOM,   Edges.BOTTOMRIGHT]]

def getSign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0

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
    ballX = 0
    ballY = 0
    def __init__(self, bitMap, ballX, ballY):
        self.ballX = ballX
        self.ballY = ballY
        for i in range(0,len(bitMap)):
            self.nodes.append([])
            for j in range(0,len(bitMap[i])):
                self.nodes[i].append(None)
                if (bitMap[i][j]):
                    self.nodes[i][j] = Node(i,j)
        self.setEdges()

    def getEdge(self, x, y, xs, ys):
        return edges[getSign(xs - x) + 1][getSign(ys - y) + 1]

    def addEdge(self, x, y, xs, ys):
        if not self.exists(x,y) or not self.exists(xs,ys):
            return
        self.nodes[x][y].edges   |= self.getEdge(x, y, xs, ys)
        self.nodes[xs][ys].edges |= self.getEdge(xs, ys, x, y)

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
        
    def canAddEdge(self, x, y, xs, ys):
        if not self.exists(x,y) or not self.exists(xs, ys):
            return False
        if self.nodes[x][y].edges & self.getEdge(x, y, xs, ys):
            return False
        if self.nodes[xs][ys].edges & self.getEdge(xs, ys, x, y):
            return False
        return self.diagonalCheck(x, y, xs, ys)

    def diagonalCheck(self, x, y, xs, ys):
        edge = self.getEdge(x, y, xs, ys)

        oppositeTop = {Edges.TOPLEFT:  Edges.BOTTOMLEFT,
                       Edges.TOPRIGHT: Edges.BOTTOMRIGHT}

        if (toCheck := oppositeTop.get(edge)) is not None:
            if toCheck & Edges.BOTTOMLEFT and not self.exists(x, y - 1):
                return False
            if toCheck & Edges.BOTTOMRIGHT and not self.exists(x, y + 1):
                return False
            if not self.exists(x - 1, y):
                return False
            return not self.nodes[x - 1][y].edges & toCheck 

        oppositeBottom = {Edges.BOTTOMLEFT:  Edges.TOPLEFT,
                          Edges.BOTTOMRIGHT: Edges.TOPRIGHT}
        
        if (toCheck := oppositeBottom.get(edge)) is not None:
            if toCheck & Edges.TOPLEFT and not self.exists(x, y - 1):
                return False
            if toCheck & Edges.TOPRIGHT and not self.exists(x, y + 1):
                return False
            if not self.exists(x + 1, y):
                return False
            return not self.nodes[x + 1][y].edges & toCheck 
        return True
        

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
    def __str__(self):
        out = ""
        for i in range(0, len(self.nodes)):
            top    = ""
            middle = ""
            bottom = ""
            for j in range(0, len(self.nodes[i])):
                if self.nodes[i][j] is None:
                    top    += '   '
                    middle += '   '
                    bottom += '   '
                    continue
                # pretty ugly......
                if Edges.TOPLEFT in self.nodes[i][j].edges:
                    top += '\\'
                else: 
                    top += ' '
                if Edges.TOP in self.nodes[i][j].edges:
                    top += '|'
                else: 
                    top += ' '
                if Edges.TOPRIGHT in self.nodes[i][j].edges:
                    top += '/'
                else: 
                    top += ' '

                if Edges.LEFT in self.nodes[i][j].edges:
                    middle += '-'
                else: 
                    middle += ' '
                if self.ballX == i and self.ballY == j:
                    middle += 'o'
                else:
                    middle += '.' 

                if Edges.RIGHT in self.nodes[i][j].edges:
                    middle += '-'
                else: 
                    middle += ' '

                if Edges.BOTTOMLEFT in self.nodes[i][j].edges:
                    bottom += '/'
                else: 
                    bottom += ' '
                if Edges.BOTTOM in self.nodes[i][j].edges:
                    bottom += '|'
                else: 
                    bottom += ' '
                if Edges.BOTTOMRIGHT in self.nodes[i][j].edges:
                    bottom += '\\'
                else: 
                    bottom += ' '
            out += top + "\n" + middle + "\n" + bottom + "\n"
        return out

    def kickBall(self, direction):
        for i in range(0, len(edges)):
            try:
                j = edges[i].index(direction)
                if self.canAddEdge(self.ballX, self.ballY, self.ballX + i - 1, self.ballY + j - 1):
                    self.addEdge(self.ballX, self.ballY, self.ballX + i - 1, self.ballY + j - 1)
                    self.ballX += i - 1 
                    self.ballY += j - 1
                    return True
            except ValueError:
                continue
        return False

    def canKickBall(self, direction):
        for i in range(0, len(edges)):
            try:
                j = edges[i].index(direction)
                return self.canAddEdge(self.ballX, self.ballY, self.ballX + i - 1, self.ballY + j - 1)
            except ValueError:
                continue
        return False

class Game:
    def __init__(self):
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
        self.board = Board(bitMap, 5, 3)

    def boardAsList(self):
        return [[i for i in line] for line in str(self.board).split("\n")]

    def loop(self):
        print(self.board)
        while True:
            direction = int(input("write direction: "))
            try:
                if self.board.kickBall(edges[int(direction / 3)][direction % 3]):
                    print(self.board)
                else:
                    print("Cannot make such move")
            except IndexError:
                print("Unknown move")


#game = Game()
#game.loop()

#print(game.boardAsList())
