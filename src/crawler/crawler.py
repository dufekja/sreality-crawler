import hydra
import psycopg2

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

from spider import SrealitySpider

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

INSERT_PROPERTY = lambda property : f"""
    INSERT INTO properties (title, img_url) VALUES ('{property['title']}', '{property['img_url']}')
"""

@hydra.main(version_base=None, config_path='../../conf', config_name='config')
def main(config):
    crawler_conf, db_conf = config['crawler'], config['db']

    results = get_results(crawler_conf)

    print('\n')
    print('-' * 30)

    print('Scraped items:', len(results))

    try:
        # create db connection
        conn = psycopg2.connect(**db_conf['db'])

        # put scraped data into db
        with conn.cursor() as cur:
            for property in results:
                cur.execute(INSERT_PROPERTY(property))

            conn.commit()
        conn.close()
        print('DB updated')

    except:
        print('DB error')


if __name__ == '__main__':
    main()


