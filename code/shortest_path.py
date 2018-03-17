# -*- coding: utf-8 -*-

import os
import csv
from graph import chengdu_graph_by_date
from networkx import average_shortest_path_length

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def average_shortest_path():
    result = chengdu_graph_by_date()
    l = list()
    for k in result.keys():
        g = result[k]
        length = average_shortest_path_length(g)
        l.append({
            'date': k.strftime("%Y-%m-%d"),
            'average_shortest_path_length': length
        })
    with open(os.path.join(base_dir, '平均最短路径.csv'), 'a') as f:
        w = csv.DictWriter(f, ['date', 'average_shortest_path_length'])
        w.writeheader()
        w.writerows(l)


if __name__ == "__main__":
    average_shortest_path()
