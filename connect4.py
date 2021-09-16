from random import shuffle
import random

import numpy as np
from copy import deepcopy


class Game:
    mat = None  # this represents the board matrix
    rows = 0  # this represents the number of rows of the board
    cols = 0  # this represents the number of columns of the board
    turn = 0  # this represents whose turn it is (1 for player 1, 2 for player 2)
    wins = 0  # this represents the number of consecutive disks you need to force in order to win


def win_in_rows(game, r, c, player):
    number_of_moves = game.wins    #number_of_moves referring to number of consective to cells to check
    # check left
    all_passed = True
    for value in range(0, number_of_moves):
        cc = c - value #number of cells required to check after removing all consecutive cells
        if cc < 0 or game.mat[r][cc] != player:  #cc<0 or you can exit the grid as will be negative
            all_passed = False
            break

    if all_passed:
        return True

    # check right
    all_passed = True
    for value in range(0, number_of_moves):
        cc = c + value
        if cc >= game.cols or game.mat[r][cc] != player:  #game.cols limit the value so as to not exit the grid
            all_passed = False
            break

    return all_passed


def win_in_cols(game, r, c, player):
    number_of_moves = game.wins
    # check up
    all_passed = True
    for value in range(0, number_of_moves):
        rr = r - value
        if rr < 0 or game.mat[rr][c] != player: #player referring to 1 or 2
                all_passed = False
                break

    if all_passed:
        return True

    # check down
    all_passed = True
    for value in range(0, number_of_moves):
        rr = r + value
        if rr >= game.rows or game.mat[rr][c] != player:
            all_passed = False
            break

    return all_passed


def win_in_diagonals(game, r, c, player):
    number_of_moves = game.wins
    all_passed = True
    # check row +1 col +1 diagonal
    for value in range(0, number_of_moves):
        rr = r + value
        cc = c + value
        if rr >= game.rows or cc >= game.cols or game.mat[rr][cc] != player:
            all_passed = False
            break

    if all_passed:
        return True

    all_passed = True
    # check row -1 col -1 diagonal
    for value in range(0, number_of_moves):
        rr = r - value
        cc = c - value
        if rr < 0 or cc < 0 or game.mat[rr][cc] != player:
            all_passed = False
            break

    if all_passed:
        return True

    all_passed = True
    # check row +1 col -1 diagonal

    for value in range(0, number_of_moves):
        rr = r + value
        cc = c - value
        if rr >= game.rows or cc < 0 or game.mat[rr][cc] != player:
            all_passed = False
            break

    if all_passed:
        return True

    all_passed = True

    # check row -1 col +1 diagonal

    for value in range(0, number_of_moves):
        rr = r - value
        cc = c + value
        if rr < 0 or cc >= game.cols or game.mat[rr][cc] != player:
            all_passed = False
            break

    return all_passed


def check_victory(game):
    # Get the rows and columns numbers
    rows = game.rows
    cols = game.cols
    player1_win_state = False
    player2_win_state = False

    # for each row and columns cell
    for r in range(0, rows):
        for c in range(0, cols):
            # if not empty cell and wins in diagonal or in columns or in rows
            if game.mat[r][c] != 0 and (
                            win_in_rows(game, r, c, game.mat[r][c]) or win_in_cols(game, r, c, game.mat[r][c])
                    or win_in_diagonals(game, r, c, game.mat[r][c])):
                if game.mat[r][c] == 1:
                    player1_win_state = True
                else:
                    player2_win_state = True

    if player1_win_state and player2_win_state:
        return 3
    elif player1_win_state:
        return 1
    elif player2_win_state:
        return 2
    else:
        return 0


