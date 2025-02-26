import argparse

from .view import View
from .controller import Controller

from .model import (
    GridGameModel,
    )

from .tictactoe import (
    TicTacToeSymbolAndPlayerHandler,
    TicTacToeWinChecker,
    TicTacToeSettingInitializer,
    )

from .notakto import (
    NotaktoSettingInitializer,
    NotaktoSymbolAndPlayerHandler,
    NotaktoWinChecker,
    )

def str_list(line: str) -> list[str]:
    return line.split(',')

def setup_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--size', type=int, default=3)
    parser.add_argument('-p', '--player_count', type=int, default=2)
    parser.add_argument(
        '--variant',
        choices=["tictactoe", "notakto", "wild", "pick15"],
        required=True,
    )
    parser.add_argument('-s', '--symbols', type=str_list, default=[])

    return parser


def make_model(args: argparse.Namespace):

    size = args.size
    player_count = args.player_count
    player_symbols = args.symbols

    match args.variant:
        case "tictactoe":

            symbol_and_player_handler = TicTacToeSymbolAndPlayerHandler
            win_checker = TicTacToeWinChecker
            gamemode = TicTacToeSettingInitializer

        case "notakto":
            # raise NotImplementedError('notakto variant is not yet implemented')
            
            symbol_and_player_handler = NotaktoSymbolAndPlayerHandler
            win_checker = NotaktoWinChecker
            gamemode = NotaktoSettingInitializer


        case "wild":
            raise NotImplementedError('wild variant is not yet implemented')

        case "pick15":
            raise NotImplementedError('pick15 variant is not yet implemented')

        case _:
            raise NotImplementedError(f'Variant "{args.variant}" is unknown')

    return GridGameModel(
        size,
        player_symbols,
        player_count,
        symbol_and_player_handler,
        win_checker,
        gamemode
        )


def main():
    parser = setup_parser()
    args = parser.parse_args()

    model = make_model(args)
    view = View()
    controller = Controller(model, view)

    controller.start_game()


if __name__ == '__main__':
    main()