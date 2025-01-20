class MyPlayer :
    '''Hrac, ktory kopiruje posledny tah supera'''

    def __init__(self, payoff_matrix, number_of_iterations=None) :
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations
        self.last_opponent_move = False     # False = spolupráca; True = podvod
        # Zaciname s predpokladom, ze super v prvom tahu spolupracuje (False).
        # Ak nemame informaciu o predoslom tahu (prvy tah), zacneme so spolupracou.

    def select_move(self) :
        # Kopirujeme predchadzajuci tah supera.
        # Ak super posledny tah podvadzal (True), podvadzame aj my.
        # Ak super posledny tah spolupracoval (False), spolupracujeme aj my.

        return self.last_opponent_move
        # Vracia hodnotu posledneho tahu supera (True = zrada, False = spolupraca).

    def record_last_moves(self, my_last_move, opponent_last_move) :
        # Zaznamename posledny tah supera, aby sme ho mohli v nasledujucom kole skopirovat.
        # Nesmie ukladat historiu, len si zapamata posledny tah.

        self.last_opponent_move = opponent_last_move
        # Ulozime posledny tah supera do premenneho atributu.
