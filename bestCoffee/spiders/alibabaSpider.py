import scrapy
from datetime import datetime as dt

class alibabaSpider(scrapy.Spider):
    """
    
    Not worked correct.
    
    """
    
    name = "alibabaSpider"
    
    def start_requests(self):
        urls = [
            'https://www.alibaba.com/products/F0/coffee_ground/----------------------10.html'
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page_with_products)
    
    def parse_page_with_products(self, response):
        self.items_amount = len(response.xpath('//*/div[@class="m-product-item    "]').extract())
        
        self.items_amount = 2

        for item in range(self.items_amount):
            self.product_url = response.xpath('//*/div[@class="m-product-item    "]/div/div/div/div/div/h2[@class="title"]/a/@href').extract()[item]
            yield scrapy.Request(url=self.product_url, callback=self.GetDataFromPage)
        
        """
        next_page = response.xpath('//*/span[@class="pagnRA"]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_page_with_products)
        else:
            yield "\nnext_page part not worked\n"
        """
        
    def GetDataFromPage(self, response):
        self.time = dt.now().strftime('%d.%m.%y %H:%M:%S')
        self.title = response.xpath('//*/div[@class="ma-title-wrap"]/h1/span/text()').extract_first().strip()
        self.product_url = response.url
        
        """
        self.image_url = response.xpath('//*/div[@id="imgTagWrapperId"]/img/@data-a-dynamic-image').extract_first()
        
        self.price = response.xpath('//*/span[@class="a-size-large a-color-price"]/text()').extract_first()
        if self.price is None:
            try:
                self.price = response.xpath('//*/span[@class="a-size-medium a-color-price"]/text()').extract_first().strip()
            except:
                self.price = "-"
        else:
            self.price = self.price.strip()
        
        if self.price is not "-" and '$' in self.price:
            self.currency = "USD"
            self.price = self.price[1:]
        
        try:    
            product_rating = response.xpath('//*/div[@id="averageCustomerReviews"]/span/span/span/a/i/span/text()').extract_first().strip()[:3]
        except:
            product_rating = "-"
            
        reviews_amount_raw = response.xpath('//*/div[@id="averageCustomerReviews"]/span[3]/a/span/text()').extract_first()
        reviews_amount = "".join([i for i in reviews_amount_raw if i.isdigit()])
        """

        return dict({
                "time": self.time,
                "title": self.title,
                "product_url": self.product_url,
            })
            #    "image_url": self.image_url,
            #    "site": "amazon",
            #    "location": "USA",
            #    "price": self.price,
            #    "currency": self.currency,
            #    "product_rating": product_rating,
            #    "reviews_amount": reviews_amount,
            #})