def apply_move(game, col, pop):
    # if pop move
    if pop:
        # get the game rows
        rows = game.rows
        # for each row
        for row in range(0, rows):
            # if last row assign it to zero
            if row == rows - 1:
                game.mat[row][col] = 0
            else:
                # else swap two consecutive row cell
                game.mat[row][col] = game.mat[row + 1][col]
    else:
        rows = game.rows
        # search for first cell equal zero
        for row in range(0, rows):
            if game.mat[row][col] == 0:
                game.mat[row][col] = game.turn
                break
    game.turn = 3 - game.turn #game turn 1 is player 2 turn
    return game


def check_move(game, col, pop):
    # if pop move
    if pop:
        # if first cell from bottom not equal the player number then it's False
        if game.mat[0][col] != game.turn: #row zero as only bottom piece out
            return False
        else:
            return True
    else:
        rows = game.rows
        # if the last cell not empty then return False
        if game.mat[rows - 1][col] != 0: #to apply move hence cannot be 1 or 2 as cell not empty
            return False
        else:
            return True


def get_valid_moves(game):
    # get the columns number
    cols = game.cols
    valid_moves = []
    # for each column try the two possible move (pop or push)
    for c in range(0, cols):
        # if pop valid
        if check_move(game, c, True):
            valid_moves.append((c, True)) #append to remove from connect4 game and add into empty set

        # if push valid
        if check_move(game, c, False):          #move works as row so add to column
            valid_moves.append((c, False))

    # return with shuffling the moves to get random moves each time.
    shuffle(valid_moves)
    return valid_moves


def computer_move(game, level):
    valid_moves = get_valid_moves(game) 
    if level == 1: ##== cause comparing between input of level and level of computer
        # return random valid move
        index = random.randint(0, len(valid_moves) - 1)
        return valid_moves[index][0], valid_moves[index][1]
    else:
        # check if i will win in next move
        for move in valid_moves:
            next_game = deepcopy(game)
            next_game = apply_move(next_game, move[0], move[1])
            if check_victory(next_game) == 3 - next_game.turn:
                return move[0], move[1]

        # check if my move not make him win in his next move
        for move in valid_moves:
            next_game = deepcopy(game)
            next_game = apply_move(next_game, move[0], move[1])
            # if the opponent win ignore this move
            if check_victory(next_game) == game.turn:
                continue
            next_valid_moves = get_valid_moves(next_game)
            is_good_move = True

            # Go to all moves the opponent can make
            for next_move in next_valid_moves:
                next_next_game = deepcopy(next_game)
                next_next_game = apply_move(next_next_game, next_move[0], next_move[1])

                # if he can make one move that make him win then our move not good enough
                if check_victory(next_next_game) != 0:
                    is_good_move = False

            if is_good_move:
                return move[0], move[1]

        # if not get good move return random move
        index = random.randint(0, len(valid_moves) - 1)
        return valid_moves[index][0], valid_moves[index][1]


def display_board(game):
    # Get rows and cols size
    rows = game.rows
    cols = game.cols
    # for each row and columns
    for r in range(0, rows):
        line = '| '
        for c in range(0, cols):
            # start from rows-1
            init_row = rows - r - 1
            line += str(game.mat[init_row][c]) + " | "
        # print line
        print(line)

    # print separated line
    print('=' * (cols * 4 + 1))

    line = '| '
    # for columns number
    for c in range(0, cols):
        line += str(c) + " | "

    # print columns number line
    print(line)


def is_game_full(game):
    rows = game.rows
    cols = game.cols
    # for each row and column if cell is empty then the game not full
    for r in range(0, rows):
        for c in range(0, cols):
            if game.mat[r][c] == 0:
                return False
    return True


