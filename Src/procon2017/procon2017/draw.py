import numpy as np
import cv2
import Store 
import copy

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
        root_list = [now_node]
        for (i) in range(len(polygon)-1):
            now_node = now_node.prev
            root_list.append(now_node)

        for (i) in range(len(polygon)-1):#len(polygon)-1
            root_n = len(root_list)-1-i
            now_node = root_list[root_n]

            #現在のノードの処理
            #piece_n = now_node.piece_n

            for (i, piece) in enumerate(total_edge):

                if now_node.next_edge_n < total_edge[i]:
                    length = len(polygon[i])

                    if i == 0:
                        next_edge_n = now_node.next_edge_n + 1
                    else:
                        next_edge_n = now_node.next_edge_n - total_edge[i-1] + 1
                    
                    if next_edge_n == length:
                       next_edge_n = 0
                
                    x = polygon[i][next_edge_n] 
                    #print(polygon[i])
                    #print(now_node.next_edge_n)
                    x1 = polygon[i][next_edge_n-1]

                    break

                elif i == len(total_edge)-1:
                    next_edge_n = now_node.next_edge_n - total_edge[i] + 1

                    if next_edge_n == length:
                       next_edge_n = 0
                
                    x = polygon[i+1][next_edge_n] 
                    x1 = polygon[i][next_edge_n-1]

            #1つ上のノードへ
            #now_node = now_node.prev
            now_node = root_list[root_n-1]
            piece_n = now_node.piece_n

            y = copy.deepcopy(polygon[piece_n][now_node.prev_edge_n])
            prev_edge_n = now_node.prev_edge_n + 1
            if prev_edge_n == len(polygon[piece_n]):
                    prev_edge_n = 0

            #2つのピースを合わせる
            instance = copy.deepcopy(x - y)
            for (i, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][i] += instance

            #角度計算
            VecA = x1 - x
            VecB = polygon[piece_n][prev_edge_n] - x
            Ang = Store.cul_angle(VecA[0], VecB[0])

            #外積の計算

            #print(Ang)

            #軸を(0,0)に平行移動
            pivot = copy.deepcopy(polygon[piece_n][prev_edge_n-1])
            for (i, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][i] -= pivot

            #print(polygon[3])

            for (i, piece) in enumerate(polygon[piece_n]):
                # 回転による座標変換
                polygon[piece_n][i] = rotate(-Ang, polygon[piece_n][i])

            #print(polygon[3])

            #もとに戻す
            for (i, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][i] += pivot

        #表示
        fontsize = 1
        font = cv2.FONT_HERSHEY_PLAIN
        for (i, piece) in enumerate(polygon):
            pts = np.array(polygon[i], np.int32)
            pts = pts.reshape((-1,1,2))
            img = cv2.polylines(img,[pts],True,(0,255,255))
            #重心を描画(文字)
            cv2.putText(img,"piece:" + str(i), pieces.Center_G[i], font, fontsize,(0,0,0))
            cv2.imshow('image', img)
            cv2.waitKey(0)          
            cv2.destroyAllWindows

def rotate(deg, matrix):
    # degreeをradianに変換
    r = np.radians(deg)
    C = np.cos(r)
    S = np.sin(r)
    
    x = copy.deepcopy(matrix[0][0])

    matrix[0][0] = matrix[0][0] * C - matrix[0][1] * S
    matrix[0][1] = x * S + matrix[0][1] * C

    return matrix
        
        
            

        



