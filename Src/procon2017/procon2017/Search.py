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

    #コンストラクタ
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


    def get_other_index(self, data, num):
        """引数1:逆の値を取得したい対象のリスト(1次元で) 引数2:引数1のリストの現在使っている値"""
        
        if data.index(num) == 0:
            return data[1]
        else:
            return data[0]

        




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
                """子供を作成"""

                #ピースを新しいデータ型にする
                tmp_main_angle, tmp_main_length = self.make_piece_collection(i)

                for (j, tmp_len) in enumerate(self.pieces.length[i]):
                    #####長さ＆角度条件を満たす#####
                    if abs(tmp_len - base_length) < __LENGTH_DELTA:
                        #対象となる角度と足し算
                        tmp_angle1 = first_angle + tmp_main_angle[tmp_main_length[j][double]][2]

                        if double == 0:
                            double2 = 1
                        else:
                            double2 = 0

                        tmp_angle2 = second_angle + tmp_main_angle[tmp_main_length[j][double2]][2]

                        if (tmp_angle1 < 360 + __ANGLE_DELTA) and (tmp_angle2 < 360 + __ANGLE_DELTA) :
                            
                            #格納先となる子供ノードを作成
                            child = State(i, j, -1, total)
                            child.prev = parent
                            child.used_piece.remove(i)
                            child.this_main_angle = copy.deepcopy(parent.this_main_angle)
                            child.this_main_length = copy.deepcopy(parent.this_main_length)
                            child.this_main_angle.extend(copy.deepcopy(tmp_main_angle))
                            child.this_main_length.extend(copy.deepcopy(tmp_main_length))
                            #後ろに追加したのでインデックスすべて更新
                            _old_len = len(parent.this_main_angle)
                            for z in range(len(tmp_main_angle)):  
                                child.this_main_angle[_old_len + z][0] += _old_len
                                child.this_main_angle[_old_len + z][1] += _old_len
                                child.this_main_length[_old_len + z][0] += _old_len
                                child.this_main_length[_old_len + z][1] += _old_len


                            #使ったエッジを消去するフラグ
                            edge_flag = [z for z in range(len(self.pieces.length[i]))]
                            edge_flag.remove(j)

                             #角度の統合
                            child.this_main_angle[f_index][2] = tmp_angle1
                            child.this_main_angle[s_index][2] = tmp_angle2


                            """
                            #辺mainの削除(通常)
                            #辺ｍainのぶつかっている辺を削除
                            child.this_main_length[parent.next_edge_n][0] = -1
                            child.this_main_length[parent.next_edge_n][1] = -1
                            child.this_main_length[len(parent.this_main_length) + j][0] = -1
                            child.this_main_length[len(parent.this_main_length) + j][1] = -1
                            """

                            ###
                            #辺mainのindex update(新しい方のindexに変更)
                            #f_index s_indexの角が古い方でそれを指しているindexを新しいのに変更                           
                            ###いる？これ

                           
                            



                            """ここから 180 360 の辺の統合処理(各辺と角が格納されているデータベースのアップデート作業)"""

                            if abs(tmp_angle1 - 180) < __ANGLE_DELTA:

                                #辺main処理→base側角をtmp側角を指すように tmp側角をbase側角を指すように
                                _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[j][double]], j)
                                _tmp_base_other = self.get_other_index(parent.this_main_angle[f_index], parent.next_edge_n)

                                __tmp_hit_angle1_index = child.this_main_length[_tmp_other + _old_len].index(tmp_main_length[j][double] + _old_len) #これにbaseの角代入
                                __base_hit_angle1_index = child.this_main_length[_tmp_base_other].index(f_index) #これにtmpの角代入

                                __tmp_next_edge = self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[j][double] + _old_len)
                                child.this_main_length[_tmp_other + _old_len][__tmp_hit_angle1_index] = self.get_other_index(child.this_main_length[_tmp_base_other], f_index) #tmpの辺mainの角にこれ代入
                                child.this_main_length[_tmp_base_other][__base_hit_angle1_index] =__tmp_next_edge #baseの辺mainの角にこれ代入
                                
                                #辺の長さ加算(base tmp 両側に(念のため))
                                child.this_main_length[_tmp_base_other][2] += child.this_main_length[_tmp_other + _old_len][2]
                                child.this_main_length[_tmp_other + _old_len][2] += child.this_main_length[_tmp_base_other][2]



                                #角main処理
                                child.this_main_angle[__tmp_next_edge][child.this_main_angle[__tmp_next_edge].index(_tmp_other + _old_len)] = _tmp_base_other


                                print("DEBUG")

                                """
                                #辺の長さを統合

                                _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[_t_index][_side]], _t_index)
                                next_tmp_length = tmp_main_length[_tmp_other][2]
                                edge_flag.remove(_tmp_other)

                                _tmp_base_other = self.get_other_index(parent.this_main_angle[parent.this_main_length[_m_index][_side_main]], _m_index)
                                next_base_length = child.this_main_length[_tmp_base_other][2]
                                #角度を格納
                                #child.this_main_length[_tmp_base_other][2] = next_main_length + next_tmp_length
                                 """     
     
                                 
                               
                            elif abs(tmp_angle1 - 360) < __ANGLE_DELTA:
                                print("DEBUG")
                                ########変数群#########
                                _side = double
                                _side_main = 0
                                _t_index = j
                                _m_index = parent.next_edge_n
                                roop_flag = False
                                #parent.this_main_length[parent.next_edge_n][0]
                                #f_index =  parent.this_main_length[_m_index][_side_main]
                                #######################

                                for edge in range(len(self.pieces.length[i]) - 2):
                                     

                                    #angle1つまり_sideの方のindexの辺の長さを辿る
                                    #360になった方の長さ取得
                                    _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[_t_index][_side]], _t_index)                         
                                    _tmp_base_other = self.get_other_index(parent.this_main_angle[parent.this_main_length[_m_index][_side_main]], _m_index)

                                    next_tmp_length = tmp_main_length[_tmp_other][2]
                                    next_base_length = parent.this_main_length[_tmp_base_other][2]

                                    next_tmp_ang = tmp_main_angle[self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side])][2]
                                    next_base_ang = parent.this_main_angle[self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main])][2]

                                    
                                    if abs(next_tmp_length - next_base_length) < __LENGTH_DELTA:
                                        #となりと長さ一致
                                        if abs((next_tmp_ang + next_base_ang) - 180) < __LENGTH_DELTA:
                                            #そしてとなり180
                                            #辺main処理→base側角をtmp側角を指すように tmp側角をbase側角を指すように
                                            __tmp_hit_angle1_index = child.this_main_length[_tmp_other + _old_len].index(tmp_main_length[_t_index][_side] + _old_len) #これにbaseの角代入
                                            __base_hit_angle1_index = child.this_main_length[_tmp_base_other].index(parent.this_main_length[_m_index][_side_main]) #これにtmpの角代入

                                            __tmp_next_edge = self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[_t_index][_side] + _old_len)
                                            child.this_main_length[_tmp_other + _old_len][__tmp_hit_angle1_index] = self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main]) #tmpの辺mainの角にこれ代入
                                            child.this_main_length[_tmp_base_other][__base_hit_angle1_index] =__tmp_next_edge #baseの辺mainの角にこれ代入
                                
                                            #辺の長さ加算(base tmp 両側に(念のため))
                                            child.this_main_length[_tmp_base_other][2] += child.this_main_length[_tmp_other + _old_len][2]
                                            child.this_main_length[_tmp_other + _old_len][2] += child.this_main_length[_tmp_base_other][2]

                                            #角main処理
                                            child.this_main_angle[__tmp_next_edge][child.this_main_angle[__tmp_next_edge].index(_tmp_other + _old_len)] = _tmp_base_other

                                            


                                        elif abs((next_tmp_ang + next_base_ang) - 360) < __LENGTH_DELTA:
                                            roop_flag = True
                                            print("360だったので次に移行します")
                                        
                                        else:
                                            #[通常360]
                                            _delta_length = abs(next_tmp_length - next_base_length)
                                            child.this_main_length[_tmp_base_other][2] = _delta_length
                                            #辺main→辺のindex変更(baseへ)
                                            __tmp_next_edge =  self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[_t_index][_side] + _old_len)
                                            child.this_main_length[_tmp_base_other][child.this_main_length[_tmp_base_other].index(parent.this_main_length[_m_index][_side_main])] = __tmp_next_edge
                                            
                                            #角mian→角のindex変更と値の更新
                                            child.this_main_angle[__tmp_next_edge][2] += 180
                                            child.this_main_angle[__tmp_next_edge][tmp_main_angle[self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side])].index(_tmp_other)] = _tmp_base_other

                                            print("BREAK POINT")







                                    if roop_flag == False:
                                        break
                                    else:
                                        roop_flag = False
                                    

                                        #前回の_sideじゃない方を_sideとして指定
                                    _side = tmp_main_length[_tmp_other].index(self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side]))
                                    _t_index = _tmp_other
                                    _side_main =  parent.this_main_length[_tmp_base_other].index(self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main]))
                                    _m_index = _tmp_base_other
                                




                            else:
                                #angle tmp1 がとりあえず[通常状態]
                                #通常[
                                    #辺mainはtmpの比較の隣接する辺の角を指しているindexを古いものに更新
                                    #角mainはbase側の角の辺を指しているindexをtmp側に更新
                                #]
                                #後index系はchildで統一
                                #tmp側のindexはj                               
                                _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[j][double]], j)
                                child.this_main_length[_tmp_other + _old_len][child.this_main_length[_tmp_other + _old_len].index(tmp_main_length[j][double] + _old_len)] = f_index

                                child.this_main_angle[f_index][parent.this_main_angle[f_index].index(parent.next_edge_n)] = _tmp_other + _old_len

                                print("通常")


                            #辺ｍainのぶつかっている辺を削除
                            child.this_main_length[parent.next_edge_n][0] = -1
                            child.this_main_length[parent.next_edge_n][1] = -1
                            child.this_main_length[len(parent.this_main_length) + j][0] = -1
                            child.this_main_length[len(parent.this_main_length) + j][1] = -1

                            print("BREAK POINT")
 
                                
                                


                                


                                
      
            
        
           


                            
                        
                            

            #またどっかでnext_edgeをそのピース分生成しなくてはならない


            #もしすべてのピースを使ったら and 頂点数が枠と同じ(±1)なら
                    #完成品として出力


