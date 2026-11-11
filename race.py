import pygame
from settings import *

class Race:
    def __init__(self):
        self.elapsed = 0.0
        self.countdown = 3.2
        self.started = False
        self.finished = False
        self.finishers = []

    def update(self, dt, cars):
        if not self.started:
            self.countdown -= dt
            if self.countdown <= 0:
                self.started = True
            return
        if self.finished:
            return
        self.elapsed += dt
        for car in cars:
            if not car.finished and car.distance >= RACE_DISTANCE:
                car.finished = True
                car.finish_time = self.elapsed
                self.finishers.append(car)
        if all(c.finished for c in cars):
            self.finished = True

    def draw_overlay(self, surf, big, small):
        if not self.started:
            value = "VAI!" if self.countdown < 0.8 else str(max(1, int(self.countdown)+1))
            txt = big.render(value, True, YELLOW)
            surf.blit(txt, txt.get_rect(center=(surf.get_width()//2, 92)))
        if self.finished:
            veil = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            veil.fill((0,0,0,190))
            surf.blit(veil, (0,0))
            title = big.render("CORRIDA FINALIZADA", True, YELLOW)
            surf.blit(title, title.get_rect(center=(surf.get_width()//2, 190)))
            for i, car in enumerate(sorted(self.finishers, key=lambda c:c.finish_time)):
                line = f"{i+1}º  {car.name}  {car.finish_time:.2f}s"
                txt = small.render(line, True, WHITE)
                surf.blit(txt, txt.get_rect(center=(surf.get_width()//2, 265+i*35)))
            hint = small.render("R: nova corrida   |   ESC: sair", True, WHITE)
            surf.blit(hint, hint.get_rect(center=(surf.get_width()//2, 490)))
