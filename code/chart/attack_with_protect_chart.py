# -*- coding: utf-8 -*-

import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


def get_data(name):
    result = list()
    with open(os.path.join(base_dir, 'shanghai_attack/{}'.format(name)), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            result.append((row['attack_fraction'], row['protect_fraction'], row['efficiency']))
    return result


def draw_chart(name):
    sns.set(style='ticks', palette='Set2')
    cmap = plt.cm.Reds
    plt.figure(dpi=200)
    result = get_data(name)
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

    plt.pcolormesh(x, y, z, cmap=cmap)
    plt.colorbar()
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    for label in ax.get_xticklabels()[::2]:
        label.set_visible(False)
    plt.xlabel('Fraction of the removed nodes')
    plt.ylabel('Fraction of the protected nodes')
    plt.show()


if __name__ == "__main__":
    draw_chart('shanghai_highest_bc_attack_with_largest_degree_protect.csv')
