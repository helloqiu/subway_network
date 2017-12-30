# -*- coding: utf-8 -*-

import requests
import os
import csv

NAME_LIST = ['一号线', '二号线', '三号线', '四号线', '十号线', '七号线']
with open('key.txt', 'r') as f:
    key = f.read()
url = 'http://restapi.amap.com/v3/geocode/geo'


def get_location_with_line(name):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/{}.csv'.format(name)),
              encoding='utf-8') as f:
        reader = csv.DictReader(f)
        result = list()
        for row in reader:
            na = row['车站名称']
            n = '成都市{}地铁站'.format(na)
            print('Getting location for:{}'.format(n))
            r = get_location(n)['geocodes'][0]['location']
            r = {'lat': r[r.find(',') + 1:], 'lng': r[:r.find(',')]}
            print('latitude:{}, longitude:{}'.format(r['lat'], r['lng']))
            result.append({'name': na, 'latitude': r['lat'], 'longitude': r['lng']})
    return result


def get_location(name):
    r = requests.get(url, params={'address': name, 'key': key})
    return r.json()


if __name__ == "__main__":
    result = list()
    for name in NAME_LIST:
        result = result + get_location_with_line(name)
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/location.csv'), 'a') as f:
        c = csv.DictWriter(f, ['name', 'latitude', 'longitude'])
        c.writeheader()
        c.writerows(result)
