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


    #ピースの合計値
    total = int

    def __init__(self, pieces):
        self.queue = queue.Queue()
        self.pieces = pieces
        global total
        total = pieces.total_piece_num
       



    def bfs(self):

        #根を作成
        self.root = State(-1,-1,-1,total)        
        
        for (i, edge_len) in enumerate(self.pieces.length[0]):

            #rootのインスタンス
            self.root_tmp = State(0,-1,i,total)
            self.root_tmp.prev = self.root
            #0のピースを使ったのでフラグに追加
            self.root_tmp.used_piece.remove(0)

            #self.root.next.append(self.root_tmp) nextの必要性が疑われるため

            #rootをプッシュ
            self.queue.put(self.root_tmp)
       




        while self.queue.empty() == False:
            #queueからpop
            self.parent = self.queue.get()          

            self._get_children(self.parent)
            #self.queue.put(children)






           
    def _get_children(self, parent):
        
            self.base_length = self.pieces.length[self.parent.piece_n][self.parent.edge_n]

            #つかったピース以外のピースの数で回す
            for i in self.parent.used_piece:
                #そのi番ピースの辺の数回し長さ取得
                for c_length in self.pieces.length[i]:
                    print(c_length)




            #もしすべてのピースを使ったら and 頂点数が枠と同じ(±1)なら
                    #完成品として出力




                