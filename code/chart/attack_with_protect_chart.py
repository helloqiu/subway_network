# -*- coding: utf-8 -*-

import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib import rc

base_dir = os.path.join(os.path.dirname(__file__), '../../data/')
save_dir = os.path.join(os.path.dirname(__file__), '../../picture/')


def get_data(name):
    result = list()
    with open(os.path.join(base_dir, 'shanghai_attack/{}'.format(name)), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            result.append((row['attack_fraction'], row['protect_fraction'], row['efficiency']))
    return result


def draw_chart(name):
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    cmap = plt.cm.Reds
    plt.figure(dpi=200)
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
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
    # plt.colorbar()
    _ax = plt.gca()
    for label in _ax.get_xticklabels()[::2]:
        label.set_visible(False)
    ax.set_xlabel('攻击节点比例', fontproperties=song)
    ax.set_ylabel('保护节点比例', fontproperties=song)
    plt.savefig(os.path.join(save_dir, 'chengdu_attack_new/{}'.format(name).replace('.csv', '.png')))


def three_d_chart(name):
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    cmap = plt.cm.Reds
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(dpi=200)
    ax = fig.add_subplot(111, projection='3d')
    result = get_data(name)
    attack = list()
    protect = list()
    efficiency = list()
    dic = dict()
    for i in result:
        attack.append(float(i[0]))
        protect.append(float(i[1]))
        efficiency.append(float(i[2]))
        dic[(float(i[0]), float(i[1]))] = float(i[2])
    # ax.plot_surface(x, y, z)
    ax.plot_trisurf(attack, protect, efficiency)
    ax.set_xlabel('攻击节点比例', fontproperties=song)
    ax.set_ylabel('保护节点比例', fontproperties=song)
    ax.set_zlabel('效率', fontproperties=song)
    plt.savefig(os.path.join(save_dir, 'shanghai_attack_protect_3d/{}'.format(name.replace('.csv', '.png'))))


if __name__ == "__main__":
    for f in os.listdir(os.path.join(base_dir, 'shanghai_attack')):
        if 'with' in f:
            three_d_chart(f)
