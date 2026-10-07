import pygame
from src.main import main_game
from src.cheat import cheat_game
from src.rect import MyRect
import json


def draw_highscores(screen: pygame.Surface) -> None:
    """display the top ten player scores"""
    running = True
    background = pygame.image.load("src/main/background.png").convert_alpha()

    try:

        with open("highscore.json", "r") as file:
            highscores = json.load(file)
        if not isinstance(highscores, list):
            highscores = []
    except (FileNotFoundError, json.JSONDecodeError):
        highscores = []
    highscores = sorted(
        highscores, key=lambda player: player["score"], reverse=True
    )
    top_ten = highscores[:10]
    screen_width, screen_height = screen.get_size()
    image_width, image_height = background.get_size()
    scale = max(screen_width / image_width, screen_height / image_height)
    new_width = int(image_width * scale)
    new_height = int(image_height * scale)
    menu_background = pygame.image.load("src/main/menu-background.png")
    (
        menu_background_width,
        menu_background_height
        ) = menu_background.get_size()
    menu_background_x = (screen_width - menu_background_width) // 2
    menu_background_y = (screen_height - menu_background_height) // 2
    menu_background.set_alpha(200)
    pacman_logo = pygame.image.load("src/main/pacman.png")
    pacman_logo = pygame.transform.smoothscale(pacman_logo, (250, 169))
    pacman_logo_x = (
        menu_background_x + (
            menu_background_width - pacman_logo.get_width()) // 2
    )
    pacman_logo_y = menu_background_y - pacman_logo.get_height() + 165
    pacman_logo.set_alpha(200)
    font = pygame.font.Font("src/main/The Magic Cookie.ttf", 40)
    while running:
        screen.fill((0, 0, 0))
        background.set_alpha(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if (
                event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                return
        y_position = 240
        background = pygame.transform.smoothscale(
            background, (new_width, new_height)
        )
        x = (screen_width - new_width) // 2
        y = (screen_height - new_height) // 2

        screen.blit(background, (x, y))
        screen.blit(
            menu_background,
            (menu_background_x, menu_background_y))
        screen.blit(pacman_logo, (pacman_logo_x, pacman_logo_y))

        for player in top_ten:
            name = player["name"]
            score = player["score"]
            result = font.render(f"{name}: {score}", True, ("BLACK"))
            result_rect = result.get_rect(
                center=(screen_width // 2, y_position))
            screen.blit(result, result_rect)
            y_position += 40
        pygame.display.flip()


def draw_instructions(screen: pygame.Surface) -> None:
    """display the game instructions screen"""
    running = True
    instruction = pygame.image.load("src/main/insta4.jpg")
    screen_width, screen_height = screen.get_size()
    instruction_width, instruction_height = instruction.get_size()
    scale = max(
        screen_width / instruction_width, screen_height / instruction_height)
    new_width = int(instruction_width * scale)
    new_height = int(instruction_height * scale)
    instruction = pygame.transform.smoothscale(
        instruction, (new_width, new_height))
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        screen.blit(instruction, (x, y))
        pygame.display.flip()


def draw_main_menu(screen: pygame.Surface) -> None:
    """display the main menu and handle menu actions"""
    background = pygame.image.load("src/main/background.png")
    running = True
    screen_width, screen_height = screen.get_size()
    image_width, image_height = background.get_size()
    scale = max(screen_width / image_width, screen_height / image_height)
    new_width = int(image_width * scale)
    new_height = int(image_height * scale)
    menu_background = pygame.image.load("src/main/menu-background.png")

    menu_background_width, menu_background_height = menu_background.get_size()
    menu_background = pygame.transform.smoothscale(
        menu_background,
        (menu_background_width, int(menu_background_height * 1.17)))
    menu_background_x = (screen_width - menu_background_width) // 2
    menu_background_y = (screen_height - menu_background_height) // 2
    menu_background.set_alpha(200)
    pacman_logo = pygame.image.load("src/main/pacman.png")
    pacman_logo = pygame.transform.smoothscale(pacman_logo, (300, 180))
    pacman_logo_x = (
        menu_background_x +
        (menu_background_width - pacman_logo.get_width()) // 2
    )
    pacman_logo_y = menu_background_y - pacman_logo.get_height() + 185
    pacman_logo.set_alpha(200)
    start = pygame.image.load("src/main/START.png")
    start = pygame.transform.smoothscale(start, (150, 100))
    start_x = menu_background_x + (
        menu_background_width - start.get_width()) // 2
    start_y = menu_background_y - start.get_height() + 220
    highscores = pygame.image.load("src/main/HIGHSCORES.png")
    highscores = pygame.transform.smoothscale(highscores, (150, 100))
    highscores_x = (
        menu_background_x +
        (menu_background_width - highscores.get_width()) // 2
    )
    highscores_y = menu_background_y - highscores.get_height() + 315
    instructions = pygame.image.load("src/main/instructions.png")
    instructions = pygame.transform.smoothscale(instructions, (150, 100))
    instructions_x = (
        menu_background_x +
        (menu_background_width - instructions.get_width()) // 2
    )
    instructions_y = menu_background_y - instructions.get_height() + 405
    exit_button = pygame.image.load("src/main/EXIT.png")
    exit_button = pygame.transform.smoothscale(exit_button, (150, 100))
    exit_button_x = (
        menu_background_x +
        (menu_background_width - exit_button.get_width()) // 2
    )
    exit_button_y = menu_background_y - exit_button.get_height() + 500
    cheat_mode = pygame.image.load("src/main/CheatMode.png")
    cheat_mode = pygame.transform.smoothscale(cheat_mode, (150, 100))
    cheat_mode_x = (
        menu_background_x +
        (menu_background_width - cheat_mode.get_width()) // 2
    )
    cheat_mode_y = menu_background_y - exit_button.get_height() + 590
    cheat_mode_rect = MyRect(
        cheat_mode.get_rect(topleft=(cheat_mode_x, cheat_mode_y))
        )
    exit_rect = MyRect(
        exit_button.get_rect(topleft=(exit_button_x, exit_button_y)))
    start_rect = MyRect(start.get_rect(topleft=(start_x, start_y)))
    instructions_rect = MyRect(instructions.get_rect(
        topleft=(instructions_x, instructions_y)))
    highscore_rect = MyRect(
        highscores.get_rect(topleft=(highscores_x, highscores_y)))
    while running:
        screen.fill((0, 0, 0))
        background.set_alpha(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    running = False
                elif highscore_rect.collidepoint(event.pos):
                    draw_highscores(screen)
                elif instructions_rect.collidepoint(event.pos):
                    draw_instructions(screen)
                elif start_rect.collidepoint(event.pos):
                    main_game(screen)
                elif cheat_mode_rect.collidepoint(event.pos):
                    cheat_game(screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        background = pygame.transform.smoothscale(
            background, (new_width, new_height))
        x = (screen_width - new_width) // 2
        y = (screen_height - new_height) // 2
        screen.blit(background, (x, y))
        screen.blit(menu_background, (menu_background_x, menu_background_y))
        screen.blit(pacman_logo, (pacman_logo_x, pacman_logo_y))
        screen.blit(start, start_rect.rect)
        screen.blit(highscores, highscore_rect.rect)
        screen.blit(instructions, instructions_rect.rect)
        screen.blit(exit_button, exit_rect.rect)
        screen.blit(cheat_mode, cheat_mode_rect.rect)
        pygame.display.flip()
