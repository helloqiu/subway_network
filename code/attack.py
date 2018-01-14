# -*- coding: utf-8 -*-

from graph import subway_graph
from random import choice


def random_attack(fraction=0.0):
    g = subway_graph()
    nodes_num = len(g)
    remove_num = int(fraction * nodes_num)
    for i in range(0, remove_num):
        n = choice(list(g.nodes))
        g.remove_node(n)
    return g


def largest_degree_attack(fraction=0.0):
    g = subway_graph()
    nodes_num = len(g)
    remove_num = int(fraction * nodes_num)
    # Get all degree
    degrees = list()
    for node in list(g.nodes):
        degrees.append({
            'name': node,
            'degree': g.degree[node]
        })
    degrees.sort(key=lambda s: s['degree'], reverse=True)
    for i in range(0, remove_num):
        g.remove_node(degrees[i]['name'])
    return g
