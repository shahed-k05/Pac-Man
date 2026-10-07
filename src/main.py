import sys
import traceback
try:
    from pydantic import ValidationError
    from mazegenerator import MazeGenerator
    from src.maze_loader import MazeAdapter
    import pygame
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)

from src.maze_render import MazeRender
from src.player import Player
from src.pacgum import Pacgums
from src.ghosts import Ghosts
from src.config_validator import read_config, Config, Level
from src.hud import HUD
from src.gameover import GameOver
from src.highscore import save_highscore
from src.pause import paused_screen
from typing import Tuple, List


def create_level(config: Config,
                 i: int,
                 screen_w: int,
                 screen_h: int,
                 score: int,
                 counter: int) -> Tuple[
                    Level,
                    List[List[int]],
                    MazeRender,
                    Player,
                    Pacgums,
                    Ghosts,
                    int
                ]:
    """create and return all objects needed for a game level"""
    level = config.level[i]
    if i == 0:
        mazegen = MazeGenerator(
            (level.width, level.height),
            perfect=False,
            seed=config.seed)
    else:
        mazegen = MazeGenerator(
            (level.width, level.height),
            perfect=False
            )
    maze_adapter = MazeAdapter(mazegen)
    maze = maze_adapter.get_maze()
    maze_render = MazeRender(maze, screen_w, screen_h)
    pacman = Player(
        ((len(maze) // 2), len(maze[0]) // 2
            if len(maze) > 0 else 0),
        maze_render)
    gum = Pacgums(
        maze_render,
        config.points_per_pacgum,
        config.points_per_super_pacgum,
        score)
    ghost = Ghosts(maze_render, config.lives, config.points_per_ghost)
    ghost.set_level(level.level_num)
    counter = counter - ((level.level_num - 1) * 3)
    return level, maze, maze_render, pacman, gum, ghost, counter


def main_game(screen: pygame.Surface) -> None:
    """Run the main pacman game"""
    try:
        pygame.init()
        screen_w, screen_h = screen.get_size()

        background_game = pygame.image.load(
            'src/main/game_background.jpg').convert_alpha()
        background_game_rect = pygame.transform.scale(
            background_game, (screen_w, screen_h))

        screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption('pacman Game')
        config = read_config(sys.argv[1])
        i = 0
        (
            level,
            maze,
            maze_render,
            pacman,
            gum,
            ghost,
            counter
            ) = create_level(config, i, screen_w, screen_h, 0, counter=240)
        position = (maze_render.margin_maze_row, maze_render.margin_maze_col)
        hud = HUD(maze_render.window_x, maze_render.window_y)
        death_time = None
        player_name = ''
        game_over_active = False
        win = False
        game_over = GameOver(screen_w, screen_h)
        clock = pygame.time.Clock()
        running = True
        paused = False
        base_font = pygame.font.Font(
            "src/main/pixel-game.regular.otf", 30)
        base_font_game_over = pygame.font.Font(
            "src/main/pixel-game.regular.otf", 45)
        timer_font = pygame.font.Font("src/main/pixel-game.regular.otf", 35)
        timer_img = pygame.image.load("src/Graphics/hourglass.png")
        timer_rect = pygame.transform.scale(timer_img, (200, 200))
        text = timer_font.render(str(counter), True, "white")
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event, 1000)
        while running:
            screen.fill((0, 0, 0))

            background_game_rect.set_alpha(150)
            screen.blit(background_game_rect, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == timer_event:
                    counter -= 1
                    text = timer_font.render(str(counter), True, "white")
                    if counter == 0:
                        pygame.time.set_timer(timer_event, 0)
                        game_over_active = True
                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if (
                                        event.key == pygame.K_ESCAPE
                                        and not game_over_active
                                        and not win
                    ):
                        paused = not paused
                    elif game_over_active or win:
                        if event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        elif event.key == pygame.K_RETURN:
                            save_highscore(player_name, gum.score)
                            running = False
                        elif (
                            len(player_name) < 10
                            and (
                                event.unicode.isalnum()
                                or event.unicode == " ")
                        ):
                            player_name += event.unicode
                text_rect = text.get_rect(center=(445, 65))
            if not game_over_active and not win:
                screen.blit(timer_rect, (350, -50))
                screen.blit(text, text_rect)

            if paused:
                maze_render.draw(screen, level.level_num)
                pacman.draw(screen)
                gum.draw(screen)
                ghost.draw(screen)
                hud.draw(
                    screen,
                    score=gum.score,
                    lives_num=ghost.lives,
                    level=ghost.level,
                    pos=position,
                    base_font=base_font
                )

                paused_act = paused_screen(screen)
                if paused_act == "continue":
                    paused = False
                elif paused_act == "exit":
                    return

                pygame.display.flip()

                continue
            keys = pygame.key.get_pressed()
            if not game_over_active and not win:
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    pacman.dir = "right"
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    pacman.dir = "left"
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    pacman.dir = "up"
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    pacman.dir = "down"
            if game_over_active:
                counter = 0
                text = timer_font.render(str(counter), True, "#00FFFF")
                pygame.time.set_timer(timer_event, 0)
                player_surface = base_font_game_over.render(
                    player_name,
                    True,
                    (255, 255, 255)
                )
                score_surface = base_font_game_over.render(
                    str(gum.score),
                    True,
                    (255, 255, 255)
                )
                game_over.generate(
                    screen, player_surface, score_surface, "gameover"
                )
            elif win:
                player_surface = base_font_game_over.render(
                    player_name,
                    True,
                    (255, 255, 255)
                )
                score_surface = base_font_game_over.render(
                    str(gum.score),
                    True,
                    (255, 255, 255)
                )

                game_over.generate(
                    screen, player_surface, score_surface, "win"
                )

            else:
                maze_render.draw(screen, level.level_num)
                pacman.draw(screen)
                gum.draw(screen)
                ghost.draw(screen)

                if death_time is None and not game_over_active and not win:
                    pacman.move()
                    is_super = gum.eat(pacman.row, pacman.col)
                    if is_super:
                        ghost.scared_ghost()
                    ghost.move(pacman.row, pacman.col)
                    gum.score += ghost.ghost_score
                    ghost.ghost_score = 0
                hud.draw(
                    screen,
                    score=gum.score,
                    lives_num=ghost.lives,
                    level=ghost.level,
                    pos=position,
                    base_font=base_font
                )
                if ghost.reborn and death_time is None:
                    death_time = pygame.time.get_ticks()
                if death_time is not None:
                    pygame.display.flip()
                    if pygame.time.get_ticks() - death_time >= 500:
                        death_time = None
                        if ghost.lives > 0:
                            pygame.time.delay(1500)
                            ghost = Ghosts(
                                maze_render,
                                ghost.lives, config.points_per_ghost)
                            ghost.set_level(level.level_num)
                            pacman = Player(
                                (
                                    (len(maze) // 2),
                                    len(maze[0]) // 2 if len(maze) > 0 else 0
                                ),
                                maze_render
                                )
                            ghost.reborn = False
            if ghost.lives == 0:
                game_over_active = True
                death_time = None
            if gum.eaten_pacgum == gum.pacgum:
                i += 1
                if i < len(config.level):
                    (
                        level,
                        maze,
                        maze_render,
                        pacman,
                        gum,
                        ghost,
                        counter) = create_level(
                        config, i, screen_w, screen_h, gum.score, counter
                    )
                else:
                    win = True
            pygame.display.update()
            clock.tick(60)
    except ValidationError as e:
        for error in e.errors():
            print(error['loc'], error['msg'])
        print()
        print()
        print("An error occurred during the game loop:")
        traceback.print_exc()
    except Exception as e:
        print(e)
        print()
        print()
        print("An error occurred during the game loop:")
        traceback.print_exc()
        raise
