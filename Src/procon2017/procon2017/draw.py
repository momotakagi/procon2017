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

        now_node = fin_node[0]
        total_edge = now_node.prev_total_edge

        for (i) in range(len(polygon)-1):
            piece_n = now_node.piece_n
            x = polygon[piece_n][now_node.prev_edge_n]

            now_node = now_node.prev

            if now_node.next_edge_n < total_edge[0]:
                length = len(polygon[0])
                next_edge_n = now_node.next_edge_n + 1
                if next_edge_n == length:
                    next_edge_n = 0
                y = polygon[0][next_edge_n] 

            elif now_node.next_edge_n >= total_edge[1]:
                length = len(polygon[2])
                next_edge_n = now_node.next_edge_n - total_edge[1] + 1
                if next_edge_n == length:
                    next_edge_n = 0
                y = polygon[2][next_edge_n]
                
            else:
                length = len(polygon[1])
                next_edge_n = now_node.next_edge_n - total_edge[0] + 1
                if next_edge_n == length:
                    next_edge_n = 0
                y = polygon[1][now_node.next_edge_n]

            instance = y - x
            for (i, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][i] += instance

        for (i, piece) in enumerate(polygon):
            pts = np.array(polygon[i], np.int32)
            pts = pts.reshape((-1,1,2))
            img = cv2.polylines(img,[pts],True,(0,255,255))
            cv2.imshow('image', img)
            cv2.waitKey(0)          
            cv2.destroyAllWindows
        
        
            

        



