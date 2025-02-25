from copy import deepcopy
from typing import Dict
from .project_types import (
    Field,
    PlayerId,
    Cell,
    Symbol,
    Feedback,
    )
from collections.abc import Sequence
from abc import ABC, abstractmethod

####################################################################################################
####################################################################################################
####################################################################################################

class GridGameSymbolHandler(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self._player_symbols = NotImplemented
        self._player_count = NotImplemented
        self._symbol_to_player = NotImplemented
        self._player_to_symbol = NotImplemented

    @abstractmethod
    def _validate_player_symbols(self
        ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        raise NotImplementedError

    @abstractmethod
    def inquire_final_cell(self, cell: Cell, field: Field) -> Cell:
        raise NotImplementedError

    @property
    def player_to_symbol(self) -> Dict[PlayerId, Symbol]:
        return deepcopy(self._player_to_symbol)

    @property
    def symbol_to_player(self) -> Dict[Symbol, PlayerId]:
        return deepcopy(self._symbol_to_player)

####################################################################################################
####################################################################################################
####################################################################################################

class GridGameWinChecker(ABC):

    def __init__(self,
        symbol_handler: GridGameSymbolHandler
        ) -> None:

        self._symbol_handler = NotImplemented # symbol_handler
        self._player_to_symbol = NotImplemented # symbol_handler.player_to_symbol
        self._symbol_to_player = NotImplemented # symbol_handler.symbol_to_player

    @property
    def symbol_handler(self):
        return self._symbol_handler

    @abstractmethod
    def winner(self, field: Field) -> PlayerId | None:
        raise NotImplementedError

    def _groups(self, field: Field) -> Sequence[list[list[Cell]]]:

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

        return row_groups, col_groups, diagonals



####################################################################################################
####################################################################################################
####################################################################################################

class GridGameMode(ABC):

    @abstractmethod
    def __init__(self,
        win_checker: GridGameWinChecker) -> None:
        self._win_checker = NotImplemented

    @property
    def win_checker(self) -> GridGameWinChecker:
        return self._win_checker

    @abstractmethod
    def validate_grid_size(self, grid_size: int) -> None:
        raise NotImplementedError

####################################################################################################
####################################################################################################
####################################################################################################

class GridGameModel:

    @abstractmethod
    def __init__(self,
        grid_size: int,
        player_symbols: Sequence[Symbol],
        player_count: int,
        setting_initializer: GridGameSettingInitizalizer
        ) -> None:

        self._field = Field(grid_size)
        self._player_count = player_count
        self._current_player: PlayerId = 1
        self._player_symbols: Symbol | Sequence[Symbol] = player_symbols

        self._setting_initializer: GridGameSettingInitizalizer = setting_initializer
        self._win_checker: GridGameWinChecker = self._setting_initializer.win_checker
        self._symbol_handler: GridGameSymbolHandler = self._win_checker.symbol_handler

        self._validate_player_existence()
        self._validate_grid_size_general()
        self._validate_grid_size_specific()

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
        final_cell = self._symbol_handler.inquire_final_cell(cell, self._field)

        self._field.place_symbol(symbol, final_cell)
        self._switch_to_next_player()

        return Feedback.VALID

    def _validate_grid_size_general(self) -> None:
        if not (grid_size := self.grid_size) >= 3:
            raise ValueError(
                f'Grid games should have grid size greater than 3! (currently {grid_size})')

    def _validate_grid_size_specific(self) -> None:
        self._setting_initializer.validate_grid_size(self.grid_size)

    @property
    def winner(self) -> PlayerId | None:
        return self._win_checker.winner(self._field)

    def _validate_player_existence(self) -> None:
        if not self.player_count:
            raise ValueError(
                f'Player count cannot be negative! (currently {self.player_count})')

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
