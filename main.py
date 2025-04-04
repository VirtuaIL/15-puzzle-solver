import argparse
import heapq
import os
import time

# solved_board = [[1, 2, 3, 4],
#                 [5, 6, 7, 8],
#                 [9, 10, 11, 12],
#                 [13, 14, 15, 0]]

max_depth = 20

def generate_solved_board(w, k):
    solved = []
    value = 1
    for i in range(k):
        row = []
        for j in range(w):
            if value < w * k:
                row.append(value)
                value += 1
            else:
                row.append(0)  # puste pole na ostatnim
        solved.append(row)
    return solved


def read_board(file_name):
    file_path = os.path.join("413", file_name)
    with open(file_path, "r") as start_board:
        w, k = map(int, start_board.readline().split())
        board = []
        for i in range(k):
            line = start_board.readline().strip() #usuwanie spacji i enterow z początku i końca
            if line:
                board.append(list(map(int, line.split())))
    return board, w, k

def save_solution(solution_file, path):
    file_path = os.path.join("solution", solution_file)
    with open(file_path, "w") as file:
        if path:
            file.write(f"{len(path)}\n")
            file.write("".join(path) + "\n")
        else:
            file.write("-1\n")


def save_info(info_file, path, visited, expanded, max_reached_depth, duration_ms):
    file_path = os.path.join("stats", info_file)
    with open(file_path, "w") as file:
        if path:
            file.write(f"{len(path)}\n")

        else:
            file.write("-1\n")
        file.write(f"{visited}\n")
        file.write(f"{expanded}\n")
        file.write(f"{max_reached_depth}\n")
        file.write(f"{duration_ms:.3f}\n")


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
        return self.board == generate_solved_board(self.w, self.k)

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        rows = []
        for row in self.board:
            rows.append(tuple(row))
        return hash(tuple(rows))

    def moves_to_make(self, last_move=None, order="UDLR"):
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

        for move in order:
            if last_move is not None and last_move == useless_direction.get(move):
                continue

            x0_new, y0_new = direction[move]

            if 0 <= x0_new < self.k and 0 <= y0_new < self.w: # Sprawdzanie granic planszy
                new_board = []

                for row in self.board:
                    new_board.append(row.copy()) #kopia bo takto by była referencja

                new_board[x0][y0], new_board[x0_new][y0_new] = new_board[x0_new][y0_new], new_board[x0][y0]

                moves.append((move, Board(new_board, self.w, self.k)))

        return moves

def DFS(board, order):
    root_node = Node(board, None, 0, None)
    stack = [(root_node, None)]
    visited = {board: 0}  # stan i głębokość
    max_reached_depth = 0
    expanded_nodes = 0

    while stack:
        node, last_move = stack.pop()

        if node.depth > max_reached_depth:
            max_reached_depth = node.depth

        expanded_nodes += 1

        if node.current_board.is_solved():
            return node.path(), len(visited), max_reached_depth, expanded_nodes

        if node.depth < max_depth:
            possible_moves = node.current_board.moves_to_make(last_move=last_move, order=order)

            for move_and_board in possible_moves:
                move, new_board = move_and_board
                new_depth = node.depth + 1

                if new_board not in visited or new_depth < visited[new_board]:
                    visited[new_board] = new_depth
                    new_node = Node(new_board, node, new_depth, move)
                    stack.append((new_node, move))

    return [], len(visited), max_reached_depth, expanded_nodes


def BFS(board,order):
    root_node = Node(board, None, 0, None)
    queue = [root_node]
    visited = {board} #set odwiedzonych stanów

    max_reached_depth = 0
    expanded_nodes = 0  # licznik przetworzonych węzłów

    while queue:
        node = queue.pop(0)

        if node.depth > max_reached_depth:
            max_reached_depth = node.depth

        expanded_nodes += 1

        if node.current_board.is_solved():
            return node.path(), len(visited), max_reached_depth, expanded_nodes

        if node.depth < max_depth:
            possible_moves = node.current_board.moves_to_make(last_move=None, order=order)

            for move_and_board in possible_moves:
                move, new_board = move_and_board

                if new_board not in visited:
                    visited.add(new_board)
                    new_node = Node(new_board, node, node.depth + 1, move)
                    queue.append(new_node)

    return [], len(visited), max_reached_depth, expanded_nodes

