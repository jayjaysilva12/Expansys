from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from ..items import ExpansysItem
from datetime import datetime
import re

class ExpansysSpider(CrawlSpider):
    ctr=0
    name = 'expansys'
    allowed_domains = ['expansys.com.sg']
    start_urls = ['http://www.expansys.com.sg/']
    rules = [Rule(LxmlLinkExtractor(allow=r'.+/\S+-\d+/'),callback='parse_items',follow=True)]    

    item = ExpansysItem()
    
    def parse_items(self, response):
        items = []
        item = ExpansysItem()
        for r in response.xpath('//div[@id="prod_core"]'):
            item['title'] = r.xpath('//h1[@itemprop="name"]/text()').extract() or None
            item['urls'] =  response.url or None
            item['price'] = r.xpath('//p[@id="price"]/strong/span/text()').extract()
            checkmate = r.xpath('//ul[@class="product-sku"]/li').extract()
            for c in checkmate:
              sku = re.search(r'sku:(\w+)',str(c))
              ean = re.search(r'ean:(\w+)',str(c))
              upc = re.search(r'upc:(\w+)',str(c))
              mfr = re.search(r'mpn:(\w+)',str(c))
              brand = re.search(r'"brand">(\w+)',str(c))
              if sku:
                item['sku'] = sku.group(1)
              if ean:
                item['ean'] = ean.group(1)
              if upc:
                item['upc'] = upc.group(1)
              if mfr:
                item['mpn'] = mfr.group(1)
              if brand:
                item['brand'] = brand.group(1)
            items.append(item)
        return(items)