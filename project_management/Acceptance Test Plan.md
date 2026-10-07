# Acceptance Test Plan

## 1. Purpose

The acceptance test plan defines the main features that should be tested before considering the Pac-Man project complete.

Testing focuses on gameplay, user interface, configuration, persistence, and additional functionality.

## 2. Functional Tests

| ID | Feature | Test | Expected Result | Status |
|---|---|---|---|---|
| AT-01 | Launch | Run `pac-man.py config.json` | Game starts and main menu appears | Passed |
| AT-02 | Main Menu | Select Start | Main game starts | Passed |
| AT-03 | High Scores | Open High Scores | Top scores are displayed | Passed |
| AT-04 | Instructions | Open Instructions | Instructions screen appears | Passed |
| AT-05 | Exit | Select Exit | Application exits | Passed |
| AT-06 | Player Movement | Press arrows/WASD | Pac-Man moves through valid paths | Passed |
| AT-07 | Walls | Move toward a wall | Player cannot move through walls | Passed |
| AT-08 | Pac-gums | Move over a pac-gum | Pac-gum disappears and score increases | Passed |
| AT-09 | Super Pac-gum | Eat a super pac-gum | Ghosts enter frightened mode | Passed |
| AT-10 | Ghost Movement | Start game | Ghosts move according to their modes | Passed |
| AT-11 | Hunter Ghost | Play against hunter | Hunter uses pathfinding toward player | Passed |
| AT-12 | Collision | Touch a dangerous ghost | Player loses a life | Passed |
| AT-13 | Ghost Respawn | Lose a life | Player and ghosts are recreated correctly | Passed |
| AT-14 | Levels | Eat all pac-gums | Next level loads | Passed |
| AT-15 | Final Level | Complete final level | Win screen appears | Passed |
| AT-16 | Lives | Lose all lives | Game Over screen appears | Passed |
| AT-17 | Name Entry | Enter player name | Name is displayed on result screen | Passed |
| AT-18 | High Score Save | Finish game | Score is saved to JSON | Passed |
| AT-19 | Top 10 | Add more than ten scores | Only top ten scores remain | Passed |
| AT-20 | Pause | Press Escape | Pause screen appears | Passed |
| AT-21 | Continue | Select Continue | Game resumes | Passed |
| AT-22 | Pause Exit | Select Exit | Game exits to the appropriate state | Passed |
| AT-23 | Cheat Mode | Open Cheat Mode | Cheat Mode starts | Passed |
| AT-24 | Invincibility | Press `I` | Player cannot lose lives normally | Passed |
| AT-25 | Freeze Ghosts | Press `F` | Ghost movement is disabled | Passed |
| AT-26 | Extra Life | Press `E` | Life is added when allowed | Passed |
| AT-27 | Skip Level | Press `L` | Current level is skipped | Passed |
| AT-28 | Configuration | Use valid JSON | Configuration is loaded | Passed |
| AT-29 | Invalid Configuration | Use invalid values | Validation/default behavior is triggered | Passed |
| AT-30 | Seed | Use configured seed | Maze generation follows configured seed behavior | Passed |
| AT-31 | Custom Rect | Click menu button | `MyRect.collidepoint()` correctly detects the click | Passed |
| AT-32 | Code Quality | Run `make lint` | Flake8 and mypy checks run successfully after fixes | Passed |

## 3. Error Handling Tests

The project was also tested against common error conditions.

### Missing Configuration

Expected behavior:
- The program detects that the required configuration argument is missing or unavailable.
- The error is reported instead of silently failing.

### Invalid JSON

Expected behavior:
- Configuration validation reports the problem.
- Default configuration behavior can be used where appropriate.

### Missing High-score File

Expected behavior:
- The game starts with an empty high-score list.
- A new file can be created when a score is saved.

### Invalid High-score Data

Expected behavior:
- Invalid JSON does not crash the high-score screen.
- The system falls back to an empty list.

## 4. Regression Testing

After major changes, previously implemented features were tested again.

Particular regression areas included:

- Ghost movement after BFS changes
- Pause behavior after UI changes
- Cheat Mode after gameplay changes
- Level transitions
- High-score saving
- Menu button collision
- Configuration and seed handling

## 5. Acceptance Criteria

The project can be considered accepted when:

- The game launches successfully.
- The main menu is functional.
- Player movement works.
- Pac-gums and scoring work.
- Ghosts move and interact with the player.
- Lives and Game Over work.
- Multiple levels work.
- The Win screen works.
- High scores persist.
- Pause works.
- Cheat Mode works.
- Configuration validation works.
- Code quality checks can be executed.
- Major functionality has been tested after integration.