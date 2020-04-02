import logging
import sys
from concurrent import futures

import grpc
from google.protobuf.json_format import MessageToDict, MessageToJson

import tictactoe_pb2
import tictactoe_pb2_grpc
from board import Board
from game import Game
from server_ports import PORTS

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


class GameService(tictactoe_pb2_grpc.GameServiceServicer):

    def AttemptMove(self, request, context):
        game = Game.from_message(request.game)
        move = request.move
        game.attemp_move(move)
        return game.game_message


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tictactoe_pb2_grpc.add_GameServiceServicer_to_server(
        GameService(), server)
    # server.add_insecure_port('[::]:50053')
    port = server.add_insecure_port(PORTS['GAME_SERVICE'])
    logger.info(f'Started game server on port {port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

# board = Board()
# print(board)
