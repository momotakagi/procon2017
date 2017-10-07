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
        img = np.zeros((768, 1366, 3), np.uint8)


        self.pieces = pieces
        global total
        total = pieces.total_piece_num

        fontsize = 1
        font = cv2.FONT_HERSHEY_PLAIN

        center_g = []

        total_piece_n=[]

        corr_edge = fin_node.corr_edge
        

        #fin_nodeの根から処理
        now_node = fin_node
        n_node = fin_node

        total_fin_node = 1
        while n_node.prev_edge_n != -1:
            total_fin_node += 1
            n_node = n_node.prev

        root_list = [now_node]
        for (i) in range(total_fin_node-1):#len(polygon)-1
            now_node = now_node.prev
            root_list.append(now_node)

        #print("total_fin_node" + str(total_fin_node))

        total_piece_n.append(0)

        for (i) in range(total_fin_node-1):#len(polygon)-1
            root_n = len(root_list)-1-i
            now_node = root_list[root_n]

            #現在のノードの処理
            total_edge = now_node.prev_total_edge
            if i != 0:

                for (j) in range(len(total_edge)+1):

                    if j == len(total_edge):
                        next_edge_n = now_node.next_edge_n - total_edge[j-1] + 1

                        x1 = polygon[now_node.piece_n][next_edge_n-1]

                        length = len(polygon[now_node.piece_n])

                        if next_edge_n == length:
                            next_edge_n = 0
                
                        x = polygon[now_node.piece_n][next_edge_n]  

                    else:

                        if now_node.next_edge_n < total_edge[j]:
                            length = len(polygon[total_piece_n[j]])

                        
                            if j == 0:
                                next_edge_n = now_node.next_edge_n + 1
                            else:
                                next_edge_n = now_node.next_edge_n - total_edge[j-1] + 1
                    
                            x1 = polygon[total_piece_n[j]][next_edge_n-1]



                            if next_edge_n == length:
                                next_edge_n = 0
                                for (k) in range(len(total_edge)+1):
                                    if k == len(total_edge):
                                            x = polygon[now_node.piece_n][corr_edge[i][2] - total_edge[k-1]]
                                    elif corr_edge[i][2] < total_edge[k]:
                                        if k == 0:
                                            x = polygon[0][next_edge_n]
                                        else:
                                            x = polygon[total_piece_n[k]][corr_edge[i][2] - total_edge[k]]
                                        break
                            else:
                                x = polygon[total_piece_n[j]][next_edge_n] 
                        

                            

                            break

            else:
                length = len(polygon[i])
                next_edge_n = now_node.next_edge_n + 1
                x1 = polygon[i][next_edge_n-1]
                if next_edge_n == length:
                            next_edge_n = 0
                x = polygon[i][next_edge_n] 

            """
            print("total_edge" + str(total_edge))
            print("x" + str(x))
            print("x1" + str(x1))
            print(corr_edge)
            print(polygon)
            """

            #1つ上のノードへ
            now_node = root_list[root_n-1]
            piece_n = now_node.piece_n

            total_piece_n.append(now_node.piece_n)
            

            y = copy.deepcopy(polygon[piece_n][now_node.prev_edge_n])
            prev_edge_n = now_node.prev_edge_n + 1
            if prev_edge_n == len(polygon[piece_n]):
                    prev_edge_n = 0

            #2つのピースを合わせる
            instance = copy.deepcopy(x - y)
            for (j, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][j] += instance

            #角度計算
            VecA = x1 - x
            VecB = polygon[piece_n][prev_edge_n] - x

            Ang = Store.cul_angle(VecA[0], VecB[0])
            """print("VecA" + str(VecA))
            print("VecB" + str(VecB))
            print("polygon" + str(polygon[piece_n][prev_edge_n]))"""
            

            #外積の計算
            direction = np.cross(VecA, VecB)

            #軸を(0,0)に平行移動
            pivot = copy.deepcopy(polygon[piece_n][prev_edge_n-1])
            for (j, piece) in enumerate(polygon[piece_n]):
                polygon[piece_n][j] -= pivot

            #print("Ang" + str(Ang))

            for (j, piece) in enumerate(polygon[piece_n]):
                # 回転による座標変換
                if direction > 0:                 
                    polygon[piece_n][j] = rotate(-Ang, polygon[piece_n][j])
                else:
                    polygon[piece_n][j] = rotate(Ang, polygon[piece_n][j])

            #もとに戻す
            for (j) in range(len(polygon[piece_n])):
                polygon[piece_n][j] += pivot

        for (i) in range(total_fin_node):#len(polygon)
            for(j, piece) in enumerate(polygon[total_piece_n[i]]):#polygon[i]
                polygon[total_piece_n[i]][j] = piece / 5#polygon[i][j] = piece / 5

        #重心計算
        """for (i, cnt) in enumerate(polygon):
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            center_g.append((cx,cy))"""
        for (i) in range(total_fin_node):
            M = cv2.moments(polygon[total_piece_n[i]])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            center_g.append((cx,cy))

        center_g_list = []
        total_center_g = []
        total_x = 0
        total_y = 0
        display_center = [1366/2, 768/2]
        transfer_center_g = []

        for (i) in range(len(center_g)):
            center_g_list.append(list(center_g[i]))

        for (i) in range(len(center_g_list)):
            total_x += center_g_list[i][0]
            total_y += center_g_list[i][1]

        #total_center_g = [int(total_x/len(polygon)), int(total_y/len(polygon))]
        total_center_g = [int(total_x/total_fin_node), int(total_y/total_fin_node)]

        dif_G = [[x - y for (x, y) in zip(display_center, total_center_g)]]
        np_dif_G = np.array(dif_G[0])

        """for (i) in range(len(polygon)):
            for(j, piece) in enumerate(polygon[i]):
                polygon[i][j] = piece + np_dif_G"""
        for (i) in range(total_fin_node):
            for(j, piece) in enumerate(polygon[total_piece_n[i]]):
                polygon[total_piece_n[i]][j] = piece + np_dif_G

        """for (i, cnt) in enumerate(polygon):
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            transfer_center_g.append((cx,cy))"""
        for (i) in range(total_fin_node):
            M = cv2.moments(polygon[total_piece_n[i]])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            transfer_center_g.append((cx,cy))

        #print("total_piece_n" + str(total_piece_n))

       

        #表示
        for (i) in range(total_fin_node):#len(polygon)
            """for(j, piece) in enumerate(polygon[i]):
                polygon[i][j] = piece / 2"""
            #pts = np.array(polygon[i], np.int32)
            pts = np.array(polygon[total_piece_n[i]], np.int32)
            pts = pts.reshape((-1,1,2))
            img = cv2.polylines(img,[pts],True,(0, 255, 255))

            #cv2.putText(img, str(i), center_g[i], font, fontsize, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(img, str(total_piece_n[i]), transfer_center_g[i], font, fontsize, (255, 255, 255), 2, cv2.LINE_AA)


        cv2.imshow('image', img)
        cv2.waitKey(0)          
        cv2.destroyAllWindows































