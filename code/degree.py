# -*- coding: utf-8 -*-

from graph import chengdu_graph_by_date
import os
import csv

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def degree_by_date():
    result = chengdu_graph_by_date()
    data = list()
    for key in result.keys():
        g = result[key]
        temp = 0
        for n in g.nodes:
            temp += g.degree(n)
        data.append({'date': key.strftime("%Y-%m-%d"), 'average_degree': temp / len(g.nodes)})
    with open(os.path.join(base_dir, '分阶段数据/平均度.csv'), 'a') as f:
        w = csv.DictWriter(f, ['date', 'average_degree'])
        w.writeheader()
        w.writerows(data)


if __name__ == "__main__":
    degree_by_date()
