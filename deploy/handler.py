import json
import requests

def run(event, context):
    url = 'https://www.lowes.com'
    page = requests.get(url)
    print(page)

