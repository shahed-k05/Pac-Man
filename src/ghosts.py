from dataclasses import dataclass
import sys
import random
from enum import Enum
from typing import List, Tuple
try:
    import pygame
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)
from src.maze_render import MazeRender


class Mode(Enum):
    """store the different ghost mode"""
    CHASE = 1  # the ghosts actively hunt down pacman.
    FRIGHTEND = 2  # Triggered when pacman eats a super pacgum.
    SPAWN = 3  # The state a ghost enters after being eaten.
    WANDER = 4  # the ghost moves randomly


@dataclass
class Ghost:
    """store the data of one ghost"""
    color: str
    col: int
    row: int
    size: int
    mode: Mode
    personality: str
    last_move: int = 0
    move_delay: int = 200
    last_position: tuple[int, int] | None = None
    area: tuple[int, int, int, int] = (0, 0, 0, 0)
    home: tuple[int, int] | None = None
    respawn_at: int = 0
    frightened_until: int = 0
    pre_mode: Mode | None = None
    frightend: int = 0
    speed: float = 1.0
    progress: float = 0.0
    target: tuple[int, int] | None = None

    @property
    def img_load(self) -> pygame.Surface:
        """Load and resize the ghost image"""
        ghost_Surface = pygame.image.load(
            f"src/Graphics/{self.color}.png").convert_alpha()
        return pygame.transform.scale(ghost_Surface, (self.size, self.size))


