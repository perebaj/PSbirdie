import json
import requests

def proxied_get(url):
    proxies = {
        'https': '147.135.7.122:3128',
        'http': '35.235.115.241'
    }
    headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' }
    return requests.get(url, proxies=proxies, headers=headers)

def run(event, context):
    url = 'https://www.lowes.com'
    page = requests.get(url)
    page_with_headers = proxied_get(url)
    print('Response with request UA')
    print(page)
    print('Response with workarounds')
    print(page_with_headers)

