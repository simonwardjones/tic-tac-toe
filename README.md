# tic-tac-toe with gRPC

This is a protocol buffer implementation of tic-tac-toe!

# Playing with protobuffers

    1. set up virtualenv and install reqs
    ```bash
    python -m venv venv
    . venv/bin activate
    pip install -U pip
    pip install -r requirements.txt
    ```

    2. run the game service and two player services
    ```bash
    make run_players_and_game
    ```

    3. run the game
    ```bash
    make play_game
    ```

