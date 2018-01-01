# -*- coding: utf-8 -*-

import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

NAME_LIST = ['一号线', '二号线', '三号线', '四号线', '十号线', '七号线']


def get_locations(name):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/{}.csv'.format(name)),
              encoding='utf-8') as f:
        reader = csv.DictReader(f)
        result = list()
        for row in reader:
            na = row['车站名称']
            n = '成都市{}地铁站'.format(na)
            result.append(n)
    return result


def search_locations():
    result = list()
    for name in NAME_LIST:
        result = result + get_locations(name)
    browser = webdriver.Chrome()
    browser.get('http://www.gpsspg.com/maps.htm')
    data = list()
    for name in result:
        ele = browser.find_element_by_xpath('//*[@id="s_t"]')
        ele.send_keys(name)
        ele.send_keys(Keys.RETURN)
        time.sleep(5)
        ele = browser.find_element_by_xpath('//*[@id="curr_xy"]')
        text = ele.get_attribute('innerHTML')
        lat = text[:text.find(',')]
        lng = text[text.find(',') + 1: text.find('北纬') - 1]
        print('地点:{} 北纬:{} 东经:{}'.format(name, lat, lng))
        data.append({
            'name': name,
            'latitude': lat,
            'longitude': lng
        })
        ele = browser.find_element_by_xpath('//*[@id="s_t"]')
        ele.clear()
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/location_gpsspg.csv'), 'a') as f:
        c = csv.DictWriter(f, ['name', 'latitude', 'longitude'])
        c.writeheader()
        c.writerows(data)


def delete_duplicate_data():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/location_gpsspg.csv'),
              encoding='utf-8') as f:
        reader = csv.DictReader(f)
        result = list()
        for r in reader:
            name = r['name']
            name = name.replace('成都市', '')
            name = name.replace('地铁站', '')
            temp = {
                'name': name,
                'latitude': r['latitude'],
                'longitude': r['longitude']
            }
            if temp not in result:
                result.append(temp)

    with open(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/locations_without_duplicate.csv'),
            'a') as f:
        c = csv.DictWriter(f, ['name', 'latitude', 'longitude'])
        c.writeheader()
        c.writerows(result)


if __name__ == "__main__":
    delete_duplicate_data()
