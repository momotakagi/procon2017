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
        __ANGLE_DELTA = 2


    
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



    def make_piece_collection(self, piece_num):

        len_piece = len(self.pieces.length[piece_num])
        main_angle = []
        main_length = []

        for i in range(len_piece):
             
                tmp1 = i + len_piece - 1
                tmp2 = i + 1

                if tmp1 >= len_piece:
                    tmp1 = tmp1 - len_piece
                if tmp2 >= len_piece:
                    tmp2 = tmp2 - len_piece 

                main_angle.append([tmp1, i, self.pieces.angle[piece_num][i]])
                main_length.append([i,tmp2, self.pieces.length[piece_num][i]])

        return (main_angle, main_length)




    def bfs(self):
        """幅優先探索"""


        #根を作成
        root = State(-1,-1,-1,total)        
        
        for (j, edge_len) in enumerate(self.pieces.length[0]):

            #rootのインスタンス
            root_tmp = State(0,-1,j,total)
            root_tmp.prev = root

            """
            #角度と長さを追加
            for i in range(len(self.pieces.length[0])):
             
                tmp1 = i + len(self.pieces.angle[0]) - 1
                tmp2 = i + 1

                if tmp1 >= len(self.pieces.angle[0]):
                    tmp1 = tmp1 - len(self.pieces.angle[0])
                if tmp2 >= len(self.pieces.length[0]):
                    tmp2 = tmp2 - len(self.pieces.length[0]) 

                root_tmp.this_main_angle.append([tmp1, i, self.pieces.angle[0][i]])
                root_tmp.this_main_length.append([i,tmp2, self.pieces.length[0][i]])

            """

            root_tmp.this_main_angle, root_tmp.this_main_length = self.make_piece_collection(0)

            #0のピースを使ったのでフラグに追加
            root_tmp.used_piece.remove(0)

            #self.root.next.append(self.root_tmp) nextの必要性が疑われるため

            #rootをプッシュ
            self.queue.put(root_tmp)
       
            



        while self.queue.empty() == False:
            #queueからpop
            parent = self.queue.get()          
            chindren = self._get_children(parent)
            #self.queue.put(children)






           
    def _get_children(self, parent):
        """探索対象は単ピース"""


        ###ベースたち###       
        f_index = parent.this_main_length[parent.next_edge_n][0]
        s_index = parent.this_main_length[parent.next_edge_n][1]

        base_length = parent.this_main_length[parent.next_edge_n][2]
        first_angle = parent.this_main_angle[f_index][2]
        second_angle = parent.this_main_angle[s_index][2]

        
        #裏表考慮のため2回
        #iはピース番号_tmp_lenは長さ
        for double in range(2):
            for i in parent.used_piece:

                #ピースを新しいデータ型にする
                tmp_main_angle, tmp_main_length = self.make_piece_collection(i)

                for (j, tmp_len) in enumerate(self.pieces.length[i]):
                    #####長さ＆角度条件を満たす#####
                    if abs(tmp_len - base_length) < __LENGTH_DELTA:
                        #対象となる角度と足し算
                        tmp_angle1 = first_angle + tmp_main_angle[tmp_main_length[j][double]][2]
                        tmp_angle2 = second_angle + tmp_main_angle[tmp_main_length[j][double + 1 if double + 1 < 2 else 1]][2]

                        if (tmp_angle1 < 360 + __ANGLE_DELTA) and (tmp_angle2 < 360 + __ANGLE_DELTA) :

                            if abs(tmp_angle1 - 360) < __ANGLE_DELTA:
                                #angle1つまりdoubleの方のindexの辺の長さを辿る
                                #tmp_main_angle[tmp_main_length[j][double]][2]
                                next_base_length = parent.this_main_angle[f_index].index(parent.next_edge_n)


                                print("DEBUG")




                                 

      
            
        
           


                            
                        
                            

            #またどっかでnext_edgeをそのピース分生成しなくてはならない


            #もしすべてのピースを使ったら and 頂点数が枠と同じ(±1)なら
                    #完成品として出力


