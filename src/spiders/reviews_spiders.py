#!/usr/bin/python3
# -*- coding: utf-8 -

import scrapy
import json
from src.dynamodb.database import put_table
from datetime import datetime


class ReviewsSpider(scrapy.Spider):

    name = 'ReviewSpider'
    URL = 'https://www.lowes.com'
    reviews_list = []

    def start_requests(self):
        self.load()
        # for refrigerator_id in self.refrigerators_id_list[:3]:
        refrigerator_id = self.refrigerators_id_list[3]
        product_detail_href = f'/rnr/r/get-by-product/{refrigerator_id}/pdp/prod'
        url = self.URL + product_detail_href
        yield scrapy.Request(url=url, callback=self.page_parse)

    def page_parse(self, response):
        product = response.json()
        total_results = product.get('TotalResults')
        print(total_results)
        limit = product.get('Limit')
        numPages = 1 if int(
            total_results/limit) == 0 else int(total_results/limit)+1
        url = response.url

        for page in range(numPages):
            offset = f'?offset={(limit*page)}'
            page_review = url + offset
            print(page_review)
            yield scrapy.Request(url=page_review, callback=self.get_reviews_parse)

    def get_reviews_parse(self, response):
        product = response.json()
        result_list = product.get('Results')
        for result in result_list:
            rating = result.get('Rating')
            reviews_id = result.get('Id')
            product_id = result.get('ProductId')
            is_recommended = result.get('IsRecommended')
            review = result.get('ReviewText')
            review_info = {
                'reviews_id': reviews_id,
                'product_id': product_id,
                'rating': rating,
                'is_recommended': is_recommended,
                'review': review
            }
            print(review_info)
            # put_table(review_info, 'Reviews')

    def load(self):
        f = open('json/product-dump.json', "r")
        self.refrigerators_id_list = json.load(f)

    def save(self, product):
        json.dump(product, open('json/reviews.json', 'w'))
