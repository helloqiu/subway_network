# -*- coding: utf-8 -*-

from graph import shanghai_graph_by_date, chengdu_graph_by_date
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
        result = shanghai_graph_by_date()
        p = os.path.join(base_dir, '上海分阶段数据/k_2.csv')
    else:
        result = chengdu_graph_by_date()
        p = os.path.join(base_dir, '分阶段数据/k_2.csv')
    for key in result.keys():
        g = result[key]
        num = 0
        for n in g.nodes:
            if g.degree(n) == 2:
                num += 1
        num = num / len(g.nodes) * 100
        data.append({'date': key.strftime("%Y-%m-%d"), 'node_num': num})

    with open(p, 'a') as f:
        w = csv.DictWriter(f, ['date', 'node_num'])
        w.writeheader()
        w.writerows(data)


def get_data(first=True, last=False):
    G = shanghai_graph_by_date()
    if first:
        G = G[list(G.keys())[1]]
    else:
        G = G[list(G.keys())[4]]
    if last:
        G = shanghai_graph_by_date()
        keys = list(G.keys())
        G = G[keys[len(keys) - 1]]
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    n = len(G.nodes)
    c = list()
    for i in range(0, len(cnt)):
        c.append(cnt[i] / n * 100)
    return deg, tuple(c)


def draw():
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    x1, y1 = get_data_with_size('k_2', 'node_num')
    p1, = ax.plot(x1, y1)
    p2, = ax.plot(x1, y1, 'o')

    x2, y2 = get_data_with_size('k_2', 'node_num', dir_name="分阶段数据")
    p3, = ax.plot(x2, y2)
    p4, = ax.plot(x2, y2, '^')

    ax.set_xlabel("规模", fontproperties=song)
    ax.set_ylabel("比例（%）", fontproperties=song)

    ax.legend(
        [(p1, p2), (p3, p4)],
        [u'上海', u'成都'],
        prop=dict(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    )

    plt.show()


def draw_2():
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    x1, y1 = get_data()
    p1 = ax.bar(x1, y1, width=0.35)
    x2, y2 = get_data(first=False)
    new_x2 = list()
    for i in range(0, len(x2)):
        new_x2.append(x2[i] + 0.35)
    p2 = ax.bar(new_x2, y2, width=0.35)

    ax.set_xticks([d + 0.175 for d in new_x2])
    ax.set_xticklabels(x2)
    ax.legend(
        [p1, p2],
        [u'1995年', u'2000年'],
        prop=dict(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    )
    ax.set_xlabel("度", fontproperties=song)
    ax.set_ylabel("比例（%）", fontproperties=song)
    plt.show()


def draw_3():
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    x1, y1 = get_data(last=True)
    p1 = ax.bar(x1, y1, width=0.70)
    ax.set_xticks([d + 0.35 for d in x1])
    ax.set_xticklabels(x1)
    ax.set_xlabel("度", fontproperties=song)
    ax.set_ylabel("比例（%）", fontproperties=song)
    plt.show()


if __name__ == "__main__":
    draw_3()
