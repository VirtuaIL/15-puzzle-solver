solved_board = [['1', '2', '3', '4'],
                ['5', '6', '7', '8'],
                ['9', '10', '11', '12'],
                ['13', '14', '15', '0']]

max_depth = 20

def read_board(file_name):
    start_board = open("files/4x4_01_00001.txt", "r")
    w, k = start_board.readline().split()
    w = int(w)
    k = int(k)
    board = [[0 for x in range(w)] for y in range(k)]
    for i in range(k):
        board[i] = list(map(int, start_board.readline().split()))

    return board, w, k

    # 4 4
    # 1 2 3 4
    # 5 6 7 8
    # 9 10 11 0
    # 13 14 15 12

# class Node:
#     def __init__(self, current_board, parent, depth, move):
#         self.current_board = current_board
#         self.parent = parent
#         self.depth = depth
#         self.move = move








def main():

    start_board, w, k = read_board("files/4x4_01_00001.txt")

    # print("Width:" + str(w) + " Height:" + str(k))
    #
    # for i in range(k):
    #     for j in range(w):
    #         print(start_board[i][j], end=" ")
    #     print()

    # print("Solved board:")
    # for i in range(k):
    #     for j in range(w):
    #         print(solved_board[i][j], end=" ")
    #     print()





if __name__ == "__main__":
    main()