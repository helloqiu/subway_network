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


def get_delta(data):
    delta = list()
    last = data[0]
    for i in range(1, len(data)):
        delta.append(data[i] - last)
        last = data[i]
    return delta


def shortest_path_data():
    path = list()
    with open(os.path.join(base_dir, "分阶段数据/平均最短路径.csv"), 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            path.append(float(row['average_shortest_path_length']))
    return path


def draw_size_diameter_shortest_path():
    sns.set(style='ticks', palette='Set2')
    diameter = diameter_data()
    size = size_data()
    plt.figure(dpi=200)
    x1, y1 = zip(*sorted(zip(size, diameter)))
    plt.plot(x1, y1, label='diameter')
    plt.plot(x1, y1, 'o')
    shortest_path = shortest_path_data()
    x2, y2 = zip(*sorted(zip(size, shortest_path)))
    plt.plot(x2, y2, label='average length')
    plt.plot(x2, y2, 'o')

    size.remove(size[0])
    size.remove(size[len(size) - 1])
    delta_diameter = get_delta(diameter)
    x3, y3 = zip(*sorted(zip(size, delta_diameter)))
    plt.plot(x3, y3, '^', label='delta diameter')
    delta_shortest_path = get_delta(shortest_path)
    x4, y4 = zip(*sorted(zip(size, delta_shortest_path)))
    plt.plot(x4, y4, '^', label='delta average length')

    plt.xlabel('N')
    plt.legend(loc='best')

    ax = plt.gca()
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.show()


def draw_size_bc():
    sns.set(style='ticks', palette='Set2')
    bc = bc_data()
    size = size_data()
    plt.figure(dpi=200)
    x1, y1 = zip(*sorted(zip(size, bc)))
    plt.plot(x1, y1, label='BC')
    plt.plot(x1, y1, 'o')
    delta = get_delta(bc)
    size.remove(size[0])
    size.remove(size[len(size) - 1])
    x2, y2 = zip(*sorted(zip(size, delta)))
    plt.plot(x2, y2, '^', label='Delta BC')
    plt.xlabel('N')
    plt.legend(loc='best')

    ax = plt.gca()
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.show()


if __name__ == "__main__":
    draw_size_diameter_shortest_path()
