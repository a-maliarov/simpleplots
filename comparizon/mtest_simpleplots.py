# -*- coding: utf-8 -*-

from simpleplots import Figure
import shutil
import random
import time
import os

#-------------------------------------------------------------------------------

def get_random_values(x, y):
    xvalues = [i for i in range(x, y)]
    yvalues = [i for i in range(x, y)]
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
    fig.plot(xvalues, yvalues, color='blue', linewidth=5, label='line2')

    fig.legend()

    fig.save(f'{test_folder}/graph{i}.png')

#-------------------------------------------------------------------------------
