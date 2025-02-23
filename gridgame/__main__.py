import sys
import argparse

from gridgame.model import GridGameModel
from gridgame.view import View
from gridgame.controller import Controller


def setup_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--size', type=int, default=3)
    parser.add_argument(
        '--variant',
        choices=["tictactoe", "notakto", "wild", "pick15"],
    )

    return parser


def make_model(args: argparse.Namespace):
    match args.variant:
        case "tictactoe":
            return GridGameModel(
                grid_size=args.size,
                player_symbols=['X', 'O'],
            )

        case "notakto":
            raise NotImplementedError('notakto variant is not yet implemented')

        case "wild":
            raise NotImplementedError('notakto variant is not yet implemented')

        case "pick15":
            raise NotImplementedError('notakto variant is not yet implemented')

        case _:
            raise NotImplementedError(f'Variant "{args.variant}" is unknown')


def main():
    parser = setup_parser()
    args = parser.parse_args(sys.argv)

    model = make_model(args)
    view = View()
    controller = Controller(model, view)

    controller.start_game()


if __name__ == '__main__':
    main()
