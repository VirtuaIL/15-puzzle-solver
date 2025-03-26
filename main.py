import argparse
import os
import time

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


def save_info(info_file, path, visited, expanded, max_reached_depth, duration_ms):
    with open(info_file, "w") as file:
        if path:
            file.write(f"{len(path)}\n")
            file.write(f"{visited}\n")
            file.write(f"{expanded}\n")
            file.write(f"{max_reached_depth}\n")
            file.write(f"{duration_ms:.3f}\n")
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

    def print_board(self):
        print("-" * (self.w * 4 + 1))
        for row in self.board:
            row_str = "|"
            for num in row:
                if num == 0:
                    row_str += "   |"
                elif num < 10:
                    row_str += f" {num} |"
                else:
                    row_str += f" {num}|"
            print(row_str)
            print("-" * (self.w * 4 + 1))
        print()

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
    max_reached_depth = 0
    expanded_nodes = 0  # licznik przetworzonych

    while stack:
        node, last_move = stack.pop()
        max_reached_depth = max(max_reached_depth, node.depth)
        expanded_nodes += 1

        if node.current_board.is_solved():
            return node.path(), len(visited), max_reached_depth, expanded_nodes

        if node.depth < max_depth:
            for move, new_board in node.current_board.moves_to_make(last_move):
                if new_board not in visited:
                    visited.add(new_board)
                    new_node = Node(new_board, node, node.depth + 1, move)
                    stack.append((new_node, move))

    return [], len(visited), max_reached_depth, expanded_nodes



def BFS(board):
    root_node = Node(board, None, 0, None)
    queue = [root_node]
    visited = {board}
    max_reached_depth = 0
    expanded_nodes = 0  # licznik przetworzonych węzłów

    while queue:
        node = queue.pop(0)
        max_reached_depth = max(max_reached_depth, node.depth)
        expanded_nodes += 1

        if node.current_board.is_solved():
            return node.path(), len(visited), max_reached_depth, expanded_nodes

        if node.depth < max_depth:
            for move, new_board in node.current_board.moves_to_make():
                if new_board not in visited:
                    visited.add(new_board)
                    new_node = Node(new_board, node, node.depth + 1, move)
                    queue.append(new_node)

    return [], len(visited), max_reached_depth, expanded_nodes




def debug_final_state(board, path):
    """Funkcja pomocnicza do debugowania - pokazuje końcowy stan układanki po wykonaniu wszystkich ruchów"""
    if not path:
        print("Brak ścieżki rozwiązania.")
        return

    print(f"\nDebug: Wykonywanie {len(path)} ruchów: {''.join(path)}")
    print("Stan początkowy:")
    board.print_board()

    # Wykonaj wszystkie ruchy i pokaż końcowy stan
    current_board = board
    for i, move in enumerate(path):
        found_move = False
        for m, new_board in current_board.moves_to_make():
            if m == move:
                current_board = new_board
                found_move = True
                break

        if not found_move:
            print(f"BŁĄD: Nie można wykonać ruchu {move} na obecnej planszy!")
            print("Aktualna plansza:")
            current_board.print_board()
            print("Dostępne ruchy:", [m for m, _ in current_board.moves_to_make()])
            return

        print(f"Po ruchu {i+1} ({move}):")
        current_board.print_board()

    print("Końcowy stan po wykonaniu wszystkich ruchów:")
    current_board.print_board()
    print(f"Czy rozwiązane: {current_board.is_solved()}")

    # Sprawdź, czy końcowa plansza jest rzeczywiście rozwiązana
    if not current_board.is_solved():
        print("UWAGA: Końcowa plansza nie jest rozwiązana!")
        print("Oczekiwana plansza rozwiązana:")
        for row in solved_board:
            print(row)
def main():
    parser = argparse.ArgumentParser(description="15 Puzzle Solver")
    parser.add_argument("strategy", choices=["dfs","bfs"], help="Strategy to use")
    parser.add_argument("board", help="File with the board to solve")
    parser.add_argument("solution", help="File to save the solution")
    parser.add_argument("stats", help="File to save the stats")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    start_board, w, k = read_board(args.board)
    board = Board(start_board, w, k)

    print("Początkowa plansza:")
    for row in board.board:
        print(row)

    print("Puste pole na pozycji:", board.find_zero())

    start_time = time.time()

    # Wybór strategii
    if args.strategy == "dfs":
        path, visited_count, max_reached_depth, expanded = DFS(board)
    elif args.strategy == "bfs":
        path, visited_count, max_reached_depth, expanded = BFS(board)

    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)

    if path:
        print("Ruchy do wykonania:", path)
        if args.debug:
            debug_final_state(board, path)
    else:
        print("Nie znaleziono rozwiązania w maksymalnej głębokości")

    save_solution(args.solution, path)
    save_info(args.stats, path, str(visited_count), str(expanded), str(max_reached_depth), duration_ms)


if __name__ == "__main__":
    main()