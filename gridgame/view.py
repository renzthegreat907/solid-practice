from .project_types import Cell, PlayerId, Symbol


class View:
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

    def print_error_invalid_symbol(self) -> None:
        print('Invalid symbol. Please try again.')

    def print_winner(self, winner: PlayerId) -> None:
        print(f'Player {winner} wins!')
