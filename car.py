import math
import pygame
from settings import *

class Car:
    def __init__(self, name, color, lane=0.0, is_player=False, controls=None, skill=1.0):
        self.name = name
        self.color = color
        self.lane = float(lane)  # -1 = left edge, +1 = right edge
        self.distance = 0.0
        self.speed = 0.0
        self.is_player = is_player
        self.controls = controls or {}
        self.skill = skill
        self.finished = False
        self.finish_time = None
        self.steer_visual = 0.0

    def update_player(self, dt, keys):
        if self.finished:
            self.speed = max(0, self.speed - PLAYER_DRAG * dt)
            return
        if keys[self.controls["accelerate"]]:
            self.speed += PLAYER_ACCEL * dt
        elif keys[self.controls["brake"]]:
            self.speed -= PLAYER_BRAKE * dt
        else:
            self.speed -= PLAYER_DRAG * dt
        self.speed = max(0, min(PLAYER_MAX_SPEED, self.speed))

        steer = int(keys[self.controls["right"]]) - int(keys[self.controls["left"]])
        self.steer_visual = steer
        # Steering becomes more responsive as the car gains speed.
        self.lane += steer * dt * (0.62 + self.speed / 900)
        self.lane = max(-1.12, min(1.12, self.lane))
        self.distance += self.speed * dt

    def update_ai(self, dt, race_time, player_distances):
        if self.finished:
            return
        target_speed = (AI_MIN_SPEED + self.skill * (AI_MAX_SPEED - AI_MIN_SPEED))
        target_speed *= 0.94 + 0.045 * math.sin(race_time * 0.7 + self.skill * 5)
        self.speed += max(-180, min(210, target_speed - self.speed)) * dt
        self.speed = max(0, self.speed)
        # Gentle lane changes keep traffic from feeling static.
        self.lane += math.sin(race_time * (0.24 + self.skill * 0.08) + self.skill * 9) * dt * 0.075
        self.lane = max(-0.88, min(0.88, self.lane))
        self.distance += self.speed * dt

    def speed_kmh(self):
        return int(self.speed * 0.36)
