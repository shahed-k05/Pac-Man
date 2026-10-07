import sys
from typing import List
try:
    import pygame
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)


class MazeRender:
    """draw and display the maze on the game screen"""
    def __init__(
        self, maze: List[List[int]], screen_width: int, screen_height: int
    ) -> None:
        """set up the maze and calculate its display position"""
        self.maze = maze
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.window_width = 740
        self.window_height = 780
        window_surface = pygame.image.load(
            'src/main/window.png').convert_alpha()
        self.window_rect = pygame.transform.scale(
            window_surface, (self.window_width, self.window_height))

        self.window_x = (self.screen_width - self.window_width) // 2
        self.window_y = 0

        maze_area_width = self.window_width - 180
        maze_area_height = self.window_height - 300
        rows = len(self.maze)
        cols = len(self.maze[0]) if len(self.maze) > 0 else 0
        self.cell_size = min(
            maze_area_width // cols,
            maze_area_height // rows
        )
        maze_width = cols * self.cell_size
        maze_height = rows * self.cell_size

        self.margin_maze_col = (
            self.window_x + (self.window_width - maze_width) // 2
        )  # pixel
        self.margin_maze_row = (
            self.window_y + 180
            + (maze_area_height - maze_height) // 2
        )

    def draw(self, screen: pygame.Surface, level: int) -> None:
        """draw the maze and its walls on the screen"""
        # Draw maze
        screen.blit(
            self.window_rect,
            (self.window_x, self.window_y)
        )
        for row, cells in enumerate(self.maze):
            for col, cell_value in enumerate(cells):
                if cell_value & 1:  # north
                    pygame.draw.line(
                        screen,
                        "#6800E8",
                        (
                            (col * self.cell_size) + self.margin_maze_col,
                            (row * self.cell_size) + self.margin_maze_row,
                        ),
                        (
                            (col * self.cell_size)
                            + self.margin_maze_col
                            + self.cell_size,
                            (row * self.cell_size) + self.margin_maze_row,
                        ), 3
                    )
                if cell_value & 2:  # east
                    pygame.draw.line(
                        screen,
                        "#6800E8",
                        (
                            (col * self.cell_size)
                            + self.margin_maze_col
                            + self.cell_size,
                            (row * self.cell_size) + self.margin_maze_row,
                        ),
                        (
                            (col * self.cell_size)
                            + self.margin_maze_col
                            + self.cell_size,
                            ((row * self.cell_size) + self.margin_maze_row)
                            + self.cell_size,
                        ), 3
                    )
                if row == len(self.maze) - 1 and cell_value & 4:  # south
                    pygame.draw.line(
                        screen,
                        "#6800E8",
                        (
                            (col * self.cell_size) + self.margin_maze_col,
                            ((row * self.cell_size) + self.margin_maze_row)
                            + self.cell_size,
                        ),
                        (
                            (col * self.cell_size)
                            + self.margin_maze_col
                            + self.cell_size,
                            ((row * self.cell_size) + self.margin_maze_row)
                            + self.cell_size,
                        ), 3
                    )
                if col == 0 and cell_value & 8:
                    pygame.draw.line(
                        screen,
                        "#6800E8",
                        (
                            (col * self.cell_size) + self.margin_maze_col,
                            (row * self.cell_size) + self.margin_maze_row,
                        ),
                        (
                            (col * self.cell_size) + self.margin_maze_col,
                            ((row * self.cell_size) + self.margin_maze_row)
                            + self.cell_size,
                        ), 3
                    )
                if (
                    cell_value & 1
                    and cell_value & 2
                    and cell_value & 4
                    and cell_value & 8
                ):
                    pygame.draw.rect(
                        screen,
                        "#AB089885",
                        (
                            (col * self.cell_size) + self.margin_maze_col,
                            (row * self.cell_size) + self.margin_maze_row,
                            self.cell_size,
                            self.cell_size,
                        )
                    )
                    if cell_value & 1:  # north
                        pygame.draw.line(
                            screen,
                            "#290552",
                            (
                                (col * self.cell_size) + self.margin_maze_col,
                                (row * self.cell_size) + self.margin_maze_row,
                            ),
                            (
                                (col * self.cell_size)
                                + self.margin_maze_col
                                + self.cell_size,
                                (row * self.cell_size) + self.margin_maze_row,
                            ), 4
                        )
                    if cell_value & 2:  # east
                        pygame.draw.line(
                            screen,
                            "#290552",
                            (
                                (col * self.cell_size)
                                + self.margin_maze_col
                                + self.cell_size,
                                (row * self.cell_size) + self.margin_maze_row,
                            ),
                            (
                                (col * self.cell_size)
                                + self.margin_maze_col
                                + self.cell_size,
                                ((row * self.cell_size) + self.margin_maze_row)
                                + self.cell_size,
                            ), 4
                        )
                    if cell_value & 4:  # south
                        pygame.draw.line(
                            screen,
                            "#290552",
                            (
                                (col * self.cell_size) + self.margin_maze_col,
                                ((row * self.cell_size) + self.margin_maze_row)
                                + self.cell_size,
                            ),
                            (
                                (col * self.cell_size)
                                + self.margin_maze_col
                                + self.cell_size,
                                ((row * self.cell_size) + self.margin_maze_row)
                                + self.cell_size,
                            ), 4
                        )
                    if cell_value & 8:
                        pygame.draw.line(
                            screen,
                            "#8547D1",
                            (
                                (col * self.cell_size) + self.margin_maze_col,
                                (row * self.cell_size) + self.margin_maze_row,
                            ),
                            (
                                (col * self.cell_size) + self.margin_maze_col,
                                ((row * self.cell_size) + self.margin_maze_row)
                                + self.cell_size,
                            ), 4
                        )
