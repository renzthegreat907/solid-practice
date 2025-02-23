import pytest

from gridgame.model import GridGameModel, Symbol, Cell, Feedback


def test_duplicate_symbols_exception():
    with pytest.raises(ValueError):
        GridGameModel(3, [Symbol.NOUGHT, Symbol.NOUGHT])

    with pytest.raises(ValueError):
        GridGameModel(3, [Symbol.CROSS, Symbol.CROSS])

    with pytest.raises(ValueError):
        GridGameModel(3, [Symbol.STAR, Symbol.STAR])

    with pytest.raises(ValueError):
        GridGameModel(3, [Symbol.CROSS, Symbol.NOUGHT, Symbol.CROSS])

    with pytest.raises(ValueError):
        GridGameModel(3, [Symbol.CROSS, Symbol.NOUGHT,
                       Symbol.STAR, Symbol.CROSS])


def test_invalid_player_counts():
    with pytest.raises(ValueError):
        GridGameModel(3, [])

    with pytest.raises(ValueError):
        GridGameModel(3, [Symbol.NOUGHT])


def test_get_player_symbol_correct_2p():
    model = GridGameModel(3, [Symbol.CROSS, Symbol.NOUGHT])

    assert model.get_player_symbol(0) is None
    assert model.get_player_symbol(1) == Symbol.CROSS
    assert model.get_player_symbol(2) == Symbol.NOUGHT
    assert model.get_player_symbol(3) is None


def test_get_symbol_initial():
    model = GridGameModel(3, [Symbol.CROSS, Symbol.NOUGHT])

    for r in range(-10, 11):
        for c in range(-10, 11):
            assert model.get_symbol_at(Cell(r, c)) is None


def test_get_current_player_initial():
    model = GridGameModel(3, [Symbol.CROSS, Symbol.NOUGHT])

    assert model.get_current_player() == 1


def test_is_valid_cell_initial_1():
    model = GridGameModel(1, [Symbol.CROSS, Symbol.NOUGHT])

    valid_coords = [1]

    for row in valid_coords:
        for col in valid_coords:
            assert model.is_within_bounds(Cell(row, col))

    assert not model.is_within_bounds(Cell(0, 0))
    assert not model.is_within_bounds(Cell(1, 0))
    assert not model.is_within_bounds(Cell(0, 1))
    assert not model.is_within_bounds(Cell(-1, 0))
    assert not model.is_within_bounds(Cell(0, -1))
    assert not model.is_within_bounds(Cell(-1, -1))
    assert not model.is_within_bounds(Cell(0, 2))
    assert not model.is_within_bounds(Cell(2, 0))
    assert not model.is_within_bounds(Cell(1, 2))
    assert not model.is_within_bounds(Cell(2, 1))


def test_is_valid_cell_initial_2():
    model = GridGameModel(2, [Symbol.CROSS, Symbol.NOUGHT])

    valid_coords = [1, 2]

    for row in valid_coords:
        for col in valid_coords:
            assert model.is_within_bounds(Cell(row, col))

    assert not model.is_within_bounds(Cell(0, 0))
    assert not model.is_within_bounds(Cell(1, 0))
    assert not model.is_within_bounds(Cell(0, 1))
    assert not model.is_within_bounds(Cell(-1, 0))
    assert not model.is_within_bounds(Cell(0, -1))
    assert not model.is_within_bounds(Cell(-1, -1))
    assert not model.is_within_bounds(Cell(0, 3))
    assert not model.is_within_bounds(Cell(3, 0))
    assert not model.is_within_bounds(Cell(1, 3))
    assert not model.is_within_bounds(Cell(3, 1))


def test_is_valid_cell_initial_3():
    model = GridGameModel(3, [Symbol.CROSS, Symbol.NOUGHT])

    valid_coords = [1, 2, 3]

    for row in valid_coords:
        for col in valid_coords:
            assert model.is_within_bounds(Cell(row, col))

    assert not model.is_within_bounds(Cell(0, 0))
    assert not model.is_within_bounds(Cell(1, 0))
    assert not model.is_within_bounds(Cell(0, 1))
    assert not model.is_within_bounds(Cell(-1, 0))
    assert not model.is_within_bounds(Cell(0, -1))
    assert not model.is_within_bounds(Cell(-1, -1))
    assert not model.is_within_bounds(Cell(0, 4))
    assert not model.is_within_bounds(Cell(4, 0))
    assert not model.is_within_bounds(Cell(1, 4))
    assert not model.is_within_bounds(Cell(4, 1))


