import random

class MyPlayer :
    '''Adaptive player who can change strategy based on the type of payoff matrix'''

    def __init__(self, payoff_matrix, number_of_iterations=None) :
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations
        self.last_opponent_move = False  # False = cooperation; True = betrayal
        self.my_move_history = []
        self.opponent_move_history = []
        self.suspicion_threshold = 0.7  # If the opponent betrays more than 70% of the time, we switch strategy
        self.noise_probability = 0.05  # Probability of noise in the move
        self.self_play_detected = False  # Flag to detect self-play
        self.turn_count = 0  # Keep track of turns
        self.alternating_strategy = False  # Flag for alternating strategy
        self.always_betray = False  # Flag if we detect that always betraying is the best strategy

        # Detect the type of matrix
        self.detect_matrix_type ()

    def detect_matrix_type(self) :
        '''Analyze the payoff matrix to determine the optimal strategy'''
        C_C = self.payoff_matrix [0] [0]  # Payoff when both cooperate
        C_D = self.payoff_matrix [0] [1]  # Payoff when I cooperate, opponent betrays
        D_C = self.payoff_matrix [1] [0]  # Payoff when I betray, opponent cooperates
        D_D = self.payoff_matrix [1] [1]  # Payoff when both betray

        # Detect if alternating strategy is beneficial (e.g., C_D and D_C are very high)
        if C_D [1] > D_D [1] and D_C [0] > D_D [0] :
            self.alternating_strategy = True

        # Detect if always betraying is the dominant strategy
        if D_D [0] > C_D [0] and D_D [0] > C_C [0] and D_D [0] > D_C [0] :
            self.always_betray = True

    def select_move(self) :
        '''Player decides whether to cooperate (False) or betray (True)'''

        # If self-play is detected, always cooperate to maximize the total gain
        if self.self_play_detected :
            return False  # Cooperation with oneself maximizes the overall score

        # If the matrix suggests always betraying, do so
        if self.always_betray :
            return True  # Always betray if it's the best strategy

        # If an alternating strategy is beneficial, alternate between cooperation and betrayal
        if self.alternating_strategy :
            self.turn_count += 1
            return self.turn_count % 2 == 1  # Betray on odd turns, cooperate on even turns

        # If the opponent is betraying too often, start betraying too
        if self.should_betray () :
            return True  # Betray if suspicion of frequent betrayal is high

        # If it's the start of the game, assume the opponent cooperates
        if len (self.opponent_move_history) == 0 :
            return False  # Cooperation at the start

        # Copy the opponent's last move (mimicking their behavior)
        return self.last_opponent_move

    def should_betray(self) :
        '''Decide whether to start betraying based on opponent's move history'''
        # If the opponent is betraying often, switch to betrayal
        if len (self.opponent_move_history) > 0 :
            betray_count = sum (self.opponent_move_history)
            betray_rate = betray_count / len (self.opponent_move_history)
            if betray_rate > self.suspicion_threshold :
                return True
        return False

    def detect_self_play(self) :
        '''Detect if the player is playing against themselves based on move history'''
        if self.my_move_history == self.opponent_move_history :
            self.self_play_detected = True

    def handle_noise(self, opponent_last_move) :
        '''Accounts for the possibility of noise in communication'''
        if random.random () < self.noise_probability :
            # Invert the opponent's move if noise occurs
            return not opponent_last_move
        return opponent_last_move

    def record_last_moves(self, my_last_move, opponent_last_move) :
        '''Records moves and adjusts decision-making based on them'''
        # Save the last moves to history
        self.my_move_history.append (my_last_move)
        self.opponent_move_history.append (opponent_last_move)

        # Check if the player is playing against themselves
        self.detect_self_play ()

        # Account for noise and record the opponent's move
        self.last_opponent_move = self.handle_noise (opponent_last_move)
