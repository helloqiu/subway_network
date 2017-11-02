# -*- coding: utf-8 -*-

from code.graph import subway_graph
import networkx as nx
import json


def generate_node_link_data():
    G = subway_graph()
    data = nx.node_link_data(G)
    with open('node_link.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


if __name__ == '__main__':
    generate_node_link_data()
