import collections
import math
from tracemalloc import start

class Puzzle:
    def __init__(self, board):
        self.width = len(board[0])
        self.height = len(board)
        self.board = board
        self.flat_statelist = [item for row in self.board for item in row]

    @property
    def manhattan(self):
        mandistance = 0
        for item in self.flat_statelist:
            y,x = [(index+self.height, row.index(item)+self.width) for index, row in enumerate(self.board) if item in row][0]
            dy,dx = math.floor(item / self.width)+self.height, (item % self.width)+self.width
            direcs = [(dy,dx),(dy-self.height,dx),(dy+self.height,dx),(dy,dx-self.width),(dy,dx+self.width)]
            arrdistances = []
            for r,c in direcs:
                arrdistances.append(abs(r-y)+abs(c-x))
            mandistance += min(arrdistances)
        return mandistance 
    
    def posCurrentItem(self,item):
        return [(index, row.index(item)) for index, row in enumerate(self.board) if item in row][0]
        
    @property
    def heuristic(self):
        misplacedcounter = 0
        for item in self.flat_statelist:
            if self.flat_statelist.index(item) != item:
                misplacedcounter += 1
        return misplacedcounter

    def actions(self,item):
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        i, j = self.posCurrentItem(item)
        direcs = {'R':(i, j+1),
                    'L':(i, j-1),
                    'D':(i+1, j),
                    'U':(i-1, j)}
        for action, (r, c) in direcs.items():
            if r < 0: r = self.height-1 # di qua bien tren
            if r >= self.height: r = 0 # di qua bien duoi
            if c < 0 : c = self.width-1 # di qua bien trai
            if c >= self.width: c = 0 # di qua bien phai
            # chi phi buoc di 
            itemSwap = self.board[r][c]
            cost = -1 if (self.manhattanItem(itemSwap,r,c) - self.manhattanItem(itemSwap,i,j)) > 0 else 1
            move = create_move((i,j), (r,c)), action, cost
            moves.append(move)        
        return moves
    
    def manhattanItem(self,item,y,x):
        dy,dx = math.floor(item / self.width), (item % self.width)
        mandistance = abs(dy-y)+abs(dx-x)
        return mandistance

    def copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def _move(self, at, to):
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return Puzzle(copy.board)

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row

class Node:
    def __init__(self, puzzle, parent=None, action='', cost=0, start = None):
        self.puzzle = puzzle
        self.parent = parent
        self.cost = cost
        self.start = start
        if (self.parent != None):
            self.action = parent.action + action
            self.cost = parent.cost + cost
            self.g = parent.g + 1
        else:
            self.action = ''
            self.g = 0

    @property
    def state(self):
        return str(self)

    def actions(self,item):
        return self.puzzle.actions(item)
    
    @property
    def stateList(self):
        return self.puzzle.flat_statelist

    @property
    def h (self):
        return self.puzzle.heuristic

    @property
    def m(self):
        return self.puzzle.manhattan

    @property
    def f(self):
        return self.m + self.g + self.cost

    def findPostStart(self,item):
        return self.puzzle.posCurrentItem(item)

    def __str__(self):
        return str(self.puzzle)

class Solver:
    def __init__(self, start):
        self.start = start
    
    def solve1(self):
        nodeInit = Node(self.start)
        queueRoute = collections.deque([nodeInit])
        for item in nodeInit.stateList:
            queue = collections.deque([nodeInit])
            seen = set()
            seen.add(nodeInit.state)
            start = nodeInit.findPostStart(item)
            while queue:
                queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
                node = queue.popleft()
                if node.h <= 2:
                    print('end node start {} action {} steps {} '.format(node.start, node.action, node.g))
                    queueRoute.appendleft(node)
                    break
                for move, action, cost in node.actions(item):
                    child = Node(move(),node,action,cost,start)
                    # print('node {}  action {} heuristic {} manhattan {}'.format(child.stateList, child.action, child.h, child.m))
                    if child.state not in seen:
                        queue.appendleft(child)
                        seen.add(child.state)
        # queueRoute = collections.deque(sorted(list(queueRoute), key=lambda node: node.g))
        # endNode = queueRoute.popleft()
        # y,x = endNode.start
        # return '{}{}\n{}\n{}'.format(x,y,len(node.g),endNode.action)

    def solve2(self):
        nodeInit = Node(self.start)
        queue = collections.deque([nodeInit])
        seen = set()
        seen.add(nodeInit.state)
        y,x = nodeInit.findPostStart(0)
        move = ''
        while queue:
            queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
            node = queue.popleft()
            # print('best node {}  action {} heuristic {} manhattan {}'.format(node.stateList, node.action, node.h, node.m))
            if node.action is not None: move = node.action
            if node.h <= 2:
                return '1\n{}{}\n{}\n{}'.format(x,y,len(move),move)
            for move, action, cost in node.actions(0):
                child = Node(move(), node, action, cost)
                # print('node {}  action {} heuristic {} manhattan {}'.format(child.stateList, child.action, child.h, child.m))
                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)

def convertTo2D(input,col,row):
    arr1d = list(map(int,input.split(",")))
    arr2d = []
    for i in range(row):
        arr2d.append(arr1d[i*col:i*col+col])
    return arr2d
