import torch
import torch.nn as nn
import torch.nn.functional as F

import chess
import pandas as pd

classes = []

def generate_all_possible_moves():
    ## Generate a dataset of every possible chess move
    files = "abcdefgh"
    ranks = "12345678"
    moves = []
    squares = [f + r for f in files for r in ranks]

    # Moves
    for start in squares:
        for end in squares:
            if start != end:
                moves.append(start + end)

    # Promotions
    for file_idx, f in enumerate(files):
        for start_rank, end_rank in [("7", "8"), ("2", "1")]:
            for target_file in (
                [f] +
                ([files[file_idx - 1]] if file_idx > 0 else []) +
                ([files[file_idx + 1]] if file_idx < 7 else [])
            ):
                for promo in "qrbn":
                    moves.append(
                        f"{f}{start_rank}{target_file}{end_rank}{promo}"
                    )
    df = pd.DataFrame({"move": moves})
    df.to_csv("data/uci_move_list.csv", index=False)

def evaluate(game_state: chess.Board):
    # Score must be relative to the side (negative black vs positive white maybe?)
    # So I think we need our nn to take in any given position and give an evaluation
    # (positive or negative) and return that from here.
    score = None
    return score

def load_evals():
    # Load stockfish game evaluations and clean the data
    evals_df = pd.read_json("data/stockfish_evaluations.jsonl")
    # Remove "mate in x" evaluations -- we only want a score.
    evals_df = evals_df[-evals_df['evaluation'].str.contains("M", case=False, na=False)]
    return evals_df

def fen_to_2d(fen):
    # translate fen into 9x8 nn input data
    # FEN info: 
    # number indicates number of blank columns until next piece or end of row
    # letter indicates piece type, uppercase for white and lowercase for black
    board = [["-" for _ in range(8)] for _ in range(8)]
    rows = fen.split("/")
    extra_info = ["-" for _ in range(8)]
    for i, s in enumerate(rows[7].split(" ")):
        if i == 0:
            rows[7] = s
        else:
            extra_info[i-1] = s

    numbers = [str(x) for x in range(1, 9)]
    cur_row = 0
    for i, row in enumerate(rows):
        col = 0
        for s in row:
            if s in numbers:
                col += int(s)
            else:
                board[i][col] = s
                col += 1
        cur_row += 1
    
    return board + [extra_info]


class chessNet(nn.Module):
    def __init__(self):
        super(chessNet, self).__init__()
        # convert input of board state (64 inputs) to a recommended move
        # (8*8) * 73 possible moves as outputs
        # probably want to use a 2d cnn,
        # think of board as a 8x8 image with 7 possible states/"colors"
        self.conv1 = nn.Conv2d(9*8, 1, 5)
    
    def forward(self, x):
        return