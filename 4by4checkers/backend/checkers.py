import numpy as np
import random
from collections import defaultdict
from copy import deepcopy

def available(player, board):
    d = defaultdict(lambda: np.zeros(4))
    if player == 0:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != " " and board[i][j] <= player:
                    if i - 1 >= 0 and j - 1 >= 0:
                        if board[i - 1][j - 1] == " ":
                            d[i, j][0] = 1
                        elif board[i - 1][j - 1] >= 1:
                            if i - 2 >= 0 and j - 2 >= 0:
                                if board[i - 2][j - 2] == " ":
                                    d[i, j][0] = 1
                    if i - 1 >= 0 and j + 1 < 4:
                        if board[i - 1][j + 1] == " ":
                            d[i, j][1] = 1
                        elif board[i - 1][j + 1] >= 1:
                            if i - 2 >= 0 and j + 2 < 4:
                                if board[i - 2][j + 2] == " ":
                                    d[i, j][1] = 1
                if board[i][j] != " " and board[i][j] < player:
                    if i + 1 < 4 and j - 1 >= 0:
                        if board[i + 1][j - 1] == " ":
                            d[i, j][2] = 1
                        elif board[i + 1][j - 1] >= 1:
                            if i + 2 < 4 and j - 2 >= 0:
                                if board[i + 2][j - 2] == " ":
                                    d[i, j][2] = 1
                    if i + 1 < 4 and j + 1 < 4:
                        if board[i + 1][j + 1] == " ":
                            d[i, j][3] = 1
                        elif board[i + 1][j + 1] >= 1:
                            if i + 2 < 4 and j + 2 < 4:
                                if board[i + 2][j + 2] == " ":
                                    d[i, j][3] = 1
    if player == 1:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != " " and board[i][j] >= player:
                    if i + 1 < 4 and j - 1 >= 0:
                        if board[i + 1][j - 1] == " ":
                            d[i, j][0] = 1
                        elif board[i + 1][j - 1] <= 0:
                            if i + 2 < 4 and j - 2 >= 0:
                                if board[i + 2][j - 2] == " ":
                                    d[i, j][0] = 1
                    if i + 1 < 4 and j + 1 < 4:
                        if board[i + 1][j + 1] == " ":
                            d[i, j][1] = 1
                        elif board[i + 1][j + 1] <= 0:
                            if i + 2 < 4 and j + 2 < 4:
                                if board[i + 2][j + 2] == " ":
                                    d[i, j][1] = 1
                if board[i][j] != " " and board[i][j] > player:
                    if i - 1 >= 0 and j - 1 >= 0:
                        if board[i - 1][j - 1] == " ":
                            d[i, j][2] = 1
                        elif board[i - 1][j - 1] <= 0:
                            if i - 2 >= 0 and j - 2 >= 0:
                                if board[i - 2][j - 2] == " ":
                                    d[i, j][2] = 1
                    if i - 1 >= 0 and j + 1 < 4:
                        if board[i - 1][j + 1] == " ":
                            d[i, j][3] = 1
                        elif board[i - 1][j + 1] <= 0:
                            if i - 2 >= 0 and j + 2 < 4:
                                if board[i - 2][j + 2] == " ":
                                    d[i, j][3] = 1
    return d


def Possible_cap(i, j, board, player):
    d = defaultdict(lambda: np.zeros(4))
    if player == 0:
        if board[i][j] <= 0:
            if i - 2 >= 0 and j - 2 >= 0 and board[i - 2][j - 2] == ' ':
                if board[i - 1][j - 1] != ' ' and board[i - 1][j - 1] >= 1:
                    d[i, j][0] = 1
            if i - 2 >= 0 and j + 2 < 4 and board[i - 2][j + 2] == ' ':
                if board[i - 1][j + 1] != ' ' and board[i - 1][j + 1] >= 1:
                    d[i, j][1] = 1
        if board[i][j] < 0:
            if i + 2 < 4 and j - 2 >= 0 and board[i + 2][j - 2] == ' ':
                if board[i + 1][j - 1] != ' ' and board[i + 1][j - 1] >= 1:
                    d[i, j][2] = 1
            if i + 2 < 4 and j + 2 < 4 and board[i + 2][j + 2] == ' ':
                if board[i + 1][j + 1] != ' ' and board[i + 1][j + 1] >= 1:
                    d[i, j][3] = 1
    if player == 1:
        if board[i][j] != " " and board[i][j] >= 1:
            if i + 2 < 4 and j - 2 >= 0 and board[i + 2][j - 2] == ' ':
                if board[i + 1][j - 1] != ' ' and board[i + 1][j - 1] <= 0:
                    d[i, j][0] = 1
            if i + 2 < 4 and j + 2 < 4 and board[i + 2][j + 2] == ' ':
                if board[i + 1][j + 1] != ' ' and board[i + 1][j + 1] <= 0:
                    d[i, j][1] = 1
        if board[i][j] != " " and board[i][j] > 1:
            if i - 2 >= 0 and j - 2 >= 0 and board[i - 2][j - 2] == ' ':
                if board[i - 1][j - 1] != ' ' and board[i - 1][j - 1] <= 0:
                    d[i, j][2] = 1
            if i - 2 >= 0 and j + 2 < 4 and board[i - 2][j + 2] == ' ':
                if board[i - 1][j + 1] != ' ' and board[i - 1][j + 1] <= 0:
                    d[i, j][3] = 1
    if d:
        action_dict = d
        action = (next(iter(action_dict)), random.choice([i for i, v in enumerate(action_dict[next(iter(action_dict))]) if v == 1.0]))
        return action


