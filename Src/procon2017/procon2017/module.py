"""
selfを付けるとクラスのインスタンス変数になる
selfとは自分自身のインスタンスを指す変数である
selfを付けないと、全てのインスタンスで変数が共有される
"""


class Data:
    '''データ型'''

    def __init__(self):

        self.polygon = []
        self.Center_G = []
        self.length = [[]]
        self.angle = [[]]
        self.pixels = []
        self.total_piece_num = int




class State:
     
    #コンストラクタ
    def __init__(self, piece_n, prev_edge_n, next_edge_n, total_piece_num):
        '''木の要素'''
        self.piece_n = piece_n
        self.prev_edge_n = prev_edge_n
        self.next_edge_n = next_edge_n

        #現在つかったピース
        self.used_piece = list(range(total_piece_num))


        #新しいデータ型
        #このブロック長さ&角度
        #this main lengthの場合　[[1番目の角度のindex, 2番目の角度のindex, 実際の角度], ...]
        self.this_main_length = []
        self.this_main_angle = []
        

        #表裏判定
        self.Is_reverse = True


        #評価値
        self.point = 0

        #現在の頂点数
        self.total_edge = 0

        #前のTree
        self.prev = object
        #次のTree
        #self.next = []
        
        

   



   


    


   

