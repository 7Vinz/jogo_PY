import pygame
from src.game import Game

def main():
    pygame.init()
    pygame.display.set_caption("Speed Racing - Rear Camera Pseudo-3D")
    Game().run()
    pygame.quit()

if __name__ == "__main__":
    main()
