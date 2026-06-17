# Chess net should be trained by associating board states to stockfish evaluations
# We need to find a way to get a stockfish python library?
import torch
import torch.nn as nn
import torch.functional as F

import pandas as pd
import numpy as np

import constants

classes = np.loadtxt(constants.UCI_MOVE_INDEX_PATH, dtype=np.str_)
y = []

class chessNet(nn.Module):
    # Use SVM instead of softmax to get a raw score?
    def __init__(self):
        super(chessNet, self).__init__()
        # convert input of board state (64 inputs) to a recommended move
        # (8*8) * 73 possible moves as outputs
        # probably want to use a 2d cnn,
        # think of board as a 8x8 image with 7 possible states/"colors"
        self.conv1 = nn.Conv2d(9*8, 1, 5)
    
    def forward(self, x):
        return

def load_evals():
    # Load stockfish game evaluations and clean the data
    evals_df = pd.read_json(constants.STOCKFISH_EVAL_PATH)
    # Remove "mate in x" evaluations -- we only want a score.
    evals_df = evals_df[-evals_df['evaluation'].str.contains("M", case=False, na=False)]
    return evals_df

def generate_all_possible_uci_moves():
    # Generate a dataset of every possible chess move in UCI notation
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
    df.to_csv(constants.UCI_MOVE_INDEX_PATH, index=False)