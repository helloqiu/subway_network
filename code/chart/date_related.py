# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.font_manager as fm
import os
import csv
import datetime
import seaborn as sns

base_dir = os.path.join(os.path.dirname(__file__), '../../data/')
marker_size = 3


def get_data(file_name, col_name, dir_name="上海分阶段数据"):
    date = list()
    size = list()
    with open(os.path.join(base_dir, "{}/{}.csv".format(dir_name, file_name)), 'r') as f:
        r = csv.DictReader(f)
        min_date = None
        for row in r:
            d = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
            if not min_date:
                min_date = d
            date.append((d - min_date).days / 365)
            # date.append(d)
            size.append(float(row[col_name]))
    return date, size


def get_data_with_size(file_name, col_name, dir_name="上海分阶段数据"):
    _, size = get_data("规模", "size", dir_name)
    _, data = get_data(file_name, col_name, dir_name)
    return size, data


def draw(xlabel, ylabel, filename, col_name):
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    x1, y1 = get_data(filename, col_name)
    ax.plot(x1, y1)
    ax.plot(x1, y1, 'o')
    ax.set_xlabel(xlabel, fontproperties=song)
    ax.set_ylabel(ylabel, fontproperties=song)
    plt.show()


def draw_double(xlabel, ylabel, filename, col_name):
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    x1, y1 = get_data_with_size(filename, col_name)
    p1, = ax.plot(x1, y1)
    p2, = ax.plot(x1, y1, 'o')

    x2, y2 = get_data_with_size(filename, col_name, dir_name="分阶段数据")
    p3, = ax.plot(x2, y2)
    p4, = ax.plot(x2, y2, '^')

    ax.set_xlabel(xlabel, fontproperties=song)
    ax.set_ylabel(ylabel, fontproperties=song)

    ax.legend(
        [(p1, p2), (p3, p4)],
        [u'上海', u'成都'],
        prop=dict(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    )

    plt.show()


if __name__ == "__main__":
    draw_double(xlabel="规模", ylabel="f", filename="核分析", col_name="f")
