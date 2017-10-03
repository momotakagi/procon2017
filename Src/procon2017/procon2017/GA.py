
import numpy as np
from sympy.geometry import Point, Polygon
#     height, width = im.shape[:2]
#定数群









class GA(object):
    """GA algorithm"""



    __N = int
    __RATHIO = int





    def __init__(self, pieces, waku_data, waku_im):
        self.pieces = pieces
        self.waku_data = waku_data
        self.waku_im = waku_im
        self.height , self.width = waku_im.shape[:2]

      

        global __N 
        global __RATHIO

        __N = 10
        __RATHIO = 10

    def MakeGrid(self):
        #実際のグリッドとグリッドの中心点を出す
        Max_X = int(self.width / __RATHIO)
        Max_Y = int(self.height / __RATHIO)

        tuples = []
        for item in self.waku_data.polygon[0]:
            tuples.append((item[0,0], item[0,1]) )
              
        
        print(tuples)
        waku_poly = Polygon(*tuples)
        
        

        #枠の内側の座標をすべて取り出す
        InsideWakuPix = []
        AreaCheckPix = []
       

        #配列の生成
        for x in range(Max_X):
            for y in range(Max_Y):
                print(str(x) + " " + str(y))
                if waku_poly.encloses_point(Point(x*__RATHIO,y*__RATHIO)):
                    InsideWakuPix.append((x*__RATHIO,y*__RATHIO))


        for x in range(5, self.width, __RATHIO):
            for y in range(5, self.height, __RATHIO):
                AreaCheckPix.append((x,y))

        print(InsideWakuPix)
        print(AreaCheckPix)
        return (InsideWakuPix, AreaCheckPix)