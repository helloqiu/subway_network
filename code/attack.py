# -*- coding: utf-8 -*-

from graph import get_chengdu_subway_graph, get_shanghai_subway_graph
from random import choice
from betweenness_centrality_list import bc_list
from util.breadth_tree import get_bt_list


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
