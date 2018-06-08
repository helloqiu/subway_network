# -*- coding: utf-8 -*-

from graph import chengdu_graph_by_date, shanghai_graph_by_date
from generate_relative_position import chengdu_relative_pos_dict
from networkx import node_link_data
import os
import json
import seaborn as sns

base_dir = os.path.join(os.path.dirname(__file__), '../data/')
work_dir = os.path.join(base_dir, 'nodes_link_分阶段数据')

if __name__ == "__main__":
    d = chengdu_relative_pos_dict()
    colors = sns.color_palette("Set2", 15).as_hex()
    g_list = chengdu_graph_by_date()
    p = os.path.join(work_dir, '成都')
    keys = list(g_list.keys())
    seen = list()
    groups = dict()
    num = 0
    for i in range(0, len(keys)):
        date = keys[i]
        g = g_list[date]
        data = node_link_data(g)
        result = dict(nodes=list(), edges=list())
        for n in data['nodes']:
            seen.append(n)
            if n['id'] in groups.keys():
                id = groups[n['id']]
            else:
                id = i + 1
                groups[n['id']] = id
            result['nodes'].append({
                'id': n['id'],
                'group': id,
                'color': colors[id - 1],
                'x': d[n['id']]['x'],
                'y': d[n['id']]['y'],
                'size': 1
            })
        for l in data['links']:
            seen.append(l)
            result['edges'].append({
                'source': l['source'],
                'target': l['target'],
                'value': 1,
                'id': '{}'.format(num)
            })
            num += 1
        with open(os.path.join(p, '{}.json'.format(i)), 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False))
