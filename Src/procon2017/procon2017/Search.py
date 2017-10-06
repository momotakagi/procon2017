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
from module import Data
from functools import lru_cache
from numba import jit




class Search:
    """探索するクラス"""

    #定数群
    __LENGTH_DELTA = int
    __ANGLE_DELTA = int
    __POINT180 = int
    __POINT360 = int
    __POINT360_samelen = int
    __POINT360_difflen = int
    __BEAM_WIDTH = int

    #ピースの合計値
    total = int

    #コンストラクタ
    def __init__(self, pieces, waku_data):
        self.queue = queue.Queue()
        self.pieces = pieces
        self.waku_data = waku_data
        self.count = 0

        self.deep = len(pieces.length) - 1
        self.deep_counter = 0
        self.deep_flag = 0
        self.deep_th = 2

        global __LENGTH_DELTA
        global __ANGLE_DELTA
        global __POINT180
        global __POINT360
        global __POINT360_samelen
        global __POINT360_difflen
        global total
        global __BEAM_WIDTH

        total = pieces.total_piece_num
        __LENGTH_DELTA = 8
        __ANGLE_DELTA = 2
        __POINT180 = 100
        __POINT360 = 180
        __POINT360_samelen = 300
        __POINT360_difflen = 1
        __BEAM_WIDTH = 30


    
    def get_other_index(self, data, num):
        """引数1:逆の値を取得したい対象のリスト(1次元で) 引数2:引数1のリストの現在使っている値"""
        try:
            if data.index(num) == 0:
                return data[1]
            else:
                return data[0]
        except:
            print(data)
            print(num)
            print("error in get other")

        


    #メモ化
    @lru_cache(maxsize=1000)
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

        ######################
        Finish_Node = []
        ######################3

        #根を作成
        root = State(-1,-1,-1,total)        
        
        for (j, edge_len) in enumerate(self.pieces.length[0]):
            #rootのインスタンス
            root_tmp = State(0,-1,j,total)
            root_tmp.prev = root
            root_tmp.this_main_angle, root_tmp.this_main_length = self.make_piece_collection(0)

            #0のピースを使ったのでフラグに追加
            root_tmp.used_piece.remove(0)
            #self.root.next.append(self.root_tmp) nextの必要性が疑われるため
            #rootをプッシュ
            self.queue.put(root_tmp)
                  


        while self.queue.empty() == False:
            #queueからpop


            parent = self.queue.get()          


            if len(parent.used_piece) != self.deep_counter:

                print(parent.used_piece)
                print("DEBUG used_piece")

                self.deep_counter = len(parent.used_piece)
                self.deep_flag += 1
                if self.deep_flag == self.deep_th:
                    #深さ既定値満たしたらソートして刈る
                    print("\n\n\n\n\nビームサーチの枝刈り！！！\n\n\n\n\n")
                    tmp_sort_list = []
                    while self.queue.empty() == False:
                        __Tmp = self.queue.get()
                        tmp_sort_list.append({"object":__Tmp, "total_edge":__Tmp.total_edge, "point":__Tmp.point})

                    sorted_list = sorted(tmp_sort_list, key=lambda x:(-x["point"], x["total_edge"]))

                    for i in range(__BEAM_WIDTH):
                        if i == len(sorted_list):
                            break
                        self.queue.put(sorted_list[i]["object"])

                    self.deep_flag = 0
                    self.deep_th = 1

                    print("total_Edge=" + str(sorted_list[0]["total_edge"]))



            children = self._get_children(parent)
            
            



            for child in children:
                if child.used_piece == []:
                    #すべてのピース使ったら                                
                    #これは角の数をカウント
                    edge_num = 0
                    for x in range(len(child.this_main_length)):
                        if child.this_main_length[x][0] != -1:
                            edge_num = edge_num + 1
                    child.total_edge = edge_num

                    
                    ##################!!!!DEBUG!!!!#################
                    print("\nUsed all pieces total_edge is " + str(child.total_edge) +" point = " + str(child.point))
                    pt = child
                    while pt.piece_n != -1:                          
                        print("piece:" + str(pt.piece_n) + " next_edge" + str(pt.next_edge_n) + " prev_edge" + str(pt.prev_edge_n) + " prev_total_edge" + str(pt.prev_total_edge) + " Is_reverse=" + str(pt.Is_reverse))
                        pt = pt.prev
                    ###############################################

                    #終わったシリーズにappend
                    Finish_Node.append(child)

                else:
                    #PUSH
                    self.queue.put(child)


            print("Get Child fin" + str(self.queue.qsize()))
            



        Finish_Node = self.Sort_by_waku_data(Finish_Node)
        print("FINISH OF BFS")  

        if Finish_Node == []:
            Finish_Node.append(parent)
        return Finish_Node

    






















    
    def _get_children(self, parent):
        """探索対象は単ピース"""

        #返却される子どもたち
        rt_children = []

        ###ベースたち###       
        f_index = parent.this_main_length[parent.next_edge_n][0]
        s_index = parent.this_main_length[parent.next_edge_n][1]

        base_length = parent.this_main_length[parent.next_edge_n][2]
        first_angle = parent.this_main_angle[f_index][2]
        second_angle = parent.this_main_angle[s_index][2]

        
        
        #裏表考慮のため2回
        #iはピース番号_tmp_lenは長さ
        for double in range(1):
            double = 1
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
                            is_reverse = True
                        else:
                            double2 = 0
                            is_reverse = False

                        tmp_angle2 = second_angle + tmp_main_angle[tmp_main_length[j][double2]][2]

                       
                        self.count += 1

                        if (tmp_angle1 < 360 + __ANGLE_DELTA) and (tmp_angle2 < 360 + __ANGLE_DELTA) :
                            #角度と長さの条件を満した   


                            

                            #格納先となる子供ノードを作成
                            child = State(i, j, -1, total)
                            child.prev = parent
                            child.used_piece = copy.deepcopy(parent.used_piece)
                            child.used_piece.remove(i)       
                            child.Is_reverse = is_reverse
                            child.prev_total_edge = copy.deepcopy(parent.prev_total_edge)
                            child.prev_total_edge.append(len(parent.this_main_angle))
                            child.this_main_angle = copy.deepcopy(parent.this_main_angle)
                            child.this_main_length = copy.deepcopy(parent.this_main_length)
                            child.this_main_angle.extend(copy.deepcopy(tmp_main_angle))
                            child.this_main_length.extend(copy.deepcopy(tmp_main_length))


                            child.corr_edge = copy.deepcopy(parent.corr_edge)
                            child.corr_edge.append([i, f_index, s_index, tmp_main_length[j][double], tmp_main_length[j][double2]])


                            #後ろに追加したのでインデックスすべて更新
                            _old_len = len(parent.this_main_angle)
                            for z in range(len(tmp_main_angle)):  
                                child.this_main_angle[_old_len + z][0] += _old_len
                                child.this_main_angle[_old_len + z][1] += _old_len
                                child.this_main_length[_old_len + z][0] += _old_len
                                child.this_main_length[_old_len + z][1] += _old_len


                            #使ったエッジを消去するフラグ
                            #edge_flag = [z for z in range(len(self.pieces.length[i]))]
                            #edge_flag.remove(j)

                             #角度の統合
                            child.this_main_angle[f_index][2] = tmp_angle1
                            child.this_main_angle[s_index][2] = tmp_angle2




                            ###
                            #辺mainのindex update(新しい方のindexに変更)
                            #f_index s_indexの角が古い方でそれを指しているindexを新しいのに変更                           
                            ###いる？これ

                           
                            

