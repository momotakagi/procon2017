# share house git 

import Store 
from module import Data #こんな書き方もできる
from Search import Search


if __name__ == '__main__':

    #変数シリーズ
    Pieces = Data()  #ピースのDBクラス
    im = Store.get_im()
    cnts, all_pixel = Store.colormask(im)

    #ここでデータ格納
    Store.approx_point(cnts, im, Pieces, all_pixel)

    #探索開始
    search = Search(Pieces)
    search.bfs()



    #eisei