import scrapy
from datetime import datetime as dt

class iherbSpider(scrapy.Spider):
    
    name = "iherbSpider"
    
    def start_requests(self):
        urls = [
            'https://www.iherb.com/c/Coffee?p=1'
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page_with_products)
    
    def parse_page_with_products(self, response):
        products_urls = response.xpath('//*/div[@class="product ga-product col-xs-12 col-sm-12 col-md-8 col-lg-6"]/a/@href').extract()
        
        for url in products_urls:
            yield scrapy.Request(url=url, callback=self.GetDataFromPage)
        
        next_page = response.xpath('//*/a[@class="pagination-next"]/@href').extract_first()
        if next_page is not None:
            print('\n>>>>>>>>>>>> NEXT PAGE >>>>>>>>>>>>>>>>\n')
            yield response.follow(next_page, callback=self.parse_page_with_products)
        else:
            yield "\nnext_page part not worked\n"
        
        
    def GetDataFromPage(self, response):
        time = dt.now().strftime('%d.%m.%y %H:%M:%S')
        title = response.xpath('//*/h1[@id="name"]/text()').extract_first()
        product_url = response.url
        image_url = response.xpath('//*/div[@class="image-container"]/div/div/a/@href').extract_first()
        price_raw = response.xpath('//*/div[@id="price"]/text()').extract_first().strip()
        price = price_raw[1:]
            
        currency = price_raw[:1]
        if currency is '$':
            currency = "USD"
            
        try:
            product_rating = response.xpath('//*/div[@class="rating"]/a/i/@title').extract_first()[:3]
        except TypeError:
            product_rating = "-"
            
        reviews_amount = response.xpath('//*/a[@class="rating-count"]/span/text()').extract_first()
            
            
        return dict({
            "time": time,
            "title": title,
            "product_url": product_url,
            "image_url": image_url,
            "site": "iherb.com",
            "location": "USA",
            "price": price,
            "currency": currency,
            "product_rating": product_rating,
            "reviews_amount": reviews_amount,
        })