#######################################################################################################################################################################

                            """angle1 !! ここから 180 360 の辺の統合処理(各辺と角が格納されているデータベースのアップデート作業)"""

                            if abs(tmp_angle1 - 180) < __ANGLE_DELTA:

                                ###180度を獲得したのでポイント
                                child.point += __POINT180


                                #辺main処理→base側角をtmp側角を指すように tmp側角をbase側角を指すように
                                _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[j][double]], j)
                                _tmp_base_other = self.get_other_index(parent.this_main_angle[f_index], parent.next_edge_n)

                                __tmp_hit_angle1_index = child.this_main_length[_tmp_other + _old_len].index(tmp_main_length[j][double] + _old_len) #これにbaseの角代入
                                __base_hit_angle1_index = child.this_main_length[_tmp_base_other].index(f_index) #これにtmpの角代入

                                __tmp_next_edge = self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[j][double] + _old_len)
                                child.this_main_length[_tmp_other + _old_len][__tmp_hit_angle1_index] = self.get_other_index(child.this_main_length[_tmp_base_other], f_index) #tmpの辺mainの角にこれ代入
                                child.this_main_length[_tmp_base_other][__base_hit_angle1_index] =__tmp_next_edge #baseの辺mainの角にこれ代入
                                
                                #辺の長さ加算(base tmp 両側に(念のため))(たぶんいらない)
                                child.this_main_length[_tmp_base_other][2] += child.this_main_length[_tmp_other + _old_len][2]
                                child.this_main_length[_tmp_other + _old_len][2] += child.this_main_length[_tmp_base_other][2]

                                #角main処理
                                child.this_main_angle[__tmp_next_edge][child.this_main_angle[__tmp_next_edge].index(_tmp_other + _old_len)] = _tmp_base_other

                                #使えない辺を-1にする
                                child.this_main_length[_tmp_other + _old_len][0] = -1
                                child.this_main_length[_tmp_other + _old_len][1] = -1




                                 
                               
                            elif abs(tmp_angle1 - 360) < __ANGLE_DELTA:


                                ###360を獲得したのでポイント給付
                                child.point += __POINT360


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
                                        if abs((next_tmp_ang + next_base_ang) - 180) < __ANGLE_DELTA:
                                            #####そしてとなり180###########

                                            ###180度を獲得したのでポイント
                                            child.point += __POINT180

                                            ######update処理##########
                                            _side = tmp_main_length[_tmp_other].index(self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side]))
                                            _t_index = _tmp_other
                                            _side_main =  parent.this_main_length[_tmp_base_other].index(self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main]))
                                            _m_index = _tmp_base_other
                                            ##########################

                                            _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[_t_index][_side]], _t_index)                         
                                            _tmp_base_other = self.get_other_index(parent.this_main_angle[parent.this_main_length[_m_index][_side_main]], _m_index)


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

                                            #使えない辺を-1にする
                                            child.this_main_length[_m_index][0] = -1
                                            child.this_main_length[_m_index][1] = -1
                                            child.this_main_length[_t_index + _old_len][0] = -1
                                            child.this_main_length[_t_index + _old_len][1] = -1
                                            child.this_main_length[_tmp_other + _old_len][0] = -1
                                            child.this_main_length[_tmp_other + _old_len][1] = -1





                                        elif abs((next_tmp_ang + next_base_ang) - 360) < __ANGLE_DELTA:
                                            roop_flag = True
                                            print("360だったので次に移行します1")


                                            ###360を獲得したのでポイント給付
                                            child.point += __POINT360
                                        




                                        else:
                                            #[長さ一致360]     
                                            
                                            #点数付与
                                            child.point += __POINT360_samelen
                                            

                                            __tmp_next_edge =  self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[_t_index][_side] + _old_len)
                                            __base_next_edge = self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main])

                                            #長さを加算
                                            child.this_main_angle[__base_next_edge][2] += child.this_main_angle[__tmp_next_edge][2]


                                            ######update処理##########
                                            _side = tmp_main_length[_tmp_other].index(self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side]))
                                            _t_index = _tmp_other
                                            _side_main =  parent.this_main_length[_tmp_base_other].index(self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main]))
                                            _m_index = _tmp_base_other
                                           
                                            _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[_t_index][_side]], _t_index)                         
                                            _tmp_base_other = self.get_other_index(parent.this_main_angle[parent.this_main_length[_m_index][_side_main]], _m_index)
                                            ##########################

                                            #角mainを変更
                                            child.this_main_angle[__base_next_edge][child.this_main_angle[__base_next_edge].index(_m_index)] = _tmp_other + _old_len

                                            #辺mainを変更
                                            child.this_main_length[_tmp_other + _old_len][child.this_main_length[_tmp_other + _old_len].index(__tmp_next_edge)] = __base_next_edge


                                            #今後使わない辺を-1する[通常]
                                            child.this_main_length[_t_index + _old_len][0] = -1
                                            child.this_main_length[_t_index + _old_len][1] = -1
                                            child.this_main_length[_m_index][0] = -1
                                            child.this_main_length[_m_index][1] = -1


                                    elif next_tmp_length < next_base_length and next_tmp_ang > 180 + __ANGLE_DELTA:
                                        #短くて角度いかれてるヤツ
                                        #おけない確定なので次！
                                        print("えだがり")
                                        continue



                                    else:
                                        #[通常360]

                                        child.point += __POINT360_difflen

                                        _delta_length = abs(next_tmp_length - next_base_length)
                                        child.this_main_length[_tmp_base_other][2] = _delta_length
                                        #辺main→辺のindex変更(baseへ)
                                        __tmp_next_edge =  self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[_t_index][_side] + _old_len)
                                        child.this_main_length[_tmp_base_other][child.this_main_length[_tmp_base_other].index(parent.this_main_length[_m_index][_side_main])] = __tmp_next_edge
                                            
                                        #角mian→角のindex変更と値の更新
                                        child.this_main_angle[__tmp_next_edge][2] += 180
                                        child.this_main_angle[__tmp_next_edge][tmp_main_angle[self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side])].index(_tmp_other)] = _tmp_base_other

                                        #今後使わない辺を-1する[通常]
                                        child.this_main_length[_tmp_other + _old_len][0] = -1
                                        child.this_main_length[_tmp_other + _old_len][1] = -1



                                    if roop_flag == False:
                                        break
                                    else:
                                        roop_flag = False
                                    

                                        #前回の_sideじゃない方を_sideとして指定
                                    _side = tmp_main_length[_tmp_other].index(self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side]))
                                    _t_index = _tmp_other
                                    _side_main =  parent.this_main_length[_tmp_base_other].index(self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main]))
                                    _m_index = _tmp_base_other
                                
                                    #今後使わない辺を-1する
                                    child.this_main_length[_tmp_other + _old_len][0] = -1
                                    child.this_main_length[_tmp_other + _old_len][1] = -1
                                    child.this_main_length[_tmp_base_other][0] = -1
                                    child.this_main_length[_tmp_base_other][1] = -1
                                
                                
                    
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

                                



  #######################################################################################################################################################################                              
                                
                                                           


                            """angle 2 !! ここから 180 360 の辺の統合処理(各辺と角が格納されているデータベースのアップデート作業)"""

                            if abs(tmp_angle2 - 180) < __ANGLE_DELTA:

                                ###180度を獲得したのでポイント
                                child.point += __POINT180


                                #辺main処理→base側角をtmp側角を指すように tmp側角をbase側角を指すように
                                _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[j][double2]], j)
                                _tmp_base_other = self.get_other_index(parent.this_main_angle[s_index], parent.next_edge_n)

                                __tmp_hit_angle1_index = child.this_main_length[_tmp_other + _old_len].index(tmp_main_length[j][double2] + _old_len) #これにbaseの角代入
                                __base_hit_angle1_index = child.this_main_length[_tmp_base_other].index(s_index) #これにtmpの角代入

                                __tmp_next_edge = self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[j][double2] + _old_len)
                                child.this_main_length[_tmp_other + _old_len][__tmp_hit_angle1_index] = self.get_other_index(child.this_main_length[_tmp_base_other], s_index) #tmpの辺mainの角にこれ代入
                                child.this_main_length[_tmp_base_other][__base_hit_angle1_index] =__tmp_next_edge #baseの辺mainの角にこれ代入
                                
                                #辺の長さ加算(base tmp 両側に(念のため))
                                child.this_main_length[_tmp_base_other][2] += child.this_main_length[_tmp_other + _old_len][2]
                                child.this_main_length[_tmp_other + _old_len][2] += child.this_main_length[_tmp_base_other][2]



                                #角main処理
                                child.this_main_angle[__tmp_next_edge][child.this_main_angle[__tmp_next_edge].index(_tmp_other + _old_len)] = _tmp_base_other

                                #使えない辺を-1にする
                                child.this_main_length[_tmp_other + _old_len][0] = -1
                                child.this_main_length[_tmp_other + _old_len][1] = -1

                                

                                 
                               
                            elif abs(tmp_angle2 - 360) < __ANGLE_DELTA:
                                

                                ###360を獲得したのでポイント給付
                                child.point += __POINT360



                                ########変数群#########
                                _side = double2
                                _side_main = 1
                                _t_index = j
                                _m_index = parent.next_edge_n
                                roop_flag = False
                                #parent.this_main_length[parent.next_edge_n][0]
                                #s_index =  parent.this_main_length[_m_index][_side_main]
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
                                        if abs((next_tmp_ang + next_base_ang) - 180) < __ANGLE_DELTA:
                                            #そしてとなり180

                                            ###180度を獲得したのでポイント
                                            child.point += __POINT180


                                            ####update#######
                                            _side = tmp_main_length[_tmp_other].index(self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side]))
                                            _t_index = _tmp_other
                                            _side_main =  parent.this_main_length[_tmp_base_other].index(self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main]))
                                            _m_index = _tmp_base_other

                                            _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[_t_index][_side]], _t_index)                         
                                            _tmp_base_other = self.get_other_index(parent.this_main_angle[parent.this_main_length[_m_index][_side_main]], _m_index)


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

                                            #使えない辺を-1にする5
                                            child.this_main_length[_m_index][0] = -1
                                            child.this_main_length[_m_index][1] = -1
                                            child.this_main_length[_t_index  + _old_len][0] = -1
                                            child.this_main_length[_t_index  + _old_len][1] = -1
                                            child.this_main_length[_tmp_other + _old_len][0] = -1
                                            child.this_main_length[_tmp_other + _old_len][1] = -1

                                        elif abs((next_tmp_ang + next_base_ang) - 360) < __ANGLE_DELTA:
                                            roop_flag = True
                                            print("360だったので次に移行します2")

                                            ###360を獲得したのでポイント給付
                                            child.point += __POINT360

                                            
                                        

                                        else:
                                            #[長さ一致360]  
                                            
                                            child.point += __POINT360_samelen
                                                                                   
                                            __tmp_next_edge =  self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[_t_index][_side] + _old_len)
                                            __base_next_edge = self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main])

                                            #長さを加算
                                            child.this_main_angle[__base_next_edge][2] += child.this_main_angle[__tmp_next_edge][2]


                                            ######update処理##########
                                            _side = tmp_main_length[_tmp_other].index(self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side]))
                                            _t_index = _tmp_other
                                            _side_main =  parent.this_main_length[_tmp_base_other].index(self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main]))
                                            _m_index = _tmp_base_other

                                            _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[_t_index][_side]], _t_index)                         
                                            _tmp_base_other = self.get_other_index(parent.this_main_angle[parent.this_main_length[_m_index][_side_main]], _m_index)

                                            ##########################

                                            #角mainを変更
                                            child.this_main_angle[__base_next_edge][child.this_main_angle[__base_next_edge].index(_m_index)] = _tmp_other + _old_len

                                            #辺mainを変更
                                            child.this_main_length[_tmp_other + _old_len][child.this_main_length[_tmp_other + _old_len].index(__tmp_next_edge)] = __base_next_edge


                                            #今後使わない辺を-1する[通常]
                                            child.this_main_length[_t_index + _old_len][0] = -1
                                            child.this_main_length[_t_index + _old_len][1] = -1
                                            child.this_main_length[_m_index][0] = -1
                                            child.this_main_length[_m_index][1] = -1



                                    elif next_tmp_length < next_base_length and next_tmp_ang > 180 + __ANGLE_DELTA:
                                        #短くて角度いかれてるヤツ
                                        #おけない確定なので次！
                                        print("えだがり")
                                        continue


                                    else:
                                        #[通常360]

                                        child.point += __POINT360_difflen

                                        _delta_length = abs(next_tmp_length - next_base_length)
                                        child.this_main_length[_tmp_base_other][2] = _delta_length
                                        #辺main→辺のindex変更(baseへ)
                                        __tmp_next_edge =  self.get_other_index(child.this_main_length[_tmp_other + _old_len], tmp_main_length[_t_index][_side] + _old_len)
                                        child.this_main_length[_tmp_base_other][child.this_main_length[_tmp_base_other].index(parent.this_main_length[_m_index][_side_main])] = __tmp_next_edge
                                        
                                        #角mian→角のindex変更と値の更新
                                        child.this_main_angle[__tmp_next_edge][2] += 180
                                        child.this_main_angle[__tmp_next_edge][tmp_main_angle[self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side])].index(_tmp_other)] = _tmp_base_other

                                        #今後使わない辺を-1する[通常]
                                        child.this_main_length[_tmp_other + _old_len][0] = -1
                                        child.this_main_length[_tmp_other + _old_len][1] = -1




                                    if roop_flag == False:
                                        break
                                    else:
                                        roop_flag = False
                                    

                                        #前回の_sideじゃない方を_sideとして指定
                                    _side = tmp_main_length[_tmp_other].index(self.get_other_index(tmp_main_length[_tmp_other], tmp_main_length[_t_index][_side]))
                                    _t_index = _tmp_other
                                    _side_main =  parent.this_main_length[_tmp_base_other].index(self.get_other_index(child.this_main_length[_tmp_base_other], parent.this_main_length[_m_index][_side_main]))
                                    _m_index = _tmp_base_other
                                

                                    #今後使わない辺を-1する
                                    child.this_main_length[_tmp_other + _old_len][0] = -1
                                    child.this_main_length[_tmp_other + _old_len][1] = -1
                                    child.this_main_length[_tmp_base_other][0] = -1
                                    child.this_main_length[_tmp_base_other][1] = -1
                                

                            else:
                                #angle tmp1 がとりあえず[通常状態]
                                #通常[
                                    #辺mainはtmpの比較の隣接する辺の角を指しているindexを古いものに更新
                                    #角mainはbase側の角の辺を指しているindexをtmp側に更新
                                #]
                                #後index系はchildで統一
                                #tmp側のindexはj                               
                                _tmp_other = self.get_other_index(tmp_main_angle[tmp_main_length[j][double2]], j)
                                child.this_main_length[_tmp_other + _old_len][child.this_main_length[_tmp_other + _old_len].index(tmp_main_length[j][double2] + _old_len)] = s_index

                                child.this_main_angle[s_index][parent.this_main_angle[s_index].index(parent.next_edge_n)] = _tmp_other + _old_len

                                


                            #辺ｍainのぶつかっている辺を削除
                            child.this_main_length[parent.next_edge_n][0] = -1
                            child.this_main_length[parent.next_edge_n][1] = -1
                            child.this_main_length[len(parent.this_main_length) + j][0] = -1
                            child.this_main_length[len(parent.this_main_length) + j][1] = -1

                            
                                
      
