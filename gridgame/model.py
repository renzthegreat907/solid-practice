# from typing import Protocol
from copy import deepcopy
# from typing import Tuple
from typing import Collection, Dict
from .project_types import (
    PlayerId,
    Cell,
    Symbol,
    Feedback,
    )
from collections.abc import Sequence
from abc import ABC, abstractmethod

from .project_types import PlayerId, Cell, Symbol, Feedback, Field

####################################################################################################
####################################################################################################
####################################################################################################

class GridGameSymbolHandler(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self._symbol_to_player = NotImplemented
        self._player_to_symbol = NotImplemented

    @abstractmethod
    def _validate_player_symbols(self,
        player_symbols: Sequence[Symbol],
        player_count: int
        ) -> None:
        raise NotImplementedError

    @abstractmethod
    def place_symbol(self, symbol: Symbol, cell: Cell) -> Feedback:
        raise NotImplementedError

    @abstractmethod
    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        raise NotImplementedError

    @property
    def player_to_symbol(self) -> Dict[PlayerId, Symbol]:
        return deepcopy(self._player_to_symbol)

    @property
    def symbol_to_player(self) -> Dict[Symbol, PlayerId]:
        return deepcopy(self.symbol_to_player)

class TicTacToeSymbolHandler(GridGameSymbolHandler):

    def __init__(self,
        player_symbols: Sequence[Symbol],
        player_count: int
        ) -> None:

        self._validate_player_symbols(player_symbols, player_count)
        self._player_symbols = player_symbols
        self._player_count = player_count

        self._player_to_symbol: dict[PlayerId, Symbol] = {
            k: symbol
            for k, symbol in enumerate(player_symbols, start=1)
        }
        self._symbol_to_player: dict[Symbol, PlayerId] = {
            symbol: k
            for k, symbol in self._player_to_symbol.items()
        }

    def _validate_player_symbols(self,
        player_symbols: Sequence[Symbol],
        player_count: int
        ) -> None:

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

    def _validate_grid_size(self, grid_size: int) -> None:
        if grid_size <= 2:
            raise ValueError(
                f'Grid size ({grid_size}) is less than 3 for game: tic-tac-toe!')

    def _inquire_final_cell(self,
        cell: Cell,
        field: Field
        ) -> Cell:
        return cell

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        if player not in self._player_to_symbol:
            raise ValueError(f'Invalid player: {player}')

        return [self._player_to_symbol[player]]

####################################################################################################
####################################################################################################
####################################################################################################

class GridGameWinChecker(ABC):

    def __init__(self,
        symbol_handler: GridGameSymbolHandler
        ) -> None:

        self._symbol_handler = symbol_handler
        self._symbol_to_player = symbol_handler.symbol_to_player

    @property
    def symbol_handler(self):
        return self._symbol_handler

    @abstractmethod
    def winner(self, field: Field) -> PlayerId | None:
        raise NotImplementedError

    def _groups(self, field: Field) -> list[list[Cell]]:

        row_groups = [
            [Cell(row, k) for k in field.valid_coords]
            for row in field.valid_coords
        ]

        col_groups = [
            [Cell(k, col) for k in field.valid_coords]
            for col in field.valid_coords
        ]

        diagonals = [
            # Backslash
            [Cell(k, k) for k in field.valid_coords],
            # Forward slash
            [Cell(k, field.grid_size - k + 1)
             for k in field.valid_coords],
        ]

        return row_groups + col_groups + diagonals

class TicTacToeWinChecker(GridGameWinChecker):

    def winner(self, field: Field) -> PlayerId | None:

        for group in self._groups:
            if (basis := field.get_symbol_at(group[0])) is not None and \
                    field.are_all_equal_to_basis(basis, group):
                winner = self._symbol_to_player.get(basis)
                assert winner is not None, \
                    f'Winning symbol {basis} in cell group {groups} has no associated player'

                return winner

####################################################################################################

class GridGameModel:

    @abstractmethod
    def _validate_grid_size(self, grid_size: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def __init__(self,
        grid_size: int,
        player_symbols: Sequence[Symbol],
        player_count: int,
        win_checker: GridGameWinChecker,
        ) -> None:

        self._field = Field(grid_size)
        self._player_count = player_count
        self._current_player: PlayerId = 1
        self._player_symbols: Symbol | Sequence[Symbol]
        self._win_checker: GridGameWinChecker = win_checker
        self._symbol_handler: GridGameSymbolHandler = win_checker.symbol_handler

        self._validate_player_existence()
        # self._validate_win_checker_containing_same_symbol_handler(self._win_checker, self._symbol_handler)
        # self._validate_grid_size(grid_size)
        # self._symbol_handler._validate_player_symbols(player_symbols, player_count)

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        return self._symbol_handler.get_symbol_choices(player)

    def place_symbol(self,
        symbol: Symbol,
        cell: Cell) -> Feedback:

        if self.is_game_over:
            return Feedback.GAME_OVER

        if symbol not in self._symbol_handler.get_symbol_choices(self.current_player):
            return Feedback.INVALID_SYMBOL

        if not self._field.is_within_bounds(cell):
            return Feedback.OUT_OF_BOUNDS

        if self._field.get_symbol_at(cell) is not None:
            return Feedback.OCCUPIED

        # when guaranteed the cell is selectable,
        # symbol stays the same, but cell may not.
        final_cell = _symbol_handler._inquire_final_cell(cell, self._field)

        self._field.place_symbol(symbol, final_cell)
        self._switch_to_next_player()

        return Feedback.VALID

    @property
    def winner(self) -> PlayerId | None:
        return self._win_checker.winner(self._field)

    def _validate_player_existence(self) -> None:
        if (player_count := self.player_count) <= 0:
            raise ValueError(
                f'Player count cannot be negative! (currently {player_count})')

    def _initialize_common_actions(self,
        grid_size: int,
        player_symbols: Symbol | Sequence[Symbol],
        player_count: int) -> tuple[
            Field,
            int,
            PlayerId
        ]:
        _field = Field(grid_size)
        _player_count = player_count
        _current_player: PlayerId = 1
        self._validate_player_existence()
        self._validate_grid_size(grid_size)
        self._validate_player_symbols(player_symbols, player_count)

        return (
            _field,
            _player_count,
            _current_player
            )

    @property
    def occupied_cells(self) -> dict[Cell, Symbol]:
        return self._field.occupied_cells

    @property
    def grid_size(self):
        return self._field.grid_size

    @property
    def is_game_over(self):
        return (
            self.winner is not None or
            not self._field.has_unoccupied_cell()
        )

    @property
    def current_player(self) -> PlayerId:
        return self._current_player

    @property
    def player_count(self):
        return self._player_count

    @property
    def next_player(self) -> PlayerId:
        return (
            self.current_player + 1 if self.current_player != self.player_count else
            1
        )

    def _switch_to_next_player(self):
        self._current_player = self.next_player