def menu():
    cur_game = Game()
    # Get input from the user
    r = int(input("Enter a row size of the board: "))
    c = int(input("Enter a col size of the board: "))
    wins_number = int(input("Enter the number of adjacent cell need to win: "))
    print("(1) Human vs Human")
    print("(2) Human vs Computer")
    print("(3) Computer vs Computer")
    game_type = int(input("Enter a choice: "))

    # initialize the Game
    cur_game_board = np.zeros((r, c), dtype=int)
    cur_game.mat = cur_game_board
    cur_game.wins = wins_number
    cur_game.rows = r
    cur_game.cols = c
    cur_game.turn = 1
    display_board(cur_game)
    pop = False

    # if Human Vs Human
    if game_type == 1:

        # iterate until win or draw or the board is full
        while check_victory(cur_game) == 0 and not is_game_full(cur_game):

            # get the col and pop option from the user
            col = int(input("Player(" + str(cur_game.turn) + ") Enter a col: "))
            pop = int(input("Player(" + str(cur_game.turn) + ")" + " Enter a choose (1) Pop (2) Push : "))
            if pop == 1:
                pop = True
            else:
                pop = False

            # loop until the user enter valid move
            while not check_move(cur_game, col, pop):
                print("Please Enter a valid column.")
                col = int(input("Player(" + str(cur_game.turn) + ") Enter a col: "))
                pop = int(input("Player(" + str(cur_game.turn) + ")" + " Enter a choose (1) Pop (2) Push : "))
                if pop == 1:
                    pop = True
                else:
                    pop = False

            cur_game = apply_move(cur_game, col, pop) #current game is move applied to the game
            display_board(cur_game) #display current game

        winner = check_victory(cur_game) #check current board for victory
        # if draw and last move is POP
        if winner == 3 and pop:
            print("Player", 3 - cur_game.turn, "wins")
        elif winner == 3:
            print("The Game is Draw")
        else:
            print("Player", winner, "wins")

    # Human vs Computer
    elif game_type == 2:
        # get computer level
        computer_level = int(input("Enter a Computer level (1 OR 2): "))

        # iterate until win or draw or the board is full
        while check_victory(cur_game) == 0 and not is_game_full(cur_game):

            # if human
            if cur_game.turn == 1:

                # get the col and pop option from the user
                col = int(input("Player Enter a col: "))
                pop = int(input("Player Enter a choose (1) Pop (2) Push : "))
                if pop == 1:
                    pop = True
                else:
                    pop = False

                # loop until the user enter valid move
                while not check_move(cur_game, col, pop):
                    print("Please Enter a valid column.")
                    col = int(input("Player Enter a col: "))
                    pop = int(input("Player Enter a choose (1) Pop (2) Push : "))
                    if pop == 1:
                        pop = True
                    else:
                        pop = False
            else:
                col, pop = computer_move(cur_game, computer_level)
                print("Computer choose col:", col, " POP:", pop)

            cur_game = apply_move(cur_game, col, pop)
            display_board(cur_game)

        winner = check_victory(cur_game)
        # if draw and last move is POP
        if winner == 3 and pop:
            if cur_game.turn == 1:
                print("Computer wins") #similar to player 2 turn
            else:
                print("Player wins")
        elif winner == 3:
            print("The Game is Draw")
        elif winner == 1:
            print("Player wins")
        else:
            print("Computer wins")

    # Computer vs Computer: 3scenarios. player vs computer, player vs player, computer vs computer
    else:
        # get the two computers level
        computer_level1 = int(input("Enter a Computer(1) level (1 OR 2): "))
        computer_level2 = int(input("Enter a Computer(2) level (1 OR 2): "))

        # iterate until win or draw or the board is full
        while check_victory(cur_game) == 0 and not is_game_full(cur_game):
            if cur_game.turn == 1:
                col, pop = computer_move(cur_game, computer_level1)
                print("Computer 1 choose col:", col, " POP:", pop)
            else:
                col, pop = computer_move(cur_game, computer_level2)
                print("Computer 2 choose col:", col, " POP:", pop)

            cur_game = apply_move(cur_game, col, pop) 
            display_board(cur_game)

        winner = check_victory(cur_game)

        # if draw and last move is POP
        if winner == 3 and pop:
            print("Computer", 3 - cur_game.turn, "wins")
        elif winner == 3:
            print("The Game is Draw")
        else:
            print("Computer", winner, "wins")
            
menu()
