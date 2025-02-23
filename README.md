# CS 12 24.2 Lab 5 Practice

## Overview

_Notakto_, _Wild Tic-tac-toe_, and _Pick15_ are games very similar to _Tic-tac-toe_–they are played on a 2D grid with players taking turns placing symbols, but they introduce variations in certain aspects of the game mechanics of Tic-tac-toe.

### Notakto

_Notakto_ is Tic-tac-toe, but with only one symbol shared by all players. The player who forms a complete row, column, or main diagonal _loses_.

To keep the rules simple for multiple players, we will take the winner to be the player who took placed a symbol right before a loser is first determined.

### Wild Tic-tac-toe

_Wild Tic-tac-toe_ is a variant of Tic-tac-toe where players can choose which symbol to play for their turn. If the player forms a complete row, column, or main diagonal with any symbol, they are considered to be the winner.

### Pick15

_Pick15_ is Tic-tac-toe played with the numbers `1` to `9` _(for a $3 \times 3$ grid)_. Each number can be played by any player, but only once. The first player who is able to form a complete row, column, or diagonal summing up to `15` _(for a $3 \times 3$ grid)_ is the winner.

For an $n \times n$ grid, numbers that be played are `1` to $n^2$ with the goal of having a complete row, column or diagonal summing up to $\frac{n(n^2 + 1)}{2}$.

## Task

The given model code in `model.py` is an implementation of _Tic-tac-toe_.

Refactor the given code and extend it with support for the _Notakto_, _Wild Tic-tac-toe_, and _Pick15_ game variants while retaining support for _Tic-tac-toe_.

### Subtask #1: Defining the `View`

Create `gridgame/view.py` and a `View` class for the existing model in `model.py` that could accommodate all the Tic-tac-toe variants listed above.

Ensure that the view can accommodate the following:

- Showing of which symbols the player can choose _(if the variant normally gives the player a choice)_
- Repeatedly asking the current player which symbol to play until a valid symbol is entered _(if applicable)_

### Subtask #2: Defining the `Controller`

Create `gridgame/controller.py` and a `Controller` class compatible with `View` and `GridGameModel`

Ensure that the controller:

- Takes in `GridGameModel` object as the first argument of its initializer
- Takes in a `View` object as the second argument of its initializer
- Has a method called `start_game() -> None` which serves as the entrypoint of the game

If done correctly, `gridgame/__main__.py` should not have Pyright errors and that the following command will start running the Tic-tac-toe game with a $3 \times 3$ grid:

```bash
python3 -m gridgame -n 3 --variant tictactoe
```

### Subtask #3: Refactoring for OCP compliance

Refactor `GridGameModel` in such a way that:

- Externalizes the win condition logic
- Externalizes the management of valid symbols to be played

It may also help to create a common interface for the objects representing the externalized logic.

Ensure that broken unit tests are fixed so that 100% code coverage is retained for the model.

### Subtask #4: Adding of new variants without editing existing code

Using your common interface, create implementing classes for each Tic-tac-toe variant _(as well as for Tic-tac-toe itself)_.

Ensure that:

1. Your code in Subtask #3 is not modified in any way _(i.e., it is OCP-compliant relative to the game variants being introduced)_
1. Your added code has 100% code coverage

You may test your work manually via the following:

```bash
python3 -m gridgame -n 3 --variant tictactoe
python3 -m gridgame -n 3 --variant notakto
python3 -m gridgame -n 3 --variant wild
python3 -m gridgame -n 3 --variant pick15
```
