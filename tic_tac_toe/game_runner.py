import logging
import os
import sys
from concurrent import futures
from itertools import cycle
from time import sleep

import grpc
from google.protobuf.json_format import MessageToDict, MessageToJson

import tictactoe_pb2
import tictactoe_pb2_grpc
from board import Board
from game import Game
from server_ports import PORTS

x_channel = grpc.insecure_channel(
    PORTS['PLAYER_PORTS'][tictactoe_pb2.X])
o_channel = grpc.insecure_channel(
    PORTS['PLAYER_PORTS'][tictactoe_pb2.O])
game_channel = grpc.insecure_channel(
    PORTS['GAME_SERVICE'])

player_x = tictactoe_pb2_grpc.PlayerServiceStub(x_channel)
player_o = tictactoe_pb2_grpc.PlayerServiceStub(o_channel)
game_service = tictactoe_pb2_grpc.GameServiceStub(game_channel)


def main():
    game = Game()
    print(game)
    turns = 0
    for player in cycle([player_x, player_o]):
        move = player.Play(game.game_message)
        game_and_move = tictactoe_pb2.GameAndMove(
            game=game.game_message, move=move)
        game_response = game_service.AttemptMove(game_and_move)
        game = Game.from_message(game_response)
        print(game)
        sleep(0.4)
        turns += 1
        if turns == 9 or game.game_state in Game.TerminatedStates:
            print(f' Game over in {turns} turns')
            break


main()
