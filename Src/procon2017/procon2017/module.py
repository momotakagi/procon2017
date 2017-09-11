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




class State:
     
    #コンストラクタ
    def __init__(self, piece_n, edge_n):
        '''木の要素'''
        self.piece_n = piece_n
        self.edge_n = edge_n

        #現在つかったピース
        self.used_piece = []

        #評価値
        self.point = 0

        #現在の頂点数
        self.total_edge = 0

        #前のTree
        self.prev
        #次のTree
        #self.next = []
        
        

   



   


    


   

