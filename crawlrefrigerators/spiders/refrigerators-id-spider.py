#!/usr/bin/python3
# -*- coding: utf-8 -

import scrapy
import pickle
import re
import json


class RefrigeratorsHrefSpider(scrapy.Spider):
    name = 'RefrigeratorsIds'
    URL = 'https://www.lowes.com'
    products_id = []

    def start_requests(self):
        urls = ['https://www.lowes.com/c/Refrigerators-Appliances']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.href_parse)

    def href_parse(self, response):
        refrigerators_href = response.css(
            '#mainContent > div.categorylist > div > div > div > h6 > a ::attr(href)').getall()
        for url in refrigerators_href:
            refrigerators_url = self.URL + url
            yield scrapy.Request(url=refrigerators_url, callback=self.page_parse)

    def page_parse(self, response):
        data = json.loads(re.findall(
            '__PRELOADED_STATE__ = ([^<]+)</script>', str(response.text))[0])
        itemsPage = int(data['itemCount'])
        numPages = 1 if int(itemsPage/36) == 0 else int(itemsPage/36)+1
        for page in range(numPages):
            newPage = response.url + f"?offset={(36*page)}"
            yield scrapy.Request(url=newPage, callback=self.id_parse)

    def id_parse(self, response):
        data = json.loads(re.findall(
            '__PRELOADED_STATE__ = ([^<]+)</script>', str(response.text))[0])
        for products in data['itemList']:
            self.products_id.append(products['product']['omniItemId'])
        print(len(self.products_id))
