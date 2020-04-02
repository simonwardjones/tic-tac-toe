import tictactoe_pb2


PORTS = {
    'PLAYER_PORTS': {
        tictactoe_pb2.X: 'localhost:50051',
        tictactoe_pb2.O: 'localhost:50052',
    },
    'GAME_SERVICE': 'localhost:50053'
}
