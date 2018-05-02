# -*- coding: utf-8 -*-

from graph import get_chengdu_subway_graph
import seaborn as sns
import matplotlib.pyplot as plt
from networkx.algorithms.centrality import betweenness_centrality


def bc_degree_relativity():
    network = get_chengdu_subway_graph()
    bc_list = betweenness_centrality(network)
    degree_list = dict()
    for node in network.nodes:
        degree_list[node] = network.degree(node)
    sns.set(style='ticks', palette='Set2')
    plt.figure(dpi=200)
    x = list()  # degree
    y = list()  # bc
    for i in degree_list.keys():
        x.append(degree_list[i])
        y.append(bc_list[i])
    x1, y1 = zip(*sorted(zip(x, y)))
    p2, = plt.plot(x1, y1, 'o', ms=4)
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    plt.xlabel('Degree')
    plt.ylabel('BC')
    plt.show()


if __name__ == "__main__":
    bc_degree_relativity()
