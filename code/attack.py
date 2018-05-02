# -*- coding: utf-8 -*-

import os
from graph import get_chengdu_subway_graph, get_shanghai_subway_graph
from random import choice
from betweenness_centrality_list import bc_list
from util.breadth_tree import get_bt_list
from networkx.algorithms.efficiency import global_efficiency
import csv

base_dir = os.path.join(os.path.dirname(__file__), '../data/')
d = 0.005


def random_attack(fraction=0.0):
    g = get_chengdu_subway_graph()
    for i in random_attack_list(g, fraction):
        g.remove_node(i)
    return g


def shanghai_random_attack(fraction=0.0):
    g = get_shanghai_subway_graph()
    for i in random_attack_list(g, fraction):
        g.remove_node(i)
    return g


def largest_degree_attack(fraction=0.0):
    g = get_chengdu_subway_graph()
    for i in largest_degree_attack_list(g, fraction):
        g.remove_node(i)
    return g


def shanghai_largest_degree_attack(fraction=0.0):
    g = get_shanghai_subway_graph()
    for i in largest_degree_attack_list(g, fraction):
        g.remove_node(i)
    return g


def highest_bc_attack(fraction=0.0):
    g = get_chengdu_subway_graph()
    for i in highest_bc_attack_list(g, fraction):
        g.remove_node(i)
    return g


def shanghai_highest_bc_attack(fraction=0.0):
    g = get_shanghai_subway_graph()
    for i in shanghai_highest_bc_attack_list(g, fraction):
        g.remove_node(i)
    return g


def random_attack_list(G, fraction=0.0):
    nodes_num = len(G)
    remove_num = int(fraction * nodes_num)
    result = list()
    for i in range(0, remove_num):
        while True:
            temp = choice(list(G.nodes))
            if temp not in result:
                break
        result.append(temp)
    return result


def largest_degree_attack_list(G, fraction=0.0):
    nodes_num = len(G)
    remove_num = int(fraction * nodes_num)
    result = list()
    degrees = list()
    for node in list(G.nodes):
        degrees.append({
            'name': node,
            'degree': G.degree[node]
        })
    degrees.sort(key=lambda s: s['degree'], reverse=True)
    for i in range(0, remove_num):
        result.append(degrees[i]['name'])
    return result


def highest_bc_attack_list(G, fraction=0.0):
    nodes_num = len(G)
    remove_num = int(fraction * nodes_num)
    result = list()
    bc = bc_list(get_chengdu_subway_graph())
    for i in range(0, remove_num):
        result.append(bc[i][0])
    return result


def shanghai_highest_bc_attack_list(G, fraction=0.0):
    nodes_num = len(G)
    remove_num = int(fraction * nodes_num)
    result = list()
    bc = bc_list(get_shanghai_subway_graph())
    for i in range(0, remove_num):
        result.append(bc[i][0])
    return result


def highest_bt_attack_list(G, fraction=0.0):
    nodes_num = len(G)
    remove_num = int(fraction * nodes_num)
    result = list()
    bt_list = get_bt_list(G)
    for i in range(0, remove_num):
        result.append(bt_list[i]['node'])
    return result


if __name__ == "__main__":
    with open(os.path.join(base_dir, 'shanghai_attack/highest_bt_attack.csv'), 'a') as f:
        result = list()
        for i in range(0, 100):
            attack_fraction = d * i
            print("Attack fraction: {}".format(attack_fraction))
            g = get_shanghai_subway_graph()
            attack_list = highest_bt_attack_list(g, fraction=attack_fraction)
            for node in attack_list:
                g.remove_node(node)
            result.append({'fraction': attack_fraction, 'efficiency': global_efficiency(g)})
        w = csv.DictWriter(f, ['fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)
