from .model import GridGameModel
from .view import View
from .project_types import Cell, Feedback, PlayerId, Symbol


class Controller:
    def __init__(self, model: GridGameModel, view: View):
        self._model = model
        self._view = view

    def start_game(self) -> None:
        model = self._model
        view = self

        while not model.is_game_over:
            while True:
                view.print_board(
                    model.grid_size,
                    model.occupied_cells,
                )

                view.print_current_player(model.current_player)

                choices = model.get_symbol_choices(model.current_player)
                symbol = (
                    view.ask_for_symbol_choice(choices) if len(choices) > 1 else
                    choices[0]
                )

                cell = view.ask_for_cell(model.grid_size)

                match model.place_symbol(symbol, cell):
                    case Feedback.VALID:
                        break

                    case Feedback.OUT_OF_BOUNDS:
                        view.print_error_out_of_bounds()

                    case Feedback.OCCUPIED:
                        view.print_error_occupied()

                    case Feedback.GAME_OVER:
                        view.print_error_game_over()

                view.print_divider()

        assert model.winner is not None

        view.print_board(model.grid_size, model.occupied_cells)
        view.print_winner(model.winner)

    def print_board(self, grid_size: int, occupied_cells: dict[Cell, Symbol]) -> None:
        for r in range(1, grid_size + 1):
            for c in range(1, grid_size + 1):
                cell = Cell(r, c)
                if (symbol := occupied_cells.get(cell)) is not None:
                    print(symbol, end='\t')
                else:
                    print('_', end='\t')

            print()

        print()

    def print_current_player(self, current_player: int) -> None:
        print(f'Turn of Player {current_player}')

    def print_divider(self) -> None:
        print('\n-----\n')

    def ask_for_symbol_choice(self, choices: list[Symbol]) -> Symbol:
        valid_choices = [str(c) for c in range(1, len(choices) + 1)]

        while True:
            print('Available symbols:')
            for n, symbol in enumerate(choices, start=1):
                print(f'- [{n}] {symbol}')

            choice = input(
                f'Enter number of symbol to play [1-{len(valid_choices)}]: ')

            if choice in valid_choices:
                return choices[int(choice) - 1]

            print('Invalid choice.')

    def ask_for_cell(self, grid_size: int) -> Cell:
        while True:
            try:
                row = int(input('Enter row: '))
                col = int(input('Enter col: '))

                if 1 <= row <= grid_size and 1 <= col <= grid_size:
                    return Cell(row, col)

                print(f'Coordinates must be within 1-{grid_size}. '
                      'Please try again.')

            except ValueError:
                pass

    def print_error_out_of_bounds(self) -> None:
        print('Invalid input; out of bounds. Please try again.')

    def print_error_occupied(self) -> None:
        print('Invalid input; cell is occupied. Please try again.')

    def print_error_game_over(self) -> None:
        print('Invalid input; game is already over.')

    def print_winner(self, winner: PlayerId) -> None:
        print(f'Player {winner} wins!')
