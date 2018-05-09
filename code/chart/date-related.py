# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
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
            # date.append((d - min_date).days / 365)
            date.append(d)
            size.append(float(row[col_name]))
    return date, size


def draw(xlabel, ylabel, filename, col_name):
    song = fm.FontProperties(fname='/Users/helloqiu/Downloads/simsun.ttc', size=10.5)
    sns.set(style='ticks', palette='Set2')
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    x1, y1 = get_data(filename, col_name)
    plt.plot(x1, y1)
    plt.plot(x1, y1, 'o')
    plt.xlabel(xlabel, fontproperties=song)
    plt.ylabel(ylabel, fontproperties=song)
    plt.show()


def draw_double(xlabel, ylabel, filename, col_name):
    song = fm.FontProperties(fname='/Users/helloqiu/Downloads/Adobe Song Std L.ttf', size=10.5)
    sns.set(style='ticks', palette='Set2')
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    x1, y1 = get_data(filename, col_name)
    p1, = plt.plot(x1, y1)
    p2, = plt.plot(x1, y1, 'o')

    x2, y2 = get_data(filename, col_name, dir_name="分阶段数据")
    p3, = plt.plot(x2, y2)
    p4, = plt.plot(x2, y2, '^')

    ax = plt.gca()
    plt.xlabel(xlabel, fontproperties=song)
    plt.ylabel(ylabel, fontproperties=song)
    plt.legend(loc='best')

    ax.legend(
        [(p1, p2), (p3, p4)],
        [u'上海', u'成都'],
        prop=dict(fname='/Users/helloqiu/Downloads/Adobe Song Std L.ttf')
    )

    plt.show()


if __name__ == "__main__":
    draw(xlabel="时间", ylabel="规模", filename="规模", col_name="size")
