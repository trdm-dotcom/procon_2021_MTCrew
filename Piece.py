import numpy as np

# Piece class, holds data of each piece
class Piece:
    def __init__(self, num, s_vert, s_horz, chn, start, data, total):
        self.pieceNum = num
        self.size_vertical = s_vert
        self.size_horizontal = s_horz
        self.pieceChn = chn
        self.pieceStart = start
        self.pieceData = np.ndarray((s_vert, s_horz, chn), buffer=data, dtype=np.uint8)
        self.pieceTotal = total

        # the 4 borders of the piece
        self.sideUp = []
        self.sideRight = []
        self.sideDown = []
        self.sideLeft = []

        for i in range(self.size_horizontal):
            self.sideUp.append(self.pieceData[0][i])
            self.sideDown.append(self.pieceData[-1][i])

        for i in range(self.size_vertical):
            self.sideRight.append(self.pieceData[i][-1])
            self.sideLeft.append(self.pieceData[i][0])
        
        self.sides = [self.sideUp, self.sideRight, self.sideDown, self.sideLeft]

        self.difference = [None for x in range(total)]

        self.neighbors = [None for x in range(4)]


# determine difference of pixel's each channel value
def pixel_difference(px1, px2):
    PIXEL_DIFFERENCE_THRESHOLD = 85
    diff = 0
    for i in range(len(px1)):
        diff += abs(int(px1[i] - int(px2[i])))
    return False if diff < PIXEL_DIFFERENCE_THRESHOLD else True


# calculate different pixels between two sides
def side_difference(side1, side2):
    difference = 0
    for i in range(len(side1)):
        difference += 1 if pixel_difference(side1[i], side2[i]) else 0
    return difference
    
# calculate difference between two pieces in all directions
import numpy as np


# Piece class, holds data of each piece
class Piece:
    def __init__(self, num, s_vert, s_horz, chn, start, data, total):
        self.pieceNum = num
        self.size_vertical = s_vert
        self.size_horizontal = s_horz
        self.pieceChn = chn
        self.pieceStart = start
        self.pieceData = np.ndarray((s_vert, s_horz, chn), buffer=data, dtype=np.uint8)
        self.pieceTotal = total

        # the 4 borders of the piece
        self.sideUp = []
        self.sideRight = []
        self.sideDown = []
        self.sideLeft = []

        for i in range(self.size_horizontal):
            self.sideUp.append(self.pieceData[0][i])
            self.sideDown.append(self.pieceData[-1][i])

        for i in range(self.size_vertical):
            self.sideRight.append(self.pieceData[i][-1])
            self.sideLeft.append(self.pieceData[i][0])

        self.sides = [self.sideUp, self.sideRight, self.sideDown, self.sideLeft]

        self.difference = [None for x in range(total)]

        self.neighbors = [None for x in range(4)]


# determine difference of pixel's each channel value
def pixel_difference(px1, px2):
    PIXEL_DIFFERENCE_THRESHOLD = 25
    diff = 0
    for i in range(len(px1)):
        diff += abs(int(px1[i] - int(px2[i])))
    return False if diff < PIXEL_DIFFERENCE_THRESHOLD else True


# calculate different pixels between two sides
def side_difference(side1, side2):
    difference = 0
    for i in range(len(side1)):
        difference += 1 if pixel_difference(side1[i], side2[i]) else 0
    return difference

def piece_difference(piece1: Piece, piece2: Piece):
    vertical_12 = side_difference(piece1.sideDown, piece2.sideUp)
    vertical_21 = side_difference(piece2.sideDown, piece1.sideUp)
    horizontal_12 = side_difference(piece1.sideRight, piece2.sideLeft)
    horizontal_21 = side_difference(piece2.sideRight, piece1.sideLeft)

    # clockwise direction
    temp1 = [vertical_21, horizontal_12, vertical_12, horizontal_21]
    temp2 = [vertical_12, horizontal_21, vertical_21, horizontal_12]

    for i in range(len(temp1)):
        temp1[i] = (temp1[i], i)
        temp2[i] = (temp2[i], i)

    # non-decreasing sort of difference
    piece1.difference[piece2.pieceNum] = sorted(temp1)
    piece2.difference[piece1.pieceNum] = sorted(temp2)


# search for neighbors
def find_neighbors(piece: Piece):
    DIFFERENCE_RATE_THRESHOLD = 0.6
    candidates = [None for x in range(4)]
    # find the best candidate for each direction
    for i in range(len(piece.difference)):
        if piece.difference[i] is None:
            continue
        temp = piece.difference[i][0]
        if candidates[temp[1]] is None or candidates[temp[1]][1][0] > temp[0]:
            candidates[temp[1]] = (i, temp)

    # test if candidate is eligible as neighbor
    for entry in candidates:
        if entry is not None and entry[1][0] <= DIFFERENCE_RATE_THRESHOLD *\
                (piece.size_vertical if (entry[1][1] == 1 or entry[1][1] == 3) else piece.size_horizontal):
            piece.neighbors[entry[1][1]] = entry[0]

