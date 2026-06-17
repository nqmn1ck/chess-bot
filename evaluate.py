import chess
import pandas as pd
import numpy as np

import os
import json

import chessnet
import constants


class Evaluation:

    def __init__(self):
        translations = self.load_translations()
        self.extra_info_translate = translations[0]
        self.piece_translate = translations[1]
    
    def load_translations(self):
        '''
        Load translation dictionaries that translate fen values to numerical values
        '''
        if not os.path.isfile(constants.FEN_TRANSLATE_PATH):
            print("fen translation dictionaries not found, recreating")

            extra_info_translate = {} # Translation from extra info to assigned numerical value

            extra_info_options = [
                "0", "1", "b", "w", "K", "Q", "k", "q",
                "KQ", "Kk", "Kq", "Qk", "Qq", "kq",
                "KQk", "KQq", "Kkq", "Qkq", "KQkq", "-",
            ]
            info_value = 0
            for option in extra_info_options:
                extra_info_translate[option] = info_value
                info_value += 1
            cols = ["a", "b", "c", "d", "e", "f", "g", "h"]

            # Give every row-col position it's own number in info_numerics
            for letter in cols:
                for i in range(1, 9):
                    extra_info_translate[letter + str(i)] = info_value
                    info_value += 1

            piece_translate = {}

            piece_options = {
                "R", "N", "B", "Q", "K", "P",
                "r", "n", "b", "q", "k", "p",
            }
            for piece in piece_options:
                piece_translate[piece] = info_value
                info_value += 1

            with open(constants.FEN_TRANSLATE_PATH, "w") as fp:
                translation_dict = {"extra_info": extra_info_translate, "pieces": piece_translate}
                json.dump(translation_dict, fp)
                return (extra_info_translate, piece_translate)
        else:
            with open(constants.FEN_TRANSLATE_PATH, "r") as fp:
                translation_dict = json.load(fp)
                return (translation_dict["extra_info"], translation_dict["pieces"])

    def evaluate(self, game_state: chess.Board):
        '''
        Score must be relative to the side (negative black vs positive white maybe?)
        So I think we need our nn to take in any given position and give an evaluation
        (positive or negative) and return that from here.
        '''
        X = self.fen_to_2d(game_state.fen()) #9x8 game state array
        score = chessnet.chessNet(X)
        max_score = max(score)

        return max_score

    def fen_to_2d(self, fen):
        '''
        Translate fen into 9x8 2d array for the conv nn.
        Empty squares wil be set to 0.5 to allow non-bias weights to still have effect.

        FEN info: 
        number indicates number of blank columns until next piece or end of row
        letter indicates piece type, uppercase for white and lowercase for black

        '''

        rows = fen.split("/")

        # Translate extra board info (castling, enpessant, etc)
        extra_info = [0.5 for _ in range(8)]
        for i, s in enumerate(rows[7].split(" ")):
            if i == 0:
                # First entry to rows[7] is the last row of the board
                rows[7] = s
            else:
                extra_info[i-1] = self.extra_info_translate[s]

        # Translate board pieces
        board = [[0.5 for _ in range(8)] for _ in range(8)] #8x8 initialized to 0.5
        numbers = [str(x) for x in range(1, 9)]

        for i, row in enumerate(rows):
            col = 0
            for s in row:
                if s in numbers:
                    col += int(s)
                else:
                    board[i][col] = self.piece_translate[s]
                    col += 1

        x = np.array(board + [extra_info])

        # Min-max normalization
        max = len(self.piece_translate)
        min = 0

        x_normalized = (x - min) / (max)

        return x_normalized