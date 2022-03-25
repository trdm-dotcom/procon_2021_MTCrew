import collections
import sys
from tracemalloc import start
import numpy as np
import math

class Puzzle:
    def __init__(self, board):
        self.width = len(board[0])
        self.height = len(board)
        self.board = board
        self.flat_statelist = [item for row in self.board for item in row]

    def manhattanItem(self,item,y,x):
        dy,dx = math.floor(item / self.width), (item % self.width)
        mandistance = abs(dy-y)+abs(dx-x)
        return mandistance

    def arrayToString(self,s):
        return (" ".join(s))

    def shufferArray(self,arr):
        seen = set()
        seen.add(self.arrayToString(arr))
        arrShuff = [self.arrayToString(arr)]
        for i in range(len(arr)):
            for j in range(len(arr)):
                tempArr = arr
                if i == j: continue
                temp = tempArr[i]
                tempArr[i] = tempArr[j]
                tempArr[j] = temp
                if self.arrayToString(tempArr) not in seen:
                    arrShuff.append(self.arrayToString(tempArr))
                    seen.add(self.arrayToString(tempArr))    
        return arrShuff
    
    def findPosItem(self,item):
        y,x = self.posCurrentItem(item)
        dy,dx = math.floor(item / self.width), (item % self.width)
        return y,x,dy,dx

    def posCurrentItem(self,item):
        return [(index, row.index(item)) for index, row in enumerate(self.board) if item in row][0]

    def directionMoveInMap(self,item):
        y,x,dy,dx = self.findPosItem(item)
        delX,delY = (dx-x),(dy-y)
        moveX = "R" if delX > 0 else "L"
        moveY = "D" if delY > 0 else "U"
        arrX = [moveX for i in range(abs(delX))]
        arrY = [moveY for i in range(abs(delY))]
        arr = arrX + arrY
        return self.shufferArray(arr);

    def directionMoveCrossBorder(self,item):
        y,x,dy,dx = self.findPosItem(item)
        direcs = [(dy-self.height,dx),(dy+self.height,dx),(dy,dx-self.width),(dy,dx+self.width)]
        arrdistances = []
        for r,c in direcs:
            arrdistances.append(abs(r-y)+abs(c-x))
        index = [i for i, x in enumerate(arrdistances) if x == min(arrdistances)]    
        target = [direcs[i] for i in index]
        arrMoves=[]
        for r,c in target:
            delY,delX = r-y,c-x
            jumpY,jumpX = None,None
            if r == (-self.height or r == 2*self.height-1 or r == 0 or r == self.height-1) and abs(delY) == self.height-1:
                jumpY = "JU" if delY < 0 else "JD"
            if c == (-self.width or c == 2*self.width-1  or c == 0 or c == self.width-1) and abs(delX) == self.width-1:
                jumpX = "JL" if delX < 0 else "JR"        
            moveY = "U" if delY < 0 else "D"
            moveX = "R" if delX > 0 else "L"
            arrX = [moveX for i in range(abs(delX))]
            arrY = [moveY for i in range(abs(delY))]
            arr = arrX + arrY
            arrMoves += self.shufferArray(arr)
            if jumpY is not None:
                arrMoves.append(self.arrayToString(arrX)+" "+jumpY)
            elif jumpX is not None:
                arrMoves.append(self.arrayToString(arrY)+" "+jumpX)
        return arrMoves

    @property
    def manhattanMap(self):
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

    @property
    def heuristic(self):
        misplacedcounter = 0
        for item in self.flat_statelist:
            if self.flat_statelist.index(item) != item:
                misplacedcounter += 1
        return misplacedcounter


    def actions(self,item,action):
        def create_move(at, to):
            return lambda: self._move(at, to)

        i, j = self.posCurrentItem(item)
        if action == 'R': 
            r, c = (i, j+1) if j+1 < self.width else (i,0)
        elif action == 'L':
            r, c = (i, j-1) if j-1 > 0 else (i,self.width-1)
        elif action == 'D':
            r, c = (i+1, j) if i+1 < self.height else (0,j)
        elif action == 'U':
            r, c = (i-1, j) if i-1 > 0 else (self.height-1,j)   
        puzzle = create_move((i,j), (r,c))
        itemSwap = self.board[r][c]
        cost = -1 if (self.manhattanItem(itemSwap,r,c) - self.manhattanItem(itemSwap,i,j)) > 0 else 1
        move = puzzle, cost
        return move

    def checkPosItem(self,item):
        y,x,dy,dx = self.findPosItem(item)
        return True if abs(dy-y)+abs(dx-x) == 0 else False

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
    def __init__(self, puzzle, parent=None, action="", cost=0, start=None):
        self.puzzle = puzzle
        self.parent = parent
        self.start  = start
        if (self.parent != None):
            self.steps = parent.steps + 1
            self.cost = parent.cost + cost
            self.action = str(parent.action) + action
        else:
            self.cost = cost
            self.steps = 0
            self.action = action

    def actions(self,item,action):
        return self.puzzle.actions(item,action)
    
    def checkPosItem(self,item):
        return self.puzzle.checkPosItem(item)
    
    @property
    def manhattanMap(self):
        return self.puzzle.manhattanMap;

    def findPostStart(self,item):
        return self.puzzle.posCurrentItem(item)

    def directionMoveInMap(self,item):
        return self.puzzle.directionMoveInMap(item)
    
    def directionMoveCrossBorder(self,item):
        return self.puzzle.directionMoveCrossBorder(item);

    @property
    def h (self):
        return self.puzzle.heuristic

    @property
    def f (self):
        return self.steps + self.manhattanMap + self.cost

    @property
    def stateList(self):
        return self.puzzle.flat_statelist
    
    @property
    def state(self):
        start = ''if self.start is None else ''.join(map(str,self.start))
        return  '{}_{}_{}'.format(''.join(map(str,self.stateList)),'{}'.format(start),self.action)

    def __str__(self):
        return str(self.puzzle)

