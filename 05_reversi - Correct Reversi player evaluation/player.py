import random

class MyPlayer:
    '''Hráč Reversi - pro první odevzdání hledá náhodně platné tahy.'''

    def __init__(self, my_color, opponent_color):
        self.my_color = my_color
        self.opponent_color = opponent_color

    def select_move(self, board):
        # Najdeme všechny platné tahy
        valid_moves = self.find_valid_moves(board)

        # Pokud nejsou platné tahy, vrátíme None
        if not valid_moves:
            return None

        # Vybereme náhodný tah z platných tahů
        return random.choice(valid_moves)

    def find_valid_moves(self, board):
        '''Vrací seznam všech platných tahů ve formátu (řádek, sloupec)'''
        valid_moves = []
        n = len(board)

        # Procházíme každé políčko
        for r in range(n):
            for c in range(n):
                if self.is_valid_move(r, c, board):
                    valid_moves.append((r, c))
        return valid_moves

    def is_valid_move(self, r, c, board):
        '''Kontroluje, zda tah na pozici (r, c) je platný podle pravidel hry Reversi'''
        if board[r][c] != -1:
            return False  # Políčko není prázdné

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        n = len(board)

        # Kontrola ve všech směrech
        for dr, dc in directions:
            if self.check_direction(r, c, dr, dc, board):
                return True
        return False

    def check_direction(self, r, c, dr, dc, board):
        '''Kontrola v jednom směru (dr, dc) pro pravidla Reversi'''
        n = len(board)
        r += dr
        c += dc
        count = 0

        while 0 <= r < n and 0 <= c < n:
            if board[r][c] == self.opponent_color:
                count += 1
            elif board[r][c] == self.my_color:
                return count > 0  # Platný tah pouze pokud je alespoň 1 soupeřův kámen mezi
            else:
                break  # Dosáhli jsme prázdného pole
            r += dr
            c += dc
        return False
