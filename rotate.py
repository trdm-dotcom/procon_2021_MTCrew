from re import L
import cv2
import os
__DIRNAME = os.getcwd()

def Rotate(id,input,col,row):
    dir = os.path.join(os.path.dirname(__DIRNAME),"procon\challenge\{}".format(id))
    arr = input.split("#")
    arr.pop(0)
    route = [0 for i in range(col*row)]
    for e in arr:
        instruction = e.split(" ")
        num, degree = int(instruction[0]), int(instruction[1])
        route[num] = route[num] + int(degree) 
        filename = os.path.join(dir,'{}.png'.format(num))
        src = cv2.imread(filename, cv2.IMREAD_COLOR)
        image = cv2.rotate(src, getDegrees(degree))
        cv2.imwrite(filename,image)
    total = ""
    for degree in route:
        total += str(getTotal(degree%360)) 
    return total

def getDegrees(degree):
    match degree: 
        case 90: return cv2.ROTATE_90_CLOCKWISE
        case 180: return cv2.ROTATE_180
        case 270: return cv2.ROTATE_90_COUNTERCLOCKWISE

def getTotal(degree):
    match degree: 
        case 0: return 0
        case 90: return 1
        case 180: return 2
        case 270: return 3
        