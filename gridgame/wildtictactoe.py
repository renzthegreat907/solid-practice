from typing import Sequence
from .tictactoe import (
    # Project types:
    Field,
    Symbol,
    PlayerId,
    # Interface
    TicTacToeSymbolAndPlayerHandler,
    TicTacToeWinChecker,
    TicTacToeSettingInitializer,
    )

####################################################################################################
####################################################################################################
####################################################################################################

class WildTicTacToeSymbolAndPlayerHandler(TicTacToeSymbolAndPlayerHandler):

    def __init__(self,
        player_symbols: Sequence[Symbol],
        player_count: int
        ) -> None:

        self._player_symbols = player_symbols
        self._player_count = player_count
        self._validate_player_symbols()
        self._validate_player_count()
        self._player_to_symbol = NotImplemented
        self._symbol_to_player = NotImplemented

    def _validate_player_count(self,
        ) -> None:
        player_count = self._player_count

        if player_count <= 1:
            raise ValueError(
            f'Must have at least two players (found {player_count})')

    def _validate_player_symbols(self,
        ) -> None:

        player_symbols: Sequence[Symbol] = self._player_symbols
        player_count: int = self._player_count

        unique_symbols = set(player_symbols)

        if len(unique_symbols) != len(player_symbols):
            raise ValueError(
                f'Player symbols must be unique (was {player_symbols}')

        if len(player_symbols) != player_count:
            raise ValueError(
                f'Player symbols must be exactly {player_count} (was {player_symbols})')

    def inquire_final_cell(self, cell: Cell, field: Field) -> Cell:
        return cell

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        if player not in self._player_to_symbol:
            raise ValueError(f'Invalid player: {player}')

        return [self._player_to_symbol[player]]

####################################################################################################
####################################################################################################
####################################################################################################

class WildTicTacToeWinChecker(TicTacToeWinChecker):

    def winner(self, field: Field, current_player: PlayerId) -> PlayerId | None:
        for groups in self._groups(field):
            for group in groups:
                if (basis := field.get_symbol_at(group[0])) is not None and \
                        field.are_all_equal_to_basis(basis, group):
                    winner = self._symbol_and_player_handler.symbol_to_player.get(basis)
                    assert winner is not None, \
                        f'Winning symbol {basis} in cell group {groups} has no associated player'
                    assert (player_symbol := self._symbol_and_player_handler.player_to_symbol[winner]) == basis, \
                        f'Detected winning player {winner} with linked symbol {player_symbol} is not the same with current player {current_player}'

                    return winner

####################################################################################################
####################################################################################################
####################################################################################################

class WildTicTacToeSettingInitializer(TicTacToeSettingInitializer):
    ...