class Ghosts:
    """control all ghost in the game"""
    def __init__(
        self,
        maze: MazeRender,
        lives: int,
        points_per_ghost: int
                ) -> None:
        """create the ghost and set their starting positiong"""
        self.maze = maze
        mid_row = len(self.maze.maze) // 2
        mid_col = len(self.maze.maze[0]) // 2
        self.ghost_score = 0
        self.points_per_ghost = points_per_ghost
        self.area = [
            (0, mid_row - 1, 0, mid_col - 1),
            (0, mid_row - 1, mid_col, len(self.maze.maze[0]) - 1),
            (mid_row, len(self.maze.maze) - 1, 0, mid_col - 1),
            (
                mid_row,
                len(self.maze.maze) - 1,
                mid_col, len(self.maze.maze[0]) - 1)
        ]
        self.frightend = 0

        personalities: list[str] = [
            "hunter",
            "wanderer",
            "guard",
            "wanderer",
        ]
        self.reborn = 0
        self.lives = lives
        colors: list[str] = ["red", "green", "pink", "yellow"]
        self.ghost = []
        self.coordinates = [
            (0, 1),
            (1, len(self.maze.maze[0]) - 1),
            (len(self.maze.maze) - 1, 1),
            (len(self.maze.maze) - 1, len(self.maze.maze[0]) - 2),
        ]
        for color, (row, col), personality, area in zip(
            colors,
            self.coordinates,
            personalities,
            self.area
                                                        ):
            self.ghost.append(
                Ghost(
                    color=color,
                    col=col,
                    row=row,
                    size=self.maze.cell_size,
                    mode=Mode.CHASE,
                    personality=personality,
                    last_move=0,
                    move_delay=200,
                    area=area,
                    home=(row, col)
                )
            )
        scared_ghost = pygame.image.load(
            "src/Graphics/scared.png").convert_alpha()
        self.scared_ghost_rect = pygame.transform.scale(
            scared_ghost, (self.maze.cell_size, self.maze.cell_size))

    def draw(self, screen: pygame.Surface) -> None:
        """Draw all ghosts on the screen"""
        for ghost in self.ghost:
            if ghost.mode == Mode.SPAWN:
                continue
            if ghost.mode == Mode.FRIGHTEND:
                img = self.scared_ghost_rect
            else:
                img = ghost.img_load
            screen.blit(img, self.pixel_pos(ghost))

    def valid_moves(
        self,
        ghost: Ghost,
        restrict_area: bool = True
                    ) -> List[Tuple[int, int]]:
        """return the possible moves for a ghost"""
        valid_moves = []
        cell_value = self.maze.maze[ghost.row][ghost.col]
        if ghost.col + 1 < len(self.maze.maze[0]) and not (cell_value & 2):
            valid_moves.append((ghost.row, ghost.col + 1))
        if ghost.col - 1 >= 0 and not (cell_value & 8):
            valid_moves.append((ghost.row, ghost.col - 1))
        if ghost.row - 1 >= 0 and not (cell_value & 1):
            valid_moves.append((ghost.row - 1, ghost.col))
        if ghost.row + 1 < len(self.maze.maze) and not (cell_value & 4):
            valid_moves.append((ghost.row + 1, ghost.col))
        if not restrict_area:
            return valid_moves
        moves = []
        min_row, max_row, min_col, max_col = ghost.area
        if not (
            min_row <= ghost.row <= max_row
            and min_col <= ghost.col <= max_col
                ):
            return valid_moves
        for row, col in valid_moves:
            if (
                0 <= row < len(self.maze.maze)
                and 0 <= col < len(self.maze.maze[0])
                and min_row <= row <= max_row
                and min_col <= col <= max_col
            ):
                moves.append((row, col))

        return moves or valid_moves

    def random_mode(self, ghost: Ghost) -> None:
        """move the ghost to a random valid position"""
        moves = self.valid_moves(ghost)
        if not moves:
            return
        if len(moves) > 1 and ghost.last_position in moves:
            moves.remove(ghost.last_position)
        ghost.last_position = (ghost.row, ghost.col)
        next_move = random.choice(moves)
        ghost.row, ghost.col = next_move

    def find_player(
        self,
        ghost: Ghost,
        player_row: int,
        player_col: int
                    ) -> List[Tuple[int, int]]:
        """used BFS to find shortest path from the ghost to pacman"""
        start = (ghost.row, ghost.col)
        target = (player_row, player_col)
        if start == target:
            return []
        queue = [start]
        visited: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        temp_ghost = Ghost(
                color=ghost.color,
                col=start[1],
                row=start[0],
                size=ghost.size,
                mode=ghost.mode,
                personality=ghost.personality,
                area=ghost.area
            )
        while queue:
            if target in visited:
                break
            current = queue.pop(0)
            temp_ghost.row, temp_ghost.col = current
            for move in self.valid_moves(
                temp_ghost,
                restrict_area=ghost.personality != "hunter"
                                        ):
                if move not in visited:
                    visited[move] = current
                    queue.append(move)
        if target not in visited:
            return []
        path = []
        current = target
        while current != start:
            path.append(current)
            previous = visited[current]
            if previous is None:
                break
            current = previous
        path.reverse()
        return path

    def check_collisions(
        self,
        ghost: Ghost,
        playr_cordinates: Tuple[int, int]
                        ) -> None:
        """check if a ghost touches pacman"""
        ghost_cordinates = (ghost.row, ghost.col)
        if ghost_cordinates != playr_cordinates:
            return
        if ghost.mode == Mode.FRIGHTEND:
            self.eat_ghost(ghost)
        elif ghost.mode == Mode.WANDER or ghost.mode == Mode.CHASE:
            self.lives -= 1
            self.reborn = 1

    def chase_mode(self, ghost: Ghost, px: int, py: int) -> None:
        """moiving the ghost toword the """
        path = self.find_player(ghost, px, py)
        if path:
            ghost.row, ghost.col = path[0]
        else:
            self.random_mode(ghost)
        self.check_collisions(ghost, (px, py))

    def set_level(self, level: int) -> None:
        """set ghost speed and mode for the currnet level"""
        self.level = level
        delays = {
            1: 350,
            2: 350,
            3: 300,
            4: 280,
            5: 250,
            6: 220,
            7: 200,
            8: 180,
            9: 150,
            10: 120,
        }
        speeds = {
            1: 1.0,
            2: 1.0,
            3: 1.2,
            4: 1.3,
            5: 1.4,
            6: 1.5,
            7: 1.6,
            8: 1.7,
            9: 1.8,
            10: 2.0,
        }
        speed = speeds.get(level, 2.0)
        for ghost in self.ghost:
            ghost.speed = speed

        delay = delays.get(level, 120)
        for ghost in self.ghost:
            ghost.move_delay = delay
            if ghost.personality == "hunter":
                ghost.mode = Mode.CHASE
            elif ghost.personality == "wanderer":
                if level >= 7:
                    ghost.mode = Mode.CHASE
                else:
                    ghost.mode = Mode.WANDER
            elif ghost.personality == "guard":
                if level >= 4:
                    ghost.mode = Mode.CHASE
                else:
                    ghost.mode = Mode.WANDER

    def pixel_pos(self, ghost: Ghost) -> Tuple[int, int]:
        """screen position of a ghost, including the slide between cells"""
        cell = self.maze.cell_size
        x = ghost.col * cell + self.maze.margin_maze_col
        y = ghost.row * cell + self.maze.margin_maze_row
        if ghost.target is not None:
            t_row, t_col = ghost.target
            x += (t_col - ghost.col) * ghost.progress
            y += (t_row - ghost.row) * ghost.progress
        return int(x), int(y)

    def slide(self, ghost: Ghost) -> None:
        """advance the ghost `speed` pixels toward its target cell"""
        if ghost.target is None:
            return
        ghost.progress = min(
            self.maze.cell_size, ghost.progress + ghost.speed)
        if ghost.progress >= self.maze.cell_size:
            ghost.row, ghost.col = ghost.target
            ghost.target = None
            ghost.progress = 0

    def frightend_mode(self, ghost: Ghost, px: int, py: int) -> None:
        """Move the ghost away from pacman"""
        ghost.frightend = 1
        moves = self.valid_moves(ghost, restrict_area=False)
        if not moves:
            return
        if len(moves) > 1 and ghost.last_position in moves:
            moves.remove(ghost.last_position)
        next_move = max(
            moves,
            key=lambda move: (
                abs(move[0] - px) + abs(move[1] - py)
            )
        )
        ghost.last_position = (ghost.row, ghost.col)
        ghost.row, ghost.col = next_move
        self.check_collisions(ghost, (px, py))

    def scared_ghost(self) -> None:
        """make all ghost scared for a few secondes"""
        current_time = pygame.time.get_ticks()
        for ghost in self.ghost:
            if ghost.mode != Mode.SPAWN:
                if ghost.mode != Mode.FRIGHTEND:
                    ghost.pre_mode = ghost.mode
                ghost.mode = Mode.FRIGHTEND
                ghost.frightened_until = current_time + 7000

    def spawn_mode(self, ghost: Ghost) -> None:
        """retun an eaten ghost to its home position"""
        current_time = pygame.time.get_ticks()
        if current_time < ghost.respawn_at:
            return
        if ghost.home is None:
            return
        if ghost.home is None:
            return
        ghost.row, ghost.col = ghost.home
        ghost.mode = ghost.pre_mode or Mode.CHASE
        ghost.pre_mode = None
        ghost.last_position = None
        ghost.last_move = current_time

    def eat_ghost(self, ghost: Ghost) -> None:
        """send a ghost to a spwan mode after pacman eats it"""
        ghost.mode = Mode.SPAWN
        ghost.respawn_at = pygame.time.get_ticks() + 3000
        ghost.last_position = None
        self.ghost_score += self.points_per_ghost

    def move(self, player_row: int, player_col: int) -> None:
        """move all ghost based on their mode"""
        current_time = pygame.time.get_ticks()
        for ghost in self.ghost:
            self.check_collisions(ghost, (player_row, player_col))
        for ghost in self.ghost:
            if ghost.mode == Mode.SPAWN:
                ghost.target = None
                ghost.progress = 0
                self.spawn_mode(ghost)
                continue
            if (
                ghost.mode == Mode.FRIGHTEND
                and current_time >= ghost.frightened_until
            ):
                ghost.mode = ghost.pre_mode or Mode.CHASE
                ghost.pre_mode = None

            if ghost.target is None:
                old = (ghost.row, ghost.col)
                if ghost.mode == Mode.CHASE:
                    self.chase_mode(ghost, player_row, player_col)
                elif ghost.mode == Mode.WANDER:
                    self.random_mode(ghost)
                elif ghost.mode == Mode.FRIGHTEND:
                    self.frightend_mode(ghost, player_row, player_col)
                new = (ghost.row, ghost.col)
                ghost.row, ghost.col = old
                if new != old:
                    ghost.target = new
                    ghost.progress = 0

            self.slide(ghost)
