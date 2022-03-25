import numpy as np
import math
from Piece import Piece

def get_pieces(imgs,cnt_column,cnt_row,size_vertical,size_horizontal,img_chn):
    cnt_total = cnt_row * cnt_column
    p_list = []
    for pIt in range(cnt_total):
        pSize_vertical, pSize_horizontal, pSize_depth = imgs[pIt].shape
        temp = np.zeros((size_vertical,size_horizontal,img_chn), dtype=np.uint8)
        start_row = size_vertical * math.floor(pIt / cnt_column)
        start_col = size_horizontal * (pIt % cnt_column)
        for i in range(pSize_vertical):
            for j in range(pSize_horizontal):
                temp[i][j] = imgs[pIt][i][j]
        if pSize_vertical < size_vertical:
            # thieu chieu doc
            temp1 = temp[size_vertical-3]
            temp[size_vertical-1] = temp[size_vertical-2]
            temp[size_vertical-2] = temp1
            temp[size_vertical-3] = temp1
        if pSize_horizontal < size_horizontal:
            # thieu chieu ngang
            for i in range(size_vertical):
                temp1 = temp[i][size_horizontal-3]
                temp[i][size_horizontal-2] = temp[i][size_horizontal-1]
                temp[i][size_horizontal-2] = temp1
                temp[i][size_horizontal-3] = temp1
        p_list.append(Piece(pIt, size_vertical, size_horizontal, img_chn, (start_row, start_col), temp, cnt_total))
    
    return p_list, cnt_total
