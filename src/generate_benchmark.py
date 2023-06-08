import os
import requests
import chess
import chess.pgn

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'artifacts')
PGN_FILE = os.path.join(ARTIFACTS_DIR, 'games.pgn')

def main():
    if not os.path.exists(ARTIFACTS_DIR):
        print('Creting artifacts directory')
        os.mkdir(ARTIFACTS_DIR)
    if not os.path.exists(PGN_FILE):
        print('Downloading games')
        response = requests.get('https://www.pgnmentor.com/events/WorldCup2021.pgn')
        with open(PGN_FILE, 'w') as f:
            f.write(response.content.decode('utf-8'))
    print('Reading games')
    with open(PGN_FILE, 'r') as pgn_f:
        game = chess.pgn.read_game(pgn_f)
        while game:
            for move in game.mainline_moves():
                print(move)
            break
            game = chess.pgn.read_game(pgn_f)




if __name__ == '__main__':
    main()
