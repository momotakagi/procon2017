# share house git 

import Store 
from module import Data #こんな書き方もできる
from Search import Search
import time

if __name__ == '__main__':

    #変数シリーズ
    Pieces = Data()  #ピースのDBクラス
    im = Store.get_im()
    cnts, all_pixel = Store.colormask(im)

    #枠を取得
    #waku = Store.get_waku()
    #cnts_waku, all_pixe_waku = Store.colormask(waku)


    #ここでデータ格納
    polygon = Store.approx_point(cnts, im, Pieces, all_pixel)


    
    #探索開始
    search = Search(Pieces)

    start = time.time()
    fin_node = search.bfs()

    print("\n\n THIS IS THE BEST POINT NODE")
    pt = fin_node[0]
    while pt.piece_n != -1:  
         print("piece:" + str(pt.piece_n) + " next_edge" + str(pt.next_edge_n) + " prev_edge" + str(pt.prev_edge_n) + " prev_total_edge" + str(pt.prev_total_edge) + " Is_reverse=" + str(pt.Is_reverse))
         pt = pt.prev

    print("\n_________________________________________________________")
    print ("elapsed_time:{0}".format(time.time() - start) + "[sec]")
   
    
    #draw = draw(Pieces, polygon)