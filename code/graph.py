# -*- coding: utf-8 -*-

import os
import csv
import networkx as nx
from collections import OrderedDict
from datetime import datetime
from util.breadth_tree import giant_connected_component

NAME_LIST = ['一号线', '二号线', '三号线', '四号线', '十号线', '七号线']
SHANGHAI_NAME_LIST = ['一号线', '二号线', '三号线', '四号线', '五号线', '六号线',
                      '七号线', '八号线', '九号线', '十号线', '十一号线', '十二号线',
                      '十三号线', '十六号线', '十七号线']


def _single_subway_graph(path):
    """
    Generate a graph with the specified path.
    :param path: The path of the metadata file.
    :return: A graph.
    """
    g = nx.Graph()
    with open(path,
              encoding='utf-8') as f:
        reader = csv.DictReader(f)
        last = None
        for row in reader:
            g.add_node(row['车站名称'])
            if row['站间距离（km）'] != '-' and row['站间距离（km）'] != '－' and row['站间距离（km）'] != '':
                g.add_edge(row['车站名称'], last, weight=float(row['站间距离（km）']))
            elif row['站间距离（km）'] == '':
                g.add_edge(row['车站名称'], last)
            last = row['车站名称']

    return g


def get_chengdu_subway_graph(with_7th_line=True):
    """
    Get chengdu subway graph.
    :param with_7th_line: Whether add the 7th line.
    :return: A graph.
    """
    g = nx.Graph()
    for name in NAME_LIST:
        if with_7th_line is True or name != '七号线':
            g = nx.compose(g, _single_subway_graph(
                path=os.path.join(os.path.dirname(__file__), '../data/chengdu_metadata/{}.csv'.format(name))))
    return g


def get_shanghai_subway_graph():
    """
    Get shanghai subway graph.
    :return: A graph
    """
    g = nx.Graph()
    for name in SHANGHAI_NAME_LIST:
        g = nx.compose(g, _single_subway_graph(
            path=os.path.join(os.path.dirname(__file__), '../data/shanghai_metadata/{}.csv'.format(name))))
    return g


def _nodes_by_date(path_list):
    """
    Get all nodes with date.
    :param path_list: The metadata path list.
    :return: A OrderedDict.
    """
    result = dict()
    for path in path_list:
        with open(path,
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


def chengdu_nodes_by_date():
    """
    Get all nodes in chengdu with date.
    :return: An OrderedDict
    """
    path_list = []
    for name in NAME_LIST:
        path_list.append(os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '../data/chengdu_metadata/{}.csv'.format(name)))
    return _nodes_by_date(path_list)


def shanghai_nodes_by_date():
    path_list = []
    for name in SHANGHAI_NAME_LIST:
        path_list.append(os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '../data/shanghai_metadata/{}.csv'.format(name)))
    return _nodes_by_date(path_list)


def chengdu_graph_by_date():
    """
    Get a graph of chengdu by date.
    :return:
    """
    nodes = chengdu_nodes_by_date()
    n = list()
    result = dict()
    for key in nodes:
        n = n + nodes[key]
        g = get_chengdu_subway_graph()
        temp = list()
        for i in g.nodes:
            if i not in n:
                temp.append(i)
        g.remove_nodes_from(temp)
        temp = list()
        for i in g.edges:
            if (i[0] not in n) or (i[1] not in n):
                temp.append(i)
        g.remove_edges_from(temp)
        result[key] = g
    return OrderedDict(sorted(result.items()))


def shanghai_graph_by_date():
    nodes = shanghai_nodes_by_date()
    n = list()
    result = dict()
    for key in nodes:
        n = n + nodes[key]
        g = get_shanghai_subway_graph()
        temp = list()
        for i in g.nodes:
            if i not in n:
                temp.append(i)
        g.remove_nodes_from(temp)
        temp = list()
        for i in g.edges:
            if (i[0] not in n) or (i[1] not in n):
                temp.append(i)
        g.remove_edges_from(temp)
        result[key] = giant_connected_component(g)
    return OrderedDict(sorted(result.items()))
