import numpy as np
import cv2

class Draw:
    """description of class"""


    def __init__(self, child, pieces):
        img = np.zeros((512, 512, 3), np.unit8)
        print("test")
        #例
        now_node = child
        for i in range(3):
            print("piece:" + str(now_node.piece_n) + " next_edge:" + str(now_node.next_edge_n) + " prev_edge:" + str(now_node.prev_edge_n) + str(now_node.coordinates))
            
        #ここに描画の関数を書く
            pts = np.array(now_node.coordinates, np.int32)
            pts = pts.reshape((-1,1,2))
            img = cv2.polylines(img,[pts],True,(0,255,255))
            cv2.imshow('image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows

            now_node = now_node.prev
 

