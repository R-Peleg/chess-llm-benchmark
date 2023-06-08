import os
import requests
import chess
import chess.pgn
import random

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
    first_moves_list = []
    legal_moves = []
    illegal_moves = []
    with open(PGN_FILE, 'r') as pgn_f:
        while True:
            game = chess.pgn.read_game(pgn_f)
            if game is None:
                break
            board = game.board()
            moves = []
            illegal_move = None
            for move in game.mainline_moves():
                san = board.san(move)
                moves.append(san)
                if len(moves) >= 5:
                    # Try to find pseudo legal move
                    for m in board.pseudo_legal_moves:
                        if not board.is_legal(m):
                            illegal_move = m
                            break
                    current_legal_moves = [board.san(m) for m in board.legal_moves]
                    while illegal_move is None:
                        m = random.choice(['K', 'Q', 'R', 'N', 'B', '']) + random.choice('abcdefgh') + random.choice('12345678')
                        if m not in current_legal_moves:
                            illegal_move = m
                    break
                board.push(move)
            moves_tuple = tuple(moves[:-1])
            if moves_tuple not in first_moves_list:
                first_moves_list.append(moves_tuple)
                legal_moves.append(moves[-1])
                illegal_moves.append(illegal_move)
    print(f'Found {len(first_moves_list)} first moves sequences')
    for moves, lm, ilm in zip(first_moves_list, legal_moves, illegal_moves):
        moves_str = ''
        for i in range(len(moves) // 2):
            moves_str += f'{i+1}. {moves[i*2]} {moves[i*2+1]} '
        moves_str = moves_str[:-1]
        text_moves = f'Given a chess game starting with the moves {moves_str}'
        legal_question = text_moves + f', is the move {lm} legal?'
        illegal_question = text_moves + f', is the move {ilm} legal?'
        print(legal_question)
        print(illegal_question)



if __name__ == '__main__':
    main()
