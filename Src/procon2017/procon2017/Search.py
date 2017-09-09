#ここで木を作り、探索を開始する

#全通りプログラム(幅優先探索)
    #キュー用意
    #キューに最初の要素を入れる
    #キューから要素を取り出す
    #要素に対して処理をする
    #要素の子供をキューに入れる
    #キューが空になるまでを繰り返す

#どっかでrootを定義

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
            self.root.next.append(State(0,i))

        #rootをプッシュ
        self.queue.put(root)


        while queue.Empty() == False:
            #queueからpop
            self.parent = self.queue.get()







