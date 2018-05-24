# -*- coding: utf-8 -*-

from graph import chengdu_graph_by_date, shanghai_graph_by_date
import networkx as nx
from networkx.algorithms import k_core
import os
import csv
from graph import get_chengdu_subway_graph, get_shanghai_subway_graph

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def core(chengdu=True):
    data = list()
    if chengdu:
        result = chengdu_graph_by_date()
        p = os.path.join(base_dir, '分阶段数据/核分析.csv')
    else:
        result = shanghai_graph_by_date()
        p = os.path.join(base_dir, '上海分阶段数据/核分析.csv')
    for key in result.keys():
        g = result[key]
        core = k_core(g, 2)
        nb = len(g.nodes()) - len(core.nodes())
        nc = len(core.nodes())
        b = nb / (nb + nc)
        temp = 0
        count = 0
        if nc != 0:
            for i in core.nodes:
                d = core.degree(i)
                temp += d
                if d == 2:
                    count += 1
            average_degree = temp / nc
            f = count / nc
        else:
            average_degree = 0
            f = 0
        data.append({'date': key.strftime("%Y-%m-%d"), 'b': b, 'average_degree': average_degree, 'f': f})
    with open(p, 'a') as f:
        w = csv.DictWriter(f, ['date', 'b', 'average_degree', 'f'])
        w.writeheader()
        w.writerows(data)


if __name__ == "__main__":
    # work(chengdu=False)
    g = get_chengdu_subway_graph()
    core = k_core(g, 2)
    print('成都:')
    print(len(core.nodes) / len(g.nodes))
    g = get_shanghai_subway_graph()
    core = k_core(g, 2)
    print('上海:')
    print(len(core.nodes) / len(g.nodes))
