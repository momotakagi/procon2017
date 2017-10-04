


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
    """description of class"""
    def __init__(self, pieces, waku_data, waku_im):
        pass

