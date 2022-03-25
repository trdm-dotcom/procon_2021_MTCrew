import cv2
import os
import sys

# image information
def read_image(challengeDir,flags,col,row):
    files = [f for f in os.listdir(challengeDir) if os.path.isfile(os.path.join(challengeDir, f)) and f.endswith(('jpg', 'png'))]
    imgs = [cv2.imread(os.path.join(challengeDir,'{}.png'.format(i)), flags) for i in range(len(files))]
    pSize_vertical = max([imgs[i].shape[0] for i in range(col*row)]) 
    pSize_horizontal = max([imgs[i].shape[1] for i in range(col*row)])
    imgChn = max([imgs[i].shape[2] for i in range(col*row)]) if flags == cv2.IMREAD_COLOR else 1
    return imgs,pSize_vertical, pSize_horizontal, imgChn
