# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import os
import csv
import seaborn as sns

base_dir = os.path.join(os.path.dirname(__file__), '../../data/')


def size_diameter_data():
    s = list()
    with open(os.path.join(base_dir, "分阶段数据/规模.csv"), 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            s.append(int(row['size']))
    diameter = list()
    with open(os.path.join(base_dir, "分阶段数据/网络直径.csv"), 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            diameter.append(int(row['diameter']))
    return s, diameter


if __name__ == "__main__":
    sns.set()
    size, diameter = size_diameter_data()
    plt.figure(dpi=200)
    x, y = zip(*sorted(zip(size, diameter)))
    plt.plot(x, y)
    plt.plot(x, y, 'o')
    plt.ylabel('L')
    plt.xlabel('N')
    plt.show()