def chk(pieces, polygon, fin_node):

    
    img = np.zeros((768, 1366, 3), np.uint8)


    
    global total
    total = pieces.total_piece_num

    fontsize = 1
    font = cv2.FONT_HERSHEY_PLAIN

    center_g = []

    total_piece_n=[]

    corr_edge = fin_node.corr_edge
    
    

    #fin_nodeの根から処理
    now_node = fin_node
    n_node = fin_node

    total_fin_node = 1
    while n_node.prev_edge_n != -1:
        total_fin_node += 1
        n_node = n_node.prev

    root_list = [now_node]
    for (i) in range(total_fin_node-1):#len(polygon)-1
        now_node = now_node.prev
        root_list.append(now_node)

    #print("total_fin_node" + str(total_fin_node))

    total_piece_n.append(0)

    for (i) in range(total_fin_node-1):#len(polygon)-1
        root_n = len(root_list)-1-i
        now_node = root_list[root_n]

        #print(now_node.corr_edge[i][2])

        #現在のノードの処理
        total_edge = now_node.prev_total_edge
        if i != 0:

            for (j) in range(len(total_edge)+1):

                if j == len(total_edge):
                    next_edge_n = now_node.next_edge_n - total_edge[j-1] + 1

                    x1 = polygon[now_node.piece_n][next_edge_n-1]

                    length = len(polygon[now_node.piece_n])

                    if next_edge_n == length:
                        next_edge_n = 0
                
                    x = polygon[now_node.piece_n][next_edge_n]  

                else:

                    if now_node.next_edge_n < total_edge[j]:
                        length = len(polygon[total_piece_n[j]])

                        
                        if j == 0:
                            next_edge_n = now_node.next_edge_n + 1
                        else:
                            next_edge_n = now_node.next_edge_n - total_edge[j-1] + 1
                    
                        x1 = polygon[total_piece_n[j]][next_edge_n-1]



                        if next_edge_n == length:
                            next_edge_n = 0
                            for (k) in range(len(total_edge)+1):
                                if k == len(total_edge):
                                        x = polygon[now_node.piece_n][corr_edge[i][2] - total_edge[k-1]]
                                elif corr_edge[i][2] < total_edge[k]:
                                    if k == 0:
                                        x = polygon[0][next_edge_n]
                                    else:
                                        x = polygon[total_piece_n[k]][corr_edge[i][2] - total_edge[k]]
                                    break
                        else:
                            x = polygon[total_piece_n[j]][next_edge_n] 
                        

                        break

        else:
            length = len(polygon[i])
            next_edge_n = now_node.next_edge_n + 1
            x1 = polygon[i][next_edge_n-1]
            if next_edge_n == length:
                        next_edge_n = 0
            x = polygon[i][next_edge_n] 
           



        #1つ上のノードへ
        now_node = root_list[root_n-1]
        piece_n = now_node.piece_n

        total_piece_n.append(now_node.piece_n)

        y = copy.deepcopy(polygon[piece_n][now_node.prev_edge_n])
        prev_edge_n = now_node.prev_edge_n + 1
        if prev_edge_n == len(polygon[piece_n]):
                prev_edge_n = 0


        #print("polygon" + str(polygon[piece_n][prev_edge_n]))
        #2つのピースを合わせる
        instance = copy.deepcopy(x - y)
        for (j, piece) in enumerate(polygon[piece_n]):
            polygon[piece_n][j] += instance

        #角度計算
        VecA = x1 - x
        VecB = polygon[piece_n][prev_edge_n] - x

        Ang = Store.cul_angle(VecA[0], VecB[0])
        """ print("x1" + str(x1))
        print("x" + str(x))     
        print(now_node.corr_edge)"""

        
        
        

            

        #外積の計算
        direction = np.cross(VecA, VecB)

        #軸を(0,0)に平行移動
        pivot = copy.deepcopy(polygon[piece_n][prev_edge_n-1])
        for (j, piece) in enumerate(polygon[piece_n]):
            polygon[piece_n][j] -= pivot

        #print("Ang" + str(Ang))

        for (j, piece) in enumerate(polygon[piece_n]):
            # 回転による座標変換
            if direction > 0:                 
                polygon[piece_n][j] = rotate(-Ang, polygon[piece_n][j])
            else:
                polygon[piece_n][j] = rotate(Ang, polygon[piece_n][j])

        #もとに戻す
        for (j) in range(len(polygon[piece_n])):
            polygon[piece_n][j] += pivot

    for (i) in range(total_fin_node):#len(polygon)
        for(j, piece) in enumerate(polygon[total_piece_n[i]]):#polygon[i]
            polygon[total_piece_n[i]][j] = piece / 5#polygon[i][j] = piece / 5





    total_x = 0
    total_y = 0
    display_center = [1366/2, 768/2]



    #print("total_piece_n" + str(total_piece_n))





    #表示
    
    __black = img.copy()

    x = []
    y = []
    for i in range(total_fin_node):
        
        __tmp = __black.copy()

        pts = np.array(polygon[total_piece_n[i]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.fillConvexPoly(__tmp,pts,(0, 10, 0))
        cv2.polylines(__tmp,[pts],True,(0, 0, 0), 3)

        img = cv2.add(img, __tmp)

        x_tmp = pts[:,0]
        y_tmp = pts[0,:]

        x.append(x_tmp.max())
        x.append(x_tmp.min())
        y.append(y_tmp.max())
        y.append(y_tmp.min())


    Xmax = max(x)
    Xmin = min(x)
    Ymax = max(y)
    Ymin = min(y)
    
    
    



    """
    print(img[img>10])
    cv2.imshow('image', img)
    cv2.waitKey(0)          
    cv2.destroyAllWindows
    """

        #もしかぶってるなら
    if len(img[img>10]) > 5:
        print("かぶってる！！")
        return (False, 0)
    else:
        tmp = [Xmax-Xmin, Ymax-Ymin]    
        return (True, (min(tmp)/max(tmp)))







 
  


def rotate(deg, matrix):
    # degreeをradianに変換
    
    r = np.radians(deg)
    C = np.cos(r)
    S = np.sin(r)
    
    x = copy.deepcopy(matrix[0][0])

    matrix[0][0] = matrix[0][0] * C - matrix[0][1] * S
    matrix[0][1] = x * S + matrix[0][1] * C

    return matrix



    
        