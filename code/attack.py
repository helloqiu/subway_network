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
