# Project Analysis

## 1. Project Objective

The objective was to develop a configurable Pac-Man-style game with multiple levels, ghosts, scoring, lives, persistent high scores, menus, pause functionality, a Game Over screen, a Win screen, and an additional Cheat Mode.

The project was implemented in Python using Pygame.

## 2. Main Technical Choices

### Python and Pygame

Python was selected as the main programming language, with Pygame used for:

- Window management
- Keyboard and mouse input
- Rendering
- Images
- Fonts
- Game timing
- Game events

This allowed the team to focus on game logic while using an existing framework for graphical functionality.

### Maze Generator

The project uses an external maze generator package rather than implementing maze generation from scratch.

A `MazeAdapter` class was introduced to separate the external maze generator from the rest of the game.

This reduces dependency on the exact interface of the external package.

### Pydantic Configuration

The configuration is validated through Pydantic models.

`config_validator.py` is responsible for:

- Validating level numbers
- Validating maze dimensions
- Validating lives
- Validating scoring values
- Validating the seed
- Providing default levels
- Reading JSON configuration files

This provides a controlled configuration system instead of relying directly on raw JSON values.

### BFS for Ghosts

Breadth-First Search was selected for the hunter ghost because it can find a shortest path through the maze.

This gives the hunter ghost more predictable behavior than purely random movement.

Other ghosts use different movement behaviors to create variety.

### Persistent High Scores

High scores are stored in `highscore.json`.

The system:

1. Reads existing scores.
2. Adds the current player's score.
3. Sorts scores from highest to lowest.
4. Keeps the top ten entries.
5. Writes the result back to the file.

### Custom `MyRect`

A custom `MyRect` wrapper was introduced to provide collision checking through the project's own `collidepoint` implementation.

The class also forwards other rectangle attributes through `__getattr__`.

## 3. Design Decisions

The project separates responsibilities into multiple files.

Examples include:

- `player.py` — Player behavior
- `pacgum.py` — Pac-gum behavior
- `ghosts.py` — Ghost behavior
- `maze_render.py` — Maze rendering
- `maze_loader.py` — Maze adaptation
- `hud.py` — Score, level, and lives display
- `gameover.py` — Win/Game Over screens
- `pause.py` — Pause screen
- `highscore.py` — High-score persistence
- `config_validator.py` — Configuration validation
- `cheat.py` — Cheat Mode
- `menu.py` — Main menu and navigation

This modular structure makes individual features easier to modify and debug.

## 4. Iterative Development

The team did not attempt to complete the entire game in a single implementation.

Features were introduced gradually and then revisited when problems appeared.

For example, Cheat Mode was initially implemented and later fixed. The pause screen was also implemented and subsequently modified.

This allowed the team to respond to problems discovered during development.

## 5. Code Quality

Near the end of development, the team focused on code quality by:

- Running Flake8
- Fixing Flake8 issues
- Adding docstrings
- Fixing seed behavior
- Creating a custom rectangle class
- Updating the README

The Makefile also provides commands for installation, running, debugging, linting, virtual environment creation, and cleaning generated files.

## 6. Analysis of the Final Approach

The final architecture is based on separation of responsibilities, incremental implementation, reusable classes, configuration validation, and repeated testing.

The main advantage of this approach was that changes could be isolated to specific modules.

The main challenge was integration: changes in one component could affect another component, particularly the interaction between the maze, player, ghosts, levels, and Cheat Mode.

The team addressed these issues through repeated debugging and Git commits.