def apply_move(board, action, player, count, reward=0.0):
    i = action[0][0]
    j = action[0][1]
    move = action[1]
    
    if player >= 1:
        if move == 0:
            if board[i + 1][j - 1] == " ":
                board[i + 1][j - 1] = board[i][j]
                board[i][j] = ' '
                if i + 1 == 3 and board[i + 1][j - 1] == 1:
                    board[i + 1][j - 1] += 1
            else:
                board[i + 1][j - 1] = " "
                board[i + 2][j - 2] = board[i][j]
                board[i][j] = ' '
                if i + 2 == 3 and board[i + 2][j - 2] == 1:
                    board[i + 2][j - 2] += 1
                reward += 1
                act = Possible_cap(i + 2, j - 2, board, player)
                if act:
                    return apply_move(board, act, player, count + 1, reward)
        if move == 1:
            if board[i + 1][j + 1] == " ":
                board[i + 1][j + 1] = board[i][j]
                board[i][j] = ' '
                if i + 1 == 3 and board[i + 1][j + 1] == 1:
                    board[i + 1][j + 1] += 1
            else:
                board[i + 1][j + 1] = " "
                board[i + 2][j + 2] = board[i][j]
                board[i][j] = ' '
                if i + 2 == 3 and board[i + 2][j + 2] == 1:
                    board[i + 2][j + 2] += 1
                reward += 1
                act = Possible_cap(i + 2, j + 2, board, player)
                if act:
                    return apply_move(board, act, player, count + 1, reward)
        if move == 2:
            if board[i - 1][j - 1] == " ":
                board[i - 1][j - 1] = board[i][j]
                board[i][j] = ' '
            else:
                board[i - 1][j - 1] = " "
                board[i - 2][j - 2] = board[i][j]
                board[i][j] = ' '
                reward += 1
                act = Possible_cap(i - 2, j - 2, board, player)
                if act:
                    return apply_move(board, act, player, count + 1, reward)
        if move == 3:
            if board[i - 1][j + 1] == " ":
                board[i - 1][j + 1] = board[i][j]
                board[i][j] = ' '
            else:
                board[i - 1][j + 1] = " "
                board[i - 2][j + 2] = board[i][j]
                board[i][j] = ' '
                reward += 1
                act = Possible_cap(i - 2, j + 2, board, player)
                if act:
                    return apply_move(board, act, player, count + 1, reward)
    
    if player <= 0:
        if move == 0:
            if board[i - 1][j - 1] == " ":
                board[i - 1][j - 1] = board[i][j]
                board[i][j] = ' '
                if i - 1 == 0 and board[i - 1][j - 1] == 0:
                    board[i - 1][j - 1] -= 1
            else:
                board[i - 1][j - 1] = " "
                board[i - 2][j - 2] = board[i][j]
                board[i][j] = ' '
                if i - 2 == 0 and board[i - 2][j - 2] == 0:
                    board[i - 2][j - 2] -= 1
                reward += 1
                act = Possible_cap(i - 2, j - 2, board, player)
                if act:
                    return apply_move(board, act, player, count + 1, reward)
        if move == 1:
            if board[i - 1][j + 1] == " ":
                board[i - 1][j + 1] = board[i][j]
                board[i][j] = ' '
                if i - 1 == 0 and board[i - 1][j + 1] == 0:
                    board[i - 1][j + 1] -= 1
            else:
                board[i - 1][j + 1] = " "
                board[i - 2][j + 2] = board[i][j]
                board[i][j] = ' '
                if i - 2 == 0 and board[i - 2][j + 2] == 0:
                    board[i - 2][j + 2] -= 1
                reward += 1
                act = Possible_cap(i - 2, j + 2, board, player)
                if act:
                    return apply_move(board, act, player, count + 1, reward)
        if move == 2:
            if board[i + 1][j - 1] == " ":
                board[i + 1][j - 1] = board[i][j]
                board[i][j] = ' '
            else:
                board[i + 1][j - 1] = " "
                board[i + 2][j - 2] = board[i][j]
                board[i][j] = ' '
                reward += 1
                act = Possible_cap(i + 2, j - 2, board, player)
                if act:
                    return apply_move(board, act, player, count + 1, reward)
        if move == 3:
            if board[i + 1][j + 1] == " ":
                board[i + 1][j + 1] = board[i][j]
                board[i][j] = ' '
            else:
                board[i + 1][j + 1] = " "
                board[i + 2][j + 2] = board[i][j]
                board[i][j] = ' '
                reward += 1
                act = Possible_cap(i + 2, j + 2, board, player)
                if act:
                    return apply_move(board, act, player, count + 1, reward)
    
    return board, reward, count + 1


def check_game_status(count, player, board):
    available_moves = available(player, board)
    if not available_moves:
        return -10
    return None


def state_to_key(state):
    return tuple(tuple(row) for row in state)


def reverse(board):
    flipped = [row[::-1] for row in board[::-1]]
    mapping = {1: 0, 0: 1, 2: -1, -1: 2, ' ': ' '}
    new_board = [[mapping.get(cell, cell) for cell in row] for row in flipped]
    return new_board


def choose_action(state, available_moves, Q_table, epsilon=0.0):
    state = tuple(tuple(row) for row in state)
    valid_actions = []
    for pos, directions in available_moves.items():
        for dir_idx, is_valid in enumerate(directions):
            if is_valid == 1:
                valid_actions.append((pos, dir_idx))
    
    if not valid_actions:
        return None
    
    if random.random() < epsilon:
        return random.choice(valid_actions)
    
    q_values = Q_table.get(state, {})
    best_action = max(valid_actions, key=lambda a: q_values.get(a, 0.0))
    return best_action