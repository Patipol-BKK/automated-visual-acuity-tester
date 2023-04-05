import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import yaml
import math

from optotypes import *
from renderer import *

config_stream = open("config.yml", 'r')
config = yaml.load(config_stream, Loader=yaml.FullLoader)

DISPLAY_WIDTH = config['display']['width']
DISPLAY_HEIGHT = config['display']['height']

ASPECT_RATIO = config['display']['aspect_ratio'].split('_')
ASPECT_RATIO = [int(x) for x in ASPECT_RATIO]

# Display Dimensions in cm
DISPLAY_DIAG_DIM = config['display']['screen_size'] * 2.54
DISPLAY_WIDTH_DIM = ASPECT_RATIO[0] * math.sqrt(
    DISPLAY_DIAG_DIM**2 / (ASPECT_RATIO[0]**2 + ASPECT_RATIO[1]**2))
DISPLAY_HEIGHT_DIM = ASPECT_RATIO[1] * math.sqrt(
    DISPLAY_DIAG_DIM**2 / (ASPECT_RATIO[0]**2 + ASPECT_RATIO[1]**2))

pygame.init()
crashed = False
def pipe_listener():
    handle = pipe_client_init()
    while not crashed:
        resp = pipe_client_read(handle)
        ev = pygame.event.Event(pygame.USEREVENT, {'msg': resp})
        pygame.event.post(ev)

if __name__ == '__main__':
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Visual Acuity Test - Display')

    optotypes = load_optotypes()

    crashed = False
    cur_logMAR = 1
    cur_optotype = 1
    cur_pointed = 0
    update_screen = True
    update_optotypes = True

    lowbound_logMAR = -0.3
    upbound_logMAR = cur_logMAR

    scores = {}
    for logMAR in snellen_dict:
        scores[logMAR] = 0

    prev = '_'
    current_score = 0
    figures = []
    test = TestScreen(list(optotypes.values())[cur_optotype], 2, 5, cur_logMAR, display)
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if figures[cur_pointed].name.lower() == 'up':
                        pass
                    if cur_pointed < len(figures) - 1:
                        cur_pointed += 1
                    else:
                        cur_pointed = -1
                    update_screen = True
                if event.key == pygame.K_DOWN:
                    if figures[cur_pointed].name.lower() == 'down':
                        pass
                    if cur_pointed < len(figures) - 1:
                        cur_pointed += 1
                    else:
                        cur_pointed = -1
                    update_screen = True

                if event.key == pygame.K_LEFT:
                    if figures[cur_pointed].name.lower() == 'left':
                        pass
                    if cur_pointed < len(figures) - 1:
                        cur_pointed += 1
                    else:
                        cur_pointed = -1
                    update_screen = True
                if event.key == pygame.K_RIGHT:
                    if figures[cur_pointed].name.lower() == 'right':
                        pass
                    if cur_pointed < len(figures) - 1:
                        cur_pointed += 1
                    else:
                        cur_pointed = -1
                    update_screen = True
        
        if update_screen:
            display.fill((255, 255, 255))
            if update_optotypes:
                test = TestScreen(list(optotypes.values())[cur_optotype], 2, 5, cur_logMAR, display)
                update_optotypes = False
            figures = test.render(cur_pointed)
            update_screen = False
        pygame.display.update()
