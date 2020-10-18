#!/usr/bin/python3
# -*- coding: utf-8 -

from .lowes_spider import LowesSpider
import scrapy
import json



class RefrigeratorsSpider(LowesSpider, scrapy.Spider):
    name = 'RefrigeratorsSpider'
    URL = 'https://www.lowes.com'
    product = {}
    def start_requests(self):
        self.load()
        for refrigerator_id in self.refrigerators_id_list[:10]:
            product_detail_href = f'/pd/{refrigerator_id}/productdetail/2707/Guest'
            # print(product_detail_href)
            url = self.URL + product_detail_href
            print(url)
            yield scrapy.Request(url=url, callback=self.product_detail_parse)
        # url = self.URL + f"/pd/{1000257811}" + "/productdetail/2707/Guest"
        # print(url)
        # yield scrapy.Request(url=url, callback=self.product_detail_parse)

    def product_detail_parse(self, response):
        product = response.json()
        details = product.get('productDetails')
        product_id = list(details.keys())[0]
        product = details.get(product_id).get('product')

        category =  product.get('categories')
        brand = product.get('brand')
        description = product.get('description')
        pdURL = product.get('pdURL')
        product = {
            "product_id": product_id,
            "category": category,
            "brand": brand,
            "description": description,
            "pdURL": pdURL, 
        }
        print(product)
        

    def load(self):
        f = open('product-dump.json', "r")
        self.refrigerators_id_list = json.load(f)

    def save(self):
        json.dump(self.products_id, open('product-dump.json', 'w'))