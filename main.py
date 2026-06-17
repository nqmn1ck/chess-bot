import chess

import evaluate
import chessnet
import constants

def main():
    print("Starting")
    evaluation = evaluate.Evaluation()
    X_mock = evaluation.fen_to_2d("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
    for row in X_mock:
        print(row)

def negaMax(depth: int, game_state: chess.Board, initial_move: chess.Move):
    '''
    Go through all possible move sequences to max depth and
    find the max score at the ending depth. The move sequence with the best score
    will then be returned.
    note: movemaking and unmaking still need to be implemented
    '''

    if depth == 0:
        # At maximum depth, return eval score back to original branching move
        return (evaluate.evaluate(game_state), None)

    max_score = float("-inf")
    best_move = None
    moves = game_state.legal_moves
    for move in moves:
        if depth == constants.SEARCH_DEPTH:
            initial_move = move
        game_state.push(move)
        score = negaMax(depth-1, game_state, initial_move)[0]
        game_state.pop()
        if score > max_score:
            max_score = score
            best_move = initial_move
    return max_score, best_move

if __name__ == "__main__":
    main()