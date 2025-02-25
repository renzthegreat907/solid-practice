from tictactoe import (
    Cell,
    Field,
    TicTacToeMode,
    TicTacToeSymbolHandler,
    TicTacToeWinChecker,
    PlayerId,
    Sequence,
    Symbol
    )

####################################################################################################
####################################################################################################
####################################################################################################

class NotaktoSymbolHandler(TicTacToeSymbolHandler):

    def __init__(self,
        player_symbol: Symbol,
        player_count: int
        ) -> None:

        self._validate_player_symbol(player_symbol)
        self._player_symbol = player_symbol
        self._player_count = player_count

    def _validate_player_symbol(self,
        player_symbol: Symbol
        ) -> None:

        if len(player_symbol) != 1:
            raise ValueError(
                f'Player symbols must be exactly 1 (was {player_symbol})')

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        return [self._player_symbol]

####################################################################################################
####################################################################################################
####################################################################################################

class NotaktoWinChecker(TicTacToeWinChecker):

    def winner(self, field: Field) -> PlayerId | None:
        for groups in self._groups(field):
            for group in groups:
                if (basis := field.get_symbol_at(group[0])) is not None and \
                        field.are_all_equal_to_basis(basis, group):
                    winner = self._symbol_to_player.get(basis)
                    assert winner is not None, \
                        f'Winning symbol {basis} in cell group {groups} has no associated player'

                    return winner

####################################################################################################
####################################################################################################
####################################################################################################

class NotaktoSettingInitializer(TicTacToeSettingInitializer):

    def __init__(self, win_checker: NotaktoWinChecker) -> None:
        self._win_checker: NotaktoWinChecker = win_checker

    def validate_grid_size(self, grid_size: int) -> None:
        if grid_size < 3:
            raise ValueError(
                f'Tic-tac-toe games must have grid size at least 3! (currently {grid_size})')
