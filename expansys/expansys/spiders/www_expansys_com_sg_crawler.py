from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from ..items import ExpansysItem
from datetime import datetime
import re

class ExpansysSpider(CrawlSpider):
    ctr=0
    name = 'expansys'
    allowed_domains = ['expansys.com.sg']
    start_urls = ['http://www.expansys.com.sg/']
    rules = [Rule(LinkExtractor(allow=r'.+/.+/',deny=(r'.+/.+\d+/',r'.+.filter.+',r'.+.user.+',r'.+.aspx.+',r'.+signin.+','.+blog.+')),follow=True),
             Rule(LinkExtractor(allow=r'.+/\S+-\w+/?page=[0-9]+#=listing',deny=(r'.+.filter.+',r'.+.user.+',r'.+.aspx.+',r'.+signin.+','.+blog.+')),follow=True),                    Rule(LinkExtractor( allow = (r'.+/.+\d+/',),deny =(r'.+?filter.+',r'.+forum.+',r'.+signin.+', r'.+aspx.+','.+blog.+')), callback='parse_items',follow = True)]
    urlList=[]
    #r'.+/\S+-\d+/'
    #Rule(LxmlLinkExtractor(allow=r'.+/\S+-\w+/?page=[0-9]+#\S+',deny=(r'.+.filter\S+',r'.+.user\S+',r'.+.aspx\S+')),callback='parse_second',follow=True),
    #Rule(LxmlLinkExtractor(allow=r'.+/\S+-\d+/',deny=(r'.+.filter\S+',r'.+.user\S+',r'.+.aspx\S+')),callback='parse_items',follow=True)
    item = ExpansysItem()

    def parse_items(self, response):
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        items = []
        item = ExpansysItem()
        urlTest=response.url
        if urlTest:
          if urlTest not in self.urlList:
            self.urlList.append(urlTest)
            for r in response.xpath('//div[@id="prod_core"]'):
                item['title'] = r.xpath('//h1[@itemprop="name"]/text()').extract() or None
                item['urls'] =  response.url or None
                item['price'] = r.xpath('//p[@id="price"]/strong/span/text()').extract() or None
                checkmate = r.xpath('//ul[@class="product-sku"]/li').extract() or None
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