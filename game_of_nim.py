from games import *


class GameOfNim(Game):
    def __init__(self, board=None):
        if board is None:
            board = [7, 5, 3, 1]
        moves = self._generate_moves(board)
        self.initial = GameState(to_move="X", utility=0, board=list(board), moves=moves)

    def _generate_moves(self, board):
        return [
            (row, num) for row, count in enumerate(board) for num in range(1, count + 1)
        ]

    def _next_player(self, current):
        return "O" if current == "X" else "X"

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state
        row, amount = move
        new_board = state.board.copy()
        new_board[row] -= amount
        updated_moves = self._generate_moves(new_board)
        next_turn = self._next_player(state.to_move)
        utility_value = 0
        if sum(new_board) == 0:
            # Player who just moved loses
            utility_value = -1 if state.to_move == "X" else 1
        return GameState(
            to_move=next_turn,
            utility=utility_value,
            board=new_board,
            moves=updated_moves,
        )

    def terminal_test(self, state):
        return all(count == 0 for count in state.board)

    def utility(self, state, player):
        return state.utility if player == "X" else -state.utility

    def display(self, state):
        print(f"Board: {state.board}")


if __name__ == "__main__":
    nim = GameOfNim()
    print(nim.initial.board)
    print(nim.initial.moves)
    print(nim.result(nim.initial, (1, 2)))
    outcome = nim.play_game(alpha_beta_player, query_player)
    if outcome < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")
