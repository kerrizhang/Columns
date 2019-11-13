'''Project #4: The Fall of the World's Own Optimist (Part 1)
Name: Kerri Zhang
SID: 21529066
Date: 11/28/2018
'''

from enum import Enum

class ColumnGameState(Enum):
    '''Columns Game State'''
    READY_FOR_FALLER = 1
    FALLER_ACTIVE = 2
    FALLER_LANDED = 3
    FALLER_FREEZE = 4
    SHOW_MATCHED_ITEM = 5
    REMOVE_MATCHED_ITEM = 6

class GameOverError(Exception):
    '''No moves left and game is over'''
    pass

class ColumnsGame:
    '''Game logic behind the game Columns'''
    def __init__(self, row: int, column: int):
        self.num_row = row
        self.num_column = column
        self.field = []
        for col in range(column):
            self.field.append([])
            for row_num in range(row):
                self.field[-1].append(0)
        self.faller_content = None
        self.faller_position = (0, 0)
        self.matching_items = []
        self.game_state = ColumnGameState.READY_FOR_FALLER
        self.left_over_faller_content = []

    def get_num_columns(self) -> int:
        '''Get number of columns'''
        return self.num_column

    def get_num_rows(self) -> int:
        '''Get number of rows'''
        return self.num_row

    def set_faller(self, faller_content: list, init_column_num: int) -> bool:
        '''Set faller content'''
        if self.faller_content is None and len(faller_content) == 3 and \
                (self.game_state == ColumnGameState.READY_FOR_FALLER or \
                    self.game_state == ColumnGameState.FALLER_ACTIVE):
            self.faller_content = faller_content
            self.faller_position = (init_column_num, 0)
            self._check_faller_set_game_state()
            if self.field[init_column_num][0] != 0:
                self.faller_content = None
                raise GameOverError
            return True
        else:
            return False

    def rotate_faller(self) -> None:
        '''Rotate faller content moving jewels bottom to top'''
        if self.faller_content is not None:
            new_content = [self.faller_content[2], self.faller_content[0], self.faller_content[1]]
            self.faller_content = new_content

    def advance_faller(self) -> bool:
        '''Advance faller down one row at a time'''
        if self.faller_content != 0:
            leading_row = self.faller_position[1] + 1
            if leading_row < self.num_row:
                if self.field[self.faller_position[0]][leading_row] == 0:
                    self.faller_position = (self.faller_position[0], leading_row)
                    return True
            return False

    def increase_col_faller(self) -> bool:
        '''Move faller to the right'''
        new_column = self.faller_position[0] + 1
        if new_column < self.num_column and self.faller_content is not None:
            for row_to_check in range(self.faller_position[1], self.faller_position[1] - 2, -1):
                if row_to_check >= 0:
                    if self.field[new_column][row_to_check] != 0:
                        return False
            self.faller_position = (new_column,self.faller_position[1])
            self._check_faller_set_game_state()
            return True
        else:
            return False

    def decrease_col_faller(self) -> bool:
        '''Move faller to the left'''
        new_column = self.faller_position[0]-1
        if new_column >= 0 and self.faller_content is not None:
            for row_to_check in range(self.faller_position[1], self.faller_position[1] - 2, -1):
                if row_to_check >= 0:
                    if self.field[new_column][row_to_check] != 0:
                        return False
            self.faller_position = (new_column, self.faller_position[1])
            self._check_faller_set_game_state()
            return True
        else:
            return False

    def check_faller_landed(self) -> bool:
        '''Check if faller has landed'''
        row_num_to_check = self.faller_position[1] + 1
        if row_num_to_check < self.num_row:
            col_num = self.faller_position[0]
            if (self.field[col_num][row_num_to_check]) == 0:
                return False
        return True

    def check_matching_field(self) -> list:
        '''Check for matching field'''
        matching_list = []
        for col_num in range(self.num_column):
            for row_num in range(self.num_row):
                if self.field[col_num][row_num] != 0:
                    matching_item = self._checking_column(col_num, row_num)
                    matching_item += self._checking_row(col_num, row_num)
                    matching_item += self._checking_diagonal_2_direction(col_num, row_num, 1)
                    matching_item += self._checking_diagonal_2_direction(col_num, row_num, -1)
                    for item in matching_item:
                        if item not in matching_list:
                            matching_list.append(item)
        self.matching_items = matching_list
        return matching_list

    def fill_the_hole_in_field(self) -> None:
        '''Fill the hole after matching field removes items'''
        for col_num in range(self.num_column):
            item_exist = False
            for row_num in range(self.num_row):
                if self.field[col_num][row_num] != 0:
                    item_exist = True
                else:
                    if item_exist is True:
                        self.field[col_num][1:row_num+1] = self.field[col_num][:row_num]
                        self.field[col_num][0] = 0

        if len(self.left_over_faller_content) != 0:
            faller_col, faller_row = self.faller_position
            for row_num in range(self.get_num_rows()):
                if self.field[faller_col][row_num] != 0:
                    self.faller_position = (faller_col, row_num - 1)
                    self._put_left_over_faller_to_field()
                    break

    def start_with_predefined_field(self) -> None:
        '''Start with predefined field and fill empty spaces followed by faller'''
        self.fill_the_hole_in_field()
        current_matching_positions = self.check_matching_field()
        if current_matching_positions == []:
            self.game_state = ColumnGameState.READY_FOR_FALLER
        else:
            self.game_state = ColumnGameState.SHOW_MATCHED_ITEM

    def next_automatic_move(self) -> None:
        '''Next automatic move'''
        if self.game_state == ColumnGameState.READY_FOR_FALLER:
            if self.faller_content is not None:
                self.game_state = ColumnGameState.FALLER_ACTIVE

        elif self.game_state == ColumnGameState.FALLER_ACTIVE:
            self.advance_faller()
            if self.check_faller_landed():
                self.game_state = ColumnGameState.FALLER_LANDED
        elif self.game_state == ColumnGameState.FALLER_LANDED:
            if self.check_faller_landed() == False:
                self.game_state = ColumnGameState.FALLER_ACTIVE
            else:
                self._put_faller_to_field()
                current_matching_positions = self.check_matching_field()
                if current_matching_positions ==[]:
                    self.game_state = ColumnGameState.READY_FOR_FALLER
                else:
                    self.game_state = ColumnGameState.SHOW_MATCHED_ITEM
        elif self.game_state == ColumnGameState.SHOW_MATCHED_ITEM:
            self._remove_items(self.matching_items)
            self.matching_items = []
            self.fill_the_hole_in_field()
            current_matching_positions = self.check_matching_field()
            if current_matching_positions == []:
                self.game_state = ColumnGameState.READY_FOR_FALLER
            else:
                self.game_state = ColumnGameState.SHOW_MATCHED_ITEM

    def _put_left_over_faller_to_field(self) -> None:
        '''Put left over content after matching into the field to check for more matching'''
        faller_pos_col, faller_pos_row = self.faller_position
        length_of_faller = len(self.left_over_faller_content)
        if faller_pos_row < length_of_faller - 1:
            self.field[faller_pos_col][:faller_pos_row + 1] = \
                self.left_over_faller_content[length_of_faller - faller_pos_row - 1:length_of_faller]
            self.left_over_faller_content = self.left_over_faller_content[:length_of_faller - faller_pos_row - 1]
            if self.check_matching_field() == []:
                raise GameOverError

        else:
            self.field[faller_pos_col][faller_pos_row - length_of_faller + 1:faller_pos_row + 1] = \
                self.left_over_faller_content[0:length_of_faller]
            self.left_over_faller_content =[]

    def _put_faller_to_field(self) -> None:
        '''Put faller into partial field to check for matching or else game over'''
        faller_pos_col, faller_pos_row = self.faller_position
        if faller_pos_row < 2:
            self.field[faller_pos_col][:faller_pos_row + 1] = \
                self.faller_content[2-faller_pos_row:3]
            self.left_over_faller_content = self.faller_content[:2 - faller_pos_row]
            if self.check_matching_field()==[]:
                self.faller_content = None
                raise GameOverError
        else:
            self.field[faller_pos_col][faller_pos_row - 2:faller_pos_row + 1] = \
                self.faller_content[0:3]
        self.faller_content = None

    def _check_faller_set_game_state(self) -> None:
        '''Check if faller has landed, if not it is still active'''
        if self.check_faller_landed():
            self.game_state = ColumnGameState.FALLER_LANDED
        else:
            self.game_state = ColumnGameState.FALLER_ACTIVE

    def _checking_column(self, col_num: int, row_num: int) -> list:
        '''Check column matching'''
        target_match_item = self.field[col_num][row_num]
        matching_num = 1
        matching_item = [(col_num, row_num)]
        for matching_row_num in range(row_num + 1, self.num_row):
            if self.field[col_num][matching_row_num] == target_match_item:
                matching_num += 1
                matching_item.append((col_num, matching_row_num))
            else:
                break
        if matching_num >= 3:
            return matching_item
        else:
            return []

    def _checking_row(self, col_num: int, row_num: int) -> list:
        '''Check row matching'''
        target_match_item = self.field[col_num][row_num]
        matching_num = 1
        matching_item = [(col_num, row_num)]
        for matching_column_num in range(col_num + 1, self.num_column):
            if self.field[matching_column_num][row_num] == target_match_item:
                matching_num += 1
                matching_item.append((matching_column_num, row_num))
            else:
                break
        if matching_num >= 3:
            return matching_item
        else:
            return []

    def _checking_diagonal_2_direction(self, col_num: int, row_num: int, delta: float) -> list:
        '''Check diagonal matching'''
        target_match_item = self.field[col_num][row_num]
        matching_num = 1
        matching_item = [(col_num, row_num)]
        for matching_column_num in range(col_num+1, self.num_column):
            matching_row_num = (matching_column_num - col_num) * delta + row_num
            if matching_row_num < self.num_row:
                if self.field[matching_column_num][matching_row_num] == target_match_item:
                    matching_num += 1
                    matching_item.append((matching_column_num, matching_row_num))
                    continue
            break
        if matching_num >= 3:
            return matching_item
        else:
            return []

    def _remove_items(self, position_list: list) -> None:
        '''Remove items for matching field'''
        for item_col, item_row in position_list:
            self.field[item_col][item_row] = 0


