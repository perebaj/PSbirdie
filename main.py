from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.spiders.lowes_spider import LowesSpider
from src.spiders.refrigerator_spider import RefrigeratorsSpider
from src.spiders.reviews_spiders import ReviewsSpider
from multiprocessing.context import Process
from src.spiders.refrigerator_spider import RefrigeratorsSpider
import sys


if sys.argv[1] == '--publisher':
    process = CrawlerProcess(get_project_settings())
    process.crawl(LowesSpider)
    process.start()


if sys.argv[1] == '--product-worker':
    process = CrawlerProcess(get_project_settings())
    process.crawl(RefrigeratorsSpider)
    process.start()


if sys.argv[1] == '--review-worker':
    process = CrawlerProcess(get_project_settings())
    process.crawl(ReviewsSpider)
    process.start()

