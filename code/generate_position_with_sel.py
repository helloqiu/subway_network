# -*- coding: utf-8 -*-

import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

NAME_LIST = ['一号线', '二号线', '三号线', '四号线', '十号线', '七号线']
SHANGHAI_NAME_LIST = ['一号线', '二号线', '三号线', '四号线', '五号线', '六号线',
                      '七号线', '八号线', '九号线', '十号线', '十一号线', '十二号线',
                      '十三号线', '十六号线', '十七号线']


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


def get_shanghai_nodes_names(name):
    with open(os.path.join(os.path.dirname(__file__), '../data/shanghai_metadate/{}.csv'.format(name)),
              encoding='utf-8') as f:
        reader = csv.DictReader(f)
        result = list()
        for row in reader:
            na = row['车站名称']
            result.append('上海{}地铁站'.format(na))
    return result


class element_change_content(object):
    """
    An exception for checking if an element changes its content.
    """

    def __init__(self, locator, content):
        self.locator = locator
        self.content = content

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.content != element.get_attribute('innerHTML'):
            self.content = element.get_attribute('innerHTML')
            return element
        else:
            return False


def search_locations():
    result = list()
    for name in SHANGHAI_NAME_LIST:
        result = result + get_shanghai_nodes_names(name)
    browser = webdriver.Chrome()
    browser.get('http://www.gpsspg.com/maps.htm')
    data = list()
    ele = browser.find_element_by_xpath('//*[@id="curr_xy"]')
    text = ele.get_attribute('innerHTML')
    for name in result:
        ele = browser.find_element_by_xpath('//*[@id="s_t"]')
        ele.send_keys(name)
        ele.send_keys(Keys.RETURN)
        try:
            WebDriverWait(browser, timeout=10).until(element_change_content(
                (By.XPATH, '//*[@id="curr_xy"]'),
                text))
        except TimeoutException:
            print('搜索"{}"失败。'.format(name))
            continue
        time.sleep(1)
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
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/shanghai_location_gpsspg.csv'),
              'a', encoding='utf-8') as f:
        c = csv.DictWriter(f, ['name', 'latitude', 'longitude'])
        c.writeheader()
        c.writerows(data)


def delete_duplicate_data():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/shanghai_location_gpsspg.csv'),
              encoding='utf-8') as f:
        reader = csv.DictReader(f)
        result = list()
        for r in reader:
            name = r['name']
            name = name.replace('上海', '')
            name = name.replace('地铁站', '')
            temp = {
                'name': name,
                'latitude': r['latitude'],
                'longitude': r['longitude']
            }
            if temp not in result:
                result.append(temp)

    with open(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/shanghai_locations_without_duplicate.csv'),
            'a', encoding='utf-8') as f:
        c = csv.DictWriter(f, ['name', 'latitude', 'longitude'])
        c.writeheader()
        c.writerows(result)


if __name__ == "__main__":
    delete_duplicate_data()
