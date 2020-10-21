#!/usr/bin/python3
# -*- coding: utf-8 -

# from src.dynamodb.database import put_table
import scrapy
import pickle
import re
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import boto3
from src.dynamodb.database import put_table

SELECTOR = {
    "URL": '#mainContent > div.categorylist > div > div > div > h6 > a ::attr(href)'
}

class LowesSpider(scrapy.Spider):
    name = 'LowesSpider'
    URL = 'https://www.lowes.com'
    products_id = []

    def start_requests(self):
        urls = ['https://www.lowes.com/c/Refrigerators-Appliances']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.href_parse)

    def href_parse(self, response):
        refrigerators_href_list = response.css(SELECTOR['URL']).getall()
        for url in refrigerators_href_list:
            url_list = self.URL + url
            yield scrapy.Request(url=url_list, callback=self.page_parse)

    def page_parse(self, response):
        data = json.loads(re.findall(
            '__PRELOADED_STATE__ = ([^<]+)</script>', str(response.text))[0])
        total_items = int(data['itemCount'])
        items_per_page = 36
        numPages = 1 if int(total_items/items_per_page) == 0 else int(total_items/items_per_page)+1
        for page in range(numPages):
            newPage = response.url + f"?offset={(items_per_page*page)}"
            yield scrapy.Request(url=newPage, callback=self.id_parse)

    def id_parse(self, response):
        data = json.loads(re.findall(
            '__PRELOADED_STATE__ = ([^<]+)</script>', str(response.text))[0])

        id_list = [product['product']['omniItemId'] for product in data['itemList']]
        self.products_id += id_list
        self.save(self.products_id)
        # for product in data['itemList']:
            # product_id = {
                # 'product_id': product['product']['omniItemId']
            # }
            # print(product_id)
            # put_table(product_id, 'Refrigerators_Id')
    
    def save(self, products_id_list):
        json.dump(products_id_list, open('json/product-id2.json', 'w'))
