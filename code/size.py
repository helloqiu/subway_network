# -*- coding: utf-8 -*-

from graph import shanghai_graph_by_date
import os
import csv

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def size():
    result = shanghai_graph_by_date()
    l = list()
    for k in result.keys():
        g = result[k]
        l.append({
            'date': k.strftime("%Y-%m-%d"),
            'size': len(g.nodes)
        })
    with open(os.path.join(base_dir, '上海分阶段数据/规模.csv'), 'a') as f:
        w = csv.DictWriter(f, ['date', 'size'])
        w.writeheader()
        w.writerows(l)


if __name__ == "__main__":
    size()
