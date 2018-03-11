# -*- coding: utf-8 -*-

import os
import csv
from attack import random_attack_list, largest_degree_attack_list, highest_bc_attack_list, highest_bt_attack_list
from graph import subway_graph
from networkx.algorithms.efficiency import global_efficiency

d = 0.01
base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


def highest_bt_attack_with_highest_bc_attack_efficiency():
    result = list()
    for i in range(0, 50):
        attack_fraction = d * i
        print('attack fraction: %.2f' % attack_fraction)
        for j in range(0, 50):
            g = subway_graph()
            attack_list = highest_bc_attack_list(g, fraction=attack_fraction)
            protect_fraction = d * j
            print('\t protect fraction: %.2f' % protect_fraction)
            protect_list = highest_bt_attack_list(g, fraction=protect_fraction)
            for node in attack_list:
                if node not in protect_list:
                    g.remove_node(node)
            result.append({
                'attack_fraction': "%.2f" % attack_fraction,
                'protect_fraction': "%.2f" % protect_fraction,
                'efficiency': global_efficiency(g)
            })
    with open(os.path.join(base_dir, 'attack/highest_bt_attack_with_highest_bc_attack_efficiency.csv'), 'a') as f:
        w = csv.DictWriter(f, ['attack_fraction', 'protect_fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


if __name__ == "__main__":
    highest_bt_attack_with_highest_bc_attack_efficiency()
