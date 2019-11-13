'''Project #4: The Fall of the World's Own Optimist (Part 1)
Name: Kerri Zhang
SID: 21529066
Date: 11/28/2018
'''

import unittest
from project4_game_logic import ColumnsGame
from project4_game_logic import ColumnGameState
from project4_game_logic import GameOverError

class ColumnGameTest(unittest.TestCase):
    def test_initial_state_of_game(self) -> None:
        '''Test initial state of game, field should be empty'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        self.assertEqual(game.num_row, row)
        self.assertEqual(game.num_column, column)
        self.faller_content = None
        for col in range(column):
            for row in range(row):
                self.assertEqual(game.field[col][row], 0)

    def test_faller_setting(self) -> None:
        '''Test faller setting, set_faller returns true or false'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        self.assertFalse(game.set_faller(["a", "b"], 3))
        self.assertEqual(game.faller_content, None)
        self.assertTrue(game.set_faller(["a", "b", "c"], 3))
        self.assertEqual(game.faller_content, ["a", "b", "c"])
        self.assertFalse(game.set_faller(["b", "c", "d"], 3))
        self.assertEqual(game.faller_content, ["a", "b", "c"])


    def test_faller_rotation(self) -> None:
        '''Test faller rotation, rotate_faller takes string or list and rotates bottom to top'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.rotate_faller()
        self.assertEqual(game.faller_content, ["c", "a", "b"])
        game.rotate_faller()
        self.assertEqual(game.faller_content, ["b", "c", "a"])

    def test_faller_advance(self) -> None:
        '''Test faller advance, advance_faller returns true or false.
        The faller should be able to advance to next row'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        for row_num in range(row - 1):
            self.assertEqual(game.faller_position, (3, row_num))
            self.assertTrue(game.advance_faller())
        else:
            self.assertEqual(game.faller_position, (3, row - 1))
            self.assertFalse(game.advance_faller())
            self.assertEqual(game.faller_position, (3, row - 1))

    def test_faller_advance_complicated(self) -> None:
        '''Test faller advance, where there is a jewel in the way'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        game.set_faller("abc", 3)
        self.assertEqual(game.faller_position, (3, 0))
        self.assertTrue(game.advance_faller())
        self.assertEqual(game.faller_position, (3, 1))
        self.assertFalse(game.advance_faller())
        self.assertEqual(game.faller_position, (3, 1))


    def test_faller_column_up(self) -> None:
        '''Test faller moving left across columns'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        for col_num in range(3, 5):
            self.assertEqual(game.faller_position, (col_num, 0))
            self.assertTrue(game.increase_col_faller())
        else:
            self.assertEqual(game.faller_position, (5, 0))
            self.assertFalse(game.increase_col_faller())
            self.assertEqual(game.faller_position, (5, 0))

    def test_faller_column_up_more(self) -> None:
        '''Should not be able to move left across column with jewel in the way'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        game.faller_position = (2, 2)
        self.assertEqual(game.faller_position, (2, 2))
        self.assertFalse(game.increase_col_faller())
        self.assertEqual(game.faller_position, (2, 2))

    def test_faller_column_down(self) -> None:
        '''Test faller moving right across columns'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        for col_num in range(3):
            self.assertEqual(game.faller_position, (3 - col_num, 0))
            self.assertTrue(game.decrease_col_faller())
        else:
            self.assertEqual(game.faller_position, (0, 0))
            self.assertFalse(game.decrease_col_faller())
            self.assertEqual(game.faller_position, (0, 0))

    def test_faller_column_down_more(self) -> None:
        '''Should not be able to move right across column with jewel in the way'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        game.faller_position = (4,2)
        self.assertEqual(game.faller_position, (4, 2))
        self.assertFalse(game.decrease_col_faller())
        self.assertEqual(game.faller_position, (4, 2))

    def test_faller_landed(self) -> None:
        '''Test faller landed and not pass the jewel in the way'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        game.faller_position = (4, 2)
        self.assertFalse(game.check_faller_landed())
        game.faller_position = (4, 4)
        self.assertTrue(game.check_faller_landed())
        game.faller_position = (3, 1)
        self.assertTrue(game.check_faller_landed())

    def test_check_column_logic(self) -> None:
        '''Test column logic after match'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [(3, 2), (3, 3), (3, 4)])

        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [])

    def test_check_row_logic(self) -> None:
        '''Test row logic after match'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [(1, 2), (2, 2), (3, 2)])

        game = ColumnsGame(row, column)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [])

    def test_check_diagonal_logic(self) -> None:
        '''Test diagonal logic after match'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [(1, 2), (2, 3), (3, 4)])

        game = ColumnsGame(row, column)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [])

        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [])

    def test_check_combo_matching_logic(self) -> None:
        '''Test multiple matching combinations logic'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [(1, 2), (2, 2), (3, 2), (2, 3), (3, 4), (2, 1), (2, 4)])
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 1, 2, 1],
            [0, 0, 0, 2, 0],
            [0, 0, 0, 2, 0]
        ]
        matching_result = game.check_matching_field()
        self.assertEqual(matching_result, [(1, 2), (2, 2), (3, 2), (2, 3), (3, 4), (2, 1), (2, 4), \
                                           (3, 3), (4, 3), (5, 3)])

    def test_remove_items(self) -> None:
        '''Test removing jewels in specific positions to later remove matched items'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.field = [
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
        ]
        remove_list = [(0, 1),(2, 3),(4, 4)]
        game._remove_items(remove_list)
        self.assertEqual(game.field, [[1, 0, 3, 4, 5],
                                      [1, 2, 3, 4, 5],
                                      [1, 2, 3, 0, 5],
                                      [1, 2, 3, 4, 5],
                                      [1, 2, 3, 4, 0],
                                      [1, 2, 3, 4, 5]])

    def test_fill_hole(self) -> None:
        '''Test filling in the hole by moving jewels down'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller("abc", 3)
        game.field = [
            [1, 0, 2, 0, 3],
            [0, 1, 2, 3, 0],
            [0, 1, 1, 1, 1],
            [0, 1, 2, 0, 3],
            [3, 1, 2, 0, 0],
            [1, 2, 3, 4, 5]
        ]
        game.fill_the_hole_in_field()
        self.assertEqual(game.field,
                         [[0, 0, 1, 2, 3],
                          [0, 0, 1, 2, 3],
                          [0, 1, 1, 1, 1],
                          [0, 0, 1, 2, 3],
                          [0, 0, 3, 1, 2],
                          [1, 2, 3, 4, 5]])

    def test_faller_to_field(self) -> None:
        '''Test faller and put into field'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller([2, 3, 4], 5)
        game.faller_position = (4, 2)
        game.field = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0]]

        game._put_faller_to_field()
        self.assertEqual(game.field,
                       [[0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 1],
                        [0, 0, 1, 0, 1],
                        [2, 3, 4, 1, 0],
                        [0, 0, 0, 0, 0]])
        game = ColumnsGame(row, column)
        game.field = [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 1],
                        [0, 0, 1, 0, 1],
                        [2, 3, 4, 1, 0],
                        [0, 0, 0, 0, 0]]

        game.set_faller([2, 3, 4], 5)
        game.faller_position = (5, 4)
        game._put_faller_to_field()
        self.assertEqual(game.field,
                       [[0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 1],
                        [0, 0, 1, 0, 1],
                        [2, 3, 4, 1, 0],
                        [0, 0, 2, 3, 4]])

    def test_predefined_field(self) -> None:
        '''Test predefined field using specified contents'''
        row = 4
        column = 4
        game = ColumnsGame(row, column)
        S = 'S'
        T = 'T'
        X = 'X'
        V = 'V'
        Y = 'Y'
        Z = 'Z'
        game.field = [
            [0, S, T, X],
            [Y, 0, X, 0],
            [0, V, Y, X],
            [X, 0, S, Y]]

        game.start_with_predefined_field()

        self.assertEqual(game.field,
                         [[0, S, T, X],
                          [0, 0, Y, X],
                          [0, V, Y, X],
                          [0, X, S, Y]]
                         )
        game.next_automatic_move()
        self.assertEqual(game.field,
                         [[0, 0, S, T],
                         [0, 0, 0, Y],
                         [0, 0, V, Y],
                         [0, X, S, Y]]
                         )
        game.next_automatic_move()
        self.assertEqual(game.field,
                         [[0, 0, S, T],
                          [0, 0, 0, 0],
                          [0, 0, 0, V],
                          [0, 0, X, S]]
                         )
        game.set_faller([X, Y, Z], 1)
        self.assertEqual(game.field,
                         [[0, 0, S, T],
                          [0, 0, 0, 0],
                          [0, 0, 0, V],
                          [0, 0, X, S]]
                         )
        self.assertEqual(game.faller_position, (1, 0))

    def test_auto_movement(self) -> None:
        '''Test next automatic move including matching and faller'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller([2, 3, 4], 5)
        game.faller_position = (3, 3)
        game.field = [
            [0, 0, 0, 0, 1],
            [0, 0, 1, 3, 4],
            [0, 1, 1, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
        game.game_state = ColumnGameState.FALLER_ACTIVE
        game.next_automatic_move()
        game.next_automatic_move()
        game.next_automatic_move()
        self.assertEqual(game.game_state, ColumnGameState.SHOW_MATCHED_ITEM)
        game.next_automatic_move()
        self.assertEqual(game.game_state, ColumnGameState.READY_FOR_FALLER)
        self.assertEqual(game.field,
                         [[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 2],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])

    def test_faller_freeze_partial_fit_matching_delay_ending(self) -> None:
        '''Test faller that will freeze with a partial fit, delaying the ending by
        having a match that makes room for more jewels in the column'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller([1, 1, 2], 0)
        game.field = [
            [0, 0, 2, 2, 1],
            [0, 0, 0, 3, 4],
            [0, 1, 1, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
        game.game_state = ColumnGameState.FALLER_ACTIVE
        game.next_automatic_move()
        self.assertEqual(game.game_state, ColumnGameState.FALLER_LANDED)
        game.next_automatic_move()
        self.assertEqual(game.field,
                         [[1, 2, 2, 2, 1],
                          [0, 0, 0, 3, 4],
                          [0, 1, 1, 3, 4],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])

        game.next_automatic_move()
        self.assertEqual(game.field,
                         [[0, 0, 1, 1, 1],
                          [0, 0, 0, 3, 4],
                          [0, 1, 1, 3, 4],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])

        game.next_automatic_move()
        self.assertEqual(game.field,
                         [[0, 0, 0, 0, 0],
                          [0, 0, 0, 3, 4],
                          [0, 1, 1, 3, 4],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])

    def test_faller_freeze_partial_fit_matching_delay_ending2(self) -> None:
        '''Test another faller that will freeze with a partial fit, delaying the ending by
        having a match that makes room for more jewels in the column'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller([3,1,2], 0)
        game.field = [
            [0, 1, 2, 2, 1],
            [2, 1, 2, 3, 4],
            [2, 4, 1, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
        game.game_state = ColumnGameState.FALLER_ACTIVE

        game.next_automatic_move()
        self.assertEqual(game.game_state, ColumnGameState.FALLER_LANDED )

        game.next_automatic_move()
        self.assertEqual(game.field,
                         [[2, 1, 2, 2, 1],
                          [2, 1, 2, 3, 4],
                          [2, 4, 1, 3, 4],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])

        game.next_automatic_move()
        self.assertEqual(game.field,
                         [[1, 1, 2, 2, 1],
                          [0, 1, 2, 3, 4],
                          [0, 4, 1, 3, 4],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])

        game.next_automatic_move()
        self.assertEqual(game.field,
                         [[3, 1, 2, 2, 1],
                          [0, 0, 2, 3, 4],
                          [0, 0, 4, 3, 4],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])
        self.assertEqual(game.game_state, ColumnGameState.READY_FOR_FALLER)

    def test_faller_freeze_partial_fit_matching_delay_ending_then_end(self) -> None:
        '''Test faller that will freeze with a partial fit, having a match but
        ending with a game over after the match'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller([3,1,2], 0)
        game.field = [
            [0, 1, 2, 2, 1],
            [2, 5, 2, 3, 4],
            [2, 4, 1, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
        game.game_state = ColumnGameState.FALLER_ACTIVE
        game.next_automatic_move()
        self.assertEqual(game.game_state, ColumnGameState.FALLER_LANDED)
        game.next_automatic_move()

        try:
            game.next_automatic_move()
        except GameOverError:
            game_over = 1
        else:
            game_over = 0
        finally:
            self.assertEqual(game_over, 1)
            self.assertRaises(GameOverError)

    def test_end_game(self) -> None:
        '''Test the ending of the game'''
        row = 5
        column = 6
        game = ColumnsGame(row, column)
        game.set_faller([3, 1, 2], 0)
        game.field = [
            [0, 1, 2, 2, 1],
            [0, 5, 2, 3, 4],
            [0, 4, 1, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
        game.game_state = ColumnGameState.FALLER_ACTIVE
        game.next_automatic_move()

        try:
            game.next_automatic_move()
        except GameOverError:
            game_over = 1
        else:
            game_over = 0
        finally:
            self.assertEqual(game_over, 1)
            self.assertRaises(GameOverError)
            self.assertEqual(game.faller_content, None)

unittest.main()
