import sys
try:
    import pygame
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)
from src.rect import MyRect


def paused_screen(screen: pygame.Surface) -> str:
    """display the pause screen and handle pause button actions"""
    screen_w, screen_h = screen.get_size()
    pause_cover = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
    pause_cover.fill((0, 0, 0, 180))
    screen.blit(pause_cover, (0, 0))
    pause_font = pygame.font.Font(
        "src/main/pixel-game.regular.otf",
        100
    )
    paused_text = pause_font.render(
        "PAUSED",
        True,
        ("#00CEFA")
    )
    pause_rect = paused_text.get_rect(
        center=(screen_w // 2, screen_h // 2 - 100)
    )
    continue_pause_surface = pygame.image.load(
        "src/Graphics/continue.png").convert_alpha()
    continue_pause = pygame.transform.smoothscale(
        continue_pause_surface, (379, 110))
    continue_rect = MyRect(continue_pause.get_rect(
        center=(screen_w // 2, screen_h // 2)
    ))
    exit_pause_surface = pygame.image.load(
        "src/Graphics/exit_from_pause.png").convert_alpha()
    exit_pause = pygame.transform.smoothscale(
        exit_pause_surface, (392, 93))
    exit_rect = MyRect(exit_pause.get_rect(
        center=(screen_w // 2, screen_h // 2 + 103))
    )
    screen.blit(paused_text, pause_rect)
    screen.blit(continue_pause, continue_rect.rect)
    screen.blit(exit_pause, exit_rect.rect)
    clock = pygame.time.Clock()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(event.pos):
                    return "continue"
                if exit_rect.collidepoint(event.pos):
                    return "exit"
        clock.tick(60)
