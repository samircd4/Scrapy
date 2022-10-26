import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        for link in response.css('h3>a::attr(href)').getall():
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.bookDetail)
        
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    
    def bookDetail(self, response):
        name = response.css('h1::text').get()
        price = response.css('.price_color::text').get().replace('£', '')
        stock = response.css('p.instock.availability').get().split('(')[-1].split(')')[0].replace(' available', '')
        rating_star = response.css('p.star-rating::attr(class)').get().split(' ')[1]
        link = response.url
        data = {
            'Name': name,
            'Price': price,
            'Stock': stock,
            'Rating_star': rating_star,
            'Link': link
        }
        yield data