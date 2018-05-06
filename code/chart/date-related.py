# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import csv
import datetime
import seaborn as sns

base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


def get_data(file_name, col_name):
    date = list()
    size = list()
    with open(os.path.join(base_dir, "分阶段数据/{}.csv".format(file_name)), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            date.append(datetime.datetime.strptime(row['date'], '%Y-%m-%d'))
            size.append(float(row[col_name]))
    return date, size


def draw(xlabel, ylabel, filename, col_name):
    song = fm.FontProperties(fname='/Users/helloqiu/Downloads/Adobe Song Std L.ttf')
    sns.set(style='ticks', palette='Set2')
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    x1, y1 = get_data(filename, col_name)
    plt.plot(x1, y1)
    plt.plot(x1, y1, 'o')
    plt.xlabel(xlabel, fontproperties=song)
    plt.ylabel(ylabel, fontproperties=song)
    plt.show()


if __name__ == "__main__":
    draw(xlabel="时间", ylabel="平均BC", filename="平均BC", col_name="average_bc")
