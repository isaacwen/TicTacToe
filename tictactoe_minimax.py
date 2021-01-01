# Isaac Wen
# This program uses the minimax algorithm to play tictactoe perfectly
# against the user

# To use this program by itself, uncomment the final line of this program
# (the line containing just 'main()') before running it.

# For the design of this program, the board will be represented as a string
# of 9 digits, with the indexes of each string representing the positions
# on the tictactoe board as follows:
#   0 | 1 | 2
#   ---------
#   3 | 4 | 5
#   ---------
#   6 | 7 | 8

#   - the digits will be numbers from 0 - 2, with 0 representing an empty
#     spot, 1 representing player's one moves, and 2 representing player 2's
#     moves
#   - if player 1 is O's and player 2 is X's, and example board for the
#     sequence 011212212 is
#             | O | O
#           ---------
#           X | O | X
#           ---------
#           X | O | X
#   - NOTE: this program will assign player 1 to be O's always, and player
#     2 to be X's always


# Takes a 9-digit string and draws the corresponding tictactoe board
def draw_board(board):
    symbols = convert_digit(board)
    display = ""
    for i in range(0, 3):
        for index in range(0 + i * 3, 3 + i * 3):
            if index % 3 != 2:
                display = display + symbols[index] + ' | '
            else:
                display = display + symbols[index]
        if i % 3 != 2:
            display = display + '\n---------\n'
    return display


# Converts a string of 9 digits to the equivalent string of tictactoe
# symbols, following the specifications outlined at the start
def convert_digit(board):
    symbols = ''
    for i in range(0, 9):
        if board[i] == '0':
            symbols = symbols + ' '
        elif board[i] == '1':
            symbols = symbols + 'O'
        else:
            symbols = symbols + 'X'
    return symbols


# Takes the player who is making a move and the location which they
# desire to make their move on (as a number from 0-8), and changes the
# board to reflect their move (adds their move to the board); if the
# location already has a piece, returns False
#   - player is input as a str
def make_move(board, player, location):
    if board[location] != '0':
        return False
    return board[:location] + str(player) + board[location + 1:]


# Determines if there is a player who has won on the board, and returns
# that player's number; otherwise returns False
def player_won(board):
    # Checks all the rows
    for row in range(0, 3):
        first_row = board[0 + row * 3]
        second_row = board[1 + row * 3]
        third_row = board[2 + row * 3]
        if first_row == second_row == third_row != '0':
            return first_row
    # Checks all the columns
    for col in range(0, 3):
        first_col = board[0 + col]
        second_col = board[3 + col]
        third_col = board[6 + col]
        if first_col == second_col == third_col != '0':
            return first_col
    # Checks both diagonals
    if board[0] == board[4] == board[8] != '0':
        return board[0]
    if board[2] == board[4] == board[6] != '0':
        return board[2]
    return False


# Generates a list of all possible moves that a player can make, that is
# all possible board positions after the player makes a move
def poss_moves(board, player):
    indices = []
    for i in range(9):
        if board[i] == '0':
            indices.append(i)
    possible_moves = []
    for index in indices:
        a_move = board[:index] + player + board[index + 1:]
        possible_moves.append(a_move)
    return possible_moves


# Determines if a board is in the final state, that is, one player has won
# or the board is filled such that there are no remaining possible moves
def final_state(board):
    if player_won(board) != False:
        return True
    if poss_moves(board, '1') == []:
        return True
    return False


# Gives a board a score: 1 if player 1 (O) wins, -1 if player 2 (X) wins,
# 0 if neither player wins, or False if the board is not in a final state
def board_score(board):
    if final_state(board) == False:
        return False
    elif player_won(board) == False:
        return 0
    elif player_won(board) == '1':
        return 1
    else:
        return -1


