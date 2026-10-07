import sys
try:
    import pygame
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)


class GameOver:
    """Displpay the game over or win screen"""
    def __init__(self, screen_w: int, screen_h: int) -> None:
        """set the screen size"""
        self.screen_w = screen_w
        self.screen_h = screen_h

    def generate(
        self,
        screen: pygame.Surface,
        player_surface: pygame.Surface,
        score_surface: pygame.Surface,
        status: str
                ) -> None:
        """draw the game over screen"""
        game_over_surface = pygame.image.load(
            f"src/Graphics/{status}.png").convert_alpha()
        game_over = pygame.transform.scale(
            game_over_surface, (600, 200))
        gameoevr_pos = (
            self.screen_w//2, self.screen_h//2 - 100)
        game_over_rect = game_over.get_rect(center=gameoevr_pos)
        name_score_surface = pygame.image.load(
            "src/Graphics/name_score.png").convert_alpha()
        score = pygame.transform.scale(
            name_score_surface, (600, 300))
        score_pos = (gameoevr_pos[0], gameoevr_pos[1] + 150)
        score_rect = score.get_rect(center=score_pos)

        cover = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        cover.fill((0, 0, 0))
        cover.set_alpha(50)
        screen.blit(cover, (0, 0))
        screen.blit(
            game_over,
            game_over_rect
        )
        screen.blit(
            score,
            score_rect
        )
        score_x = score_rect.right - 200
        score_y = score_rect.centery
        screen.blit(score_surface, (score_x, score_y))
        name_x = score_x - 300
        name_y = score_y
        screen.blit(
            player_surface,
            (name_x, name_y)
        )
