import logging
import sys
from concurrent import futures
from random import choice

import grpc
from google.protobuf.json_format import MessageToDict, MessageToJson

import tictactoe_pb2
import tictactoe_pb2_grpc
from game import Game
from server_ports import PORTS

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


class RandomPlayer(tictactoe_pb2_grpc.PlayerServiceServicer):
    def __init__(self, player=tictactoe_pb2.X):
        self.player = player
        self.move = tictactoe_pb2.Move(player=self.player, tile_id=0)

    def Play(self, request, context):
        game = Game.from_message(request)
        available_moves = game.available_moves()
        print(game)
        print('moves = ', available_moves)
        if (game.game_state in Game.TerminatedStates
                or len(available_moves) == 0):
            logger.warning('Game terminated or no available moves')
            move = tictactoe_pb2.Move(
                player=self.player,
                tile_id=-1)
        else:
            move = tictactoe_pb2.Move(
                player=self.player,
                tile_id=choice(available_moves))
        print(move)
        return move


def serve(player='X'):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    player = RandomPlayer(player=tictactoe_pb2.TileState.Value(player))
    tictactoe_pb2_grpc.add_PlayerServiceServicer_to_server(
        player, server)
    port = server.add_insecure_port(PORTS['PLAYER_PORTS'][player.player])
    logger.info(f'Started palyer server on port {port}'
                f' with token {tictactoe_pb2.TileState.Name(player.player)}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    player = sys.argv[1][-1]
    serve(player=player)

# board = Board()
# print(board)
