# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
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

test_folder = 'mtest_mpl'
try:
    os.mkdir(test_folder)
except:
    shutil.rmtree(test_folder)
    os.mkdir(test_folder)

for i in range(100):
    plt.figure(figsize=(16, 12))

    xvalues, yvalues = get_random_values(1, 10000)
    plt.plot(xvalues, yvalues, color='red', linewidth=5)

    xvalues, yvalues = get_random_values(1, 10000)
    plt.plot(xvalues, yvalues, color='blue', linewidth=5)

    plt.savefig(f'{test_folder}/graph{i}.png')
    plt.close()

#-------------------------------------------------------------------------------
