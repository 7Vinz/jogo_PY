import math
import pygame
from settings import *

class Renderer:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 16, bold=True)

    def polygon(self, surf, color, points):
        pygame.draw.polygon(surf, color, points)

    def draw_background(self, surf, camera_offset, elapsed):
        # Vertical pixel-art sky gradient.
        for y in range(HORIZON_Y + 8):
            t = y / max(1, HORIZON_Y + 8)
            c = tuple(int(SKY_TOP[i] * (1-t) + SKY_BOTTOM[i] * t) for i in range(3))
            pygame.draw.line(surf, c, (0, y), (surf.get_width(), y))
        pygame.draw.rect(surf, (83, 139, 147), (0, HORIZON_Y-4, surf.get_width(), 9))

        # Distant blocky skyline, scrolling slowly for depth.
        w = surf.get_width()
        for i in range(19):
            bx = int((i * 73 - camera_offset * 0.12) % (w + 90)) - 45
            bh = 22 + (i * 31 % 57)
            col = (65 + i % 3 * 8, 91 + i % 4 * 5, 99 + i % 3 * 4)
            pygame.draw.rect(surf, col, (bx, HORIZON_Y - bh - 5, 47, bh + 5))
            for wx in range(bx+7, bx+43, 12):
                for wy in range(HORIZON_Y-bh+4, HORIZON_Y-7, 13):
                    pygame.draw.rect(surf, (219, 190, 125), (wx, wy, 4, 5))

    def road_edges(self, y, t):
        depth = t * t
        center = 0.5
        half = ROAD_HALF_TOP + (ROAD_HALF_BOTTOM - ROAD_HALF_TOP) * depth
        return center, half

    def draw_road(self, surf, camera_offset, elapsed):
        w, h = surf.get_size()
        # Grass and shoulder bands.
        pygame.draw.rect(surf, GRASS_A, (0, HORIZON_Y, w, h-HORIZON_Y))
        # Scanline road geometry gives a pseudo-3D perspective.
        for y in range(HORIZON_Y, h):
            t = (y - HORIZON_Y) / max(1, h - HORIZON_Y)
            depth = t*t
            half = ROAD_HALF_TOP + (ROAD_HALF_BOTTOM - ROAD_HALF_TOP) * depth
            center_x = w * 0.5 + math.sin(elapsed * 0.22) * (1-depth) * 8
            left = int(center_x - half)
            right = int(center_x + half)
            stripe = int((y + camera_offset * 0.42) / 22) % 2
            road_col = ROAD_A if stripe == 0 else ROAD_B
            pygame.draw.line(surf, road_col, (left, y), (right, y), 1)
            # Grass verge / rumble strips.
            curb = 5 + int(depth * 10)
            curb_col = (225, 220, 196) if stripe == 0 else (190, 57, 52)
            pygame.draw.line(surf, curb_col, (left-curb, y), (left, y), 1)
            pygame.draw.line(surf, curb_col, (right, y), (right+curb, y), 1)

        # Lane markers as perspective-scaled dashes.
        scroll = camera_offset * 0.9
        for divider in (-1/3, 1/3):
            for n in range(18):
                z = ((n / 18) + (scroll / 420.0)) % 1.0
                depth = z*z
                y = int(HORIZON_Y + depth * (h-HORIZON_Y))
                half = ROAD_HALF_TOP + (ROAD_HALF_BOTTOM-ROAD_HALF_TOP)*depth
                cx = w*0.5
                x = int(cx + divider * half)
                dash_h = max(2, int(2 + depth*18))
                dash_w = max(1, int(1 + depth*3))
                pygame.draw.rect(surf, (213, 211, 190), (x-dash_w//2, y, dash_w, dash_h))

        # Roadside dashed barriers and lamps.
        for n in range(12):
            z = ((n / 12) + (scroll / 620.0)) % 1.0
            depth = z*z
            y = int(HORIZON_Y + depth * (h-HORIZON_Y))
            half = ROAD_HALF_TOP + (ROAD_HALF_BOTTOM-ROAD_HALF_TOP)*depth
            size = max(2, int(3 + depth*13))
            for sign in (-1, 1):
                x = int(w*0.5 + sign*(half+10+size))
                pygame.draw.rect(surf, (55, 63, 65), (x-size//2, y-size*3, size, size*3))
                pygame.draw.rect(surf, (238, 211, 132), (x-size, y-size*3, size*2, max(2,size//2)))

    def project_car(self, surf, car, player, screen_bottom, scale_bias=1.0):
        rel = car.distance - player.distance
        if rel > 900 or rel < -180:
            return
        # Convert relative world distance into screen depth. Cars ahead approach horizon.
        depth = max(0.0, min(1.0, 1.0 - (rel + 180) / 1080.0))
        y = HORIZON_Y + (screen_bottom - HORIZON_Y) * (1-depth)
        perspective = 0.22 + depth * 1.12
        road_half = ROAD_HALF_TOP + (ROAD_HALF_BOTTOM - ROAD_HALF_TOP) * ((y-HORIZON_Y)/(screen_bottom-HORIZON_Y))**2
        lane_x = surf.get_width()*0.5 + car.lane * road_half * 0.78
        width = max(7, int(40 * perspective * scale_bias))
        height = max(5, int(24 * perspective * scale_bias))
        x = int(lane_x)
        y = int(y)
        # Pixel-art rear view: tires, body, rear window, lights, bumper.
        pygame.draw.rect(surf, (22, 24, 26), (x-width//2-3, y-height//2+height//3, width+6, max(3,height//3)))
        pygame.draw.rect(surf, BLACK, (x-width//2, y-height//2, width, height))
        pygame.draw.rect(surf, car.color, (x-width//2+2, y-height//2+2, width-4, height-5))
        pygame.draw.rect(surf, (112, 166, 177), (x-width//3, y-height//2+2, 2*width//3, max(2,height//4)))
        light_w = max(2, width//7)
        pygame.draw.rect(surf, (255, 82, 65), (x-width//2+2, y+height//5, light_w, max(2,height//5)))
        pygame.draw.rect(surf, (255, 82, 65), (x+width//2-light_w-2, y+height//5, light_w, max(2,height//5)))
        pygame.draw.rect(surf, (180, 183, 177), (x-width//3, y+height//2-3, 2*width//3, max(2,height//8)))
        if depth > 0.55:
            tag = self.font.render(car.name, True, WHITE)
            surf.blit(tag, tag.get_rect(center=(x, y-height//2-12)))

    def draw_player_car(self, surf, color, steer=0):
        w = surf.get_width()
        x = w//2 + int(steer*4)
        y = surf.get_height()-95
        cw, ch = 92, 112
        # Shadow and tires
        pygame.draw.ellipse(surf, (24, 27, 28), (x-55, y+75, 110, 20))
        pygame.draw.rect(surf, BLACK, (x-49, y+20, 14, 65))
        pygame.draw.rect(surf, BLACK, (x+35, y+20, 14, 65))
        # Rear body and fenders
        pygame.draw.rect(surf, color, (x-43, y+8, 86, 83))
        pygame.draw.rect(surf, (28, 31, 33), (x-34, y+2, 68, 36))
        pygame.draw.rect(surf, color, (x-30, y-3, 60, 33))
        pygame.draw.rect(surf, (112, 174, 185), (x-24, y+1, 48, 20))
        pygame.draw.rect(surf, (76, 111, 121), (x-21, y+4, 42, 13))
        # Rear spoiler
        pygame.draw.rect(surf, BLACK, (x-49, y+12, 98, 7))
        pygame.draw.rect(surf, (178, 181, 177), (x-42, y+15, 84, 3))
        # Tail lamps and license plate
        pygame.draw.rect(surf, (255, 72, 58), (x-39, y+54, 15, 13))
        pygame.draw.rect(surf, (255, 72, 58), (x+24, y+54, 15, 13))
        pygame.draw.rect(surf, (222, 219, 188), (x-12, y+65, 24, 9))
        pygame.draw.rect(surf, BLACK, (x-8, y+67, 16, 4))
        pygame.draw.rect(surf, (90, 95, 97), (x-43, y+85, 86, 7))
