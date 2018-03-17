# -*- coding: utf-8 -*-

from code.graph import get_chengdu_subway_graph
import networkx as nx
import csv

if __name__ == '__main__':
    G = get_chengdu_subway_graph()
    nx.write_weighted_edgelist(G, 'subway_graph.csv')
    l = list()
    with open('subway_graph_node.csv', 'a', encoding='utf-8') as f:
        for node in G.nodes:
            l.append({
                'label': node
            })
        c = csv.DictWriter(f, ['label'])
        c.writeheader()
        c.writerows(l)
