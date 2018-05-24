# -*- coding: utf-8 -*-

from graph import get_chengdu_subway_graph, get_shanghai_subway_graph
import seaborn as sns
import matplotlib.pyplot as plt
from networkx.algorithms.centrality import betweenness_centrality
import os
from matplotlib import rc
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data')


def bc_degree_relativity():
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    plt.figure(dpi=200)
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    network = get_shanghai_subway_graph()
    bc_list = betweenness_centrality(network)
    degree_list = dict()
    for node in network.nodes:
        degree_list[node] = network.degree(node)
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    x = list()  # degree
    y = list()  # bc
    for i in degree_list.keys():
        x.append(degree_list[i])
        y.append(bc_list[i])
    x1, y1 = zip(*sorted(zip(x, y)))
    p2, = ax.plot(x1, y1, 'o', ms=4)
    ax.set_xlabel('度', fontproperties=song)
    ax.set_ylabel('介数中心性', fontproperties=song)
    plt.show()


if __name__ == "__main__":
    bc_degree_relativity()
