import sys
try:
    import pygame
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)
import traceback
from menu import draw_main_menu


def main() -> None:
    """start the game and display the main menu"""
    try:
        if len(sys.argv) != 2:
            raise Exception("Missing config.json file")
        pygame.init()
        screen = pygame.display.set_mode((900, 800))
        draw_main_menu(screen)
    except FileNotFoundError as e:
        traceback.print_exc()
        print(e)
    except PermissionError as e:
        traceback.print_exc()
        print(e)
    except IsADirectoryError as e:
        traceback.print_exc()
        print(e)
    except OSError as e:
        traceback.print_exc()
        print(e)
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        traceback.print_exc()
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
