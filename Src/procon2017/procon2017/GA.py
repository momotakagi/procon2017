
import numpy as np
#from sympy.geometry import Point, Polygon
import cv2
from numpy.random import *
import copy
#     height, width = im.shape[:2]
#定数群


# height, width = im.shape[:2]
# 9.5pix = 1 grid
# http://d.hatena.ne.jp/factal/touch/20121013/1350092190



#           GA方針
#   枠の左上座標から[1]？を基準とする
#   その基準から10pixずつグリッドを作成する(numpy配列にでも保存)
#   その中点のグリッドの座標値をnumpy配列にでも保存
#   pieceの角[0]をグリッド上に撒く（回転込み）
#   hight widthを超える座標値はなし（もっかいランダム引く）
#   N個の世代を作成しエリート世代を取り出す(この時gridの中点がない分しているかで点数をつける)
#   エリート世代のピースをランダムに動かし回転(そのうち2ピース)
#   次世代を作成
#
#
#
#
#
#





class GA(object):
    """GA algorithm"""



    __N = int
    __RATIO = int





    def __init__(self, pieces, waku_data, waku_im):
        self.pieces = pieces
        self.waku_data = waku_data
        self.waku_im = waku_im
        self.height , self.width = waku_im.shape[:2]
        self.img = np.zeros((self.height, self.width, 3), np.uint8)
      

        global __N 
        global __RATIO_X
        global __RATIO_Y

        __N = 10
        __RATIO_X = 12.921875
        __RATIO_Y = 11.67

    def MakeGrid(self):


        White = 0
        Black = 0
        Total_pixels =0

        pieces = self.pieces.polygon
        pix = self.waku_data.pixels
        
        for (i) in range(len(pieces)): 
            #ピースバラマキ
            for (i) in range(len(pieces)):
            
                pivot = copy.deepcopy(pieces[i][0])
                random_ang = randint(360)

                for (j) in range(len(pieces[i])):
                #軸を(0,0)に平行移動
                    pieces[i][j] -= pivot

                # 回転による座標変換           
                    pieces[i][j] = self.rotate(random_ang, pieces[i][j])
            
                #枠内のピクセル値をランダムで抽出
                random_n = randint(len(pix))                                             
                random_pixel = pix[random_n]
            
                #グリッド化  問題あるかも？
                random_gred = random_pixel / [__RATIO_Y,__RATIO_X]                                          

                #移動距離を計算
                s = random_gred - (pieces[i][0] / [__RATIO_X,__RATIO_Y])                       
            
                #ピースの全頂点を移動
                for (j) in range(len(pieces[i])):                                              
           
                    pieces[i][j] =  pieces[i][j] + s * [__RATIO_X,__RATIO_Y]
            
                #描画　表示はしていない
                pts = np.array(pieces[i], np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.fillPoly(self.img, [pts], color=(255,255,255))
                self.img = cv2.polylines(self.img,[pts],True,(0,255,0))  

        #枠内での白黒確認
        for i in range(len(pix)):
            
            self.pixelValue = self.img[pix[i][0][1],pix[i][0][0],1]

            Total_pixels += 1    
            
            if self.pixelValue == 255:
                White += 1
         
            
                    
        Black = Total_pixels - White
        
        print("Total =" + str(Total_pixels))
        print("White =" + str(White))
        print("Black =" + str(Black))
        
        cv2.imshow('image', self.img)         
        cv2.waitKey(0)
        cv2.destroyAllWindows

    def rotate(self, deg, matrix):
        # degreeをradianに変換
    
        r = np.radians(deg)
        C = np.cos(r)
        S = np.sin(r)
    
        x = copy.deepcopy(matrix[0][0])

        matrix[0][0] = matrix[0][0] * C - matrix[0][1] * S
        matrix[0][1] = x * S + matrix[0][1] * C

        return matrix    