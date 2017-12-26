# -*- coding: utf-8 -*-

import os
import csv
from graph import subway_graph, subway_graph_without_7th_line
from networkx.algorithms.centrality import betweenness_centrality

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def bc_list(with_7th=True):
    if with_7th:
        result = betweenness_centrality(subway_graph())
    else:
        result = betweenness_centrality(subway_graph_without_7th_line())
    l = list()
    for key in result:
        l.append((key, result[key]))
    return sorted(l, key=lambda s: s[1], reverse=True)


if __name__ == "__main__":
    result = bc_list()
    l = list()
    for i in result:
        l.append({
            'name': i[0],
            'BC': i[1]
        })
    with open(os.path.join(base_dir, 'BC排序-七号线开通后.csv'), 'a', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['name', 'BC'])
        w.writeheader()
        w.writerows(l)

    result = bc_list(with_7th=False)
    l = list()
    for i in result:
        l.append({
            'name': i[0],
            'BC': i[1]
        })
    with open(os.path.join(base_dir, 'BC排序-七号线开通前.csv'), 'a', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['name', 'BC'])
        w.writeheader()
        w.writerows(l)
