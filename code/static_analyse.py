# -*- coding: utf-8 -*-

from graph import get_chengdu_subway_graph
import collections


def degree():
    G = get_chengdu_subway_graph()
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degree_count = collections.Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())
    print(deg)
    print(cnt)


if __name__ == "__main__":
    degree()
