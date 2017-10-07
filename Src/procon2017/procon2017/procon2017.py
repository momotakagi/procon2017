# share house git 
import threading
import Store 
from module import Data #こんな書き方もできる
from Search import Search
import time
from draw import draw
import copy


if __name__ == '__main__':

    #変数シリーズ
    Pieces1 = Data()  #ピースのDBクラス
    im1 = Store.get_im('1.jpg')
    cnts1, all_pixel1 = Store.colormask(im1)
    

    Pieces2 = Data()  #ピースのDBクラス
    im2 = Store.get_im('2.jpg')
    cnts2, all_pixel2 = Store.colormask(im2)

    Pieces3 = Data()  #ピースのDBクラス
    im3 = Store.get_im('3.jpg')
    cnts3, all_pixel3 = Store.colormask(im3)

    #ここでデータ格納
    polygon1, im1 = Store.approx_point(cnts1, im1, Pieces1, all_pixel1)
    polygon2, im2 = Store.approx_point(cnts2, im2, Pieces2, all_pixel2)
    polygon3, im3 = Store.approx_point(cnts3, im3, Pieces3, all_pixel3)

    Store.write_im(im1, "im1.png")
    Store.write_im(im2, "im2.png")    
    Store.write_im(im3, "im3.png")

    Pieces = Data()
    Pieces.angle = Pieces1.angle + Pieces2.angle + Pieces3.angle
    Pieces.Center_G = Pieces1.Center_G + Pieces2.Center_G + Pieces3.Center_G
    Pieces.length = Pieces1.length + Pieces2.length + Pieces3.length
    Pieces.polygon = Pieces1.polygon + Pieces2.polygon + Pieces3.polygon
    Pieces.total_piece_num = Pieces1.total_piece_num + Pieces2.total_piece_num + Pieces3.total_piece_num



    #枠を取得
    Waku_data = Data()
    waku_im = Store.get_im('waku.jpg')
    cnts_waku, all_pixe_waku = Store.colormask_waku(waku_im)
    _ = Store.approx_point(cnts_waku, waku_im, Waku_data, all_pixe_waku)

    
    

    #探索開始
    search = Search(Pieces, Waku_data)

    start = time.time()
    fin_node = search.bfs()


    print("\n\n THIS IS THE BEST POINT NODE")
    pt = fin_node[0]
    while pt.piece_n != -1:  
         print("piece:" + str(pt.piece_n) + " next_edge" + str(pt.next_edge_n) + " prev_edge" + str(pt.prev_edge_n) + " total_edge" + str(pt.total_edge) + " Is_reverse=" + str(pt.Is_reverse) + " point" + str(pt.point))
         pt = pt.prev

    print("\n_________________________________________________________")
    print ("elapsed_time:{0}".format(time.time() - start) + "[sec]")
   
    PiecesBackup = copy.deepcopy(Pieces)

    __tmp = []
    for pt in fin_node:
        print("node") 
        print(pt)
        print("piece:" + str(pt.piece_n) + " next_edge" + str(pt.next_edge_n) + " prev_edge" + str(pt.prev_edge_n) + " total_edge" + str(pt.total_edge) + " Is_reverse=" + str(pt.Is_reverse) + " point" + str(pt.point)+"corrpiece" + str(pt.corr_edge))
        __tmp.append(draw(copy.deepcopy(Pieces), copy.deepcopy(Pieces.polygon), pt))