# calculate difference between two pieces in all directions
# def piece_difference(piece1: Piece, piece2: Piece):
#     print(piece1.pieceNum,piece2.pieceNum)
#     #0 
#     down_0 = side_difference(piece2.sideDown,piece1.sideUp)
#     left_0 = side_difference(piece1.sideRight,piece2.sideLeft)
#     up_0 = side_difference(piece1.sideDown,piece2.sideUp)
#     right_0 = side_difference(piece2.sideRight,piece1.sideLeft)
#     #90
#     # manh 1 xoay 90
#     down_90_1 = side_difference(piece2.sideDown,piece1.sideLeft)
#     left_90_1 = side_difference(piece1.sideUp,piece2.sideLeft)
#     up_90_1 = side_difference(piece1.sideRight,piece2.sideUp)
#     right_90_1 = side_difference(piece2.sideLeft,piece1.sideDown)
#     # manh 2 xoay 90
#     down_90_2 = side_difference(piece2.sideRight,piece1.sideUp)
#     left_90_2 = side_difference(piece1.sideRight,piece2.sideDown)
#     up_90_2 = side_difference(piece1.sideDown,piece2.sideLeft)
#     right_90_2 = side_difference(piece2.sideUp,piece1.sideLeft)
#     #180
#     # manh 1 xoay 180
#     down_180_1 = side_difference(piece2.sideDown,piece1.sideDown)
#     left_180_1 = side_difference(piece1.sideLeft,piece2.sideLeft)
#     up_180_1 = side_difference(piece1.sideUp,piece2.sideUp)
#     right_180_1 = side_difference(piece2.sideRight,piece1.sideRight)
#     # manh 2 xoay 180
#     down_180_2 = side_difference(piece2.sideUp,piece1.sideUp)
#     left_180_2 = side_difference(piece1.sideRight,piece2.sideRight)
#     up_180_2 = side_difference(piece1.sideDown,piece2.sideDown)
#     right_180_2 = side_difference(piece2.sideLeft,piece1.sideLeft)
#     #270
#     # manh 1 xoau 270 
#     down_270_1 = side_difference(piece2.sideDown,piece1.sideRight)
#     left_270_1 = side_difference(piece1.sideDown,piece2.sideLeft)
#     up_270_1 = side_difference(piece1.sideLeft,piece2.sideUp)
#     right_270_1 = side_difference(piece2.sideRight,piece1.sideUp)
#     # manh 2 xoay 270 
#     down_270_2 = side_difference(piece2.sideLeft,piece1.sideUp)
#     left_270_2 = side_difference(piece1.sideRight,piece2.sideUp)
#     up_270_2 = side_difference(piece1.sideDown,piece2.sideRight)
#     right_270_2 = side_difference(piece2.sideDown,piece1.sideLeft)
#     # clockwise direction
#     temp1 = [
#         down_0, left_0, up_0, right_0,
#         down_90_1,left_90_1,up_90_1,right_90_1,
#         down_90_2,left_90_2,up_90_2,right_90_2,
#         down_180_1,left_180_1,up_180_1,right_180_1,
#         down_180_2,left_180_2,up_180_2,right_180_2,
#         down_270_1,left_270_1,up_270_1,right_270_1,
#         down_270_2,left_270_2,up_270_2,right_270_2
#     ]

#     temp2 = [
#         up_0, right_0, down_0, left_0,
#         up_90_1,right_90_1,down_90_1,left_90_1,
#         up_90_2,right_90_2,down_90_2,left_90_2,
#         up_180_1,up_180_1,down_180_1,left_180_1,
#         up_180_2,right_180_2,down_180_2,left_180_2,
#         up_270_1,right_270_1,down_270_1,left_270_1,
#         up_270_2,right_270_2,down_270_2,left_270_2
#     ]

#     for i in range(len(temp1)):
#         temp1[i] = (temp1[i], i)
#         temp2[i] = (temp2[i], i)

#     # non-decreasing sort of difference
#     piece1.difference[piece2.pieceNum] = sorted(temp1)
#     piece2.difference[piece1.pieceNum] = sorted(temp2)


# # search for neighbors
# def find_neighbors(piece: Piece):
#     DIFFERENCE_RATE_THRESHOLD = 0.3
#     candidates = [None for x in range(4)]
#     for i in range(len(piece.difference)):
#         if piece.difference[i] is None:
#             continue
#         temp = piece.difference[i][0]
#         index = temp[1] % 4
#         if candidates[index] is None or candidates[index][1][0] > temp[0]:
#             candidates[index] = (i, temp)
#     for entry in candidates:
#         if entry is not None:
#             index = entry[1][1] % 4
#             if entry[1][0] <= DIFFERENCE_RATE_THRESHOLD * (piece.size_vertical if (index == 1 or index == 3) else piece.size_horizontal):
#                 piece.neighbors[index] = entry[0]
#     print("piece {} neighbors {}".format(piece.pieceNum,piece.neighbors))

            