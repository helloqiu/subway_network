# -*- coding: utf-8 -*-

import os
import csv
import networkx as nx
from collections import OrderedDict
from datetime import datetime

NAME_LIST = ['一号线', '二号线', '三号线', '四号线', '十号线', '七号线']


def single_subway_graph(name):
    g = nx.Graph()
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/{}.csv'.format(name)),
              encoding='utf-8') as f:
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


def subway_graph_without_7th_line():
    g = nx.Graph()
    temp_list = NAME_LIST
    temp_list.remove('七号线')
    for name in temp_list:
        g = nx.compose(g, single_subway_graph(name))
    return g


def graph_by_data():
    result = dict()
    for name in NAME_LIST:
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/{}.csv'.format(name)),
                  encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = datetime.strptime(row['开通时间'], "%Y-%m-%d")
                if t not in result.keys():
                    result[t] = [row['车站名称']]
                else:
                    if row['车站名称'] not in result[t]:
                        result[t].append(row['车站名称'])
    return OrderedDict(sorted(result.items()))
