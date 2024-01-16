import hydra
import psycopg2

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

from spider import SrealitySpider

INSERT_PROPERTY = lambda property : f"""
    INSERT INTO properties (title, img_url) VALUES ('{property['title']}', '{property['img_url']}')
"""

def db_connect(config):
    """ Connect to database and return connection object """
    return psycopg2.connect(
        host = 'db',
        port = '5432',
        database = config['database'],
        user = config['user'],
        password = config['password']
    )
    

def get_results(config):
    """ Get result from crawler based on config """
    
    # connect dispatcher to save each property object into results
    results = []
    def spider_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(spider_results, signal=signals.item_scraped)

    # run spider in process model
    process = CrawlerProcess(settings=dict(config['settings']))
    process.crawl(SrealitySpider, config=config['spider'])
    process.start()

    return results


@hydra.main(version_base=None, config_path='../../conf', config_name='config')
def main(config):
    print('\n')
    print('-' * 30)

    # get results from crawler
    results = get_results(config['crawler'])
    print('Scraped items:', len(results))

    # connect to database and insert results
    try:
        conn = db_connect(config['db']['db'])

        with conn.cursor() as cur:
            for property in results:
                cur.execute(INSERT_PROPERTY(property))

            conn.commit()
        conn.close()

        print('DB updated')
    except Exception as err:
        print('DB err:', err)


if __name__ == '__main__':
    main()


