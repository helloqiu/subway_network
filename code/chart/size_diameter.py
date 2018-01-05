# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import os
import csv
import seaborn as sns

base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


def diameter_data():
    diameter = list()
    with open(os.path.join(base_dir, "分阶段数据/网络直径.csv"), 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            diameter.append(int(row['diameter']))
    return diameter


def size_data():
    s = list()
    with open(os.path.join(base_dir, "分阶段数据/规模.csv"), 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            s.append(int(row['size']))
    return s


def bc_data():
    result = list()
    with open(os.path.join(base_dir, "分阶段数据/平均BC.csv"), 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            result.append(float(row['average_bc']))
    return result


def delta_bc():
    bc = bc_data()
    delta = list()
    last = bc[0]
    for i in range(1, len(bc)):
        delta.append(bc[i] - last)
        last = bc[i]
    return delta


def draw_size_diameter():
    sns.set(style='ticks', palette='Set2')
    diameter = diameter_data()
    size = size_data()
    plt.figure(dpi=200)
    x1, y1 = zip(*sorted(zip(size, diameter)))
    plt.plot(x1, y1)
    plt.plot(x1, y1, 'o')
    plt.ylabel('L')
    plt.xlabel('N')

    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.show()


def draw_size_bc():
    sns.set(style='ticks', palette='Set2')
    bc = bc_data()
    size = size_data()
    plt.figure(dpi=200)
    x1, y1 = zip(*sorted(zip(size, bc)))
    plt.plot(x1, y1)
    plt.plot(x1, y1, 'o')
    delta = delta_bc()
    size.remove(size[0])
    size.remove(size[len(size) - 1])
    x2, y2 = zip(*sorted(zip(size, delta)))
    plt.plot(x2, y2, '^')
    plt.ylabel('BC')
    plt.xlabel('N')

    ax = plt.gca()
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.show()


if __name__ == "__main__":
    draw_size_diameter()
