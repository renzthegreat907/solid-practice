from typing import Iterable

from .project_types import PlayerId, Cell, Symbol, Feedback


class GridGameModel:
    def __init__(self, grid_size: int, player_symbols: Iterable[Symbol]):
        if len(set(player_symbols)) != len(list(player_symbols)):
            raise ValueError(
                f'Player symbols must be unique: {player_symbols}')

        if (player_count := len(list(player_symbols))) <= 1:
            raise ValueError(
                f'Must have at least two players (found {player_count})')

        self._grid_size = grid_size
        self._valid_coords = list(range(1, self._grid_size + 1))
        self._valid_cells = set(
            Cell(r, c)
            for r in self._valid_coords
            for c in self._valid_coords
        )
        self._grid: dict[Cell, Symbol | None] = {
            cell: None for cell in self._valid_cells
        }

        self._player_to_symbol: dict[PlayerId, Symbol] = {
            k: symbol
            for k, symbol in enumerate(player_symbols, start=1)
        }
        self._symbol_to_player: dict[Symbol, PlayerId] = {
            symbol: k
            for k, symbol in self._player_to_symbol.items()
        }
        self._current_player: PlayerId = 1

    def get_grid_size(self):
        return self._grid_size

    def get_player_symbol(self, player: PlayerId) -> Symbol | None:
        return self._player_to_symbol.get(player)

    def get_current_player(self) -> PlayerId:
        return self._current_player

    def get_symbol_at(self, cell: Cell) -> Symbol | None:
        return self._grid.get(cell)

    def is_within_bounds(self, cell: Cell) -> bool:
        return (
            1 <= cell.row <= self._grid_size and
            1 <= cell.col <= self._grid_size
        )

    def place_on(self, cell: Cell) -> Feedback:
        symbol = self._player_to_symbol.get(self.get_current_player())
        assert symbol is not None, f'No symbol found for {self.get_current_player()}'

        if self.is_game_over():
            return Feedback.GAME_OVER

        if not self.is_within_bounds(cell):
            return Feedback.OUT_OF_BOUNDS

        if self.get_symbol_at(cell) is not None:
            return Feedback.OCCUPIED

        self._place_symbol(symbol, cell)
        self._switch_to_next_player()

        return Feedback.VALID

    def _switch_to_next_player(self):
        self._current_player = self.get_next_player()

    def get_player_count(self):
        return len(self._player_to_symbol)

    def get_next_player(self) -> PlayerId:
        current = self.get_current_player()

        return current + 1 if current != self.get_player_count() else 1

    def _place_symbol(self, symbol: Symbol, cell: Cell):
        assert self.is_within_bounds(cell)

        self._grid[cell] = symbol

    def has_unoccupied_cell(self):
        return any(
            True for cell in self._valid_cells
            if self.get_symbol_at(cell) is None
        )

    def get_winner(self) -> PlayerId | None:
        row_groups = [
            [Cell(row, k) for k in self._valid_coords]
            for row in self._valid_coords
        ]

        col_groups = [
            [Cell(k, col) for k in self._valid_coords]
            for col in self._valid_coords
        ]

        diagonals = [
            # Backslash
            [Cell(k, k) for k in self._valid_coords],
            # Forward slash
            [Cell(k, self._grid_size - k + 1) for k in self._valid_coords],
        ]

        for groups in [row_groups, col_groups, diagonals]:
            for group in groups:
                if (basis := self.get_symbol_at(group[0])) is not None and \
                        self._are_all_equal_to_basis(basis, group):
                    winner = self._symbol_to_player.get(basis)
                    assert winner is not None, \
                        f'Winning symbol {basis} in cell group {groups} has no associated player'

                    return winner

        return None

    def _are_all_equal_to_basis(self, basis: Symbol, group: Iterable[Cell]):
        return all(self.get_symbol_at(cell) == basis for cell in group)

    def is_game_over(self):
        return (
            self.get_winner() is not None or
            not self.has_unoccupied_cell()
        )
