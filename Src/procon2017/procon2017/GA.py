
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

        pix_outside = self.waku_data.polygon[0]

        Max_y = 0
        Max_x = 0
        y = 0
        x = 0

        print(len(pix_outside))
        


        for (i) in range(len(pix_outside)-1):
            x = pix_outside[i][0][0]
            y = pix_outside[i][0][1]
            if y >= Max_y:
                Max_y = y

            elif x >= Max_x:
                Max_x = x
                
        print(Max_y)        
        print(Max_x) 


        __N = 10
        __RATIO_X = 11.34375
        __RATIO_Y = 10.75

    def MakeGrid(self):


        White = 0
        Black = 0
        Total_pixels = 0

        Max_White = []
        suit_pix = []

        super_elite_pix = []
        
        temp2 = []

        pieces = self.pieces.polygon
        temp_pieces = self.pieces.polygon
        



        pix = self.waku_data.pixels

      

        print("理論上MAX! " + str(self.width * self.height * 3))
        
        for (n) in range(len(pieces)):
            temp = []
            White = 0
            Total_pixels =0
            self.img = np.zeros((self.height, self.width, 3), np.uint8)
            #ピースバラマキ
            for (i) in range(len(pieces)):
                """
                pivot = copy.deepcopy(pieces[i][0])
                random_ang = randint(360)
                
                for (j) in range(len(pieces[i])):
                #軸を(0,0)に平行移動
                    pieces[i][j] -= pivot

                # 回転による座標変換           
                    pieces[i][j] = self.rotate(random_ang, pieces[i][j])
                """
                #枠内のピクセル値をランダムで抽出
                random_n = randint(len(pix))                                             
                random_pixel = pix[random_n]
            
                #グリッド化  問題あるかも？
                random_gred = random_pixel / [__RATIO_Y,__RATIO_X]                                          

                #移動距離を計算
                s = random_gred - (copy.deepcopy(pieces[i][0]) / [__RATIO_Y,__RATIO_X])

                temp_s = s * [__RATIO_Y,__RATIO_X]
                #print(temp_s[0][0])
                round(copy.deepcopy(temp_s[0][0]))
                round(copy.deepcopy(temp_s[0][1]))
              
            
                #ピースの全頂点を移動
                for (j) in range(len(pieces[i])):
                      
                    temp_pieces[i][j] =  pieces[i][j] + temp_s


                #描画　表示はしていない
                pts = copy.deepcopy(np.array(temp_pieces[i], np.int32))
                pts = pts.reshape((-1,1,2))
                cv2.fillPoly(self.img, [copy.deepcopy(pts)], color=(255,255,255))
                temp.append(copy.deepcopy(pieces[i][0]))
                
            suit_pix.append(copy.deepcopy(temp))

           
            """
            cv2.imshow('image', self.img)
            cv2.imwrite("output"+str(n)+".jpg", self.img)
            cv2.waitKey(0)
            cv2.destroyAllWindows
            """
                    

            White = len(self.img[self.img  > 254])

            print("White")
            print(White)
           


            Max_White.append(copy.deepcopy(White))

            


        
        

        print("index")
        print(Max_White.index((max(Max_White))))

        print("suit_pix[Max_White.index((max(Max_White)))]")
        print(suit_pix[Max_White.index((max(Max_White)))])
        
        for (i) in range(len(pieces)):
            suit_pix[i] = copy.deepcopy(suit_pix[Max_White.index((max(Max_White)))])
            Max_White[i] = copy.deepcopy(max(Max_White))

       
        print("Max_White")
        print(Max_White[0])

        print("suit_pix[0]")
        print(suit_pix[0])


