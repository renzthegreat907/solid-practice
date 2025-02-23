from gridgame.project_types import Field, Cell


def test_is_valid_cell_initial_1():
    field = Field(1)

    valid_coords = [1]

    for row in valid_coords:
        for col in valid_coords:
            assert field.is_within_bounds(Cell(row, col))

    assert not field.is_within_bounds(Cell(0, 0))
    assert not field.is_within_bounds(Cell(1, 0))
    assert not field.is_within_bounds(Cell(0, 1))
    assert not field.is_within_bounds(Cell(-1, 0))
    assert not field.is_within_bounds(Cell(0, -1))
    assert not field.is_within_bounds(Cell(-1, -1))
    assert not field.is_within_bounds(Cell(0, 2))
    assert not field.is_within_bounds(Cell(2, 0))
    assert not field.is_within_bounds(Cell(1, 2))
    assert not field.is_within_bounds(Cell(2, 1))


def test_is_valid_cell_initial_2():
    field = Field(2)

    valid_coords = [1, 2]

    for row in valid_coords:
        for col in valid_coords:
            assert field.is_within_bounds(Cell(row, col))

    assert not field.is_within_bounds(Cell(0, 0))
    assert not field.is_within_bounds(Cell(1, 0))
    assert not field.is_within_bounds(Cell(0, 1))
    assert not field.is_within_bounds(Cell(-1, 0))
    assert not field.is_within_bounds(Cell(0, -1))
    assert not field.is_within_bounds(Cell(-1, -1))
    assert not field.is_within_bounds(Cell(0, 3))
    assert not field.is_within_bounds(Cell(3, 0))
    assert not field.is_within_bounds(Cell(1, 3))
    assert not field.is_within_bounds(Cell(3, 1))


def test_is_valid_cell_initial_3():
    field = Field(3)

    valid_coords = [1, 2, 3]

    for row in valid_coords:
        for col in valid_coords:
            assert field.is_within_bounds(Cell(row, col))

    assert not field.is_within_bounds(Cell(0, 0))
    assert not field.is_within_bounds(Cell(1, 0))
    assert not field.is_within_bounds(Cell(0, 1))
    assert not field.is_within_bounds(Cell(-1, 0))
    assert not field.is_within_bounds(Cell(0, -1))
    assert not field.is_within_bounds(Cell(-1, -1))
    assert not field.is_within_bounds(Cell(0, 4))
    assert not field.is_within_bounds(Cell(4, 0))
    assert not field.is_within_bounds(Cell(1, 4))
    assert not field.is_within_bounds(Cell(4, 1))


def test_is_valid_cell_initial_4():
    field = Field(4)

    valid_coords = [1, 2, 3, 4]

    for row in valid_coords:
        for col in valid_coords:
            assert field.is_within_bounds(Cell(row, col))

    assert not field.is_within_bounds(Cell(0, 0))
    assert not field.is_within_bounds(Cell(1, 0))
    assert not field.is_within_bounds(Cell(0, 1))
    assert not field.is_within_bounds(Cell(-1, 0))
    assert not field.is_within_bounds(Cell(0, -1))
    assert not field.is_within_bounds(Cell(-1, -1))
    assert not field.is_within_bounds(Cell(0, 5))
    assert not field.is_within_bounds(Cell(5, 0))
    assert not field.is_within_bounds(Cell(1, 5))
    assert not field.is_within_bounds(Cell(5, 1))


def test_has_unoccupied_cell_2():
    field = Field(2)
    assert field.has_unoccupied_cell()

    field.place_symbol('O', Cell(1, 1))
    assert field.has_unoccupied_cell()
    field.place_symbol('X', Cell(2, 2))
    assert field.has_unoccupied_cell()
    field.place_symbol('O', Cell(1, 2))
    assert field.has_unoccupied_cell()
    field.place_symbol('X', Cell(2, 1))
    assert not field.has_unoccupied_cell()


def test_has_unoccupied_cell_3():
    field = Field(3)
    assert field.has_unoccupied_cell()

    field.place_symbol('O', Cell(1, 1))
    assert field.has_unoccupied_cell()
    field.place_symbol('X', Cell(2, 2))
    assert field.has_unoccupied_cell()
    field.place_symbol('O', Cell(1, 2))
    assert field.has_unoccupied_cell()
    field.place_symbol('X', Cell(2, 1))
    assert field.has_unoccupied_cell()
    field.place_symbol('O', Cell(3, 3))
    assert field.has_unoccupied_cell()
    field.place_symbol('X', Cell(3, 2))
    assert field.has_unoccupied_cell()
    field.place_symbol('O', Cell(3, 1))
    assert field.has_unoccupied_cell()
    field.place_symbol('X', Cell(1, 3))
    assert field.has_unoccupied_cell()
    field.place_symbol('O', Cell(2, 3))
    assert not field.has_unoccupied_cell()
