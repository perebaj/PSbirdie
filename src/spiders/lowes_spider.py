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
from src.sqs.client import send_message

SELECTOR = {
    "URL": '#mainContent > div.categorylist > div > div > div > h6 > a ::attr(href)'
}

class LowesSpider(scrapy.Spider):
    name = 'LowesSpider'
    URL = 'https://www.lowes.com'
    product_queue_url = 'https://sqs.us-east-2.amazonaws.com/268650732939/refrigerators-urls'
    review_queue_url = 'https://sqs.us-east-2.amazonaws.com/268650732939/reviews_url'

    products_id_list = []

    def start_requests(self):

        urls = ['https://www.lowes.com/c/Refrigerators-Appliances']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.href_parse)

    def href_parse(self, response):
        refrigerators_href_list = response.css(SELECTOR['URL']).getall()
        for url in refrigerators_href_list:
            url_list = self.URL + url
            yield scrapy.Request(url=url_list, callback=self.page_parse, dont_filter=True)

    def page_parse(self, response):
        data = json.loads(re.findall(
            '__PRELOADED_STATE__ = ([^<]+)</script>', str(response.text))[0])
        total_items = int(data['itemCount'])
        items_per_page = 36
        num_pages = 1 if int(total_items/items_per_page) == 0 else int(total_items/items_per_page)+1
        for page in range(num_pages):
            newPage = response.url + f"?offset={(items_per_page*page)}"
            yield scrapy.Request(url=newPage, callback=self.id_parse, dont_filter=True)

    def id_parse(self, response):
        data = json.loads(re.findall(
            '__PRELOADED_STATE__ = ([^<]+)</script>', str(response.text))[0])
        for product in data['itemList']:
            product_id = product['product']['omniItemId']
            product_detail_href = f'/pd/{product_id}/productdetail/2707/Guest'
            product_review_href = f'/rnr/r/get-by-product/{product_id}/pdp/prod'
            product_detail_url = self.URL + product_detail_href
            product_review_url = self.URL + product_review_href
            print(f"- Send url {product_review_url}...")
            # print(f"- send message {product_review_url}...")

            # send_message(product_detail_url, self.product_queue_url)
            send_message(product_review_url, self.review_queue_url)
