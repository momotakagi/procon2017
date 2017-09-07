# share house git 

import Store 
import module



if __name__ == '__main__':

    #変数シリーズ
    Pieces = module.Data()  #ピースのDBクラス
    im = Store.get_im()
    cnts, all_pixel = Store.colormask(im)

    Store.approx_point(cnts, im, Pieces, all_pixel)