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

class GridGameSymbolAndPlayerHandler(ABC):

    @abstractmethod
    def __init__(self,
        player_symbols: Symbol | Sequence[Symbol],
        player_count: int,
        ) -> None:
        self._player_symbol: Symbol = NotImplemented
        self._player_symbols: Sequence[Symbol] = NotImplemented
        self._player_count = NotImplemented
        self._symbol_to_player = NotImplemented
        self._player_to_symbol = NotImplemented

    @abstractmethod
    def validate_player_count(self
        ) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def validate_player_symbols(self
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

    @property
    def player_symbol(self) -> Symbol:
        return deepcopy(self._player_symbol)

    @property
    def player_symbols(self) -> Sequence[Symbol]:
        return deepcopy(self._player_symbols)

    def next_player(self, current_player: PlayerId) -> PlayerId:
        return (
            current_player + 1 if current_player != self._player_count else
            1
        )

    def prev_player(self, current_player: PlayerId) -> PlayerId:
        return (
            current_player - 1 if current_player != 1 else
            self._player_count
        )

####################################################################################################
####################################################################################################
####################################################################################################

class GridGameWinChecker(ABC):

    def __init__(self,
        symbol_and_player_handler: GridGameSymbolAndPlayerHandler
        ) -> None:

        self._symbol_and_player_handler = symbol_and_player_handler
        self._player_to_symbol = NotImplemented
        self._symbol_to_player = NotImplemented

    @property
    def symbol_and_player_handler(self):
        return self._symbol_and_player_handler

    @abstractmethod
    def winner(self, field: Field, current_player: PlayerId) -> PlayerId | None:
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

class GridGameSettingInitializer(ABC):

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

    def __init__(self,
        grid_size: int,
        player_symbols: Sequence[Symbol],
        player_count: int,
        symbol_and_player_handler: type[GridGameSymbolAndPlayerHandler],
        win_checker: type[GridGameWinChecker],
        setting_initializer: type[GridGameSettingInitializer],
        ) -> None:

        self._field = Field(grid_size)
        self._player_count = player_count
        self._current_player: PlayerId = 1
        self._player_symbols: Symbol | Sequence[Symbol] = player_symbols

        # self._symbol_and_player_handler: GridGameSymbolAndPlayerHandler = self._win_checker.symbol_and_player_handler
        # self._win_checker: GridGameWinChecker = self._setting_initializer.win_checker
        # self._setting_initializer: GridGameSettingInitializer = setting_initializer

        self._symbol_and_player_handler = symbol_and_player_handler(
            player_symbols=player_symbols,
            player_count=player_count,
            )

        self._win_checker = win_checker(
            self._symbol_and_player_handler
            )

        self._setting_initializer = setting_initializer(
            self._win_checker
            )

        self._validate_player_count()
        self._validate_player_symbols()
        self._validate_grid_size()

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        return self._symbol_and_player_handler.get_symbol_choices(player)

    def place_symbol(self,
        symbol: Symbol,
        cell: Cell) -> Feedback:

        if self.is_game_over:
            return Feedback.GAME_OVER

        if symbol not in self._symbol_and_player_handler.get_symbol_choices(self.current_player):
            return Feedback.INVALID_SYMBOL

        if not self._field.is_within_bounds(cell):
            return Feedback.OUT_OF_BOUNDS

        if self._field.get_symbol_at(cell) is not None:
            return Feedback.OCCUPIED

        # when guaranteed the cell is selectable,
        # symbol stays the same, but cell may not.
        final_cell = self._symbol_and_player_handler.inquire_final_cell(cell, self._field)

        self._field.place_symbol(symbol, final_cell)
        self._switch_to_next_player()

        return Feedback.VALID

    def _validate_player_symbols(self) -> None:
        self._symbol_and_player_handler.validate_player_symbols()

    def _validate_grid_size(self) -> None:
        # General
        if not (grid_size := self.grid_size) >= 2:
            raise ValueError(
                f'Grid games should have grid size greater than 3! (currently {grid_size})')
        # Game specific
        self._setting_initializer.validate_grid_size(self.grid_size)

    @property
    def winner(self) -> PlayerId | None:
        return self._win_checker.winner(self._field, self._current_player)

    """
    what are the baseline factors needed to determine a winner?
    you can look at:
    - the field
        to know if a line is completed? ALWAYS
        to know what block has finished/completed a line? NOT ALWAYS !!!
            case for notakto and pick15:
                you cannot look at JUST the field to know who won
                because blocks belong to everyone.
    - the current player !!!
        to know who was playing when the game finished? ALWAYS
            but depending on the game, it may be:
                the one who recently placed; or
                the one who placed previously

    overall, winner needs access to:
        the field
        the current player(id)
        the ability to know who was the PREVIOUS player

    recall the hierarchy of inheritance:
        symbol handler
        win checker
        setting initializer
        game model

    therefore, the "player cycler" cannot be in the actual game model
    it must be at least in the symbol handler

    in this line of thought, symbol handler now becomes symbol-player handler
    """

    def _validate_player_count(self) -> None:
        # General
        if self.player_count < 1:
            raise ValueError(
                f'Player count must be a positive integer! (currently {self.player_count})')
        # Game specific
        self._symbol_and_player_handler.validate_player_count()

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
        return self._symbol_and_player_handler.next_player(self.current_player)

    def _switch_to_next_player(self):
        self._current_player = self.next_player


####################################################################################################
####################################################################################################
####################################################################################################