def hamming(board):
    count = 0
    for i in range(4):
        for j in range(4):
            # if board.board[i][j] != 0 and board.board[i][j] != solved_board[i][j]:
            if board.board[i][j] != 0 and board.board[i][j] != generate_solved_board(board.w,board.k)[i][j]:
                count += 1
    return count

def manhattan(board):
    distance = 0
    for i in range(board.k):
        for j in range(board.w):
            value = board.board[i][j]
            if value != 0:
                target_i = (value - 1) // board.w
                target_j = (value - 1) % board.w
                distance += abs(i - target_i) + abs(j - target_j)
    return distance

def ASTR(board, heuristic):
    root_node = Node(board, None, 0, None)
    heap = []
    counter = 0  # unikalny licznik dla kolejności węzłów

    heapq.heappush(heap, (heuristic(board), 0, counter, root_node))

    visited = {board}
    max_reached_depth = 0
    expanded_nodes = 0

    while heap:
        f,g,_, current = heapq.heappop(heap)

        if current.depth > max_reached_depth:
            max_reached_depth = current.depth

        expanded_nodes += 1

        for row in current.current_board.board:
            print(row)
        print("f = g + h = ", g, "+", heuristic(current.current_board), "=", g + heuristic(current.current_board))

        if current.current_board.is_solved():
            return current.path(), len(visited), max_reached_depth, expanded_nodes

        possible_moves = current.current_board.moves_to_make(last_move=current.move)

        for move_and_board in possible_moves:
            move, new_board = move_and_board

            if new_board not in visited:
                visited.add(new_board)
                h = heuristic(new_board)
                new_g = g + 1
                new_f = new_g + h

                new_node = Node(new_board, current, g + 1, move)

                counter += 1

                # for row in new_board.board:
                #     print(row)

                heapq.heappush(heap, (new_f, new_g, counter, new_node))


    print("Nie znaleziono rozwiązania.")
    return [], len(visited), max_reached_depth, expanded_nodes


def main():
    parser = argparse.ArgumentParser(description="15 Puzzle Solver")
    parser.add_argument("strategy", choices=["dfs","bfs","astr"], help="Strategy to use")

    args_strat_checker, _ = parser.parse_known_args()

    if args_strat_checker.strategy == "astr":
        parser.add_argument("heuristic", choices=["hamm", "manh"], help="Heuristic function")
    else:
        parser.add_argument("order", choices=["UDLR", "UDRL", "ULDR", "ULRD", "URLD", "URDL",
                                                        "DULR", "DURL", "DLUR", "DLRU", "DRUL", "DRLU",
                                                        "LUDR", "LURD", "LDUR", "LDRU", "LRUD", "LRDU",
                                                        "RUDL", "RULD", "RDUL", "RDLU", "RLUD", "RLDU"
                                                        ], help="Order of the search")

    parser.add_argument("board", help="File with the board to solve")
    parser.add_argument("solution", help="File to save the solution")
    parser.add_argument("stats", help="File to save the stats")

    args = parser.parse_args()

    start_board, w, k = read_board(args.board)

    board = Board(start_board, w, k)

    if args.strategy == "astr":
        if args.heuristic == "hamm":
            print("Szukam astr z heurystyką Hamminga")
        elif args.heuristic == "manh":
            print("Szukam astr z heurystyką Manhattan")
    else:
        print("Szukam w kolejnosci", args.order)

    print("Początkowa plansza:")
    for row in board.board:
        print(row)

    print("Puste pole na pozycji:", board.find_zero())

    start_time = time.time()

    # Wybór strategii
    if args.strategy == "dfs":
        path, visited_count, max_reached_depth, expanded = DFS(board,args.order)
    elif args.strategy == "bfs":
        path, visited_count, max_reached_depth, expanded = BFS(board,args.order)
    elif args.strategy == "astr":
        if args.heuristic == "hamm":
            path, visited_count, max_reached_depth, expanded = ASTR(board, hamming)
        elif args.heuristic == "manh":
            path, visited_count, max_reached_depth, expanded = ASTR(board, manhattan)

    end_time = time.time()
    duration_ms = round((end_time - start_time) * 1000, 3)

    if path:
        print("Ruchy do wykonania:", path)

    else:
        print("Nie znaleziono rozwiązania w maksymalnej głębokości")

    save_solution(args.solution, path)
    save_info(args.stats, path, str(visited_count), str(expanded), str(max_reached_depth), duration_ms)


if __name__ == "__main__":
    main()