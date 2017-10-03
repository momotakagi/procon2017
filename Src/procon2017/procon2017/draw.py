import numpy as np
import cv2
import Store 

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

        #fin_nodeの葉から根へ向けて処理
        now_node = fin_node[0]
        total_edge = now_node.prev_total_edge

        for (i) in range(len(polygon)-1):
            #現在のノードの処理
            piece_n = now_node.piece_n
            x = polygon[piece_n][now_node.prev_edge_n]
            prev_edge_n = now_node.prev_edge_n + 1
            if prev_edge_n == len(polygon[piece_n]):
                    prev_edge_n = 0

            #1つ上のノードへ
            now_node = now_node.prev 

            if now_node.next_edge_n < total_edge[0]:
                length = len(polygon[0])
                next_edge_n = now_node.next_edge_n + 1
                
                if next_edge_n == length:
                   next_edge_n = 0
                
                y = polygon[0][next_edge_n]
                
                y1 = polygon[0][now_node.next_edge_n]
            
            elif now_node.next_edge_n >= total_edge[1]:
                length = len(polygon[2])
                next_edge_n = now_node.next_edge_n - total_edge[1] + 1
                if next_edge_n == length:
                    next_edge_n = 0
                y = polygon[2][next_edge_n] 
                y1 = polygon[2][now_node.next_edge_n - total_edge[1]]
            else:
                length = len(polygon[1])
                next_edge_n = now_node.next_edge_n - total_edge[0] + 1
                if next_edge_n == length:
                    next_edge_n = 0
                y = polygon[1][next_edge_n]
                y1 = polygon[1][now_node.next_edge_n - total_edge[0]]

            #2つのピースを合わせる
            instance = y - x
            for (i, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][i] += instance

            #角度計算
            VecA = y1 - y
            VecB = polygon[piece_n][prev_edge_n] - y
            Ang = Store.cul_angle(VecA[0], VecB[0])

            #軸を(0,0)に平行移動
            instance = x - 0
            for (i, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][i] -= instance

            for (i, piece) in enumerate(polygon[piece_n]):
                # 回転による座標変換
                polygon[piece_n][i] = rotate(Ang, polygon[piece_n][i])

            #もとに戻す
            for (i, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][i] += instance

        #表示
        for (i, piece) in enumerate(polygon):
            pts = np.array(polygon[i], np.int32)
            pts = pts.reshape((-1,1,2))
            img = cv2.polylines(img,[pts],True,(0,255,255))
            cv2.imshow('image', img)
            cv2.waitKey(0)          
            cv2.destroyAllWindows

def rotate(deg, matrix):
    # degreeをradianに変換
    r = np.radians(deg)
    C = np.cos(r)
    S = np.sin(r)
    
    matrix[0][0] = matrix[0][0] * C - matrix[0][1] * S
    matrix[0][1] = matrix[0][0] * S + matrix[0][1] * C

    return matrix
        
        
            

        



