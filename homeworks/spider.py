import scrapy
from scrapy.loader import ItemLoader


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def content_title_parser(self, mystr):
        return mystr[0].split(' ')[3]

    def parse(self, response):
        for url in response.css('ul li a::attr("href")').re('.*/category/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_titles)

    def parse_titles(self, response):
        l = ItemLoader(item=Posts(), response=response)
        l.add_css('content_title', 'h1.pagetitle::text', self.content_title_parser)
        l.add_css('post_title', 'div.entries > ul > li a::text')
        return l.load_item()


class Posts(scrapy.Item):
    content_title = scrapy.Field()
    post_title = scrapy.Field()
