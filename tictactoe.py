from model import (
    Cell,
    Field,
    GridGameMode,
    GridGameSymbolHandler,
    GridGameWinChecker,
    PlayerId,
    Sequence,
    Symbol
    )

####################################################################################################
####################################################################################################
####################################################################################################

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

    def inquire_final_cell(self, cell: Cell, field: Field) -> Cell:
        return cell

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        if player not in self._player_to_symbol:
            raise ValueError(f'Invalid player: {player}')

        return [self._player_to_symbol[player]]

####################################################################################################
####################################################################################################
####################################################################################################

class TicTacToeWinChecker(GridGameWinChecker):

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

class TicTacToeGamemode(GridGameMode):

    def __init__(self, win_checker: TicTacToeWinChecker) -> None:
        self._win_checker: TicTacToeWinChecker = win_checker

    def validate_grid_size(self, grid_size: int) -> None:
        if grid_size < 3:
            raise ValueError(
                f'Tic-tac-toe games must have grid size at least 3! (currently {grid_size})')
