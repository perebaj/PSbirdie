from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.spiders.lowes_spider import LowesSpider
from multiprocessing.context import Process
from src.spiders.refrigerator_spider import RefrigeratorsSpider

process = CrawlerProcess(get_project_settings())
process.crawl(LowesSpider)
process.start()



