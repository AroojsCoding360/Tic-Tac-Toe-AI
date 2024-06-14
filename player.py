import math
import random


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanParticipant(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        a = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9): ')
            try:
                a = int(square)
                if a not in game.max_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square.Please try again.')
        return a


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.max_moves())
        return square


class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.max_moves()) == 9:
            square = random.choice(game.max_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # maximize
        else:
            best = {'position': None, 'score': math.inf}  # minimize
        for possible_move in state.max_moves():
            state.make_move(possible_move, player)
            scores = self.minimax(state, other_player)  # simulate a game after move

            # undo trial
            state.board[possible_move] = ' '
            state.current_winner = None
            scores['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if scores['score'] > best['score']:
                    best = scores
            else:
                if scores['score'] < best['score']:
                    best = scores
        return best
