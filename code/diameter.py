# -*- coding: utf-8 -*-

import os
import csv
from graph import graph_by_date
from networkx.algorithms.distance_measures import diameter

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def get_diameter():
    l = list()
    result = graph_by_date()
    for k in result.keys():
        g = result[k]
        d = diameter(g)
        l.append({
            'date': k.strftime("%Y-%m-%d"),
            'diameter': d
        })
    with open(os.path.join(base_dir, '网络直径.csv'), 'a') as f:
        w = csv.DictWriter(f, ['date', 'diameter'])
        w.writeheader()
        w.writerows(l)


if __name__ == "__main__":
    get_diameter()
