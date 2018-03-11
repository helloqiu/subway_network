# -*- coding: utf-8 -*-

import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import MultipleLocator

base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


def get_data(name):
    result = list()
    with open(os.path.join(base_dir, 'attack/{}'.format(name)), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            result.append((row['attack_fraction'], row['protect_fraction'], row['efficiency']))
    return result


def largest_degree_attack_with_highest_bt_protect_chart():
    sns.set(style='ticks', palette='Set2')
    plt.figure(dpi=200)
    result = get_data('largest_degree_attack_with_highest_bt_protect.csv')
    attack = list()
    protect = list()
    efficiency = list()
    dic = dict()
    for i in result:
        attack.append(i[0])
        protect.append(i[1])
        efficiency.append(i[2])
        dic[(i[0], i[1])] = i[2]
    x, y = np.meshgrid(attack, protect)
    z = np.zeros(x.shape)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            z[i, j] = dic[(x[i, j], y[i, j])]

    plt.pcolor(x, y, z)
    plt.colorbar()
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    xmajorLocator = MultipleLocator(0.1)
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.yaxis.set_major_locator(xmajorLocator)
    plt.xlabel('Fraction of the removed nodes')
    plt.ylabel('Fraction of the protected nodes')
    plt.show()


if __name__ == "__main__":
    largest_degree_attack_with_highest_bt_protect_chart()
