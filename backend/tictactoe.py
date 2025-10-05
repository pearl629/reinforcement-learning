import random

class TicTacToe:
    def __init__(self):
        self.board = [0] * 9          # 0 = empty, 1 = X, -1 = O
        self.current_player = 1       # 1 = X (AI), -1 = O (human)

    def reset(self):
        self.board = [0] * 9
        self.current_player = 1
        return self.board

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == 0]

    def make_move(self, pos):
        if self.board[pos] != 0:
            return False
        self.board[pos] = self.current_player
        self.current_player *= -1      # switch player
        return True

    def check_winner(self):
        lines = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for i,j,k in lines:
            if self.board[i] == self.board[j] == self.board[k] != 0:
                return 1 if self.board[i] == 1 else -1
        if 0 not in self.board:
            return 0  # draw
        return None

class AIPlayer:
    def __init__(self, Q_table):
        self.Q_table = Q_table

    def get_move(self, board):
        # Convert numeric board to string board matching Colab Q-table keys
        state = tuple(['x' if x == 1 else 'o' if x == -1 else ' ' for x in board])
        available_moves = [i for i, v in enumerate(board) if v == 0]
        if not available_moves:
            return None
        q_vals = self.Q_table.get(state, [0]*9)

        # Tie-breaking if multiple moves have the same max Q-value
        max_val = max(q_vals[a] for a in available_moves)
        best_moves = [a for a in available_moves if q_vals[a] == max_val]
        return random.choice(best_moves)

