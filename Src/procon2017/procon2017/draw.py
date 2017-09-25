class Draw:
    """description of class"""


    def __init__(self, child, pieces):
        print("test")
        #例
        now_node = child
        for i in range(3):
            print("piece:" + str(now_node.piece_n) + " next_edge:" + str(now_node.next_edge_n) + " prev_edge:" + str(now_node.prev_edge_n))
            now_node = now_node.prev
            
        #ここに描画の関数を書く

