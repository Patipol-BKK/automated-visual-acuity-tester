import os
import time
import win32pipe, win32file, pywintypes
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import yaml
import math

from optotypes import *
from renderer import *

from windows_pipe import pipe_client_init, pipe_client_read
from threading import Thread

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

commands_dict = {
    'c' : 'c',
    'see': 'c',
    'letter c': 'c',
    'letter see': 'c',
    'let us see': 'c',
    'let us c': 'c',
    'd' : 'd',
    'letter d': 'd',
    'h' : 'h',
    'letter h': 'h',
    'k' : 'k',
    'letter k': 'k',
    'n' : 'n',
    'letter n': 'n',
    'o' : 'o',
    'oh' : 'o',
    'letter o': 'o',
    'letter oh': 'o',
    'r' : 'r',
    'are' : 'r',
    'letter r': 'r',
    'letter are': 'r',
    's' : 's',
    'letter s': 's',
    'v' : 'v',
    'letter v': 'v',
    'z' : 'z',
    'that' : 'z',
    'letter z': 'z',
    'letter that': 'z',
}

if __name__ == '__main__':
    # # Open a named pipe for recieving transcribed msgs (Linux)
    # pipe_path = "/tmp/transcribed-txt"
    # if not os.path.exists(pipe_path):
    #     os.mkfifo(pipe_path)

    # Initialize Pygame for Display
    p = Thread(target=pipe_listener)
    p.start()
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Visual Acuity Test - Display')

    optotypes = load_optotypes()

    crashed = False
    cur_logMAR = 1
    cur_optotype = 4
    cur_pointed = 0
    update_screen = True
    update_optotypes = True

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
            if event.type == pygame.USEREVENT:
                if prev != event.msg.lower() and prev != event.msg[:-1].lower():
                    print(f"Event: {event.msg.lower()}")
                    prev = event.msg.lower()
                    try:
                        print(f'Recieved  : {commands_dict[event.msg.lower()]}')
                        if commands_dict[event.msg.lower()] == figures[cur_pointed].name.lower():
                            current_score += 1
                        print('# Correct  : ', current_score)
                        cur_pointed += 1
                        update_screen = True
                        if cur_pointed > len(figures) - 1:
                            if current_score >= 4:
                                cur_logMAR = round((cur_logMAR - 0.1) * 10) / 10 
                                update_screen = True
                                update_optotypes = True

                                current_score = 0
                                cur_pointed = 0

                            else:
                                print(f'Diagnosed LogMAR  : {round((cur_logMAR + 0.1) * 10) / 10}')
                                update_screen = False
                                update_optotypes = False
                                crashed = True
                                exit(0)



                    except:
                        print('Invalid Input')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if cur_logMAR < 1:
                        cur_logMAR = round((cur_logMAR + 0.1) * 10) / 10
                        update_screen = True
                        update_optotypes = True
                if event.key == pygame.K_DOWN:
                    if cur_logMAR > -0.3:
                        cur_logMAR = round((cur_logMAR - 0.1) * 10) / 10 
                        update_screen = True
                        update_optotypes = True

                if event.key == pygame.K_LEFT:
                    if cur_optotype > 0:
                        cur_optotype -= 1
                        update_screen = True
                        update_optotypes = True
                if event.key == pygame.K_RIGHT:
                    if cur_optotype < len(figures) - 1:
                        cur_optotype += 1
                        update_screen = True
                        update_optotypes = True

                if event.key == pygame.K_SPACE:
                    update_screen = True
                    update_optotypes = True

                if event.key == pygame.K_a:
                    if cur_pointed > -1:
                        cur_pointed -= 1
                    update_screen = True
                if event.key == pygame.K_d:
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
