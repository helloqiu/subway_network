# -*- coding: utf-8 -*-

import os
import csv
from graph import get_chengdu_subway_graph, chengdu_graph_by_date
from networkx.algorithms.centrality import betweenness_centrality

base_dir = os.path.join(os.path.dirname(__file__), '../data/')


def bc_list(with_7th=True):
    if with_7th:
        result = betweenness_centrality(get_chengdu_subway_graph())
    else:
        result = betweenness_centrality(get_chengdu_subway_graph(with_7th_line=False))
    l = list()
    for key in result:
        l.append((key, result[key]))
    return sorted(l, key=lambda s: s[1], reverse=True)


def work():
    result = bc_list()
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

    result = bc_list(with_7th=False)
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


def bc_with_date():
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


def average_bc():
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


if __name__ == "__main__":
    average_bc()
