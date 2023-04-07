import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]
    
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
    }
    
    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        
        quotes.extend(response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        )
        
        next_page_link = response.xpath(
            '//nav/ul[@class="pager"]/li[@class="next"]/a/@href'
        ).get()
        
        if(next_page_link):
            yield response.follow(
                next_page_link, 
                callback=self.parse_only_quotes,
                cb_kwargs={'quotes': quotes}
            )
        else:
            yield { 'quotes': quotes }
    
    def parse(self, response):
        
        title = response.xpath('//h1/a/text()').get()
        
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()'
        ).getall()
        
        tags = response.xpath(
            '//div[contains(@class, "tags-box")]//a[contains(@class, "tag")]/text()'
        ).getall()
        
        yield {
            'title': title,
            'tags': tags
        }
        
        next_page_link = response.xpath(
            '//nav/ul[@class="pager"]/li[@class="next"]/a/@href'
        ).get()
        
        if(next_page_link):
            yield response.follow(
                next_page_link, 
                callback=self.parse_only_quotes,
                cb_kwargs={'quotes': quotes}
            )