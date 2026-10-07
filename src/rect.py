import pygame


class MyRect:
    """Wrap a rectangle and provide collision checking"""
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect

    def collidepoint(self, point: tuple[int, int]) -> bool:
        """check if a point is inside the rectangle"""
        mouse_x, mouse_y = point
        return bool(
            self.rect.x <= mouse_x <= self.rect.right
            and self.rect.y <= mouse_y <= self.rect.bottom
        )

    def __getattr__(self, name: str) -> object:
        """get an attribute from wrapped rectangle"""
        return getattr(self.rect, name)
