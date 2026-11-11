import pygame
from settings import *

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 17, bold=True)
        self.small = pygame.font.SysFont("consolas", 13, bold=True)

    def draw_view(self, surf, car, player_index, elapsed, started):
        bar = pygame.Surface((surf.get_width(), 52))
        bar.fill((20, 28, 34))
        surf.blit(bar, (0,0))
        label = f"{car.name}   {car.speed_kmh():03d} KM/H"
        surf.blit(self.font.render(label, True, car.color), (12, 8))
        pygame.draw.rect(surf, (66, 76, 80), (12, 32, 170, 9))
        pygame.draw.rect(surf, car.color, (12, 32, int(170*car.speed/max(1,car.max_speed)), 9))
        timer = self.small.render(f"TEMPO {elapsed:05.1f}s", True, WHITE)
        surf.blit(timer, (surf.get_width()-timer.get_width()-12, 13))
        if started:
            hint = "W/S freia/acelera?  W acelera  S freia  A/D vira" if player_index == 1 else "↑ acelera  ↓ freia  ←/→ vira"
            # Correct compact controls are rendered per viewport.
            hint = "W acelera  S freia  A/D vira" if player_index == 1 else "↑ acelera  ↓ freia  ←/→ vira"
            surf.blit(self.small.render(hint, True, WHITE), (12, 48))
