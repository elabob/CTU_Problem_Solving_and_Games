class MyPlayer :
    '''Hraci objekt s vylepsenou strategiou pre Reversi.'''

    def __init__(self, my_color, opponent_color) :
        '''Inicializuje hraca s farbou a farbou protivnika.'''
        self.my_color = my_color  # Nastavi farbu hraca
        self.opponent_color = opponent_color  # Nastavi farbu protivnika

    def select_move(self, board) :
        '''Vyberie najlepsie mozne tahy pomocou minimax algoritmu.'''
        # Dynamicka hlbka pre minimax: ak je hra v koncovej faze, hlbka sa zvysi.
        depth = 4 if self.is_endgame(board) else 3  # Ak je koniec hry, zvysi sa hlbka
        best_score = float('-inf')  # Inicializujeme najhorsie mozne skore
        best_move = None  # Inicializujeme najlepsie mozne tahy

        # Ziskame vsetky platne tahy
        valid_moves = self.find_valid_moves(board)  # Ziskame platne tahy
        if not valid_moves :
            return None  # Ak nie su platne tahy, vratime None.

        # Pre kazdy platny tah simulujeme hru a hodnotime tahy
        for move in valid_moves :
            new_board = self.simulate_move(board, move, self.my_color)  # Simulujeme tah
            score = self.minimax(new_board, depth - 1, False, float('-inf'), float('inf'))  # Vyhodnotime tah pomocou minimax algoritmu
            if score > best_score :
                best_score = score  # Ak je tento tah lepsi, ulozime ho
                best_move = move

        return best_move  # Vratime najlepsie hodnoteny tah

    def minimax(self, board, depth, is_maximizing, alpha, beta) :
        '''Minimax algoritmus s alfa-beta orezavanim pre optimalizaciu.'''
        # Ak dosiahne hlbku 0 alebo nie su platne tahy, vyhodnotime dosku
        if depth == 0 or not self.find_valid_moves(board) :
            return self.evaluate_board(board)  # Vyhodnotime stav dosky

        # Maximizing player - hrac, ktory sa snazi maximalizovat svoje skore
        if is_maximizing :
            max_eval = float('-inf')  # Inicializujeme najvyssie skore
            for move in self.find_valid_moves(board) :
                new_board = self.simulate_move(board, move, self.my_color)  # Simulujeme tah
                eval = self.minimax(new_board, depth - 1, False, alpha, beta)  # Rekurzivne vyhodnotime nas tah
                max_eval = max(max_eval, eval)  # Aktualizujeme najvyssie skore
                alpha = max(alpha, eval)  # Alfa orezavanie
                if beta <= alpha :
                    break  # Alfa-beta orezavanie
            return max_eval  # Vratime najvyssie skore

        # Minimizing player - protivnik sa snazi minimalizovat nase skore
        else :
            min_eval = float('inf')  # Inicializujeme najnizsie skore
            for move in self.find_valid_moves(board) :
                new_board = self.simulate_move(board, move, self.opponent_color)  # Simulujeme tah protivnika
                eval = self.minimax(new_board, depth - 1, True, alpha, beta)  # Rekurzivne vyhodnotime tah protivnika
                min_eval = min(min_eval, eval)  # Aktualizujeme najnizsie skore
                beta = min(beta, eval)  # Beta orezavanie
                if beta <= alpha :
                    break  # Alfa-beta orezavanie
            return min_eval  # Vratime najnizsie skore

    def find_valid_moves(self, board) :
        '''Ziska vsetky platne tahy podla pravidiel Reversi.'''
        valid_moves = []  # Zoznam platnych tahov
        n = len(board)  # Velkost dosky

        for r in range(n) :
            for c in range(n) :
                if self.is_valid_move(r, c, board) :  # Skontrolujeme, ci je tah na tomto poli platny
                    valid_moves.append((r, c))  # Ak je tah platny, pridame ho do zoznamu platnych tahov

        return valid_moves  # Vratime zoznam platnych tahov

    def is_valid_move(self, r, c, board) :
        '''Skontroluje, ci je tah na pozicii (r, c) platny.'''
        # Tah je neplatny, ak nie je na prazdnej policke
        if board[r][c] != -1 :
            return False

        # Kontrolujeme, ci existuje smer, v ktorom je mozne ziskat kamene
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]  # Možné smerové vektory
        for dr, dc in directions :
            if self.check_direction(r, c, dr, dc, board) :  # Skontrolujeme, ci v tomto smere vieme ziskat kamene
                return True

        return False  # Ak nie je mozne ziskat kamene, tah je neplatny

    def check_direction(self, r, c, dr, dc, board) :
        '''Kontroluje, ci je mozne ziskat kamene v jednom smere.'''
        n = len(board)  # Velkost dosky
        r += dr
        c += dc
        count = 0  # Pocitadlo kameni

        # Pohybujeme sa v smere a pocitame kamene proti hracovi
        while 0 <= r < n and 0 <= c < n :
            if board[r][c] == self.opponent_color :
                count += 1  # Ak je to kamen protivnika, pocitame ho
            elif board[r][c] == self.my_color :
                return count > 0  # Ak narazime na nas kamen, vratime True, ak sme predtym pocitali kamene
            else :
                break  # Ak narazime na prazdnu policku, tah nie je platny

            r += dr
            c += dc

        return False  # Ak nie je mozne ziskat kamene, vratime False

    def simulate_move(self, board, move, color) :
        '''Simuluje tah na kopii hracej dosky.'''
        r, c = move
        new_board = [row[:] for row in board]  # Vytvorime kopiu dosky
        new_board[r][c] = color  # Vykoname tah

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]  # Možné smerové vektory
        # Pre kazdy smer, ak je mozne, otocime kamene
        for dr, dc in directions :
            if self.check_direction(r, c, dr, dc, new_board) :  # Skontrolujeme, ci je mozne otocit kamene v tomto smere
                self.flip_stones(r, c, dr, dc, new_board, color)  # Otočíme kamene

        return new_board  # Vratime novú dosku po vykonani tahu

    def flip_stones(self, r, c, dr, dc, board, color) :
        '''Otočí kamene v jednom smere.'''
        r += dr
        c += dc
        # Otočíme kamene v danom smere
        while 0 <= r < len(board) and 0 <= c < len(board) and board[r][c] == self.opponent_color :
            board[r][c] = color  # Otočíme kamen protivnika na náš
            r += dr
            c += dc

    def evaluate_board(self, board) :
        '''Vyhodnoti stav hracej dosky.'''
        score = 0  # Inicializujeme skore
        n = len(board)  # Velkost dosky

        # Hodnoty pre rohy a okraje
        corner_value = 100  # Skore pre rohy
        edge_value = 10  # Skore pre okraje
        stability_bonus = 50  # Bonus za stabilitu
        penalty_near_corner = -25  # Penalizacia za pozicie blizko roh

        # Rohy dosky
        corners = [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]
        # Polia blizko roh
        near_corners = [(0, 1), (1, 0), (1, 1), (0, n - 2), (1, n - 1), (1, n - 2),
                        (n - 2, 0), (n - 1, 1), (n - 2, 1), (n - 2, n - 1), (n - 1, n - 2), (n - 2, n - 2)]

        # Zohodnotenie kazdeho policka na doske
        for r in range(n) :
            for c in range(n) :
                if board[r][c] == self.my_color :
                    if (r, c) in corners :
                        score += corner_value  # Pridame hodnotu pre rohy
                    elif (r, c) in near_corners :
                        score += penalty_near_corner  # Penalizacia za blizkost roh
                    elif r == 0 or r == n - 1 or c == 0 or c == n - 1 :
                        score += edge_value  # Hodnotenie okrajov
                    else :
                        score += 1  # Zvycajne hodnotenie
                elif board[r][c] == self.opponent_color :
                    score -= 1  # Zle hodnotenie pre protivnika

        # Bonus za mobilitu
        my_moves = len(self.find_valid_moves(board))  # Pocet platnych tahov pre nas
        opp_moves = len(self.find_valid_moves([[cell if cell != self.my_color else self.opponent_color for cell in row] for row in board]))  # Pocet platnych tahov pre protivnika
        score += 2 * (my_moves - opp_moves)  # Bonus za viac moznych tahov

        return score  # Vratime vyhodnotene skore

    def is_endgame(self, board) :
        '''Skontroluje, ci je hra v koncovej faze.'''
        # Ak je na doske menej nez 12 prazdnych miest, je to koniec hry
        return sum(row.count(-1) for row in board) <= 12  # Ak je menej ako 12 prazdnych polii, koniec hry
