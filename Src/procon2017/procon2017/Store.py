
import numpy as np
import cv2
import random
import sys
import copy
import module 
from matplotlib import pyplot as plt



def cul_angle(x, y):

    dot_xy = np.dot(x, y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos = dot_xy / (norm_x*norm_y)
    rad = np.arccos(cos)
    theta = rad * 180 / np.pi

    return theta


def get_im():
    src = cv2.imread('test.jpg', cv2.IMREAD_COLOR)
    im = half_size(src)
    return im


def half_size(im):
    hight = im.shape[0]
    width = im.shape[1]
    half_size = cv2.resize(im,(round(width/6),round(hight/6)))
    return half_size
    



def findcontours(im):

    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY) 

    #ret,thresh = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY)

    ret,thresh = cv2.threshold(im, 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)
    show_im(thresh, "thresh")

    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)



    #imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    #ret,thresh = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)
    #ret,thresh = cv2.threshold(im, 0, 255, cv2.THRESH_TOZERO | cv2.THRESH_OTSU)
    #thresh = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,3)


    
    for i in reversed(range(len(contours))):
        if(cv2.contourArea(contours[i]) < 150):
            del contours[i]
            
    #filter(lambda x: x % 2 is 0, list01)


    im = cv2.drawContours(im, contours, -1, (0,255,0), 3)

    cnt = contours[1]
    M = cv2.moments(cnt)
    area = cv2.contourArea(cnt)
    print(area)
    show_im(im, "findcountours")




def colormask(im):

    #im = cv2.GaussianBlur(im,(5,5),0)

    # フレームをHSVに変換
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)


    # 取得する色の範囲を指定する
    lower_piece = np.array([0, 25, 50])
    upper_piece = np.array([50, 255, 255])

    #指定した色に基づいてマスクの作成
    img_mask = cv2.inRange(hsv, lower_piece, upper_piece)

    #マスクと元画像の共通の領域を抽出
    #img_color = cv2.bitwise_and(im, im, mask=img_mask)

    show_im(img_mask, "colormask")
    
    #how_im(img_mask, "gaussian")
    image, contours, hierarchy = cv2.findContours(img_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=cv2.contourArea, reverse=True)


    for i in reversed(range(len(contours))):
        if(cv2.contourArea(contours[i]) < 800):
            del contours[i]
            
    #filter(lambda x: x % 2 is 0, contours)

    #これらはとりあえずすべての近似
    im_all= np.copy(im)
    im_all = cv2.drawContours(im_all, contours, -1, (0,255,0), 3)
    show_im(im_all, "findcountours")
    #***************************************************#


    #ピースの領域情報(角度の時使う)
    pixelpoints = cv2.findNonZero(img_mask)


    return (contours, pixelpoints)
    





def approx_point(contours, im, Pieces, all_pixel):
    im0 = np.copy(im)
    #pieces = DATA.Piece()

    polygon = []
    Center_G = []
    length = [[] for i in range(len(contours))]
    angle = [[] for i in range(len(contours))]
    
    for (i, cnt) in enumerate(contours):

        #重心計算
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        Center_G.append((cx,cy))

        #輪郭近似
        epsilon = 0.01*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,False)
        approx = approx[0:-1]  #順番重複回避
        polygon.append(approx)


        #iは添字そさせる
        #辺の長さを求める
        for (prev, cordinate) in enumerate(approx):
            next = prev
            next += 1
            if(next == len(approx)):
                next = 0
            #辺の長さを格納
            length[i].append(np.linalg.norm(approx[next] - approx[prev]))      
            


      


       #角度を求める
        for (prev, cordinate) in enumerate(approx):
             pivot = prev + 1            
             if(pivot == len(approx)):
                 pivot = 0

             next = pivot + 1  
             
             if(next == len(approx)):
                 next = 0

             #角度計算
             VecA = approx[prev] - approx[pivot]
             VecB = approx[next] - approx[pivot]
      
             Ang = cul_angle(VecA[0], VecB[0])        


############################################力技###################################################
             #2点間の中点にピースは含まれていなかったら360から引く
             direction = (VecA + VecB) / 10            
             direction = direction + approx[pivot]
             casted = direction.astype(int)

             Ang = 360 - Ang
             for(pixel) in all_pixel:
                 if(casted[0,0] == pixel[0,0] and casted[0,1] == pixel[0,1]):
                     Ang = 360 - Ang
                     break

             angle[i].append(Ang)
             
        #角度リストをシフトして調整
        tmp = angle[i]
        angle[i].insert(0,tmp[-1])
        angle[i].pop()

        
     
     
    


   #********************************DEBUG表示用***********************************************************###
    fontsize = 1
    font = cv2.FONT_HERSHEY_PLAIN
    for (i, approx) in enumerate(polygon):
          #輪郭描画
          im0 =  cv2.drawContours(im, [approx], 0, (0,255,0), 3)
          

         
          #重心を描画(文字)
          cv2.putText(im0,"piece:" + str(i),Center_G[i],font, fontsize,(0,0,0))

          
          #角ピースの情報表示
          for (prev, cordinate) in enumerate(approx):
              im0 = cv2.circle(im, tuple(cordinate[0]), 3, (0,0,255), -1)

              next = prev
              next += 1
              if(next == len(approx)):
                  next = 0
              #辺の長さを格納
              #length[i].append(np.linalg.norm(approx[next] - approx[prev]))        
              
              #各角番号を描画
              cv2.putText(im0,str(prev),tuple(cordinate[0]),font, fontsize + 1,(255,0,0))
              
              cv2.putText(im0,str(int(angle[i][prev])),tuple(cordinate[0] - 20),font, fontsize,(255,0,255))

              #辺の長さを描画
              Mp = (approx[next] + approx[prev]) / 2
              cv2.putText(im0,str(int(length[i][prev])),(int(Mp[0,0]), int(Mp[0,1])),font, fontsize,(0,0,0))

   #********************************DEBUG表示用***********************************************************###
    

    show_im(im0, "im0")    
    
    #データを格納
    Pieces.polygon = polygon
    Pieces.Center_G = Center_G
    Pieces.length = length
    Pieces.angle = angle
    Pieces.pixels = all_pixel
   





def show_im(im, name):
    cv2.imshow(name ,im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




"""
if __name__ == '__main__':

    Pieces = module.Data()  #ピースのDBクラス
    im = get_im()
   
    cnts = colormask(im)
    approx_point(cnts, im, Pieces)
"""


   
