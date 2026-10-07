import sys
from typing import Any
from src.main import create_level
from src.config_validator import read_config
from src.hud import HUD
from src.gameover import GameOver
from src.pause import paused_screen
from src.highscore import save_highscore
try:
    import pygame
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)


class CheatMode:
    """Control the cheat mode of the Pac-Man game"""
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.screen_w, self.screen_h = screen.get_size()
        self.invincible = False
        self.freeze_ghosts = False
        self.paused = False
        self.running = True
        self.win = False
        self.game_over = False
        self.level_index = 0
        self.player_name = ""
        self.score = 0
        self.death_time: int | None = None

    def load_level(self, config: Any) -> None:
        """Load the current level"""
        (
            self.level,
            self.maze,
            self.maze_render,
            self.pacman,
            self.gum,
            self.ghost,
            self.counter
        ) = create_level(
            config,
            self.level_index,
            self.screen_w,
            self.screen_h,
            self.score,
            0
        )
        self.score = self.gum.score

    def skip_level(self, config: Any) -> None:
        """Skip the level"""
        self.level_index += 1
        if self.level_index < len(config.level):
            self.load_level(config)
        else:
            self.win = True

    def handle_keys(self, event: Any, config: Any) -> None:
        """Handle cheat mode keyboard controls"""
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_i:
            self.invincible = not self.invincible
        elif event.key == pygame.K_f:
            self.freeze_ghosts = not self.freeze_ghosts
        elif event.key == pygame.K_e:
            if self.ghost.lives < 3:
                self.ghost.lives += 1
        elif event.key == pygame.K_l:
            self.skip_level(config)

    def run(self) -> None:
        """Run the cheat mode game loop"""
        pygame.init()
        config = read_config(sys.argv[1])
        self.config = config
        self.load_level(config)
        background_game = pygame.image.load(
            'src/main/game_background.jpg').convert_alpha()
        background_game = pygame.transform.scale(
            background_game, (self.screen_w, self.screen_h))
        background_game.set_alpha(150)
        hud = HUD(
            self.maze_render.window_x,
            self.maze_render.window_y,
        )
        game_over_screen = GameOver(
            self.screen_w,
            self.screen_h,
        )
        base_font_game_over = pygame.font.Font(
            "src/main/pixel-game.regular.otf",
            45
            )
        clock = pygame.time.Clock()
        font = pygame.font.Font("src/main/pixel-game.regular.otf", 30)
        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(background_game, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_ESCAPE
                        and not self.game_over
                        and not self.win
                    ):
                        self.paused = not self.paused
                    elif self.game_over or self.win:
                        if event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif event.key == pygame.K_RETURN:
                            save_highscore(
                                self.player_name,
                                self.gum.score
                            )
                            self.running = False
                        elif (
                            len(self.player_name) < 10
                            and (
                                event.unicode.isalnum() or event.unicode == " "
                            )
                        ):
                            self.player_name += event.unicode
                    elif not self.paused and not self.game_over:
                        self.handle_keys(
                            event,
                            config,
                        )
            if self.paused:
                self.maze_render.draw(
                    self.screen,
                    self.level.level_num
                )
                self.pacman.draw(self.screen)
                self.gum.draw(self.screen)
                self.ghost.draw(self.screen)
                hud.draw(
                    self.screen,
                    score=self.gum.score,
                    lives_num=self.ghost.lives,
                    level=self.ghost.level,
                    pos=(
                        self.maze_render.margin_maze_row,
                        self.maze_render.margin_maze_col
                    ),
                    base_font=font
                )
                result = paused_screen(self.screen)
                if result == "continue":
                    self.paused = False
                elif result == "exit":
                    return
                pygame.display.flip()
                continue
            if self.game_over:
                player_surface = base_font_game_over.render(
                    self.player_name,
                    True,
                    (255, 255, 255)
                )
                score_surface = base_font_game_over.render(
                    str(self.gum.score),
                    True,
                    (255, 255, 255)
                )
                game_over_screen.generate(
                    self.screen, player_surface, score_surface, "gameover"
                )
                pygame.display.flip()
                continue
            if self.win:
                player_surface = base_font_game_over.render(
                        self.player_name,
                        True,
                        (255, 255, 255)
                    )
                score_surface = base_font_game_over.render(
                    str(self.gum.score),
                    True,
                    (255, 255, 255)
                )

                game_over_screen.generate(
                    self.screen, player_surface, score_surface, "win"
                )
                pygame.display.flip()
                continue
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.pacman.dir = "right"
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.pacman.dir = "left"
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.pacman.dir = "up"
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.pacman.dir = "down"
            self.maze_render.draw(
                self.screen,
                self.level.level_num
            )
            self.pacman.draw(self.screen)
            self.gum.draw(self.screen)
            self.ghost.draw(self.screen)
            if self.death_time is None:
                self.pacman.move()

                is_super = self.gum.eat(
                    self.pacman.row,
                    self.pacman.col
                )
                if is_super:
                    self.ghost.scared_ghost()
                old_lives = self.ghost.lives
                if self.freeze_ghosts:
                    for ghost in self.ghost.ghost:
                        self.ghost.check_collisions(
                            ghost,
                            (self.pacman.row, self.pacman.col)
                        )
                else:
                    self.ghost.move(
                        self.pacman.row,
                        self.pacman.col
                    )
                if self.invincible:
                    self.ghost.lives = old_lives
                    self.ghost.reborn = False
            if (
                self.ghost.reborn
                and not self.invincible and self.death_time is None
            ):
                self.death_time = pygame.time.get_ticks()
            if self.death_time is not None:
                if pygame.time.get_ticks() - self.death_time >= 500:
                    self.death_time = None
                    if self.ghost.lives > 0:
                        self.ghost = type(self.ghost)(
                            self.maze_render,
                            self.ghost.lives,
                            self.config.points_per_ghost
                        )
                        self.ghost.set_level(self.level.level_num)
                        self.pacman = type(self.pacman)(
                            (
                                len(self.maze) // 2,
                                len(self.maze[0]) // 2
                            ),
                            self.maze_render
                        )
                        self.ghost.reborn = False
            self.gum.score += self.ghost.ghost_score
            self.ghost.ghost_score = 0
            self.score = self.gum.score
            hud.draw(
                self.screen,
                score=self.gum.score,
                lives_num=self.ghost.lives,
                level=self.ghost.level,
                pos=(
                    self.maze_render.margin_maze_row,
                    self.maze_render.margin_maze_col
                ),
                base_font=font
            )

            if self.ghost.lives == 0 and not self.invincible:
                self.game_over = True
            if self.gum.eaten_pacgum == self.gum.pacgum:
                self.score = self.gum.score
                self.level_index += 1
                if self.level_index < len(config.level):
                    self.load_level(config)
                else:
                    self.win = True
            pygame.display.flip()
            clock.tick(60)


def cheat_game(screen: pygame.Surface) -> None:
    """Start cheat mode"""
    game = CheatMode(screen)
    game.run()
