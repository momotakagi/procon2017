class draw:
    """description of class"""

    #ピースの合計値
    total = int

    #コンストラクタ
    def __init__(self, pieces):
        self.queue = queue.Queue()
        self.pieces = pieces
        global total
        total = pieces.total_piece_num


