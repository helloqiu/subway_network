# -*- coding: utf-8 -*-

import os
import csv


def relative_position():
    result = list()
    max_lat = 0
    max_lng = 0
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/locations_without_duplicate.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append(row)
            if float(row['latitude']) > max_lat:
                max_lat = float(row['latitude'])
            if float(row['longitude']) > max_lng:
                max_lng = float(row['longitude'])
    for i in result:
        i['latitude'] = (max_lat + 0.1 - float(i['latitude'])) * 5000
        i['longitude'] = (max_lng + 0.1 - float(i['longitude'])) * 5000
    return result


if __name__ == "__main__":
    result = relative_position()
    print(result)
