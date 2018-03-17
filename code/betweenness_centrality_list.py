# -*- coding: utf-8 -*-

import os
import csv
from graph import get_chengdu_subway_graph, chengdu_graph_by_date
from networkx.algorithms.centrality import betweenness_centrality

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def bc_list(g):
    """
    生成降序 BC 排列的节点 list。
    :param g: 要分析的 Graph
    :return: 一个 list
    """
    result = betweenness_centrality(g)
    l = list()
    for key in result:
        l.append((key, result[key]))
    return sorted(l, key=lambda s: s[1], reverse=True)


def generate_chengdu_bc_list():
    """
    生成成都BC排序的结果。
    :return:
    """
    result = bc_list(get_chengdu_subway_graph())
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

    result = bc_list(get_chengdu_subway_graph(with_7th_line=False))
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


def chengdu_bc_with_date():
    """
    分阶段的BC排序。
    :return:
    """
    result = chengdu_graph_by_date()
    for k in result.keys():
        s = betweenness_centrality(result[k])
        l = list()
        for key in s:
            l.append((key, s[key]))
        l = sorted(l, key=lambda t: t[1], reverse=True)
        temp = list()
        for i in l:
            temp.append({
                'name': i[0],
                'BC': i[1]
            })
        with open(os.path.join(base_dir, '分阶段数据/{}.csv'.format(k.strftime("%Y-%m-%d"))), 'a') as f:
            w = csv.DictWriter(f, ['name', 'BC'])
            w.writeheader()
            w.writerows(temp)


def chengdu_average_bc():
    """
    分阶段的成都平均BC。
    :return:
    """
    result = chengdu_graph_by_date()
    l = list()
    for k in result.keys():
        s = betweenness_centrality(result[k])
        count = 0
        for i in s:
            count += s[i]
        l.append({
            'date': k.strftime("%Y-%m-%d"),
            'average_bc': count / len(s)
        })
    with open(os.path.join(base_dir, 'average_bc.csv'), 'a') as f:
        w = csv.DictWriter(f, ['date', 'average_bc'])
        w.writeheader()
        w.writerows(l)
