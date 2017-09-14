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


    
    def _route_list(route): #引数でリストを受け取る。
        route_ = route[:]
        row = []
        box = route_
        row.append(box) #リストの0番目（元の値）を格納
        for node in xrange(len(route)-1): #リストを一回転する。
           row.append(box) #リストのnode+1番目の初期化
           row[node+1] = row[node][:] #初期化したものを、前のリストのコピーに置き換える。
           row[node+1].append(row[node][0])
           row[node+1].pop(0)

        return row




    def bfs(self):

        #根を作成
        self.root = State(-1,-1,-1,total)        
        
        for (i, edge_len) in enumerate(self.pieces.length[0]):

            #rootのインスタンス
            self.root_tmp = State(0,-1,i,total)
            self.root_tmp.prev = self.root

            #角度と長さを追加
            for i in range(len(self.pieces.length[0])):
             
                tmp1 = i + len(self.pieces.angle[0]) - 1
                tmp2 = i + 1

                if tmp1 >= len(self.pieces.angle[0]):
                    tmp1 = tmp1 - len(self.pieces.angle[0])
                if tmp2 >= len(self.pieces.length[0]):
                    tmp2 = tmp2 - len(self.pieces.length[0]) 

                self.root_tmp.this_main_angle.append([tmp1, i])
                self.root_tmp.this_main_length.append([i,tmp2])

            #0のピースを使ったのでフラグに追加
            self.root_tmp.used_piece.remove(0)

            #self.root.next.append(self.root_tmp) nextの必要性が疑われるため

            #rootをプッシュ
            self.queue.put(self.root_tmp)
       
            



        while self.queue.empty() == False:
            #queueからpop
            self.parent = self.queue.get()          
            chindren = self._get_children(self.parent)
            #self.queue.put(children)






           
    def _get_children(self, parent):
        
            ###ベースたち###
            self.base_length = self.parent.this_length[self.parent.next_edge_n]

           


                            
                        
                            




            #もしすべてのピースを使ったら and 頂点数が枠と同じ(±1)なら
                    #完成品として出力


