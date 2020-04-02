import logging

from google.protobuf.json_format import MessageToDict, MessageToJson

import tictactoe_pb2
from board import Board

logging.basicConfig()
logger = logging.getLogger(__file__)


class Game:
    """Wrapper for game message"""

    TerminatedStates = [
        tictactoe_pb2.X_WIN,
        tictactoe_pb2.O_WIN,
        tictactoe_pb2.DRAW,
    ]

    Wins = [
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},  # rows
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},  # cols
        {0, 4, 8}, {6, 4, 2}  # diagonal
    ]

    def __init__(self,
                 board=None,
                 last_player=tictactoe_pb2.EMPTY,
                 game_state=tictactoe_pb2.WAITING_TO_START):
        if not board:
            self.board = Board()
        elif isinstance(board, Board):
            self.board = board
        else:
            self.board = Board.from_message(board)
        self.last_player = last_player
        self.game_state = game_state

    def __repr__(self):
        return self.board.__repr__() + '\n\n State: {}'.format(
            tictactoe_pb2.GameState.Name(self.game_state))

    def available_moves(self):
        return [i for i, tile in enumerate(self.board.tiles)
                if tile == tictactoe_pb2.EMPTY]

    def attemp_move(self, move):
        if move.tile_id not in self.available_moves():
            logger.warn('Move not in avialbale moves')
        elif self.game_state in Game.TerminatedStates:
            logger.warn('Attempted move in terminated state')
        else:
            self.board.tiles[move.tile_id] = move.player
        self.update_state()

    def update_state(self):
        if len(self.available_moves()) == self.board.ntiles:
            self.game_state = tictactoe_pb2.WAITING_TO_START
        elif self.check_if_player_has_won(tictactoe_pb2.X):
            self.game_state = tictactoe_pb2.X_WIN
        elif self.check_if_player_has_won(tictactoe_pb2.O):
            self.game_state = tictactoe_pb2.O_WIN
        elif len(self.available_moves()) == 0:
            self.game_state = tictactoe_pb2.DRAW
        else:
            self.game_state = tictactoe_pb2.RUNNING

    def check_if_player_has_won(self, player):
        player_tiles = set(tile_id
                           for tile_id, tile in enumerate(self.board.tiles)
                           if tile == player)
        if any(win.issubset(player_tiles) for win in self.Wins):
            logger.info('player {} has won'.format(
                tictactoe_pb2.TileState.Name(player)
            ))
            return True
        return False

    @property
    def game_message(self):
        return tictactoe_pb2.Game(
            board=self.board.board_message,
            last_player=self.last_player,
            game_state=self.game_state)

    @classmethod
    def from_message(cls, game_message):
        return cls(
            board=game_message.board,
            last_player=game_message.last_player,
            game_state=game_message.game_state)
