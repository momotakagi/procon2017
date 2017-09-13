#ここで木を作り、探索を開始する

#幅優先探索 → ビームサーチ → chokudai_search

#全通りプログラム(幅優先探索)
    #キュー用意
    #キューに最初の要素を入れる
    #キューから要素を取り出す
    #要素に対して処理をする
    #要素の子供をキューに入れる
    #キューが空になるまでを繰り返す

#どっかでrootを定義

#ピースを新しくこどもとして定義したら

import queue
import copy
from module import State



class Search:
    """探索するクラス"""

    #定数群
    __LENGTH_DELTA = int
    __ANGLE_DELTA = int

    #ピースの合計値
    total = int

    def __init__(self, pieces):
        self.queue = queue.Queue()
        self.pieces = pieces
        global __LENGTH_DELTA
        global __ANGLE_DELTA
        global total
        total = pieces.total_piece_num
        __LENGTH_DELTA = 9
        __ANGLE_DELTA = 3


    def bfs(self):

        #根を作成
        self.root = State(-1,-1,-1,total)        
        
        for (i, edge_len) in enumerate(self.pieces.length[0]):

            #rootのインスタンス
            self.root_tmp = State(0,-1,i,total)
            self.root_tmp.prev = self.root
            #角度と長さを追加
            self.root_tmp.this_length = copy.deepcopy(self.pieces.length[0])
            self.root_tmp.this_angle = copy.deepcopy(self.pieces.angle[0])
            #0のピースを使ったのでフラグに追加
            self.root_tmp.used_piece.remove(0)


            #self.root.next.append(self.root_tmp) nextの必要性が疑われるため

            #rootをプッシュ
            self.queue.put(self.root_tmp)
       
            



        while self.queue.empty() == False:
            #queueからpop
            self.parent = self.queue.get()          
            self.__get_children(self.parent)
            #self.queue.put(children)






           
    def __get_children(self, parent):
        
            #ベース
            self.base_length = self.parent.this_length[self.parent.next_edge_n]

            self.second = self.parent.next_edge_n + 1
            if self.second == len(self.parent.this_angle):
                self.second = 0

            self.base_first_angle = self.parent.this_angle[self.parent.next_edge_n]
            self.base_second_angle = self.parent.this_angle[self.second]


            
            #つかったピース以外のピースの数で回す (iはピースの添字)
            for i in self.parent.used_piece:
                #そのi番ピースの辺の数回し長さ取得
                for (j, c_length) in enumerate(self.pieces.length[i]):
                    #ピース長さ一致
                    if abs(self.base_length - c_length) < __LENGTH_DELTA:

                        self.tmp_second = j + 1
                        if self.tmp_second == len(self.pieces.angle[i]):
                            self.tmp_second = 0

                        self.tmp_first_angle = self.pieces.angle[i][j]
                        self.tmp_second_angle = self.pieces.angle[i][self.tmp_second]
                        
                        #合計の角度
                        self.first_total = self.base_first_angle + self.tmp_first_angle 
                        self.second_total = self.base_second_angle + self.tmp_second_angle
                        
                        #角度もおっけい
                        if abs(self.first_total - 360) < __ANGLE_DELTA:
                            #木に追加(インスタンス作成&深いコピー)ノードごとにブロックとして長さと角度を保持
                            if abs(self.fist_total - 180) < __ANGLE_DELTA:
                            
                        
                            




            #もしすべてのピースを使ったら and 頂点数が枠と同じ(±1)なら
                    #完成品として出力