class Solver:
    def __init__(self, start):
        self.start = start

    def solve(self):
        queue = collections.deque([Node(self.start)])
        choose = 0
        result = ''
        seen = set()
        seen.add(queue[0].state)
        while queue:
            queue = collections.deque(sorted(list(queue), key = lambda node: (node.manhattanMap,node.h)))
            node = queue.popleft()
            queueRoute = collections.deque()
            # chay tung o di den vi tri dich,
            print('start {}'.format(node.stateList))
            for item in node.stateList:
                if node.checkPosItem(item): continue
                start = node.findPostStart(item)
                inMap = node.directionMoveInMap(item)
                crossBorder = node.directionMoveCrossBorder(item) # tim vi tri dich gan nhat map mo rong
                moves = inMap + crossBorder;
                # print("item {}, move : {}".format(item,moves))
                # thu cac tuyen duong di ve vi tri dich
                queueRouteItem = collections.deque()
                for move in moves:
                    moveNode = node
                    moveNode.action = ''
                    queueMove = collections.deque()
                    for action in move.split():
                        if action == 'JU':
                            action = 'D' 
                        elif action == 'JD':
                            action = 'U'
                        elif action == 'JL':
                            action = 'R'
                        elif action == 'JR':
                            action = 'L'
                        else:
                            action = action
                        step, cost = moveNode.actions(item,action)
                        stepNode = Node(step(), moveNode, action, cost, start)
                        moveNode = stepNode
                        queueMove.appendleft(moveNode)
                    routeNode = queueMove.popleft()
                    queueRouteItem.appendleft(routeNode)
                queueRouteItem = collections.deque(sorted(list(queueRouteItem), key = lambda n: (n.manhattanMap,n.f,n.h)))
                bestRouteItem = queueRouteItem.popleft()
                queueRoute.appendleft(bestRouteItem)
                print('item {}  best route {}, action {}, heuristic {}, f {}, steps {}, manhattan {}'.format(item,bestRouteItem.stateList,bestRouteItem.action,bestRouteItem.h,bestRouteItem.f,bestRouteItem.steps,bestRouteItem.manhattanMap))
            queueRoute = collections.deque(sorted(list(queueRoute), key = lambda n: (n.f,n.h)))
            bestRoute = queueRoute.popleft()
            if bestRoute.state not in seen:
                queue.appendleft(bestRoute)
                print('best route {}, action {}, heuristic {}, f {}, steps {}, manhattan {}\n'.format(bestRoute.stateList,bestRoute.action,bestRoute.h,bestRoute.f,bestRoute.steps,bestRoute.manhattanMap))
            y,x = bestRoute.start
            choose += 1
            result += "{}{}\n{}\n{}\n".format(x,y,len(bestRoute.action),bestRoute.action)
            if bestRoute.h == 0:
                return "{}\n{}".format(choose,result)       

def convertTo2D(input,col,row):
    arr1d = list(map(int,input.split(",")))
    arr2d = []
    for i in range(row):
        arr2d.append(arr1d[i*col:i*col+col])
    return arr2d

            
            