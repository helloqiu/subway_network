# -*- coding: utf-8 -*-

import os
import csv
from multiprocessing import Process, Lock, Queue
from queue import Empty
from code.attack import random_attack, largest_degree_attack
from networkx.algorithms.efficiency import global_efficiency
import seaborn as sns
import matplotlib.pyplot as plt

d = 0.005
base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


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


def chart():
    fraction = list()
    random_efficiency = list()
    largest_degree_efficiency = list()
    with open(os.path.join(base_dir, 'attack/random_attack.csv'), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            fraction.append(float(row['fraction']))
            random_efficiency.append(float(row['efficiency']))
    sns.set(style='ticks', palette='Set2')
    plt.figure(dpi=200)
    x1, y1 = zip(*sorted(zip(fraction, random_efficiency)))
    p1, = plt.plot(x1, y1)
    p2, = plt.plot(x1, y1, '*')

    fraction.clear()
    with open(os.path.join(base_dir, 'attack/largest_degree_attack.csv'), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            fraction.append(float(row['fraction']))
            largest_degree_efficiency.append(float(row['efficiency']))
    x2, y2 = zip(*sorted(zip(fraction, largest_degree_efficiency)))
    p3, = plt.plot(x2, y2)
    p4, = plt.plot(x2, y2, '^')

    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    plt.xlabel('Fraction of the removed nodes')
    plt.ylabel('Network efficiency')
    ax.legend([(p1, p2), (p3, p4)], ['Random attacks', 'Largest degree node-based attacks'])

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


if __name__ == "__main__":
    chart()
