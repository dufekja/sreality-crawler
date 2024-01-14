import scrapy

# https://www.sreality.cz/en/search/for-sale/apartments?page=1
# https://www.sreality.cz/api/en/v2/estates?page=1

get_exact_url = lambda url, page: f"{url}?noredirect=1&page={page}"

class SrealitySpider(scrapy.Spider):
    
    meta = { 'playwright' : True }
    count, page = 1, 1
    running = True    

    def __init__(self, config):
        self.name = config['name']
        self.url = config['start_urls'][0]
        self.limit = config['limit']


    def start_requests(self):
        yield scrapy.Request(url=get_exact_url(self.url, self.page), meta=self.meta, callback=self.parse)

    def parse(self, response):
        
        for property in response.css(".property"):
            yield {
                'title' : property.css(".name::text").get(),
                'img_url': property.css("img::attr(src)").getall()[0]
            }

            self.count += 1
            if self.count > self.limit:
                self.running = False
                break
        
        if self.running:
            self.page += 1
            yield scrapy.Request(url=get_exact_url(self.url, self.page), meta=self.meta, callback=self.parse)
