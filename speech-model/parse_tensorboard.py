import pandas as pd
try:
    from tqdm.auto import tqdm
except ImportError:
    tqdm = lambda _: _


from importlib import reload

import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt

from PIL import Image
from IPython.core.pylabtools import figsize

mpl.rcParams['pdf.fonttype'] = 42     # use true-type
mpl.rcParams['ps.fonttype'] = 42      # use true-type
mpl.rcParams['font.size'] = 12



import expt

import pandas as pd
import numpy as np

run = expt.get_runs('./logs/v12/train/events.out.tfevents.1678234522.b4595d14199b.8704.9.v2')
print(run[0].df)
# print(expt.parse_run_tensorboard('/logs/v12'))