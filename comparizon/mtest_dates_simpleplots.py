# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from simpleplots import Figure
import shutil
import random
import time
import os

#-------------------------------------------------------------------------------

def get_random_values(x, y):
    start = datetime.today()
    xvalues = [start + timedelta(days=i) for i in range(y)]
    yvalues = [i for i in range(len(xvalues))]
    random.shuffle(yvalues)
    return xvalues, yvalues

test_folder = 'mtest_sp'
try:
    os.mkdir(test_folder)
except:
    shutil.rmtree(test_folder)
    os.mkdir(test_folder)

for i in range(100):
    fig = Figure()

    xvalues, yvalues = get_random_values(1, 10000)
    fig.plot(xvalues, yvalues, color='red', linewidth=5, label='line1')

    xvalues, yvalues = get_random_values(1, 10000)
    fig.plot(xvalues, yvalues, color='blue', linewidth=5, label='line1')

    fig.legend()

    fig.save(f'{test_folder}/graph{i}.png')

#-------------------------------------------------------------------------------
