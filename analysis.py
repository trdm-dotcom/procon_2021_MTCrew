import cv2
import numpy as np
import os
import sys
import readImage as readImg
from makePieces import get_pieces
import drawPieces as drawP
import Piece
import math
import json
import sys
from rotate import Rotate
__DIRNAME = os.getcwd()

def Analysis(id,pCnt_column,pCnt_row,tutorial):
    dir = os.path.join(os.path.dirname(__DIRNAME),"procon\challenge\{}".format(id))   
    if not os.path.isdir(dir):
        print("Image dir NOT found.")
        sys.exit(1)
    img, pSize_vertical, pSize_horizontal, imgChn = readImg.read_image(dir, cv2.IMREAD_COLOR,pCnt_column,pCnt_row)
    pList, pCnt_total = get_pieces(img, pCnt_column, pCnt_row, pSize_vertical, pSize_horizontal, imgChn)
    for i in range(pCnt_total):
        for j in range(i + 1, pCnt_total):
            if i == j:
                continue
            Piece.piece_difference(pList[i], pList[j])
    startPiece = None
    black = np.zeros((pSize_vertical, pSize_horizontal, imgChn), dtype=np.uint8)
    blackPiece = Piece.Piece(-1, pSize_vertical, pSize_horizontal, imgChn, (0, 0), black, pCnt_total)
    temp = [blackPiece for x in range(pCnt_total)]
    for piece in pList:
        Piece.find_neighbors(piece)
        if piece.neighbors[0] is None and piece.neighbors[3] is None:
            startPiece = piece
    
    if startPiece is None:
        startPiece = pList[0]
        temp[math.floor(pCnt_total/2)] = startPiece
    else:
        temp[0] = startPiece
    arr = [-1 for x in range(pCnt_total)]
    arr[startPiece.pieceNum] = 0
    for i in range(pCnt_total):
        if i % pCnt_row < pCnt_row - 1 and temp[i].neighbors[1] is not None:
            temp[i + 1] = pList[temp[i].neighbors[1]]
            arr[temp[i+1].pieceNum] = i + 1
        if i / pCnt_row < pCnt_column - 1 and temp[i].neighbors[2] is not None:
            temp[i + pCnt_row] = pList[temp[i].neighbors[2]]
            arr[temp[i + pCnt_row].pieceNum] = i + pCnt_row
        if i % pCnt_row < pCnt_row - 1 and temp[i].neighbors[3] is not None:
            temp[i - 1] = pList[temp[i].neighbors[3]]
            arr[temp[i-1].pieceNum] = i - 1
        if i / pCnt_row < pCnt_column - 1 and temp[i].neighbors[0] is not None:
            temp[i - pCnt_row] = pList[temp[i].neighbors[0]]
            arr[temp[i - pCnt_row].pieceNum] = i - pCnt_row
    filename = os.path.join(os.path.dirname(__DIRNAME),"procon\solve\{}_solve.png".format(id));
    temp = drawP.combine_pieces(pSize_vertical, pSize_horizontal, pCnt_row, pCnt_column, pCnt_total, imgChn, temp)
    cv2.imwrite(filename, temp)
    tutorial = list(tutorial)
    rotate = [0]*len(arr)
    for i in range(len(arr)):
        rotate[arr[i]] = int(tutorial[i])
    rotate = ''.join(map(str, rotate))
    filename = 'http://localhost:8080/solve/{}_solve.png'.format(id)
    print(json.dumps({"arr":arr,"solved":filename,"rotate":rotate}))

if __name__ == "__main__" :
    id,pCnt_column,pCnt_row,tutorial = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
    rotate = Rotate(id,tutorial,pCnt_column,pCnt_row)
    Analysis(id,pCnt_column,pCnt_row,rotate)

    