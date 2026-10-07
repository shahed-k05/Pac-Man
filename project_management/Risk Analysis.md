# Risk Analysis

## 1. Purpose

Risk analysis was used to identify technical and organizational problems that could affect the completion of the Pac-Man project.

## 2. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Ghost movement behaving incorrectly | High | High | Test movement separately and use BFS/pathfinding for hunter behavior |
| Changes breaking existing gameplay | High | High | Commit changes incrementally and test after major modifications |
| Integration conflicts between team members | Medium | High | Use Git and separate responsibilities between modules |
| Configuration containing invalid values | Medium | High | Validate configuration using Pydantic |
| Missing or invalid high-score file | Medium | Medium | Handle missing and invalid JSON and fall back to an empty list |
| External maze generator causing compatibility problems | Medium | High | Use `MazeAdapter` to isolate the dependency |
| Code quality problems | Medium | Medium | Run Flake8 and fix reported issues |
| Incorrect game state after player death | Medium | High | Track death state and recreate player/ghost objects after respawn |
| Cheat Mode affecting normal gameplay | Medium | High | Keep Cheat Mode in a separate module and provide explicit controls |
| Incorrect seed behavior | Medium | Medium | Test and correct seed handling before finalization |
| UI collision problems | Medium | Medium | Implement and test custom `MyRect.collidepoint()` |
| Documentation becoming outdated | Medium | Medium | Update README and add docstrings near the end of development |

## 3. Main Technical Risks

### Ghost and Player Interaction

Ghosts interact directly with the player's position. Incorrect movement or collision logic can affect lives, scoring, and Game Over behavior.

Mitigation included separate ghost modes, movement validation, collision checking, and BFS for the hunter.

### Level Transitions

Completing a level requires creating a new maze, player, pac-gums, and ghosts while preserving the score.

The `create_level()` function centralizes this process.

### Configuration

Invalid configuration values could cause runtime problems.

The Pydantic models validate configuration values and provide defaults when required.

### Git Integration

Because two developers worked on the same project, changes could overlap.

The team used Git commits to track changes and identify which developer introduced each change.

## 4. Risk Status

The major identified risks were addressed through implementation, debugging, testing, and repeated commits.

Some risks were discovered during development rather than before implementation. These were handled through corrective commits.