# -*- coding: utf-8 -*-

import os
import csv
from multiprocessing import Process, Lock, Queue
from queue import Empty
from matplotlib import rc
import matplotlib.font_manager as fm
from attack import random_attack, largest_degree_attack, highest_bc_attack, shanghai_random_attack, \
    shanghai_largest_degree_attack, shanghai_highest_bc_attack
from networkx.algorithms.efficiency import global_efficiency
import seaborn as sns
import matplotlib.pyplot as plt

d = 0.005
base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../data')
marker_size = 6
line_width = 0.6


def random_attack_efficiency():
    result = list()
    lock = Lock()
    queue = Queue()
    result_queue = Queue()

    def worker(id, q, lock, result):
        while True:
            try:
                fraction = q.get(block=False)
                print(">>> Worker {}:".format(id))
                print("Random attack with fraction: %.3f" % fraction)
                # Do 100 times and get average num
                e = 0
                for j in range(0, 100):
                    g = random_attack(fraction)
                    e += global_efficiency(g)
                e = e / 100
                print(">>> Worker {}:".format(id))
                print("Get e: %f" % e)
                with lock:
                    result.put({
                        'fraction': "%.3f" % fraction,
                        'efficiency': e
                    })
            except Empty:
                return

    for i in range(0, 100):
        queue.put(i * d)
    t_list = list()

    for i in range(0, 4):
        t = Process(target=worker, args=(i, queue, lock, result_queue))
        t_list.append(t)
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
    while not result_queue.empty():
        result.append(result_queue.get())

    with open(os.path.join(base_dir, 'attack/random_attack.csv'), 'a') as f:
        w = csv.DictWriter(f, ['fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


def get_delta(x, y):
    new_x = list()
    new_y = list()
    last = y[0]
    for i in range(1, len(x)):
        new_x.append(x[i])
        new_y.append(y[i] - last)
        last = y[i]
    return new_x, new_y


def chart():
    song = fm.FontProperties(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    sns.set(style='ticks', palette='Set2')
    plt.figure(dpi=200)
    c = {'family': 'sans-serif', 'sans-serif': ['Times New Roman', 'NSimSun'], 'size': 10.5}
    rc('font', **c)
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(num=1, figsize=(3.54, 2.26))
    plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    fraction = list()
    random_efficiency = list()
    largest_degree_efficiency = list()
    highest_bc_efficiency = list()
    highest_bt_efficiency = list()
    # with open(os.path.join(base_dir, 'new_attack/shanghai_random_attack_with_random_protect.csv'), 'r') as f:
    # with open(os.path.join(base_dir, 'attack/random_attack.csv'), 'r') as f:
    with open(os.path.join(base_dir, '攻击与核-分支关系/成都/random.csv'), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            fraction.append(float(row['fraction']))
            random_efficiency.append(float(row['result']))
    x1, y1 = zip(*sorted(zip(fraction, random_efficiency)))
    # x1, y1 = get_delta(x1, y1)
    p1, = ax.plot(x1, y1)
    p2, = ax.plot(x1, y1, '*')

    fraction.clear()
    # with open(os.path.join(base_dir, 'new_attack/shanghai_largest_degree_attack.csv'), 'r') as f:
    # with open(os.path.join(base_dir, 'new_attack/largest_degree_attack_with_random_protect.csv'), 'r') as f:
    with open(os.path.join(base_dir, '攻击与核-分支关系/成都/largest_degree.csv'), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            fraction.append(float(row['fraction']))
            largest_degree_efficiency.append(float(row['result']))
    x2, y2 = zip(*sorted(zip(fraction, largest_degree_efficiency)))
    # x2, y2 = get_delta(x2, y2)
    p3, = ax.plot(x2, y2)
    p4, = ax.plot(x2, y2, '^',)

    fraction.clear()
    # with open(os.path.join(base_dir, 'new_attack/shanghai_highest_bc_attack.csv'), 'r') as f:
    # with open(os.path.join(base_dir, 'attack/highest_bc_attack.csv'), 'r') as f:
    with open(os.path.join(base_dir, '攻击与核-分支关系/成都/highest_bc.csv'), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            fraction.append(float(row['fraction']))
            highest_bc_efficiency.append(float(row['result']))
    x3, y3 = zip(*sorted(zip(fraction, highest_bc_efficiency)))
    # x3, y3 = get_delta(x3, y3)
    p5, = ax.plot(x3, y3,)
    p6, = ax.plot(x3, y3, 'o',)

    fraction.clear()
    # with open(os.path.join(base_dir, 'new_attack/shanghai_highest_bt_attack.csv'), 'r') as f:
    # with open(os.path.join(base_dir, 'attack/highest_bt_attack.csv'), 'r') as f:
    with open(os.path.join(base_dir, '攻击与核-分支关系/成都/highest_bt.csv'), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            fraction.append(float(row['fraction']))
            highest_bt_efficiency.append(float(row['result']))
    x4, y4 = zip(*sorted(zip(fraction, highest_bt_efficiency)))
    # x4, y4 = get_delta(x4, y4)
    p7, = ax.plot(x4, y4,)
    p8, = ax.plot(x4, y4, 'v',)

    ax = plt.gca()
    ax.set_xlabel('攻击节点比例', fontproperties=song)
    ax.set_ylabel('攻击节点在核上比例', fontproperties=song)
    ax.legend(
        [(p1, p2), (p3, p4), (p5, p6), (p7, p8)],
        ['随机攻击', '度优先攻击', '介数中心性优先攻击',
         '广度优先树优先攻击'],
        prop=dict(fname=os.path.join(base_dir, '../simsun.ttc'), size=10.5)
    )

    plt.show()


def largest_degree_attack_efficiency():
    result = list()
    for i in range(0, 100):
        fraction = i * d
        print("Largest degree attack with fraction %.3f" % fraction)
        g = largest_degree_attack(fraction)
        result.append({
            'fraction': "%.3f" % fraction,
            'efficiency': global_efficiency(g)
        })
    with open(os.path.join(base_dir, 'attack/largest_degree_attack.csv'), 'a') as f:
        w = csv.DictWriter(f, ['fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


def highest_bc_attack_efficiency():
    result = list()
    for i in range(0, 100):
        fraction = i * d
        print("Highest BC attack with fraction %.3f" % fraction)
        g = highest_bc_attack(fraction)
        result.append({
            'fraction': "%.3f" % fraction,
            'efficiency': global_efficiency(g)
        })
    with open(os.path.join(base_dir, 'attack/highest_bc_attack.csv'), 'a') as f:
        w = csv.DictWriter(f, ['fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


def shanghai_worker(id, q, lock, result):
    while True:
        try:
            fraction = q.get(block=False)
            print(">>> Worker {}:".format(id))
            print("Random attack with fraction: %.3f" % fraction)
            # Do 100 times and get average num
            e = 0
            for j in range(0, 100):
                print(">>>Worker {} No {} attack.".format(id, j))
                g = shanghai_random_attack(fraction)
                e += global_efficiency(g)
            e = e / 100
            print(">>> Worker {}:".format(id))
            print("Get e: %f" % e)
            with lock:
                result.put({
                    'fraction': "%.3f" % fraction,
                    'efficiency': e
                })
        except Empty:
            return


def shanghai_random_attack_efficiency():
    result = list()
    lock = Lock()
    queue = Queue()
    result_queue = Queue()

    for i in range(0, 100):
        queue.put(i * d)
    t_list = list()

    for i in range(0, 4):
        t = Process(target=shanghai_worker, args=(i, queue, lock, result_queue))
        t_list.append(t)
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
    while not result_queue.empty():
        result.append(result_queue.get())

    with open(os.path.join(base_dir, 'shanghai_attack/random_attack.csv'), 'a') as f:
        w = csv.DictWriter(f, ['fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


def shanghai_largest_degree_attack_efficiency():
    result = list()
    for i in range(0, 100):
        fraction = i * d
        print("Largest degree attack with fraction %.3f" % fraction)
        g = shanghai_largest_degree_attack(fraction)
        result.append({
            'fraction': "%.3f" % fraction,
            'efficiency': global_efficiency(g)
        })
    with open(os.path.join(base_dir, 'shanghai_attack/largest_degree_attack.csv'), 'a') as f:
        w = csv.DictWriter(f, ['fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


def shanghai_highest_bc_attack_efficiency():
    result = list()
    for i in range(0, 100):
        fraction = i * d
        print("Highest BC attack with fraction %.3f" % fraction)
        g = shanghai_highest_bc_attack(fraction)
        result.append({
            'fraction': "%.3f" % fraction,
            'efficiency': global_efficiency(g)
        })
    with open(os.path.join(base_dir, 'shanghai_attack/highest_bc_attack.csv'), 'a') as f:
        w = csv.DictWriter(f, ['fraction', 'efficiency'])
        w.writeheader()
        w.writerows(result)


if __name__ == "__main__":
    chart()
