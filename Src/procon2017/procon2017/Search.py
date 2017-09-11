#ここで木を作り、探索を開始する

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
from module import State

class Search:

    def __init__(self, pieces):
        self.queue = queue.Queue()
        self.pieces = pieces
        
       
    def bfs(self):


        #根を作成
        self.root = State(-1,-1)             
        for (i, edge_len) in enumerate(self.pieces.length[0]):
            #rootのインスタンス
            self.root_tmp = State(0,i)
            self.root_tmp.prev = self.root
            """self.root.next.append(self.root_tmp) nextの必要性が疑われるため"""
            #rootをプッシュ
            self.queue.put(self.root_tmp)
       

        while queue.Empty() == False:
            #queueからpop
            self.parent = self.queue.get()          

            # children = get_child(parent)
            #self.queue.put(children)


            #もしすべてのピースを使ったら and 頂点数が枠と同じ(±1)なら
                #完成品として出力
                

    def get_children(self, parent):
        
        self.length = self.pieces.length[self.parent.piece_n, self.parent.edge_n]

       for(self.parent.piece_n)