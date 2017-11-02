# -*- coding: utf-8 -*-

from code.graph import subway_graph
import networkx as nx

if __name__ == '__main__':
    G = subway_graph()
    nx.write_gexf(G, 'subway_graph.gexf')
