# -*- coding: utf-8 -*-

import csv
import os

if __name__ == "__main__":
    l = list()
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/gephi_edge.csv'), 'r',
              encoding='utf-8') as f:
        r = csv.DictReader(f)
        names = r.fieldnames
        for row in r:
            l.append(row)
    for item in l:
        item['Label'] = item['Weight']

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/gephi_edge_with_label.csv'), 'a',
              encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=names)
        w.writeheader()
        w.writerows(l)