#######################################################################################################################################################################            
                                                    

                            #next_edgeをそのピースの辺分生成

                            if child.used_piece == []:
                                rt_children.append(child)
                            else:
                                
                                count = 0
                                for x in range(len(child.this_main_length)):
                                    if child.this_main_length[x][0] != -1:
                                        count += 1

                                for x in range(len(child.this_main_length)):
                                    if child.this_main_length[x][0] != -1:
                                        tmp_child = copy.deepcopy(child)
                                        tmp_child.next_edge_n = x   
                                        tmp_child.total_edge = count
                                        rt_children.append(tmp_child)

                                                           

                        
            
        return rt_children

            #もしすべてのピースを使ったら and 頂点数が枠と同じ(±1)なら
                    #完成品として出力





    def Sort_by_waku_data(self, fin_node):
       
       

        #すべての角度を反転
        Angles = [360-x for x in self.waku_data.angle[0]]

        dic_fin_node = []

        for (index, node) in enumerate(fin_node):
            #角度を取り出す
            length_1dg = []
            tmp_angles = []
            matched_list = []

            length_1dg = [flatten for inner in node.this_main_length for flatten in inner]
            for i in range(len(node.this_main_angle)):
                if i in length_1dg:
                    tmp_angles.append(node.this_main_angle[i][2])

            
            
            matched_list = []
            for j in reversed(range(len((Angles)))):
                for k in reversed(range(len((tmp_angles)))):
                    if abs(Angles[j] - tmp_angles[k]) < __ANGLE_DELTA:
                        matched_list.append(tmp_angles[k])
                        del tmp_angles[k]
                        break


                

           

            dic_fin_node.append({"node":node, "match_len":len(matched_list),"total_edge":node.total_edge})



        dic_fin_node = sorted(dic_fin_node, key=lambda x:(x["total_edge"], -x["match_len"]))



        return [dic_fin_node[j]["node"] for j in range(len(dic_fin_node))]