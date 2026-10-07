import traceback
try:
    import pygame
except Exception as e:
    traceback.print_exc()
    print()
    print(e)
from typing import Tuple


class HUD:
    """display the score, level, and lives"""
    def __init__(self, posx: int, posy: int) -> None:
        """set the HUD position and load the heart image"""
        self.posx = posx
        self.posy = posy
        heart_surface = pygame.image.load('src/Graphics/heart.png')
        self.heart_rect = pygame.transform.scale(heart_surface, (40, 20))

    def draw(
        self,
        screen: pygame.Surface,
        score: int,
        level: int,
        lives_num: int,
        pos: Tuple[int, int],
        base_font: pygame.font.Font
            ) -> None:
        """draw the score , level, and lives on screen"""
        score_surface = base_font.render(f"{score}", True, "White")
        level_surface = base_font.render(f"{level}", True, "White")
        screen.blit(
            score_surface,
            (
                self.posx + 160, self.posy + 120
            )
        )
        screen.blit(
            level_surface,
            (
                self.posx + 390, self.posy + 120
            )
        )
        for live in range(lives_num):
            screen.blit(
                self.heart_rect,
                (
                    self.posx + 520 + (live * 30), self.posy + 120
                )
            )
