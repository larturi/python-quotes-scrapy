import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]
    
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['lea@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'SpiderQuotesUser',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
        
    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            authors = kwargs['authors']
        
        quotes.extend(response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        )
        
        authors.extend(response.xpath(
            '//small[@class="author"]/text()').getall()
        )
        
        next_page_link = response.xpath(
            '//nav/ul[@class="pager"]/li[@class="next"]/a/@href'
        ).get()
        
        if(next_page_link):
            yield response.follow(
                next_page_link, 
                callback=self.parse_only_quotes,
                cb_kwargs={'quotes': quotes, 'authors': authors}
            )
        else:
            # quotes_author = list(zip(quotes, authors))
            quotes_author = []
            
            for i in range(1, len(quotes)):
                quotes_author.append({
                    'quote': quotes[i],
                    'author': authors[i],
                })
            
            yield { 'quotes': quotes_author }
    
    def parse(self, response):
        
        title = response.xpath('//h1/a/text()').get()
        
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        
        authors = response.xpath('//small[@class="author"]/text()').getall()
        
        tags = response.xpath(
            '//div[contains(@class, "tags-box")]//a[contains(@class, "tag")]/text()'
        ).getall()
        
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            tags = tags[:top]

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
                cb_kwargs={'quotes': quotes ,'authors': authors}
            )
