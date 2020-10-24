#!/usr/bin/python3
# -*- coding: utf-8 -

import scrapy
import json
from datetime import datetime
from src.dynamodb.database import put_table
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.sqs.client import send_message, receive_message
from scrapy.logformatter import LogFormatter
import os
import logging


class RefrigeratorsSpider(scrapy.Spider):
    name = 'RefrigeratorsSpider'
    URL = 'https://www.lowes.com'
    queue_url = 'https://sqs.us-east-2.amazonaws.com/268650732939/refrigerators-urls'

    def start_requests(self):
        message = receive_message(self.queue_url)
        if message:
            yield scrapy.Request(url=message, callback=self.product_detail_parse, dont_filter=True)

    def product_detail_parse(self, response):
        product = response.json()
        details = product.get('productDetails')
        product_id = list(details.keys())[0]
        product = details.get(product_id).get('product')
        category_id = list(product.get('categories').keys())[0]
        category_name = product.get('categories').get(
            category_id).replace('_', ' ')
        brand = product.get('brand')
        description = product.get('description')
        pdURL = product.get('pdURL')
        product_url = self.URL + pdURL
        current_time_date = datetime.now().isoformat()

        print(f"- Fetching product {product_id}...")

        product_dict = {
            "product_id": product_id,
            "category": category_name,
            "brand": brand,
            "description": description,
            "product_url": product_url,
            "date-time": current_time_date,

        }
        put_table(item=product_dict)
        message = receive_message(self.queue_url)
        if message:
            yield scrapy.Request(url=message, callback=self.product_detail_parse, dont_filter=True)
