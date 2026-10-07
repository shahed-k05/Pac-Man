# Actual Progress Tracking

## 1. Purpose

This document compares the planned development stages with the actual progress recorded in the GitHub repository.

The Git history was used as evidence because each development step was committed separately.

## 2. Progress Table

| Feature / Task | Planned Stage | Actual Progress | Status |
|---|---|---|---|
| Project setup | Foundation | Repository created and main branch established | Completed |
| Main game | Foundation | `main.py` and `pac-man.py` developed | Completed |
| Maze rendering | Foundation | `maze_render.py` implemented and improved | Completed |
| Player | Core Gameplay | `player.py` implemented | Completed |
| Pac-gums | Core Gameplay | `pacgum.py` implemented | Completed |
| Ghosts | Core Gameplay | `ghosts.py` implemented collaboratively | Completed |
| Random ghost movement | Core Gameplay | Implemented | Completed |
| BFS pathfinding | Advanced Gameplay | Implemented | Completed |
| Ghost personalities | Advanced Gameplay | Hunter, wanderer, and guard behavior implemented | Completed |
| Levels | Advanced Gameplay | Multiple levels and level numbers implemented | Completed |
| Lives | Advanced Gameplay | Lives and respawning implemented | Completed |
| Scoring | Advanced Gameplay | Pac-gum and ghost scoring implemented | Completed |
| Game Over | UI / Gameplay | Game Over screen and logic implemented | Completed |
| Win screen | UI / Gameplay | Win screen implemented | Completed |
| Main menu | UI | Menu implemented | Completed |
| Instructions | UI | Instructions screen implemented and later modified | Completed |
| Pause | UI | Pause screen implemented and corrected | Completed |
| High scores | UI / Data | Persistent Top 10 high scores implemented | Completed |
| Cheat Mode | Additional Feature | Cheat Mode implemented and fixed | Completed |
| Configuration validation | Quality | Pydantic configuration validation implemented | Completed |
| Custom collision class | Quality | `MyRect` implemented | Completed |
| Flake8 | Quality | Issues corrected | Completed |
| Seed handling | Quality | Seed behavior fixed | Completed |
| Docstrings | Documentation | Docstrings added to project classes/functions | Completed |
| README | Documentation | README updated | Completed |

## 3. Evidence from GitHub

The following commits demonstrate the progression:

- `main and high scores`
- `render`
- `pacgums, player, partitions`
- `Add instructions menu`
- `ghost with random movment`
- `just added bfs`
- `ghost movment and main`
- `speed`
- `level_num add`
- `game over, lives`
- `fineshed the Gameover screen`
- `pause screen`
- `maze colors again and lives heart`
- `added a cheat mode button and fixed the pause screen`
- `CheatMode`
- `changed the instraction screen and fixed the cheat mode`
- `readme`
- `did flake8 and fixed the seed`
- `fixed some flake8`
- `added a rect class so i can create my own collidepoint`
- `added duc string`

## 4. Actual Progress vs Initial Plan

The project did not follow a perfectly linear timeline. Some features were revisited after their initial implementation.

For example:

1. Ghost movement was implemented.
2. BFS was added.
3. Ghost movement and speed were subsequently modified.
4. Game Over was implemented.
5. Pause was implemented and later fixed.
6. Cheat Mode was implemented and subsequently fixed.
7. Code quality improvements were performed near the end.

This shows an iterative development process where testing led to additional corrections.

## 5. Final Progress

At the current stage, the major gameplay, interface, configuration, quality, and documentation requirements have been implemented.

The final development stage focused mainly on fixing issues, improving code quality, and documenting the code.