# -*- coding: utf-8 -*-

import os
import csv
import networkx as nx

NAME_LIST = ['一号线', '二号线', '三号线', '四号线', '十号线']


def single_subway_graph(name):
    g = nx.Graph()
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/{}.csv'.format(name))) as f:
        reader = csv.DictReader(f)
        last = None
        for row in reader:
            g.add_node(row['车站名称'])
            if row['站间距离（km）'] != '-':
                g.add_edge(row['车站名称'], last, weight=float(row['站间距离（km）']))
            last = row['车站名称']

    return g


def subway_graph():
    g = nx.Graph()
    for name in NAME_LIST:
        g = nx.compose(g, single_subway_graph(name))
    return g
