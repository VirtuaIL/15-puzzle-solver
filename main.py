import argparse
import os

solved_board = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 0]]

max_depth = 20


def read_board(file_name):
    file_path = os.path.join("files", file_name)
    with open(file_path, "r") as start_board:
        w, k = map(int, start_board.readline().split())
        board = [list(map(int, start_board.readline().split())) for _ in range(k)]
    return board, w, k

def save_solution(solution_file, path):
    with open(solution_file, "w") as file:
        if path:
            file.write(f"{len(path)}\n")
            file.write("".join(path) + "\n")
        else:
            file.write("-1\n")


class Node:
    def __init__(self, current_board, parent, depth, move):
        self.current_board = current_board
        self.parent = parent
        self.depth = depth
        self.move = move

    def path(self):
        path = []
        node = self
        while node.parent:
            path.append(node.move)
            node = node.parent
        return path[::-1]  # Muszę odwrócić listę, żeby pokazać poprawną kolejność ruchów


class Board:
    def __init__(self, board, w, k):
        self.board = board
        self.w = w
        self.k = k

    def find_zero(self):
        for i in range(self.k):
            for j in range(self.w):
                if self.board[i][j] == 0:
                    return i, j

    def is_solved(self):
        return self.board == solved_board

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def moves_to_make(self, last_move=None):
        x0, y0 = self.find_zero()
        moves = []

        direction = {
            "U": (x0 - 1, y0),
            "D": (x0 + 1, y0),
            "L": (x0, y0 - 1),
            "R": (x0, y0 + 1)
        }

        useless_direction = {
            "U": "D",
            "D": "U",
            "L": "R",
            "R": "L"
        }

        for move, (x0_new, y0_new) in direction.items():
            if last_move == useless_direction.get(move):
                continue
            if 0 <= x0_new < self.k and 0 <= y0_new < self.w:  # Sprawdzanie granic planszy
                new_board = [row.copy() for row in self.board]
                new_board[x0][y0], new_board[x0_new][y0_new] = new_board[x0_new][y0_new], new_board[x0][y0]
                moves.append((move, Board(new_board, self.w, self.k)))

        return moves


def DFS(board):

    root_node = Node(board, None, 0, None)
    stack = [(root_node, None)]
    visited = {board}

    while stack:
        node, last_move = stack.pop()

        if node.current_board.is_solved():
            return node.path()

        if node.depth < max_depth:
            for move, new_board in node.current_board.moves_to_make(last_move):
                if new_board not in visited:
                    visited.add(new_board)
                    new_node = Node(new_board, node, node.depth + 1, move)
                    stack.append((new_node, move))

    return []

def BFS(board):
    root_node = Node(board, None, 0, None)
    queue = [root_node]
    visited = {board}

    while queue:
        node = queue.pop(0)

        if node.current_board.is_solved():
            return node.path()

        if node.depth < max_depth:
            for move, new_board in node.current_board.moves_to_make():
                if new_board not in visited:
                    visited.add(new_board)
                    new_node = Node(new_board, node, node.depth + 1, move)
                    queue.append(new_node)

    return []


def main():
    parser = argparse.ArgumentParser(description="15 Puzzle Solver")
    parser.add_argument("strategy", choices=["dfs","bfs"], help="Strategy to use")
    parser.add_argument("board", help="File with the board to solve")
    parser.add_argument("solution", help="File to save the solution")
    args = parser.parse_args()

    start_board, w, k = read_board(args.board)
    board = Board(start_board, w, k)

    print("Początkowa plansza:")
    for row in board.board:
        print(row)

    print("Puste pole na pozycji:", board.find_zero())

    if args.strategy == "dfs":
        path = DFS(board)
        if path:
            print("Ruchy do wykonania:", path)
        else:
            print("Nie znaleziono rozwiązania w maksymalnej głębokości")

        save_solution(args.solution, path)

    if args.strategy == "bfs":
        path = BFS(board)
        if path:
            print("Ruchy do wykonania:", path)
        else:
            print("Nie znaleziono rozwiązania w maksymalnej głębokości")

        save_solution(args.solution, path)


if __name__ == "__main__":
    main()
