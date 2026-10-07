# Blocking Points and Conflicts

## 1. Purpose

This document records the main difficulties encountered during the development of the Pac-Man project and how the team addressed them.

## 2. Ghost Movement

Ghost movement was one of the more complex parts of the project.

The implementation evolved from random movement to more advanced behavior using BFS and different ghost personalities.

The team also had to correct:

- Ghost coordinates
- Spawn behavior
- Ghost speed
- Ghost scoring
- Collision behavior
- Level-dependent behavior

The Git history contains multiple commits related to these changes, demonstrating that the feature required several iterations.

## 3. Game Over and Lives

Game Over functionality was implemented progressively.

The team first worked on lives and then integrated them with:

- Ghost collisions
- Respawning
- Game Over
- Player name entry
- Score display
- High-score saving

This required coordination between several modules.

## 4. Pause Screen

The pause system required integration with the main game loop.

The pause functionality had to preserve the current game state while displaying the pause interface.

The team later modified the pause screen after its initial implementation, as shown by multiple pause-related commits.

## 5. Cheat Mode

Cheat Mode was an additional feature and required interaction with the existing gameplay system.

It supports:

- Invincibility
- Freezing ghosts
- Adding lives
- Skipping levels
- Pause
- Win/Game Over behavior
- High-score saving

Because Cheat Mode uses many existing game components, integration issues occurred and were corrected through subsequent commits.

## 6. Code Quality

Near the end of development, Flake8 identified code-quality problems.

The team addressed these issues through dedicated commits:

- `did flake8 and fixed the seed`
- `fixed some flake8`

Docstrings were also added afterward.

## 7. Custom Collision Handling

The team decided to introduce a custom `MyRect` class instead of directly relying on Pygame's collision method for menu buttons.

The class wraps a Pygame rectangle and provides its own `collidepoint()` method.

This was added late in the development process and integrated into the menu and pause functionality.

## 8. Configuration and Seed Issues

Configuration validation and maze generation required additional debugging.

The seed behavior was corrected near the end of development.

The configuration validator also provides defaults and validation for important game parameters.

## 9. How Blocking Points Were Managed

The general process for dealing with blockers was:

1. Reproduce the problem.
2. Identify the affected module.
3. Inspect the interaction with other components.
4. Apply a focused fix.
5. Run the relevant functionality again.
6. Check for regressions.
7. Commit the fix.

This process prevented unresolved problems from accumulating until the end of the project.

## 10. Conclusion

The project encountered several technical difficulties, particularly around ghost behavior, gameplay state management, pause functionality, Cheat Mode, configuration, and integration.

These issues were handled iteratively through debugging, testing, code changes, and Git commits.

The commit history therefore provides evidence not only of completed features but also of the problem-solving process used by the team.