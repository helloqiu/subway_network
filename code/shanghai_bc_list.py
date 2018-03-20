# -*- coding: utf-8 -*-

import os
import csv
from graph import get_shanghai_subway_graph
from networkx.algorithms.centrality import betweenness_centrality

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def bc_list(g):
    """
    生成降序 BC 排列的节点 list。
    :param g: 要分析的 Graph
    :return: 一个 list
    """
    result = betweenness_centrality(g)
    l = list()
    for key in result:
        l.append((key, result[key]))
    return sorted(l, key=lambda s: s[1], reverse=True)


def generate_shanghai_bc_list():
    """
    生成成都BC排序的结果。
    :return:
    """
    result = bc_list(get_shanghai_subway_graph())
    l = list()
    for i in result:
        l.append({
            'name': i[0],
            'BC': i[1]
        })
    with open(os.path.join(base_dir, '上海BC排序.csv'), 'a', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['name', 'BC'])
        w.writeheader()
        w.writerows(l)


if __name__ == "__main__":
    generate_shanghai_bc_list()
