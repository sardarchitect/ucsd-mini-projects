import scrapy


class XpathSpider(scrapy.Spider):
    name = "toscrape-xpath"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')[0].xpath('//span[@class="text"]/text()').getall()
        authors = response.xpath('//div[@class="quote"]')[0].xpath('//small[@class="author"]/text()').getall()
	
        for i in range(len(quotes)):
            yield {
                'text': quotes[i],
                'author': authors[i],
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)