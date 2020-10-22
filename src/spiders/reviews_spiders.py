#!/usr/bin/python3
# -*- coding: utf-8 -

import scrapy
import json
from src.dynamodb.database import put_table
from datetime import datetime
from src.sqs.client import send_message
from src.sqs.client import receive_message

class ReviewsSpider(scrapy.Spider):

    name = 'ReviewSpider'
    URL = 'https://www.lowes.com'
    reviews_list = []
    queue_url = 'https://sqs.us-east-2.amazonaws.com/268650732939/reviews_url'
    def start_requests(self):
        message = receive_message(self.queue_url)
        print(f"- Fetching url {message}...")

        if message:
            yield scrapy.Request(url=message, callback=self.page_parse, dont_filter=True)

    def page_parse(self, response):
        product = response.json()
        total_results = product.get('TotalResults')
        if total_results == 0:
            message = receive_message(self.queue_url)
            if message:
                yield scrapy.Request(url=message, callback=self.page_parse, dont_filter=True)

        limit = product.get('Limit')
        numPages = 1 if int(
            total_results/limit) == 0 else int(total_results/limit)+1
        url = response.url
        print(f"- Info {total_results}, {limit} {numPages}...")

        for page in range(numPages):
            offset = f'?offset={(limit*page)}'
            page_review = url + offset
            # send_message(page_review, self.queue_url)
            yield scrapy.Request(url=page_review, callback=self.get_reviews_parse, dont_filter=True)

    def get_reviews_parse(self, response):
        product = response.json()
        result_list = product.get('Results')
        for result in result_list:
            rating = result.get('Rating')
            review_id = result.get('Id')
            product_id = result.get('ProductId')
            is_recommended = result.get('IsRecommended')
            review = result.get('ReviewText')
            print(f"- Fetching review {review_id}, {product_id} {response.url}...")

            review_info = {
                'review_id': review_id,
                'product_id': product_id,
                'rating': rating,
                'is_recommended': is_recommended,
                'review': review
            }
            put_table(review_info,'Reviews')
            message = receive_message(self.queue_url)
            if message:
                yield scrapy.Request(url=message, callback=self.page_parse, dont_filter=True)

