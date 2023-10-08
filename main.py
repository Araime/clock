import math
from datetime import datetime
from os import path

import pygame as pg

RES = WIDTH, HEIGHT = 1366, 768
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
RADIUS = H_HEIGHT - 50
RADIUS_LIST = {'sec': RADIUS - 10, 'min': RADIUS - 55, 'hour': RADIUS - 100, 'digit': RADIUS - 30}
RADIUS_ARK = RADIUS + 8


def get_clock_pos(clock_dict, clock_hand, key):
    x = H_WIDTH + RADIUS_LIST[key] * math.cos(math.radians(clock_dict[clock_hand]) - math.pi / 2)
    y = H_HEIGHT + RADIUS_LIST[key] * math.sin(math.radians(clock_dict[clock_hand]) - math.pi / 2)
    return x, y


if __name__ == '__main__':
    pg.init()
    surface = pg.display.set_mode(RES, pg.FULLSCREEN)
    clock = pg.time.Clock()

    clock12 = dict(zip(range(12), range(0, 360, 30)))  # for hours
    clock60 = dict(zip(range(60), range(0, 360, 6)))  # for minutes

    font = pg.font.SysFont('Verdana', 60)

    img_dir = path.join(path.dirname(__file__), 'img')
    img = pg.image.load(path.join(img_dir, '3.png')).convert_alpha()
    bg = pg.image.load(path.join(img_dir, 'bg5.jpg')).convert()
    bg_rect = bg.get_rect()
    bg_rect.center = WIDTH, HEIGHT
    dx, dy = 1, 1

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

        # set bg
        dx *= -1 if bg_rect.left > 0 or bg_rect.right < WIDTH else 1
        dy *= -1 if bg_rect.top > 0 or bg_rect.bottom < HEIGHT else 1
        bg_rect.centerx += dx
        bg_rect.centery += dy
        surface.blit(bg, bg_rect)
        surface.blit(img, (0, 0))

        # get time
        t = datetime.now()
        hour, minute, second = ((t.hour % 12) * 5 + t.minute // 12) % 60, t.minute, t.second

        # draw face
        for digit, pos in clock60.items():
            radius = 20 if not digit % 3 and not digit % 5 else 8 if not digit % 5 else 2
            pg.draw.circle(surface, pg.Color('gainsboro'), get_clock_pos(clock60, digit, 'digit'), radius, 7)

        # draw clock
        pg.draw.line(surface, pg.Color('orange'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, hour, 'hour'), 15)
        pg.draw.line(surface, pg.Color('green'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, minute, 'min'), 7)
        pg.draw.line(surface, pg.Color('magenta'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, second, 'sec'), 4)
        pg.draw.circle(surface, pg.Color('white'), (H_WIDTH, H_HEIGHT), 10)

        # draw arc
        sec_angle = -math.radians(clock60[t.second]) + math.pi / 2
        pg.draw.arc(surface, pg.Color('magenta'),
                    (H_WIDTH - RADIUS_ARK, H_HEIGHT - RADIUS_ARK, 2 * RADIUS_ARK, 2 * RADIUS_ARK),
                    math.pi / 2, sec_angle, 8)

        pg.display.flip()
        clock.tick(30)
