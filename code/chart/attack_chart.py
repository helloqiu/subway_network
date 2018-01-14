# -*- coding: utf-8 -*-

import os
import csv
from multiprocessing import Process, Lock, Queue
from queue import Empty
from code.attack import random_attack
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


def random_attack_chart():
    fraction = list()
    efficiency = list()
    with open(os.path.join(base_dir, 'attack/random_attack.csv'), 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            fraction.append(float(row['fraction']))
            efficiency.append(float(row['efficiency']))
    sns.set(style='ticks', palette='Set2')
    plt.figure(dpi=200)
    x1, y1 = zip(*sorted(zip(fraction, efficiency)))
    plt.plot(x1, y1)
    plt.plot(x1, y1, '*')
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    plt.xlabel('Fraction of the removed nodes')
    plt.ylabel('Network efficiency')

    plt.show()


if __name__ == "__main__":
    random_attack_chart()
