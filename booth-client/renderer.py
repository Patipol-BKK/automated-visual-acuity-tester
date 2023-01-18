import pygame

from utils import *

import yaml

config_stream = open("config.yml", 'r')
config = yaml.load(config_stream, Loader=yaml.FullLoader)

DISPLAY_WIDTH = config['display']['width']
DISPLAY_HEIGHT = config['display']['height']

ASPECT_RATIO = config['display']['aspect_ratio'].split('_')
ASPECT_RATIO = [int(x) for x in ASPECT_RATIO]


class Line:
    def __init__(self, figures, height):
        self.figures = figures
        self.height = height
        self.gap = height

        # Calculate total line width
        self.line_width = 0
        for i, figure in enumerate(figures):
            self.line_width += figure.render(self.height).get_size()[0]
            self.line_width += self.gap
        self.line_width -= self.gap

    def render(self, display):
        center_x = DISPLAY_WIDTH / 2
        center_y = DISPLAY_HEIGHT / 2

        # Render each figure
        current_x = center_x - self.line_width / 2
        for i, figure in enumerate(self.figures):
            rendered_figure = figure.render(self.height)
            display.blit(rendered_figure,
                (current_x, center_y - rendered_figure.get_size()[1] / 2))
            current_x += rendered_figure.get_size()[0] + self.gap


class TestScreen:
    def __init__(self, optotype, distance, display):
        self.optotype = optotype
        self.distance = distance
        self.display = display

    def render(self, count, logMAR):
        figure_size = get_figure_size(
            logMAR,
            self.distance,
            self.optotype.height)
        line = Line(self.optotype.choose_random(count), figure_size)
        line.render(self.display)

        # Render current test info
        str_optotype = 'Optotype: ' + self.optotype.name

        str_figures = 'Displayed Figures: '
        for figure in line.figures:
            str_figures += figure.name + ' '

        str_logMAR = 'logMAR: ' + str(logMAR)
        str_snellen = 'Snellen: ' + snellen_dict[logMAR]

        FONT = 'fonts/' + config['font']
        small_font = pygame.font.Font(FONT, 20)

        text = small_font.render(str_optotype, True, (0, 0, 0))
        self.display.blit(text, (10, 10))

        text = small_font.render(str_figures, True, (0, 0, 0))
        self.display.blit(text, (10, 40))

        text = small_font.render(str_logMAR, True, (0, 0, 0))
        self.display.blit(text, (10, 70))

        text = small_font.render(str_snellen, True, (0, 0, 0))
        self.display.blit(text, (10, 100))
