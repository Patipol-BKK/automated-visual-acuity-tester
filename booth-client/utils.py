import math

import yaml

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


def cm_to_pixels(cm):
    return DISPLAY_WIDTH / DISPLAY_WIDTH_DIM * cm


def get_figure_size(logMAR, distance):
    figure_cm = 5.818
    figure_cm /= 1.2589**((1 - logMAR) / 0.1)
    return cm_to_pixels(figure_cm) * distance / 4


snellen_dict = {
    1: '6/60',
    0.9: '6/48',
    0.8: '6/38',
    0.7: '6/30',
    0.6: '6/24',
    0.5: '6/19',
    0.4: '6/15',
    0.3: '6/12',
    0.2: '6/9.5',
    0.1: '6/7.5',
    0.0: '6/6',
    -0.1: '6/4.8',
    -0.2: '6/3.8',
    -0.3: '6/3',
}