def test_is_valid_cell_initial_4():
    model = GridGameModel(4, [Symbol.CROSS, Symbol.NOUGHT])

    valid_coords = [1, 2, 3, 4]

    for row in valid_coords:
        for col in valid_coords:
            assert model.is_within_bounds(Cell(row, col))

    assert not model.is_within_bounds(Cell(0, 0))
    assert not model.is_within_bounds(Cell(1, 0))
    assert not model.is_within_bounds(Cell(0, 1))
    assert not model.is_within_bounds(Cell(-1, 0))
    assert not model.is_within_bounds(Cell(0, -1))
    assert not model.is_within_bounds(Cell(-1, -1))
    assert not model.is_within_bounds(Cell(0, 5))
    assert not model.is_within_bounds(Cell(5, 0))
    assert not model.is_within_bounds(Cell(1, 5))
    assert not model.is_within_bounds(Cell(5, 1))


def test_place_on_out_of_bounds():
    model = GridGameModel(3, [Symbol.CROSS, Symbol.NOUGHT])

    assert model.place_symbol(Cell(0, 0)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(1, 0)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(0, 1)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(-1, 0)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(0, -1)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(-1, -1)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(0, 4)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(4, 0)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(1, 4)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol(Cell(4, 1)) == Feedback.OUT_OF_BOUNDS


def test_place_on_all_valid():
    model = GridGameModel(3, [Symbol.CROSS, Symbol.NOUGHT])

    assert model.place_symbol(Cell(1, 1)) == Feedback.VALID
    assert model.place_symbol(Cell(2, 2)) == Feedback.VALID
    assert model.place_symbol(Cell(3, 3)) == Feedback.VALID

    assert model.get_symbol_at(Cell(1, 1)) == Symbol.CROSS
    assert model.get_symbol_at(Cell(2, 2)) == Symbol.NOUGHT
    assert model.get_symbol_at(Cell(3, 3)) == Symbol.CROSS


def test_place_on_game_over():
    model = GridGameModel(2, [Symbol.NOUGHT, Symbol.CROSS])
    model.place_symbol(Cell(1, 1))
    model.place_symbol(Cell(2, 2))
    model.place_symbol(Cell(1, 2))

    assert model.place_symbol(Cell(2, 1)) == Feedback.GAME_OVER
    assert model.place_symbol(Cell(2, 2)) == Feedback.GAME_OVER


def test_get_player_count:
    assert GridGameModel(3, [
        Symbol.NOUGHT,
        Symbol.CROSS,
    ]).player_count == 2

    assert GridGameModel(3, [
        Symbol.CROSS,
        Symbol.STAR,
        Symbol.NOUGHT,
    ]).player_count == 3


def test_get_next_player_initial():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])

    assert model.next_player == 2


def test_get_next_player_multiple_2_all_valid():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])

    assert model.next_player == 2
    model.place_symbol(Cell(1, 1))
    assert model.next_player == 1
    model.place_symbol(Cell(2, 2))
    assert model.next_player == 2
    model.place_symbol(Cell(2, 1))
    assert model.next_player == 1


def test_get_next_player_multiple_2_with_errors():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])

    assert model.next_player == 2
    model.place_symbol(Cell(1, 1))
    assert model.next_player == 1
    model.place_symbol(Cell(1, 1))
    assert model.next_player == 1
    model.place_symbol(Cell(2, 2))
    assert model.next_player == 2
    model.place_symbol(Cell(-1, -1))
    model.place_symbol(Cell(-1, -1))
    model.place_symbol(Cell(0, 0))
    model.place_symbol(Cell(4, 1))
    assert model.next_player == 2
    model.place_symbol(Cell(1, 3))
    assert model.next_player == 1
    model.place_symbol(Cell(1, 3))
    model.place_symbol(Cell(1, 3))
    model.place_symbol(Cell(1, 3))
    assert model.next_player == 1


def test_get_next_player_multiple_3_all_valid():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS, Symbol.STAR])

    assert model.next_player == 2
    model.place_symbol(Cell(1, 1))
    assert model.next_player == 3
    model.place_symbol(Cell(2, 2))
    assert model.next_player == 1
    model.place_symbol(Cell(2, 1))
    assert model.next_player == 2
    model.place_symbol(Cell(3, 3))
    assert model.next_player == 3
    model.place_symbol(Cell(3, 2))
    assert model.next_player == 1


def test_get_next_player_multiple_3_with_errors():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS, Symbol.STAR])

    assert model.next_player == 2
    model.place_symbol(Cell(1, 1))
    assert model.next_player == 3
    model.place_symbol(Cell(1, 2))
    assert model.next_player == 1
    model.place_symbol(Cell(2, 2))
    assert model.next_player == 2
    model.place_symbol(Cell(-1, -1))
    model.place_symbol(Cell(-1, -1))
    model.place_symbol(Cell(0, 0))
    model.place_symbol(Cell(4, 1))
    assert model.next_player == 2
    model.place_symbol(Cell(1, 3))
    assert model.next_player == 3
    model.place_symbol(Cell(1, 3))
    model.place_symbol(Cell(1, 3))
    model.place_symbol(Cell(1, 3))
    assert model.next_player == 3


