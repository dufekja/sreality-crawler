import hydra

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

from spider import SrealitySpider
from database.database import DatabaseSreality

def get_results(config):
    results = []

    def spider_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(spider_results, signal=signals.item_scraped)

    process = CrawlerProcess(settings=dict(config['settings']))
    process.crawl(SrealitySpider, config=config['spider'])
    process.start()

    return results

@hydra.main(version_base=None, config_path='../conf', config_name='config')
def main(config):

    crawler_conf, db_conf = config['crawler'], config['db']
    results = get_results(crawler_conf)

    print(len(results))
    

if __name__ == '__main__':
    main()


