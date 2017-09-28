# share house git 

import Store 
from module import Data #こんな書き方もできる
from Search import Search
import time
from draw import draw

if __name__ == '__main__':

    #変数シリーズ
    Pieces = Data()  #ピースのDBクラス
    im = Store.get_im('test.jpg')
    cnts, all_pixel = Store.colormask(im)

    #枠を取得
    Waku_data = Data()
    waku_im = Store.get_im('waku.jpg')
    cnts_waku, all_pixe_waku = Store.colormask_waku(waku_im)


    #ここでデータ格納
    polygon = Store.approx_point(cnts, im, Pieces, all_pixel)
    _ = Store.approx_point(cnts_waku, waku_im, Waku_data, all_pixe_waku)
    

    
    #探索開始
    search = Search(Pieces, Waku_data)

    start = time.time()
    fin_node = search.bfs()


    print("\n\n THIS IS THE BEST POINT NODE")
    pt = fin_node[0]
    while pt.piece_n != -1:  
         print("piece:" + str(pt.piece_n) + " next_edge" + str(pt.next_edge_n) + " prev_edge" + str(pt.prev_edge_n) + " prev_total_edge" + str(pt.prev_total_edge) + " Is_reverse=" + str(pt.Is_reverse))
         pt = pt.prev

    print("\n_________________________________________________________")
    print ("elapsed_time:{0}".format(time.time() - start) + "[sec]")
   


    draw = draw(Pieces, polygon, fin_node)