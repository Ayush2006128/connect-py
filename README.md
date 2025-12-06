# Connect-Py

**Connect-Py** is a classic Connect 4 game implementation built with Python, [Pygame](https://www.pygame.org/), and [NumPy](https://numpy.org/). It features a fully interactive graphical interface, local 2-player support, and robust game logic.

## Features
- **Classic Gameplay**: Standard 6x7 grid with gravity-based piece dropping.
- **Local Multiplayer**: Play against a friend on the same machine.
- **Interactive UI**: Mouse-controlled piece placement with real-time hovering.
- **Win Detection**: Automatically detects wins (horizontal, vertical, diagonal) and announces the winner.
- **Restart Functionality**: Click anywhere after a game ends to instantly reset the board.

## Prerequisites
- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) OR standard `pip`

## Installation & Running

### Using uv (Recommended)
This project is managed with `uv`. To run it immediately with all dependencies handled:

```sh
uv run main.py
```

### Using pip
If you prefer standard pip, install the required dependencies first:

```sh
pip install pygame numpy
```

Then run the game:

```sh
python main.py
```

## How to Play
1.  **Launch the game.**
2.  **Player 1 (Blue)** starts first.
3.  **Move your mouse** horizontally across the top of the window to position your chip.
4.  **Click** the left mouse button to drop the chip into the selected column.
5.  **Player 2 (Yellow)** takes the next turn.
6.  The first player to connect **4 chips** in a row (horizontally, vertically, or diagonally) wins!
7.  **Click anywhere** on the screen after a win to restart the game.

## Project Structure
- `main.py`: The entry point. Handles the main game loop, input processing, and game coordination.
- `board.py`: Contains the `Board` class, managing the game state (grid), move validation, and win algorithms.
- `ui.py`: Handles all Pygame rendering, including the board, pieces, and text.

## Tests
Unit tests have been implemented for the core game logic, primarily focusing on the `Board` class.
To run the tests, navigate to the project root directory and execute:

```sh
PYTHONPATH=. .venv/bin/pytest
```

## Citations
- **BigBlueTerm Nerd Font**: Used for its retro aesthetic.

## License
This project is licensed under the GPL 3 License. See the `LICENSE` file for details.

