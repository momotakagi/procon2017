import numpy as np
import cv2

class draw:
    """description of class"""

    #ピースの合計値
    total = int

    #コンストラクタ
    def __init__(self, pieces, polygon, fin_node):
        img = np.zeros((1024, 1024, 3), np.uint8)
        self.pieces = pieces
        global total
        total = pieces.total_piece_num

        #now_node = fin_node
        for (i, piece) in enumerate(polygon):
            print(piece)
            pts = np.array(polygon[i], np.int32)
            pts = pts.reshape((-1,1,2))
            img = cv2.polylines(img,[pts],True,(0,255,255))
            cv2.imshow('image', img)
            cv2.waitKey(0)          
            cv2.destroyAllWindows
        



