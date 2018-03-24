# -*- coding: utf-8 -*-

import os
import csv
from attack import random_attack_list, largest_degree_attack_list, highest_bc_attack_list, highest_bt_attack_list
from attack import shanghai_highest_bc_attack_list
from graph import get_chengdu_subway_graph, get_shanghai_subway_graph
from networkx.algorithms.efficiency import global_efficiency
from multiprocessing import Process

d = 0.02
base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


def attack_with_protect_efficiency(attack, protect):
    attack_name = attack.__name__.replace('_attack_list', '')
    protect_name = protect.__name__.replace('_attack_list', '')
    result = get_result(attack, protect)
    with open(os.path.join(base_dir, 'shanghai_attack/{}_attack_with_{}_protect.csv').format(attack_name, protect_name),
              'a') as f:
        w = csv.DictWriter(f, ['attack_fraction', 'protect_fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


def random_related_efficiency(attack, protect):
    attack_name = attack.__name__.replace('_attack_list', '')
    protect_name = protect.__name__.replace('_attack_list', '')
    result = None
    for i in range(0, 10):
        if result is None:
            result = get_result(attack, protect)
        else:
            temp = get_result(attack, protect)
            for r in range(0, len(result)):
                result[r]['efficiency'] += temp[r]['efficiency']
    for i in result:
        i['efficiency'] = i['efficiency'] / 10
    with open(os.path.join(base_dir, 'shanghai_attack/{}_attack_with_{}_protect.csv').format(attack_name, protect_name),
              'a') as f:
        w = csv.DictWriter(f, ['attack_fraction', 'protect_fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


def get_result(attack, protect):
    result = list()
    attack_name = attack.__name__.replace('_attack_list', '')
    protect_name = protect.__name__.replace('_attack_list', '')
    for i in range(0, 25):
        print('{} attack with {} protect:'.format(attack_name, protect_name))
        attack_fraction = d * i
        print('attack fraction: %.2f' % attack_fraction)
        for j in range(0, 25):
            # g = get_chengdu_subway_graph()
            g = get_shanghai_subway_graph()
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
    return result


if __name__ == "__main__":
    t_list = list()
    t = Process(target=attack_with_protect_efficiency, args=(largest_degree_attack_list, shanghai_highest_bc_attack_list))
    t_list.append(t)

    t = Process(target=attack_with_protect_efficiency,
                args=(shanghai_highest_bc_attack_list, shanghai_highest_bc_attack_list))
    t_list.append(t)

    t = Process(target=attack_with_protect_efficiency,
                args=(highest_bt_attack_list, shanghai_highest_bc_attack_list))
    t_list.append(t)

    t = Process(target=random_related_efficiency,
                args=(random_attack_list, shanghai_highest_bc_attack_list))
    t_list.append(t)

    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
