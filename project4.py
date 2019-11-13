'''Project #4: The Fall of the World's Own Optimist (Part 1)
Name: Kerri Zhang
SID: 21529066
Date: 11/28/2018
'''

import project4_game_logic
from project4_game_logic import ColumnsGame
from project4_game_logic import ColumnGameState
from project4_game_logic import GameOverError

def display_game(game: ColumnsGame) -> None:
    '''Display game'''
    num_col = game.get_num_columns()
    num_row = game.get_num_rows()
    for row_num in range(num_row):
        string = "|"
        for col_num in range(num_col):
            string += generate_string_for_cell(game,col_num,row_num)
        string += "|"
        print(string)
    string = " "
    for col_num in range(num_col):
        string += "---"
    string += " "
    print(string)

def generate_string_for_cell(game: ColumnsGame, col_num: int, row_num: int) -> str:
    '''Generate string to print jewels in cells'''
    faller_col, faller_row = game.faller_position
    if col_num == faller_col and faller_row >= row_num \
            and row_num >= (faller_row - 2) and game.faller_content is not None:
        if game.game_state == ColumnGameState.FALLER_FREEZE:
            string = " {} ".format(game.field[col_num][row_num])
        elif game.game_state == ColumnGameState.FALLER_LANDED:
            string = "|{}|".format(game.faller_content[row_num - faller_row + 2])
        else:
            string = "[{}]".format(game.faller_content[row_num - faller_row + 2])
    else:
        if game.game_state == ColumnGameState.SHOW_MATCHED_ITEM and \
                        (col_num, row_num) in game.matching_items:
            string = "*{}*".format(game.field[col_num][row_num])
        else:
            content = game.field[col_num][row_num]
            if content == 0:
                string = "   "
            else:
                string = " {} ".format(content)
    return string

def columns_main() -> None:
    '''Set up game'''
    try:
        num_row = int(input())
        num_column = int(input())
    except ValueError:
        print("ERROR")
    game_init_method = input().upper()
    game = ColumnsGame(num_row, num_column)
    if game_init_method != "EMPTY":
        for row_num in range(num_row):
            row_content = input().upper()
            for col_num in range(num_column):
                if row_content[col_num] == " ":
                    game.field[col_num][row_num] = 0
                else:
                    game.field[col_num][row_num]=row_content[col_num]
        game.start_with_predefined_field()

    try:
        while True:
            display_game(game)
            command = input().upper().split()
            if command ==[]:
                game.next_automatic_move()
            elif command[0] == "F" and len(command) == 5:
                game.set_faller([command[2], command[3], command[4]], int(command[1]) - 1)
            elif command[0] == "<":
                game.decrease_col_faller()
            elif command[0] == ">":
                game.increase_col_faller()
            elif command[0] == "R":
                game.rotate_faller()
            elif command[0] == "Q":
                break
    except GameOverError:
        display_game(game)
        print("GAME OVER")


if __name__ == '__main__':
    columns_main()

