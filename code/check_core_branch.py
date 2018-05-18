# -*- coding: utf-8 -*-

import os
import csv
from attack import random_attack_list, largest_degree_attack_list, highest_bc_attack_list, highest_bt_attack_list
from attack import shanghai_highest_bc_attack_list
from graph import get_chengdu_subway_graph, get_shanghai_subway_graph
from networkx.algorithms import k_core
import networkx as nx
import copy

d = 0.02
base_dir = os.path.join(os.path.dirname(__file__), '../data/攻击与核-分支关系/成都')


def cal_core_branch(g, attack, fraction):
    result = 0
    core = k_core(g, 2)
    for i in range(0, 10):
        attack_list = attack(g, fraction)
        for node in attack_list:
            if node in core.nodes:
                result += 1
    result = result / 10.0
    result = result / len(attack_list)
    return result


def check_attack(g, attack):
    attack_name = attack.__name__.replace('_attack_list', '')
    result = list()
    fractions = list()
    for i in range(1, 25):
        fractions.append(i * d)
    for i in fractions:
        print(i)
        result.append({'fraction': i, 'result': cal_core_branch(g, attack, i)})
    with open(os.path.join(base_dir, '{}.csv'.format(attack_name)), 'a') as f:
        w = csv.DictWriter(f, ['fraction', 'result'])
        w.writeheader()
        w.writerows(result)


if __name__ == "__main__":
    g = get_chengdu_subway_graph()
    attack_list = [random_attack_list, largest_degree_attack_list, highest_bc_attack_list,
                   highest_bt_attack_list]
    for attack in attack_list:
        check_attack(g, attack)
