# -*- coding: utf-8 -*-

import csv
import os


def convert_graph(with_7th=True):
    if not with_7th:
        file_name = "gephi_edge"
    else:
        file_name = "gephi_edge_with_7th"
    l = list()
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/{}.csv'.format(file_name)), 'r',
              encoding='utf-8') as f:
        r = csv.DictReader(f)
        names = r.fieldnames
        for row in r:
            l.append(row)
    for item in l:
        item['Label'] = item['Weight']

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/{}_with_label.csv'.format(file_name)),
              'a',
              encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=names)
        w.writeheader()
        w.writerows(l)


if __name__ == "__main__":
    convert_graph(with_7th=True)
