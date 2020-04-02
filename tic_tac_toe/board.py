from google.protobuf.json_format import MessageToDict, MessageToJson

import tictactoe_pb2
from board_format import board_format


class Board:
    """Wrapper on message class"""

    Counters = {
        tictactoe_pb2.EMPTY: '-',
        tictactoe_pb2.X: 'X',
        tictactoe_pb2.O: 'O',
    }

    def __init__(self, n_tiles=9, tiles=None):
        self.ntiles= 9
        if tiles:
            self.tiles= tiles
        else:
            self.tiles= [tictactoe_pb2.EMPTY for _ in range(self.ntiles)]

    def __repr__(self):
        counters= [self.Counters[tile] for tile in self.tiles]
        if self.ntiles == 9:
            return board_format.format(*counters)
        return MessageToJson(self.board_message)

    @property
    def board_message(self):
        return tictactoe_pb2.Board(tiles=self.tiles)

    @classmethod
    def from_message(cls, board_message):
        return cls(tiles=board_message.tiles)
