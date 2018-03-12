# -*- coding: utf-8 -*-

import os
import csv
from attack import random_attack_list, largest_degree_attack_list, highest_bc_attack_list, highest_bt_attack_list
from graph import subway_graph
from networkx.algorithms.efficiency import global_efficiency

d = 0.02
base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


def attack_with_protect_efficiency(attack, protect):
    result = list()
    attack_name = attack.__name__.replace('_attack_list', '')
    protect_name = protect.__name__.replace('_attack_list', '')
    for i in range(0, 25):
        print('{} attack with {} protect:'.format(attack_name, protect_name))
        attack_fraction = d * i
        print('attack fraction: %.2f' % attack_fraction)
        for j in range(0, 25):
            g = subway_graph()
            attack_list = attack(g, fraction=attack_fraction)
            protect_fraction = d * j
            print('\t protect fraction: %.2f' % protect_fraction)
            protect_list = protect(g, fraction=protect_fraction)
            for node in attack_list:
                if node not in protect_list:
                    g.remove_node(node)
            result.append({
                'attack_fraction': "%.2f" % attack_fraction,
                'protect_fraction': "%.2f" % protect_fraction,
                'efficiency': global_efficiency(g)
            })
    with open(os.path.join(base_dir, 'attack/{}_attack_with_{}_protect.csv').format(attack_name, protect_name),
              'a') as f:
        w = csv.DictWriter(f, ['attack_fraction', 'protect_fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


if __name__ == "__main__":
    attack_with_protect_efficiency(attack=largest_degree_attack_list, protect=highest_bc_attack_list)
    attack_with_protect_efficiency(attack=highest_bc_attack_list, protect=highest_bc_attack_list)
    attack_with_protect_efficiency(attack=highest_bt_attack_list, protect=highest_bc_attack_list)
