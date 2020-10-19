#!/usr/bin/python3
# -*- coding: utf-8 -

import scrapy
import json
from datetime import datetime
from src.database import put_table

class RefrigeratorsSpider(scrapy.Spider):
    name = 'RefrigeratorsSpider'
    URL = 'https://www.lowes.com'

    def start_requests(self):
        self.load()
        for refrigerator_id in self.refrigerators_id_list[:5]:
            product_detail_href = f'/pd/{refrigerator_id}/productdetail/2707/Guest'
            url = self.URL + product_detail_href
            print(url)
            yield scrapy.Request(url=url, callback=self.product_detail_parse)

    def product_detail_parse(self, response):
        product = response.json()
        details = product.get('productDetails')
        product_id = list(details.keys())[0]
        product = details.get(product_id).get('product')
        category_id = list(product.get('categories').keys())[0]
        category_name = product.get('categories').get(category_id).replace('_', ' ')
        brand = product.get('brand')
        description = product.get('description')
        pdURL = product.get('pdURL')
        product_url = self.URL + pdURL
        current_time_date = datetime.now().isoformat()
        product_dict = {
            "product_id": product_id,
            "category": category_name,
            "brand": brand,
            "description": description,
            "product_url": product_url,
            "date-time": current_time_date,
        
        }
        put_table(product)

    def load(self):
        f = open('product-dump.json', "r")
        self.refrigerators_id_list = json.load(f)

    def save(self, product):
        json.dump(product, open('products.json', 'w'))
