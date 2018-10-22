import scrapy
import logging
import gzip
import sys
from scrapy.utils.log import configure_logging
from datetime import datetime as dt
from items import BestcoffeeItem

class AmazonSpider(scrapy.Spider):
    
    name = "amazonSpider"
    time_for_log = dt.now().strftime('-%d%m%y-%H%M%S')
    
    # Logging spider output
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=name+time_for_log+'.log',
        format='%(levelname)s: %(message)s',
        level=logging.INFO,
    #    stream=sys.stdout,
    )
    
    #with gzip.GzipFile(filename="log.gz", mode='wb') as gz:
    #    gz.write(sys.stdout)
    
    def start_requests(self):
        urls = [
            'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=coffee'
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page_with_products)
    
    def parse_page_with_products(self, response):
        items_urls = response.xpath('//*/a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href').extract()

        for raw_url in items_urls:
            url = response.urljoin(raw_url)
            yield scrapy.Request(url=url, callback=self.GetDataFromPage)
        
        next_page = response.xpath('//*/span[@class="pagnRA"]/a/@href').extract_first()
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            logging.info("\n>>>>>>>>>>>>>>>>>>> NEXT PAGE >>>>>>>>>>>>>>>>>>>>>\n")
            yield response.follow(next_page, callback=self.parse_page_with_products)
        else:
            yield "\nnext_page part not worked\n"
            
    def GetDataFromPage(self, response):
        time = dt.now().strftime('%d.%m.%y %H:%M:%S')
        title = response.xpath('//*/span[@id="productTitle"]/text()').extract_first().strip()
        product_url = response.url
        image_url = response.xpath('//*/div[@id="imgTagWrapperId"]/img/@data-a-dynamic-image').extract_first()
        price = response.xpath('//*/span[@class="a-size-large a-color-price"]/text()').extract_first()
        
        if price is None:
            try:
                price = response.xpath('//*/span[@class="a-size-medium a-color-price"]/text()').extract_first().strip()
            except:
                price = "-"
        else:
            price = price.strip()
        
        if price is not "-" and '$' in price:
            currency = "USD"
            price = price[1:]
        
        try:    
            product_rating = response.xpath('//*/div[@id="averageCustomerReviews"]/span/span/span/a/i/span/text()').extract_first().strip()[:3]
        except:
            product_rating = "-"
            
        reviews_amount_raw = response.xpath('//*/div[@id="averageCustomerReviews"]/span[3]/a/span/text()').extract_first()
        reviews_amount = "".join([i for i in reviews_amount_raw if i.isdigit()])


        product_items = BestcoffeeItem(time = time, 
                                        title = title, 
                                        product_url = product_url, 
                                        image_url = image_url,
                                        price = price,
                                        currency = currency,
                                        site = site,
                                        location = location,
                                        product_rating = product_rating
                                        )
        yield BestcoffeeItem

        """
        return dict({
                "time": time,
                "title": title,
                "product_url": product_url,
                "image_url": image_url,
                "site": "amazon",
                "location": "USA",
                "price": price,
                "currency": currency,
                "product_rating": product_rating,
                "reviews_amount": reviews_amount,
            })
        """
