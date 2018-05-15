# -*- coding: utf-8 -*-

from graph import chengdu_graph_by_date, shanghai_graph_by_date
import networkx as nx
import numpy.polynomial.polynomial as poly
from numpy import array
import numpy
from networkx.algorithms import k_core
import os
import csv
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.font_manager as fm
import seaborn as sns
from chart.date_related import get_data_with_size

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def work(chengdu=True):
    data = list()
    if chengdu:
        result = chengdu_graph_by_date()
        p = os.path.join(base_dir, '分阶段数据/分支数量.csv')
    else:
        result = shanghai_graph_by_date()
        p = os.path.join(base_dir, '上海分阶段数据/分支数量.csv')

    for key in result.keys():
        g = result[key]
        core = k_core(g, 2)
        branch_nodes = list()
        nb = 0
        if len(core.nodes) != 0:
            for node in g.nodes:
                if node not in core.nodes:
                    branch_nodes.append(node)
            for node in branch_nodes:
                for i in core.nodes:
                    if i in g.neighbors(node):
                        nb += 1
        data.append({'date': key.strftime("%Y-%m-%d"), 'nb': nb})
    with open(p, 'a') as f:
        w = csv.DictWriter(f, ['date', 'nb'])
        w.writeheader()
        w.writerows(data)


def remove_zero(x, y):
    result_x = list()
    result_y = list()
    for i in range(0, len(y)):
        if y[i] != 0:
            result_y.append(y[i])
            result_x.append(x[i])
    return result_x, result_y


def draw():
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(dpi=200)
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    x1, y1 = get_data_with_size("分支数量", "nb")
    x1, y1 = remove_zero(x1, y1)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_adjustable("datalim")
    p1, = ax.plot(x1, y1, 'o')
    x2, y2 = get_data_with_size("分支数量", "nb", "分阶段数据")
    x2, y2 = remove_zero(x2, y2)
    x = array(x1 + x2)
    y = array(y1 + y2)
    x = numpy.log10(x)
    y = numpy.log10(y)
    result = poly.polyfit(x, y, 1)
    a = result[0]
    b = result[1]
    p2, = ax.plot(x2, y2, '^')
    ax.set_xlabel("规模", fontproperties=song)
    ax.set_ylabel("分支数量", fontproperties=song)
    ax.legend(
        [p1, p2],
        [u'上海', u'成都'],
        prop=dict(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    )
    ax.set_xlim(1e1, 1e3)
    ax.set_ylim(1e0, 1e2)

    new_x = numpy.linspace(30, 400)
    ffit = 10 ** (b * numpy.log10(new_x) + a)
    ax.plot(new_x, ffit)

    print("b:{}".format(b))
    print("a:{}".format(a))

    plt.show()


if __name__ == "__main__":
    draw()
