import chess
import evaluate

def main():
    print("Starting chess nn")
    nn_input = evaluate.fen_to_2d("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
    for row in nn_input:
        print(row)
    evaluate.generate_all_possible_moves()

def negaMax(depth: int, game_state: chess.Board):
    if depth == 0:
        return evaluate.evaluate(game_state)

    # Go through all possible move sequences to max depth and
    # find the max score at the ending depth. The move sequence with the best score
    # will then be returned.
    # note: movemaking and unmaking still need to be implemented
    max = int(float("inf"))
    best_game_state = None
    for move in all_moves:
        game_state
        score = -negaMax(depth - 1)
        if score > max:
            max = score
    return max

if __name__ == "__main__":
    main()