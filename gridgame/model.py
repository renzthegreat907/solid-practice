from collections.abc import Sequence, Iterable

from .project_types import PlayerId, Cell, Symbol, Feedback


class GridGameModel:
    def __init__(self, grid_size: int, player_symbols: Sequence[Symbol], player_count: int):
        if player_count <= 1:
            raise ValueError(
                f'Must have at least two players (found {player_count})')

        unique_symbols = set(player_symbols)

        if len(unique_symbols) != len(player_symbols):
            raise ValueError(
                f'Player symbols must be unique (was {player_symbols}')

        if len(player_symbols) != player_count:
            raise ValueError(
                f'Player symbols must be exactly {player_count} (was {player_symbols})')

        self._player_count = player_count
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

    @property
    def occupied_cells(self) -> dict[Cell, Symbol]:
        return {
            cell: symbol for cell, symbol in self._grid.items()
            if symbol is not None
        }

    @property
    def grid_size(self):
        return self._grid_size

    @property
    def is_game_over(self):
        return (
            self.winner is not None or
            not self.has_unoccupied_cell()
        )

    @property
    def current_player(self) -> PlayerId:
        return self._current_player

    @property
    def player_count(self):
        return len(self._player_to_symbol)

    @property
    def next_player(self) -> PlayerId:
        return (
            self.current_player + 1 if self.current_player != self.player_count else
            1
        )

    @property
    def winner(self) -> PlayerId | None:
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
                if (basis := self._get_symbol_at(group[0])) is not None and \
                        self._are_all_equal_to_basis(basis, group):
                    winner = self._symbol_to_player.get(basis)
                    assert winner is not None, \
                        f'Winning symbol {basis} in cell group {groups} has no associated player'

                    return winner

        return None

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        if player not in self._player_to_symbol:
            raise ValueError(f'Invalid player: {player}')

        return [self._player_to_symbol[player]]

    def is_within_bounds(self, cell: Cell) -> bool:
        return (
            1 <= cell.row <= self._grid_size and
            1 <= cell.col <= self._grid_size
        )

    def place_symbol(self, symbol: Symbol, cell: Cell) -> Feedback:
        if self.is_game_over:
            return Feedback.GAME_OVER

        if symbol not in self.get_symbol_choices(self.current_player):
            return Feedback.INVALID_SYMBOL

        if not self.is_within_bounds(cell):
            return Feedback.OUT_OF_BOUNDS

        if self._get_symbol_at(cell) is not None:
            return Feedback.OCCUPIED

        self._place_symbol(symbol, cell)
        self._switch_to_next_player()

        return Feedback.VALID

    def has_unoccupied_cell(self):
        return any(
            True for cell in self._valid_cells
            if self._get_symbol_at(cell) is None
        )

    def _are_all_equal_to_basis(self, basis: Symbol, group: Iterable[Cell]):
        return all(self._get_symbol_at(cell) == basis for cell in group)

    def _get_symbol_at(self, cell: Cell) -> Symbol | None:
        return self._grid.get(cell)

    def _switch_to_next_player(self):
        self._current_player = self.next_player

    def _place_symbol(self, symbol: Symbol, cell: Cell):
        assert self.is_within_bounds(cell)

        self._grid[cell] = symbol
