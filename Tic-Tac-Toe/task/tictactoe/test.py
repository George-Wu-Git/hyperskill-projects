selection = input("Enter cells: ")
board = [[selection[6], selection[3], selection[0]], [selection[7], selection[4], selection[1]],
         [selection[8], selection[5], selection[2]]]


def print_board():
    print(9 * "-")
    print(f"| {board[0][2]} {board[1][2]} {board[2][2]} |")
    print(f"| {board[0][1]} {board[1][1]} {board[2][1]} |")
    print(f"| {board[0][0]} {board[1][0]} {board[2][0]} |")
    print(9 * "-")


print_board()
while True:
    next_move = input("Enter the coordinates: ").split()
    if next_move[0].isdecimal() and next_move[1].isdecimal:
        if int(next_move[0]) > 3 or int(next_move[1]) > 3:
            print("Coordinates should be from 1 to 3!")
        elif board[int(next_move[0]) - 1][int(next_move[1]) - 1] in ("X", "O"):
            print("This cell is occupied! Choose another one!")
        else:
            board[int(next_move[0]) - 1][int(next_move[1]) - 1] = "X"
            print_board()
            break
    else:
        print("You should enter numbers!")

# seqs = [selection[:3], selection[3:6], selection[6:], selection[0] + selection[3] + selection[6],
#        selection[1] + selection[4] + selection[7], selection[2] + selection[5] + selection[8],
#        selection[0] + selection[4] + selection[8], selection[2] + selection[4] + selection[6]]
# count_X = [group.count("X") for group in seqs]
# count_O = [group.count("O") for group in seqs]
# if abs(selection.count("X") - selection.count("O")) > 1 or (3 in count_X and 3 in count_O):
#    print("Impossible")
# elif 3 in count_X:
#    print("X wins")
# elif 3 in count_O:
#    print("O wins")
# elif selection.count("_") == 0:
#    print("Draw")
# else:
#    print("Game not finished")

