#!/usr/bin/python3
# -*- coding: utf-8 -

import asyncio
from aiohttp import ClientSession
import json 

header = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}


async def fetch(url):
    async with ClientSession(headers=header) as session:
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            else:
                response = await response.json()
                return response['ratings']

async def fetch_all():
    URL = 'https://www.lowes.com'
    refrigerators_id_list = load()
    tasks_list = []
    
    for refrigerator_id in refrigerators_id_list[:70]:
        product_detail_href = f'/pd/{refrigerator_id}/productdetail/2707/Guest'
        url = URL + product_detail_href
        task = asyncio.create_task(fetch(url))
        tasks_list.append(task)
    results = await asyncio.gather(*tasks_list)
    print(results) 

def load():
    f = open('json/product-dump.json', "r")
    return json.load(f)

loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_all())