# CS 12 24.2 Lab 5 Practice

## Overview

_Notakto_, _Wild Tic-Tac-Toe_, and _Pick15_ are games very similar to _Tic-Tac-Toe_–they are played on a 2D grid with two or more players taking turns placing symbols, but have variations in certain game mechanics that make them distinct.

### Wild Tic-Tac-Toe

_Wild Tic-Tac-Toe_ is a variant of Tic-Tac-Toe where players can _choose which symbol to play_ for their turn. If the player forms a complete row, column, or main diagonal with any symbol, they are considered to be the winner.

### Notakto

_Notakto_ is Tic-Tac-Toe, but with only _one symbol_ shared by all players. The player who forms a complete row, column, or main diagonal _loses_.

To keep the rules simple for multiple players, we will take the winner to be the player who last placed a symbol when a loser is first determined.

### Pick15

_Pick15_ is Tic-Tac-Toe played with the numbers `1` to `9` _(for a $`3 \times 3`$ grid)_. Each number can be played by any player, but only once. The first player who is able to form a complete row, column, or diagonal summing up to `15` _(for a $`3 \times 3`$ grid)_ is the winner, regardless of who played the other numbers in the winning sequence.

For an $n \times n$ grid, numbers that be played are `1` to $n^2$ with the goal of having a complete row, column or diagonal summing up to $\displaystyle \frac{n(n^2 + 1)}{2}$.

## Task

The repository contains a complete MVC-based implementation of Tic-Tac-Toe. Command line arguments are used to specify parameters of the game.

The following command starts a game of two-player Tic-Tac-Toe on a $3 \times 3$ grid with `X` and `O` as symbols for Players 1 and 2 respectively:

```bash
python3 -m gridgame -n 3 -p 2 --variant tictactoe --symbols X,O
```

The given model code in `model.py` is an implementation of _Tic-Tac-Toe_.

Refactor the given code and extend it with support for the _Wild Tic-Tac-Toe_, _Notakto_, and _Pick15_ game variants while retaining support for _Tic-Tac-Toe_.

Note that the given view and controller are already set up to accommodate the variants–you only have to refactor `model.py`.

### Subtask #1: Refactoring for OCP compliance

Refactor `GridGameModel` in such a way that:

- Externalizes the win condition logic
- Externalizes the management of valid symbols to be played

You will likely need to create a common interface for the objects representing the externalized logic–subtype polymorphism is the key to creating OCP-compliant code.

Upon doing so, create a class that implements the newly created interface. This class should reflect the mechanics of Tic-Tac-Toe.

Then, modify the `tictactoe` case in `make_model` of `gridgame/__main__.py` by instantiating the newly created class and using it when initializing `GridGameModel`–this should create a `GridGameModel` object that simulates Tic-Tac-Toe.

Ensure that broken unit tests are fixed so that 100% code coverage is retained for the model.

You may test your work manually via the following command:

```bash
python3 -m gridgame -n 3 -p 2 --variant tictactoe --symbols X,O
```

### Subtask #2: Adding of new variants without editing existing code

As you have done for the `tictactoe` case, do the same for all the other variants.

Ensure that:

1. Your code in Subtask #1 is not modified in any way _(i.e., it is OCP-compliant relative to the game variants being introduced)_
1. Your added code has 100% code coverage
1. `notakto` raises an exception if more than one symbol is supplied
1. `pick15` raises an exception if any symbol is supplied

You may test your work manually via the following commands:

```bash
python3 -m gridgame -n 3 -p 2 --variant wild --symbols X,O
python3 -m gridgame -n 3 -p 3 --variant notakto --symbols X
python3 -m gridgame -n 3 -p 2 --variant pick15
```
