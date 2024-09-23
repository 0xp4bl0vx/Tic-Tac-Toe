import numpy as np
from copy import deepcopy

PLAYER_1 = 0
PLAYER_2 = 1

HUMAN_PLAYER = -1
AI_PLAYER = 1

CROSS = 1
CIRCLE = -1
EMPTY = 0


def check_winner(board):
    # Filas
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            if board[i][0] == CROSS:
                return CROSS
            elif board[i][0] == CIRCLE:
                return CIRCLE

    # Columnas
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            if board[0][i] == CROSS:
                return CROSS
            elif board[0][i] == CIRCLE:
                return CIRCLE

    # Diagonal 1
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        if board[1][1] == CROSS:
            return CROSS
        elif board[1][1] == CIRCLE:
            return CIRCLE

    # Diagonal 2
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        if board[1][1] == CROSS:
            return CROSS
        elif board[1][1] == CIRCLE:
            return CIRCLE

    # Empate
    if EMPTY not in board:
        return 0


class Game:
    def __init__(self, players):
        self.players = players
        self.winner = None
        self.n_turn = 0
        self.symbol = None
        self.board = np.full(shape=(3, 3), fill_value=EMPTY)
        if players[0] == AI_PLAYER:
            self.ai_player_symbol = CROSS
            self.ai_player = AlgorithmPlayer(CROSS)
        if players[1] == AI_PLAYER:
            self.ai_player_symbol = CIRCLE
            self.ai_player = AlgorithmPlayer(CIRCLE)

    def turn(self, n_button):
        if self.n_turn % 2 == PLAYER_1:
            if self.players[0] == HUMAN_PLAYER:
                self.symbol = CROSS
                self.board[int(n_button // 3)][int(n_button % 3)] = CROSS
            elif self.players[0] == AI_PLAYER:
                self.symbol = CROSS
                new_board = self.ai_player.find_best_move(self.board, self.ai_player_symbol)[0]
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] != new_board[i][j]:
                            self.board = new_board
                            self.n_turn += 1
                            return i * 3 + j
                
        elif self.n_turn % 2 == PLAYER_2:
            if self.players[1] == HUMAN_PLAYER:
                self.symbol = CIRCLE
                self.board[int(n_button // 3)][int(n_button % 3)] = CIRCLE
            elif self.players[1] == AI_PLAYER:
                self.symbol = CIRCLE
                new_board = self.ai_player.find_best_move(self.board, self.ai_player_symbol)[0]
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] != new_board[i][j]:
                            self.board = new_board
                            self.n_turn += 1
                            return i * 3 + j
        self.n_turn += 1


class AlgorithmPlayer:
    def __init__(self, ai_player):
        self.ai_player = ai_player
        self.best_move = None
        self.empty_cells = []
        self.nodes = 0

    def find_best_move(self, board, turn):
        self.nodes += 1
        self.find_empty_cells(board)
        moves = []
        results = []
        for cell in self.empty_cells:
            moves.append(deepcopy(board))
            if self.ai_player == turn:
                moves[-1][cell[0]][cell[1]] = self.ai_player
            elif self.ai_player == -turn:
                moves[-1][cell[0]][cell[1]] = -self.ai_player
        for move in moves:
            winner = check_winner(move)
            if winner in (-1, 0, 1):
                results.append(winner)
            else:
                results.append(self.find_best_move(move, -turn)[1])
        for i in range(0, len(results)):
            if results[i] == max(results) and turn == 1:
                return [moves[i], results[i]]
            elif results[i] == min(results) and turn == -1:
                return [moves[i], results[i]]

    def find_empty_cells(self, board):
        self.empty_cells = []
        for i in range(2 if np.array_equal(board[0, :], board[2, :]) else 3):
            for j in range(2 if np.array_equal(board[:, 0], board[:, 2]) else 3):
                if board[i][j] == EMPTY:
                    self.empty_cells.append((i, j))