# Maximizer: given a board position, determines which of the possible
# moves that player 1 can make which will result in the best possible
# outcome; if one of the possible moves is not a final board state, then
# its score will be determined by minimizer
def maximizer(board):
    moves = poss_moves(board, '1')
    move_scores = []
    for move in moves:
        if final_state(move):
            move_scores.append(board_score(move))
        else:
            (min_score, min_move) = minimizer(move)
            move_scores.append(min_score)
    max_score = max(move_scores)
    index_max = move_scores.index(max_score)
    return (max_score, moves[index_max])


# Minimizer: given a board position, determines which of the possible moves
# that player 2 can make which will result in the best possible outcome; if
# one of the possible moves is not a final board state, then its score will
# be determined by maximizer
def minimizer(board):
    moves = poss_moves(board, '2')
    move_scores = []
    for move in moves:
        if final_state(move):
            move_scores.append(board_score(move))
        else:
            (max_score, max_move) = maximizer(move)
            move_scores.append(max_score)
    min_score = min(move_scores)
    index_min = move_scores.index(min_score)
    return (min_score, moves[index_min])


# Produces the best possible move given a board position and the player whose
# turn it is
def best_move(board, player):
    if player == '1':
        comp_move = maximizer(board)
        return comp_move[1]
    else:
        comp_move = minimizer(board)
        return comp_move[1]


# Simulates a computer's turn, given a board and the player which the
# computer is (1 or 2), and ending the game if approriate
def computer_turn(board, user, computer):
    print('The computer plays:')
    next_board = best_move(board, computer)
    print(draw_board(next_board))
    score = board_score(next_board)
    if not (type(score) == int):
        user_turn(next_board, user, computer)
    elif score == 0:
        end_screen('tie')
    else:
        end_screen('computer')


# Simulates a user's turn, by displaying the board, giving instructions for
# giving input, and ending the game if appropriate
def user_turn(board, user, computer):
    print('It is now your turn. The current board is as shown:')
    print(draw_board(board))
    if user == '1':
        print('You are O\'s.')
    else:
        print('You are X\'s.')
    # The numbers are changed to a nicer looking 1 - 9 rather than 0 - 8,
    # and this is adjusted by subtracting one to match the specifications of
    # the functions
    print('Each spot on the board is represented by a number from 0 - 8, as'
          ' follows: \n1 | 2 | 3\n---------\n4 | 5 | 6\n---------\n7 | 8 | '
          '9\n')
    index = input('Enter a num from 1 - 9 where you would like to place'
                  ' your next piece: ')
    try:
        user_move = make_move(board, user, int(index) - 1)
    except:
        print('That was not a valid input.')
        user_turn(board, user, computer)
        return
    if user_move == False:
        print('The move you entered is already occupied by a piece.')
        user_turn(board, user, computer)
        return
    else:
        print('You have made the following move: ')
        print(draw_board(user_move))
    user_score = board_score(user_move)
    if not (type(user_score) == int):
        computer_turn(user_move, user, computer)
    elif user_score == 0:
        end_screen('tie')
    else:
        end_screen('user')


# Given a value of 'user' if the user wins, 'computer' if the computer has
# won, or 'tie' if the game ends in a tie, displays the ending screen with a
# prompt to play again
def end_screen(result):
    if result == 'user':
        play_again = input('Congratulations! You have done the impossible'
                           'and beaten the minimax algorithm.\nWould you'
                           ' like to play again? (Enter Y if so): ')
    elif result == 'tie':
        play_again = input('The game has ended in a tie.\nWould you like'
                           ' to play again? (Enter Y if so): ')
    else:
        play_again = input('You lost. Better luck next time!\nWould you like'
                           ' to play again? (Enter Y if so): ')
    if play_again == 'Y':
        main()
    return


# Main function for initializing the game:
def main():
    start_board = '000000000'
    player = input('Welcome to TicTacToe! You will be playing against the '
                   'minimax algorithm.\nWould you like to go first or '
                   'second? (Enter 1 to go first, 2 to go second): ')
    if player == '1':
        computer = '2'
        user_turn(start_board, player, computer)
    elif player == '2':
        computer = '1'
        computer_turn(start_board, player, computer)
    else:
        print("That was not a valid input.")
        main()
        return


# main()