#####################　　　まき直し　　　############################################
        super_elite_pix = []

        for (n) in range (60):

            super_suit_pix = []
            
            temp_pix = copy.deepcopy(suit_pix[0])

            for (i) in range(len(pieces)):

                while True:                
                    White = 0
          
                    self.img = np.zeros((self.height, self.width, 3), np.uint8)

                    temp_pieces = copy.deepcopy(pieces)
                

                    #枠内のピクセル値をランダムで抽出
                    random_n = randint(len(pix))                                             
                    random_pixel = pix[random_n]
            
                    #グリッド化  問題あるかも？
                    random_gred = random_pixel / [__RATIO_Y,__RATIO_X]                                          

                    #移動距離を計算
                    s = random_gred - (copy.deepcopy(temp_pix[i]) / [__RATIO_Y,__RATIO_X])

                    temp_s = s * [__RATIO_Y,__RATIO_X]

                    round(copy.deepcopy(temp_s[0][0]))
                    round(copy.deepcopy(temp_s[0][1]))

                    temp_pix[i] =  copy.deepcopy(temp_pix[i]) + temp_s 

               
                    
                    for (r) in range(len(pieces)):
                        temp_grid = copy.deepcopy(temp_pix[r]) / [__RATIO_Y,__RATIO_X]
                        
                        s2 = temp_grid - (copy.deepcopy(pieces[r][0])) / [__RATIO_Y,__RATIO_X]

                        temp_s2 = s2 * [__RATIO_Y,__RATIO_X]
                        round(copy.deepcopy(temp_s2[0][0]))
                        round(copy.deepcopy(temp_s2[0][1]))

                        for (t) in range(len(pieces[r])):
                           
                            temp_pieces[r][t] =  copy.deepcopy(pieces[r][t]) + temp_s2

                    #print(temp_pix[0])     
                    
                    #描画　表示はしていない
                    for (k) in range(len(pieces)):
                        pts = copy.deepcopy(np.array(temp_pieces[k], np.int32))
                        pts = pts.reshape((-1,1,2))
                        cv2.fillPoly(self.img, [copy.deepcopy(pts)], color=(255,255,255))
                    
                    White = len(self.img[self.img  > 254])
                    #print("White"+ str(i) +" = " + str(White))
                    """
                    cv2.imshow('image', self.img)         
                    cv2.waitKey(0)
                    cv2.destroyAllWindows
                    """
                    


                    if (White + 50000) >= Max_White[i]:
                        Max_White[i] = copy.deepcopy(White)

                        super_suit_pix.append(copy.deepcopy(temp_pix))

                        print(Max_White)
                        """
                        cv2.imshow('image', self.img)         
                        cv2.waitKey(0)
                        cv2.destroyAllWindows
                        """
                        break



                    #super_elite_pix.append(copy.deepcopy(suit_pix))

                    cv2.imshow('image', self.img)         
                    cv2.waitKey(0)
                    cv2.destroyAllWindows

            super_elite_pix.append(copy.deepcopy(super_suit_pix[Max_White.index(max(Max_White))]))
            
            Max_White[0] = max(Max_White)

            for (i) in range(len(pieces)):
                Max_White[i] = copy.deepcopy(max(Max_White))

            suit_pix[0] = copy.deepcopy(super_suit_pix[Max_White.index(max(Max_White))])

       
        
        #print("Max_White =" + str(Max_White))
        """
        for (r) in range(len(pieces)):
            temp2_grid = copy.deepcopy(super_elite_pix[r] / [__RATIO_Y,__RATIO_X])            
            s3 = copy.deepcopy (temp2_grid - (pieces[r][0]) / [__RATIO_Y,__RATIO_X])
            for (t) in range(len(pieces[r])):
                           
                pieces[r][t] =  copy.deepcopy(pieces[r][t] + (s3 * [__RATIO_Y,__RATIO_X]))
        """

        for (r) in range(len(pieces)):
            temp2_grid = copy.deepcopy(suit_pix[r] / [__RATIO_Y,__RATIO_X])            
            s3 = copy.deepcopy (temp2_grid - (pieces[r][0]) / [__RATIO_Y,__RATIO_X])
            temp_s3 = s3 * [__RATIO_Y,__RATIO_X]

            round(copy.deepcopy(temp_s3[0][0]))
            round(copy.deepcopy(temp_s3[0][1]))   
            for (t) in range(len(pieces[r])):
                        
                temp_pieces[r][t] =  copy.deepcopy(pieces[r][t]) + temp_s3


        for (i) in range(len(pieces)):
            pts = np.array(temp_pieces[i], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.fillPoly(self.img, [pts], color=(255,255,255))
            self.img = cv2.polylines(self.img,[pts],True,(0,255,0))  
         
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