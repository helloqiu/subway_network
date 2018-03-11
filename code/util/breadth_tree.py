# -*- coding: utf-8 -*-

import networkx as nx
from copy import deepcopy


def get_bt_list(G):
    bc_tree = get_bc_tree(G)
    result = list()
    for i in bc_tree.nodes():
        temp = deepcopy(bc_tree)
        temp.remove_node(i)
        nodes_in_gcc = len(giant_connected_component(temp).nodes())
        result.append({'node': i, 'bt': 1 / nodes_in_gcc})
    return sorted(result, key=lambda node: node['bt'], reverse=True)


def giant_connected_component(G):
    return max(nx.connected_component_subgraphs(G.to_undirected()), key=len)


def get_bc_tree(G):
    d = nx.degree_centrality(G)
    node = max(d, key=lambda n: d[n])
    return nx.bfs_tree(G, node)
