import pygame
from settings import *
from src.car import Car
from src.renderer import Renderer
from src.race import Race
from src.hud import HUD

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.renderer = Renderer()
        self.hud = HUD()
        self.big = pygame.font.SysFont("consolas", 42, bold=True)
        self.small = pygame.font.SysFont("consolas", 20, bold=True)
        self.running = True
        self.reset()

    def reset(self):
        self.p1 = Car("P1", BLUE, is_player=True, controls={
            "accelerate": pygame.K_w, "brake": pygame.K_s,
            "left": pygame.K_a, "right": pygame.K_d
        })
        self.p2 = Car("P2", ORANGE, is_player=True, controls={
            "accelerate": pygame.K_UP, "brake": pygame.K_DOWN,
            "left": pygame.K_LEFT, "right": pygame.K_RIGHT
        })
        self.rivals = [
            Car("RIVAL 1", RED, -0.55, skill=0.93),
            Car("RIVAL 2", GREEN, 0.45, skill=0.82),
            Car("RIVAL 3", PURPLE, 0.0, skill=1.0),
            Car("RIVAL 4", YELLOW, -0.2, skill=0.76),
        ]
        self.cars = [self.p1, self.p2] + self.rivals
        self.race = Race()
        self.camera_shake = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.race.finished:
                    self.reset()

    def update(self, dt):
        if not self.race.started or self.race.finished:
            self.race.update(dt, self.cars)
            return
        keys = pygame.key.get_pressed()
        self.p1.update_player(dt, keys)
        self.p2.update_player(dt, keys)
        for rival in self.rivals:
            rival.update_ai(dt, self.race.elapsed, [self.p1.distance, self.p2.distance])
        self.race.update(dt, self.cars)

    def render_view(self, rect, player, player_index):
        view = pygame.Surface((rect.width, rect.height))
        self.renderer.draw_background(view, player.distance, self.race.elapsed)
        self.renderer.draw_road(view, player.distance, self.race.elapsed)

        # Render rivals and the other human driver relative to this viewport's camera.
        visible_cars = [c for c in self.cars if c is not player and c.distance > player.distance-180]
        visible_cars.sort(key=lambda c: c.distance)
        for car in visible_cars:
            self.renderer.project_car(view, car, player, view.get_height()-95)
        steer = int(pygame.key.get_pressed()[player.controls["right"]]) - int(pygame.key.get_pressed()[player.controls["left"]])
        self.renderer.draw_player_car(view, player.color, steer)
        self.hud.draw_view(view, player, player_index, self.race.elapsed, self.race.started)
        self.screen.blit(view, rect.topleft)
        pygame.draw.rect(self.screen, (15, 19, 22), rect, 3)

    def draw(self):
        self.screen.fill((12, 16, 19))
        left = pygame.Rect(0, 0, WIDTH//2, HEIGHT)
        right = pygame.Rect(WIDTH//2, 0, WIDTH//2, HEIGHT)
        self.render_view(left, self.p1, 1)
        self.render_view(right, self.p2, 2)

        # Shared header label and center divider.
        pygame.draw.rect(self.screen, (15, 20, 24), (0, 0, WIDTH, 5))
        pygame.draw.line(self.screen, (225, 222, 198), (WIDTH//2, 0), (WIDTH//2, HEIGHT), 3)
        if self.race.finished:
            self.race.draw_overlay(self.screen, self.big, self.small)
        elif not self.race.started:
            countdown = "VAI!" if self.race.countdown < 0.8 else str(max(1, int(self.race.countdown)+1))
            label = self.big.render(countdown, True, YELLOW)
            self.screen.blit(label, label.get_rect(center=(WIDTH//2, 110)))
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS)/1000.0, 0.035)
            self.handle_events()
            self.update(dt)
            self.draw()
