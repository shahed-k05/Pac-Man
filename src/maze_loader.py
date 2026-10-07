from mazegenerator import MazeGenerator
from typing import List


class MazeAdapter:
    """adapt the maze generator to provide the generated maze"""
    def __init__(self, mazegen: MazeGenerator) -> None:
        """store the maze generator"""
        self.maze_class_loader = mazegen

    def get_maze(self) -> List[List[int]]:
        """return the generated maze"""
        maze: List[List[int]] = self.maze_class_loader.maze
        return maze