def test_is_game_over_2():
    model = GridGameModel(2, [Symbol.NOUGHT, Symbol.CROSS])
    assert not model.is_game_over

    model.place_symbol(Cell(1, 1))
    assert not model.is_game_over
    model.place_symbol(Cell(2, 2))
    assert not model.is_game_over
    model.place_symbol(Cell(1, 2))
    assert model.is_game_over


def test_has_unoccupied_cell_2():
    model = GridGameModel(2, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.has_unoccupied_cell()

    model.place_symbol(Cell(1, 1))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(2, 2))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(1, 2))
    assert model.has_unoccupied_cell()

    # Invalid move
    model.place_symbol(Cell(2, 1))
    assert model.has_unoccupied_cell()


def test_has_unoccupied_cell_3():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.has_unoccupied_cell()

    model.place_symbol(Cell(1, 1))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(2, 2))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(1, 2))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(2, 1))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(3, 3))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(3, 2))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(3, 1))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(1, 3))
    assert model.has_unoccupied_cell()
    model.place_symbol(Cell(2, 3))
    assert not model.has_unoccupied_cell()


def test_get_winner_2():
    model = GridGameModel(2, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(1, 1))
    assert model.winner is None
    model.place_symbol(Cell(2, 2))
    assert model.winner is None
    model.place_symbol(Cell(1, 2))
    assert model.winner == 1

    # Invalid move
    model.place_symbol(Cell(2, 1))
    assert model.winner == 1


def test_get_winner_3_backslash():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(1, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 2))  # O
    assert model.winner is None
    model.place_symbol(Cell(2, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(2, 1))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 3))  # X
    assert model.winner == 1


def test_get_winner_3_forward_slash():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(1, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 3))  # O
    assert model.winner is None
    model.place_symbol(Cell(2, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(2, 2))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(3, 1))  # O
    assert model.winner == 2


def test_get_winner_3_row_1():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(1, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(2, 1))  # O
    assert model.winner is None
    model.place_symbol(Cell(1, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(2, 2))  # O
    assert model.winner is None
    model.place_symbol(Cell(1, 3))  # X
    assert model.winner == 1


def test_get_winner_3_row_2():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(2, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 1))  # O
    assert model.winner is None
    model.place_symbol(Cell(2, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 2))  # O
    assert model.winner is None
    model.place_symbol(Cell(2, 3))  # X
    assert model.winner == 1


def test_get_winner_3_row_3():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(3, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 1))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 2))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 3))  # X
    assert model.winner == 1


def test_get_winner_3_col_1():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(2, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 1))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 3))  # X
    assert model.winner is None
    model.place_symbol(Cell(2, 1))  # O
    assert model.winner is None
    model.place_symbol(Cell(1, 3))  # X
    assert model.winner is None
    model.place_symbol(Cell(3, 1))  # O
    assert model.winner == 2


def test_get_winner_3_col_2():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(2, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 2))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 3))  # X
    assert model.winner is None
    model.place_symbol(Cell(2, 2))  # O
    assert model.winner is None
    model.place_symbol(Cell(1, 3))  # X
    assert model.winner is None
    model.place_symbol(Cell(3, 2))  # O
    assert model.winner == 2


def test_get_winner_3_col_3():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(2, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 3))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(2, 3))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(3, 3))  # O
    assert model.winner == 2


def test_get_winner_draw_3():
    model = GridGameModel(3, [Symbol.NOUGHT, Symbol.CROSS])
    assert model.winner is None

    model.place_symbol(Cell(2, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 1))  # O
    assert model.winner is None
    model.place_symbol(Cell(1, 2))  # X
    assert model.winner is None
    model.place_symbol(Cell(3, 2))  # O
    assert model.winner is None
    model.place_symbol(Cell(2, 3))  # X
    assert model.winner is None
    model.place_symbol(Cell(2, 1))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 1))  # X
    assert model.winner is None
    model.place_symbol(Cell(1, 3))  # O
    assert model.winner is None
    model.place_symbol(Cell(3, 3))  # X
    assert model.winner is None


def test_grid_size:
    assert GridGameModel(
        2, [Symbol.NOUGHT, Symbol.CROSS]).grid_size == 2
    assert GridGameModel(
        3, [Symbol.NOUGHT, Symbol.CROSS]).grid_size == 3
    assert GridGameModel(
        4, [Symbol.NOUGHT, Symbol.CROSS]).grid_size == 4
    assert GridGameModel(
        5, [Symbol.NOUGHT, Symbol.CROSS]).grid_size == 5
    assert GridGameModel(
        10, [Symbol.NOUGHT, Symbol.CROSS]).grid_size == 10
