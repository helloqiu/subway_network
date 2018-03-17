# -*- coding: utf-8 -*-

from code.graph import get_chengdu_subway_graph
import networkx as nx

if __name__ == '__main__':
    G = get_chengdu_subway_graph()
    nx.write_gexf(G, 'subway_graph.gexf')
