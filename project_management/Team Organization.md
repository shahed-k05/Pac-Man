# Team Organization

## 1. Team Members

The project was developed by two team members:

- **Shaden Shakhatreh**
- **Shahed Yassin**

Both members contributed to the development and integration of the project.

## 2. Division of Work

### Shaden Shakhatreh

Shaden was mainly responsible for:

- Cheat Mode
- Pause screen
- High-score functionality
- Main menu
- Custom `MyRect` class
- Configuration validator
- Docstrings
- Flake8 fixes
- Seed fixes
- Part of the ghost implementation

### Shahed Yassin

Shahed was mainly responsible for:

- Main game implementation
- Player implementation
- Pac-gums
- Maze rendering
- Game Over and Win screens
- HUD
- Main gameplay integration
- Visual and graphical improvements
- Other remaining project components

### Shared Work

The `ghosts.py` implementation was developed collaboratively.

Both team members also participated in:

- Debugging
- Testing
- Integration
- Fixing issues
- Reviewing changes

## 3. Decision Making

Technical decisions were made based on the requirements of the project and the problems encountered during implementation.

Examples include:

- Using BFS for hunter ghost pathfinding.
- Using Pydantic for configuration validation.
- Separating Cheat Mode into its own module.
- Creating a custom rectangle wrapper.
- Using JSON for persistent high scores.
- Separating rendering and gameplay responsibilities into different modules.

## 4. Issue Handling

When an issue was discovered, the team generally followed this process:

1. Identify the failing feature.
2. Locate the responsible module.
3. Modify the implementation.
4. Run the game or relevant checks.
5. Fix additional problems caused by integration.
6. Commit the change to Git.
7. Continue with the next feature.

The Git history demonstrates this iterative process through commits such as:

- `fixed spawn mode and ghost score and its movement`
- `fix cordinates`
- `fineshed the Gameover screen`
- `added a cheat mode button and fixed the pause screen`
- `changed the instraction screen and fixed the cheat mode`
- `did flake8 and fixed the seed`
- `fixed some flake8`

## 5. GitHub as Evidence

GitHub was used as the main version-control and progress-tracking system.

Each member's commits provide evidence of individual contributions while the shared repository provides evidence of integration between the two parts of the project.

## 6. Collaboration Model

The team used a shared repository and worked through incremental commits.

The work was divided by features, while components that required close interaction, particularly ghosts and gameplay integration, were handled collaboratively.