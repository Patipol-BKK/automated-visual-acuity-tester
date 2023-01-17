import os
import io
import random
import pygame


class Figure:
    def __init__(self, name, svg_string):
        self.name = name
        self.svg_string = svg_string
        self.pygame_img = pygame.image.load(io.BytesIO(svg_string.encode()))
        self.size = self.pygame_img.get_size()

    # Returns a pygame surface with the given height in pixels
    def render(self, height):
        scaling_ratio = height / self.size[0]
        start = self.svg_string.find('<svg')
        scaled_svg_string = self.svg_string[:start + 4] + \
            f' transform="scale({scaling_ratio})"' + \
            self.svg_string[start + 4:]
        return pygame.image.load(io.BytesIO(scaled_svg_string.encode()))


class Optotype:
    def __init__(self, name, figures):
        self.name = name
        self.figures = figures

    def choose_random(self, count):
        random_list = []
        try:
            random_list = random.sample(list(self.figures.values()), count)
        except ValueError:
            random_list = random.choices(list(self.figures.values()), k=count)
        return random_list
# Load Optotypes


def load_optotypes():
    base_dir = os.getcwd()
    base_dir = os.path.join(base_dir, 'optotypes')
    optotypes = {}
    for optotype_name in os.listdir(base_dir):
        optotype_path = os.path.join(base_dir, optotype_name)
        figures = {}
        for figure in os.listdir(optotype_path):
            figure_path = os.path.join(optotype_path, figure)
            svg_string = open(figure_path, "rt").read()

            figure_name = os.path.splitext(figure)[0]
            figures[figure_name] = Figure(figure_name, svg_string)

        optotypes[optotype_name] = Optotype(optotype_name, figures)
    return optotypes
