import matplotlib.pyplot as plt
import networkx as nx
from code.graph import subway_graph


def draw_photo():
    G = subway_graph()
    e = G.edges(data=True)
    pos = nx.spring_layout(G, iterations=7000, k=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_nodes(G, pos, node_size=10)
    nx.draw_networkx_edges(G, pos, edgelist=e, width=0.4)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_family='Adobe Heiti Std', font_size=1)
    nx.draw_networkx_labels(G, pos, font_size=1, font_family='Adobe Heiti Std')

    plt.axis('off')
    plt.savefig('地铁拓扑图.png', dpi=2000)


if __name__ == '__main__':
    draw_photo()
