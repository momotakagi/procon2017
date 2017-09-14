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
        
       
        ###########人力で木を組む################
        #rootのインスタンス
        self.root_tmp = State(0,-1,2,total)
        self.root_tmp.prev = self.root

        self.PIECE2 = State(2,1,3,total)
        self.PIECE2.prev = root_tmp

        self.PIECE1 = State(1,2,-1,total)
        self.PIECE1.prev = PIECE2
        
        #ここで探索そしてreturn

        children = self.PIECE1

        return children
            



"""













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
            chindren = self._get_children(self.parent)
            #self.queue.put(children)






           
    def _get_children(self, parent):
        
            ###ベースたち###
            self.base_length = self.parent.this_length[self.parent.next_edge_n]

            #いっこ前の添え字
            self.zero = self.parent.next_edge_n - 1
            if self.zero == -1:
                self.zero = len(self.parent.this_angle) - 1

            self.second = self.parent.next_edge_n + 1
            if self.second == len(self.parent.this_angle):
                self.second = 0

            self.third = self.second + 1
            if self.third == len(self.parent.this_angle):
                self.third = 0

            self.base_first_angle = self.parent.this_angle[self.parent.next_edge_n]
            self.base_second_angle = self.parent.this_angle[self.second]

            self.base_zero_length = self.parent.this_length[self.zero]
            self.base_second_length = self.parent.this_length[self.second]
            

            
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
                        
                        #角度条件満たす
                        #木に追加(インスタンス作成&深いコピー)ノードごとにブロックとして長さと角度を保持
                        #ふたつの角で条件を満たすならば
                        if self.first_total < (360 + __ANGLE_DELTA) and self.second_total < (360 + __ANGLE_DELTA):
                            
                            #i番ピースの情報
                            self.new_piece_edge = copy.deepcopy(self.pieces.length[i])
                            self.new_piece_angle = copy.deepcopy(self.pieces.angle[i])


                            
                        
                            




            #もしすべてのピースを使ったら and 頂点数が枠と同じ(±1)なら
                    #完成品として出力



"""