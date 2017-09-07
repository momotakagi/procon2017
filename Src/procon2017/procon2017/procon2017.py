# share house git 

import Store 
import module



if __name__ == '__main__':

    Pieces = module.Data()  #ピースのDBクラス
    im = Store.get_im()
    cnts = Store.colormask(im)

    Store.approx_point(cnts, im, Pieces)