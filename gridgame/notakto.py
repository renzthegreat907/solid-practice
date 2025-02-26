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

class NotaktoSymbolAndPlayerHandler(TicTacToeSymbolAndPlayerHandler):

    def __init__(self,
        player_symbols: Symbol,
        player_count: int
        ) -> None:

        self._validate_player_symbol(player_symbols)
        self._player_symbol = player_symbols[0]
        self._player_count = player_count

    def _validate_player_symbol(self,
        player_symbol: Symbol
        ) -> None:

        if len(player_symbol) != 1:
            raise ValueError(
                f'Player symbols must be exactly 1 (was {player_symbol})')

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        return [self._player_symbol]

    @property
    def player_symbol(self) -> Symbol:
        return self._player_symbol

####################################################################################################
####################################################################################################
####################################################################################################

class NotaktoWinChecker(TicTacToeWinChecker):

    def winner(self, field: Field, current_player: PlayerId) -> PlayerId | None:
        for groups in self._groups(field):
            for group in groups:
                basis = self.symbol_and_player_handler.player_symbol
                loser_player = self.symbol_and_player_handler.prev_player(current_player)
                if field.are_all_equal_to_basis(basis, group):
                    winner = self.symbol_and_player_handler.prev_player(loser_player)

                    return winner

####################################################################################################
####################################################################################################
####################################################################################################

class NotaktoSettingInitializer(TicTacToeSettingInitializer):
    ...