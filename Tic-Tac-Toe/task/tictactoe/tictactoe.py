elements = list('_' * 9)


def print_board():
    print(f'''
---------
| {elements[0]} {elements[1]} {elements[2]} |
| {elements[3]} {elements[4]} {elements[5]} |
| {elements[6]} {elements[7]} {elements[8]} |
---------
''')


def print_status():
    win = (elements[:3], elements[3:6], elements[6:], elements[0:9:3],
           elements[1:9:3], elements[2:9:3], elements[0:9:4], elements[2:7:2])

    impossible = ['X', 'X', 'X'] in elements and {'O', 'O', 'O'} in elements or abs(
        elements.count('X') - elements.count('O')) > 1
    x_win = ['X', 'X', 'X'] in win
    o_win = ['O', 'O', 'O'] in win
    game_not_finished = '_' in elements
    draw = '_' not in elements

    if impossible:
        print('impossible')
    elif x_win:
        print('X wins')
        exit()
    elif o_win:
        print('O wins')
        exit()
    # elif game_not_finished:
    #     print('Game not finished')
    elif draw:
        print('Draw')
        exit()
    else:
        pass


def enter_coordination():
    player = 'X'
    coordination = input('Enter the coordinates: ').split()

    if ''.join(coordination).replace(' ', '').isnumeric():

        for i in map(int, coordination):
            if i not in range(1, 4):
                print("Coordinates should be from 1 to 3!")
                return enter_coordination()

        coor = (int(coordination[0]) - 1) + (9 - (3 * int(coordination[1])))

        if elements[coor] != '_':
            print("This cell is occupied! Choose another one!")
            return enter_coordination()

        else:
            if player == 'X':
                elements[coor] = player
                player = 'O'
            elif player == 'O':
                elements[coor] = player
                player = 'X'

            print_board()
            print_status()


    else:
        print("You should enter numbers!")
        return enter_coordination()


print_board()
enter_coordination()
