# -*- coding: utf-8 -*-

from graph import shanghai_graph_by_date, chengdu_graph_by_date, get_chengdu_subway_graph, get_shanghai_subway_graph
import os
import csv
from chart.date_related import get_data_with_size
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.font_manager as fm
import seaborn as sns
import collections

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def cal_data(shanghai=True):
    data = list()
    if shanghai:
        with open(os.path.join(base_dir, '上海BC排序.csv'), 'r', encoding='utf-8') as f:
            r = csv.DictReader(f)
            for row in r:
                data.append(row['BC'])
        p = os.path.join(base_dir, '上海BC分布.csv')
        g = get_shanghai_subway_graph()
    else:
        with open(os.path.join(base_dir, 'BC排序-七号线开通后.csv'), 'r', encoding='utf-8') as f:
            r = csv.DictReader(f)
            for row in r:
                data.append(row['BC'])
        p = os.path.join(base_dir, '成都BC分布.csv')
        g = get_chengdu_subway_graph()
    r = [0, 0, 0, 0, 0, 0]
    for i in data:
        temp = int(float(i) // 0.05)
        r[temp] += 1
    result = list()
    for i in range(0, len(r)):
        result.append({'num': (i + 1) * 0.05, 'distribution': r[i] / len(g.nodes)})
    with open(p, 'a') as f:
        w = csv.DictWriter(f, ['num', 'distribution'])
        w.writeheader()
        w.writerows(result)


def get_data(shanghai=True):
    num = list()
    d = list()
    if shanghai:
        f = open(os.path.join(base_dir, '上海BC分布.csv'), 'r')
    else:
        f = open(os.path.join(base_dir, '成都BC分布.csv'), 'r')
    r = csv.DictReader(f)
    for row in r:
        num.append(float(row['num']))
        d.append(float(row['distribution']))
    return tuple(num), tuple(d)


def draw_3():
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    x1, y1 = get_data()
    p1 = ax.bar(x1, y1, width=0.025)
    x2, y2 = get_data(shanghai=False)
    new_x2 = list()
    for i in range(0, len(x2)):
        new_x2.append(x2[i] + 0.025)
    p2 = ax.bar(new_x2, y2, width=0.025)
    ax.set_xticks([d + 0.0375 for d in x2])
    ax.set_xticklabels(x2)
    ax.set_xlabel("介数中心性", fontproperties=song)
    ax.set_ylabel("比例（%）", fontproperties=song)
    ax.legend(
        [p1, p2],
        [u'上海', u'成都'],
        prop=dict(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    )
    plt.show()


if __name__ == "__main__":
    draw_3()
