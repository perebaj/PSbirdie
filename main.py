from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.spiders.lowes_spider import LowesSpider
from multiprocessing.context import Process
from src.spiders.refrigerator_spider import RefrigeratorsSpider
from src.spiders.reviews_spiders import ReviewsSpider

process = CrawlerProcess(get_project_settings())
process.crawl(ReviewsSpider)
process.start()



