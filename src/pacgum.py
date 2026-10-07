import sys
from dataclasses import dataclass
try:
    import pygame
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)
from src.maze_render import MazeRender


@dataclass
class Pacgum:
    """store the position and state of pacgum"""
    row: int
    col: int
    is_super: bool = False
    is_eaten: bool = False


class Pacgums:
    """manage all pacgums in the maze"""
    def __init__(
            self,
            maze: MazeRender,
            points_per_pacgum: int,
            points_per_super_pacgum: int, score: int) -> None:
        """create the pacgums and set their strting values"""
        self.maze = maze
        row = len(self.maze.maze)
        col = len(self.maze.maze[0])
        self.super_pacgum = [
            (0, 0), (0, col - 1), (row - 1, 0), (row - 1, col - 1)]
        self.pacgums = []
        self.p_pacgum = points_per_pacgum
        self.super_p_pacgum = points_per_super_pacgum
        self.score = score
        self.pacgum = 0
        self.eaten_pacgum = 0

        for row, cells in enumerate(self.maze.maze):
            for col, cell_value in enumerate(cells):
                if cell_value != 15:
                    if (row, col) in self.super_pacgum:
                        is_super = True
                    else:
                        is_super = False
                    self.pacgums.append(Pacgum(row, col, is_super))
                    self.pacgum += 1

    def eat(self, pacman_row: int, pacman_col: int) -> bool | None:
        """check if pacman eats a pacgum and update the score"""
        for pacgum in self.pacgums:
            if not pacgum.is_eaten:
                if pacgum.row == pacman_row and pacgum.col == pacman_col:
                    pacgum.is_eaten = True
                    if not pacgum.is_super:
                        self.score += self.p_pacgum
                    else:
                        self.score += self.super_p_pacgum
                    self.eaten_pacgum += 1
                    return pacgum.is_super
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """draw all uneaten pacgums on the screen"""
        for pacgum in self.pacgums:
            if pacgum.is_eaten:
                continue
            if pacgum.is_super:
                red = 7
                color = "#eb70b4"
            else:
                red = 3
                color = "#ffffff"
            pygame.draw.circle(
                screen,
                color,
                (
                    (
                        pacgum.col * self.maze.cell_size +
                        self.maze.margin_maze_col + (self.maze.cell_size//2)),
                    (
                        pacgum.row * self.maze.cell_size +
                        self.maze.margin_maze_row + (self.maze.cell_size//2))
                ),
                red
            )
